from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime

from database.connection import get_db
from models.database import User, ChatSession, LegalQuery, SystemAnalytics, UserFeedback
from schemas.models import (
    ChatRequest, ChatResponse, ChatSessionCreate, ChatSessionResponse,
    LegalQueryResponse, FeedbackCreate, FeedbackResponse, SourceInfo
)
from auth.security import get_current_user
from services.gemini_rag_service import GeminiRAGService

router = APIRouter(prefix="/chat", tags=["Chat"])

# Initialize RAG service
rag_service = GeminiRAGService()

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    
    # Create new chat session
    chat_session = ChatSession(
        user_id=current_user["user_id"],
        session_name=session_data.session_name,
        topic=session_data.topic
    )
    
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)
    
    # Update session count analytics
    session_count = db.query(SystemAnalytics).filter(
        SystemAnalytics.metric_name == "total_sessions"
    ).first()
    if session_count:
        session_count.metric_value += 1
        db.commit()
    
    return ChatSessionResponse.model_validate(chat_session)

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_user_chat_sessions(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get all chat sessions for current user"""
    
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user["user_id"],
        ChatSession.is_archived == False
    ).order_by(ChatSession.updated_at.desc()).offset(skip).limit(limit).all()
    
    # Add query count to each session
    session_responses = []
    for session in sessions:
        session_dict = session.__dict__.copy()
        query_count = db.query(LegalQuery).filter(
            LegalQuery.chat_session_id == session.id
        ).count()
        session_dict["query_count"] = query_count
        session_responses.append(ChatSessionResponse(**session_dict))
    
    return session_responses

@router.get("/sessions/{session_id}/queries", response_model=List[LegalQueryResponse])
async def get_session_queries(
    session_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all queries in a specific chat session"""
    
    # Verify session belongs to user
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user["user_id"]
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    queries = db.query(LegalQuery).filter(
        LegalQuery.chat_session_id == session_id
    ).order_by(LegalQuery.created_at.asc()).all()
    
    # Convert to response format with sources
    query_responses = []
    for query in queries:
        query_dict = query.__dict__.copy()
        
        # Parse sources JSON
        if query.response_sources:
            try:
                sources_data = json.loads(query.response_sources)
                query_dict["sources"] = [SourceInfo(**source) for source in sources_data]
            except:
                query_dict["sources"] = []
        else:
            query_dict["sources"] = []
        
        query_responses.append(LegalQueryResponse(**query_dict))
    
    return query_responses

@router.post("/message", response_model=ChatResponse)
async def send_chat_message(
    chat_data: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a chat message and get AI response"""
    
    start_time = datetime.utcnow()
    
    # Get or create chat session
    if chat_data.chat_session_id:
        # Verify session belongs to user
        session = db.query(ChatSession).filter(
            ChatSession.id == chat_data.chat_session_id,
            ChatSession.user_id == current_user["user_id"]
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
    else:
        # Create new session with auto-generated name
        session_name = f"Legal Chat - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        session = ChatSession(
            user_id=current_user["user_id"],
            session_name=session_name,
            topic=chat_data.message[:100] + "..." if len(chat_data.message) > 100 else chat_data.message
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    
    # Generate AI response
    try:
        ai_response = await rag_service.generate_response(
            query=chat_data.message,
            include_sources=True
        )
        
        # Calculate response time
        response_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        # Determine query category based on response
        query_category = _determine_category(chat_data.message, ai_response["answer"])
        
        # Save query and response to database
        legal_query = LegalQuery(
            user_id=current_user["user_id"],
            chat_session_id=session.id,
            query_text=chat_data.message,
            query_category=query_category,
            response_text=ai_response["answer"],
            ai_model_used=ai_response.get("ai_model", "gemini-2.0-flash"),
            response_sources=json.dumps(ai_response["sources"]) if ai_response["sources"] else None,
            response_time_ms=response_time,
            confidence_score=85  # Default confidence score
        )
        
        db.add(legal_query)
        
        # Update session timestamp
        session.updated_at = datetime.utcnow()
        
        # Update query count analytics
        query_count = db.query(SystemAnalytics).filter(
            SystemAnalytics.metric_name == "total_queries"
        ).first()
        if query_count:
            query_count.metric_value += 1
        
        db.commit()
        db.refresh(legal_query)
        
        return ChatResponse(
            answer=ai_response["answer"],
            sources=ai_response["sources"],
            context_used=ai_response["context_used"],
            ai_powered=ai_response["ai_powered"],
            query_id=legal_query.id,
            chat_session_id=session.id
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit feedback for a legal query response"""
    
    # Verify query belongs to user
    query = db.query(LegalQuery).filter(
        LegalQuery.id == feedback_data.legal_query_id,
        LegalQuery.user_id == current_user["user_id"]
    ).first()
    
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Legal query not found"
        )
    
    # Create feedback
    feedback = UserFeedback(
        user_id=current_user["user_id"],
        legal_query_id=feedback_data.legal_query_id,
        rating=feedback_data.rating,
        feedback_text=feedback_data.feedback_text,
        is_helpful=feedback_data.is_helpful
    )
    
    db.add(feedback)
    
    # Update query rating
    query.user_rating = feedback_data.rating
    
    db.commit()
    db.refresh(feedback)
    
    return FeedbackResponse.model_validate(feedback)

@router.post("/queries/{query_id}/bookmark")
async def bookmark_query(
    query_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Bookmark/unbookmark a legal query"""
    
    query = db.query(LegalQuery).filter(
        LegalQuery.id == query_id,
        LegalQuery.user_id == current_user["user_id"]
    ).first()
    
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Legal query not found"
        )
    
    query.is_bookmarked = not query.is_bookmarked
    db.commit()
    
    return {"message": f"Query {'bookmarked' if query.is_bookmarked else 'unbookmarked'} successfully"}

def _determine_category(query: str, response: str) -> str:
    """Determine legal category based on query and response content"""
    
    query_lower = query.lower()
    response_lower = response.lower()
    combined = f"{query_lower} {response_lower}"
    
    if any(term in combined for term in ["constitution", "fundamental rights", "article", "pil", "writ"]):
        return "Constitutional Law"
    elif any(term in combined for term in ["criminal", "ipc", "murder", "theft", "fir", "police"]):
        return "Criminal Law"
    elif any(term in combined for term in ["contract", "agreement", "breach", "civil"]):
        return "Civil Law"
    elif any(term in combined for term in ["consumer", "protection", "goods", "services"]):
        return "Consumer Law"
    elif any(term in combined for term in ["company", "corporate", "business", "shares"]):
        return "Corporate Law"
    elif any(term in combined for term in ["family", "marriage", "divorce", "adoption", "surrogacy"]):
        return "Family Law"
    elif any(term in combined for term in ["property", "land", "real estate", "transfer"]):
        return "Property Law"
    elif any(term in combined for term in ["labor", "employment", "worker", "industrial"]):
        return "Labor Law"
    else:
        return "General Law"