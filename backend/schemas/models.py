from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}

class UserAuth(BaseModel):
    user: UserResponse
    token: str
    token_type: str = "bearer"

# Chat Session schemas
class ChatSessionCreate(BaseModel):
    session_name: str
    topic: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: int
    session_name: str
    topic: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    is_archived: bool
    query_count: Optional[int] = 0
    
    model_config = {"from_attributes": True}

# Legal Query schemas  
class LegalQueryCreate(BaseModel):
    query_text: str
    chat_session_id: Optional[int] = None

class SourceInfo(BaseModel):
    title: str
    content: str
    source: str
    section: Optional[str]
    url: Optional[str]

class LegalQueryResponse(BaseModel):
    id: int
    query_text: str
    response_text: str
    query_category: Optional[str]
    ai_model_used: str
    sources: Optional[List[SourceInfo]] = []
    confidence_score: Optional[int]
    created_at: datetime
    response_time_ms: Optional[int]
    is_bookmarked: bool
    user_rating: Optional[int]
    
    model_config = {"from_attributes": True}

# Chat Request/Response (existing)
class ChatRequest(BaseModel):
    message: str
    chat_session_id: Optional[int] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceInfo] = []
    context_used: bool = True
    ai_powered: bool = True
    query_id: Optional[int] = None
    chat_session_id: Optional[int] = None

# Legal Document schemas
class LegalDocumentResponse(BaseModel):
    id: int
    title: str
    document_type: str
    category: str
    year: Optional[int]
    official_url: Optional[str]
    
    model_config = {"from_attributes": True}

# Feedback schemas
class FeedbackCreate(BaseModel):
    legal_query_id: int
    rating: int  # 1-5
    feedback_text: Optional[str] = None
    is_helpful: Optional[bool] = None

class FeedbackResponse(BaseModel):
    id: int
    rating: int
    feedback_text: Optional[str]
    is_helpful: Optional[bool]
    created_at: datetime
    
    model_config = {"from_attributes": True}

# Analytics schemas
class AnalyticsResponse(BaseModel):
    total_queries: int
    total_users: int
    total_sessions: int
    popular_categories: List[dict]
    recent_activity: List[dict]