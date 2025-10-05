from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import json
import asyncio
import uuid
from datetime import datetime

from services.gemini_rag_service import GeminiRAGService
from services.legal_service import LegalService
from database.connection import init_database, get_db
from routes.auth import router as auth_router
from routes.chat import router as chat_router
from schemas.models import AnalyticsResponse
from models.database import SystemAnalytics
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

app = FastAPI(
    title="LegalGPT API",
    description="Open Source Indian Legal AI Assistant with Authentication & Chat History",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(chat_router)

@app.on_event("startup")
async def startup_event():
    """Initialize services and database on startup"""
    print("🚀 Starting LegalGPT API v2.0...")
    
    # Initialize database
    init_database()
    print("✅ Database initialized successfully!")
    
    print("✅ Services initialized successfully!")

# Initialize services  
rag_service = GeminiRAGService()
legal_service = LegalService()

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None
    sources: Optional[List[dict]] = None

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    include_sources: bool = True

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    sources: List[dict] = []
    disclaimer: str

# In-memory storage for conversations (use Redis/DB in production)
conversations = {}

@app.get("/")
async def root():
    return {
        "message": "LegalGPT API v2.0 with Authentication & Database is running!",
        "version": "2.0.0",
        "status": "healthy",
        "features": ["User Authentication", "Chat History", "Database Storage", "Gemini AI"]
    }

@app.get("/health")
async def health_check():
    try:
        # Test if services are working
        await rag_service.health_check()
        return {"status": "healthy", "services": {"rag": "ok", "legal": "ok"}}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get or create conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Get conversation history
        history = conversations.get(conversation_id, [])
        
        # Add user message to history
        user_message = ChatMessage(
            role="user",
            content=request.message,
            timestamp=datetime.now()
        )
        history.append(user_message)
        
        # Generate response using RAG
        response_data = await rag_service.generate_response(
            query=request.message,
            conversation_history=history,
            include_sources=request.include_sources
        )
        
        # Create assistant message
        assistant_message = ChatMessage(
            role="assistant",
            content=response_data["answer"],
            timestamp=datetime.now(),
            sources=response_data.get("sources", [])
        )
        history.append(assistant_message)
        
        # Save updated conversation
        conversations[conversation_id] = history
        
        return ChatResponse(
            message=response_data["answer"],
            conversation_id=conversation_id,
            sources=response_data.get("sources", []),
            disclaimer=legal_service.get_disclaimer()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id]
    }

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    del conversations[conversation_id]
    return {"message": "Conversation deleted successfully"}

@app.get("/legal-documents")
async def get_legal_documents():
    """Get list of available legal documents in the system"""
    try:
        documents = await rag_service.get_document_list()
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching documents: {str(e)}")

@app.post("/feedback")
async def submit_feedback(feedback_data: dict):
    """Submit feedback on AI responses"""
    # In production, store this in a database
    print(f"Feedback received: {feedback_data}")
    return {"message": "Feedback submitted successfully"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port, reload=True)