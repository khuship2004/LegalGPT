from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    legal_queries = relationship("LegalQuery", back_populates="user", cascade="all, delete-orphan")

class ChatSession(Base):
    """Chat sessions to group related conversations"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_name = Column(String(200), nullable=False)
    topic = Column(String(500), nullable=True)  # Auto-generated based on first query
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_archived = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    legal_queries = relationship("LegalQuery", back_populates="chat_session", cascade="all, delete-orphan")

class LegalQuery(Base):
    """Individual legal queries and responses"""
    __tablename__ = "legal_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chat_session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    
    # Query details
    query_text = Column(Text, nullable=False)
    query_category = Column(String(100), nullable=True)  # e.g., "Constitutional Law", "Criminal Law"
    
    # Response details
    response_text = Column(Text, nullable=False)
    ai_model_used = Column(String(50), default="gemini-2.0-flash")
    response_sources = Column(Text, nullable=True)  # JSON string of sources
    confidence_score = Column(Integer, nullable=True)  # 1-100 rating
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    response_time_ms = Column(Integer, nullable=True)  # Response generation time
    is_bookmarked = Column(Boolean, default=False)
    user_rating = Column(Integer, nullable=True)  # 1-5 rating by user
    
    # Relationships
    user = relationship("User", back_populates="legal_queries")
    chat_session = relationship("ChatSession", back_populates="legal_queries")

class LegalDocument(Base):
    """Legal documents and acts for reference"""
    __tablename__ = "legal_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    document_type = Column(String(50), nullable=False)  # "Act", "Constitution", "Code"
    category = Column(String(100), nullable=False)  # "Criminal Law", "Civil Law", etc.
    year = Column(Integer, nullable=True)
    content = Column(Text, nullable=True)  # Full text or summary
    official_url = Column(String(500), nullable=True)
    section_info = Column(Text, nullable=True)  # JSON of sections
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserFeedback(Base):
    """User feedback on responses for system improvement"""
    __tablename__ = "user_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    legal_query_id = Column(Integer, ForeignKey("legal_queries.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    feedback_text = Column(Text, nullable=True)
    is_helpful = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SystemAnalytics(Base):
    """System usage analytics and counters"""
    __tablename__ = "system_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False)  # "total_queries", "daily_users"
    metric_value = Column(Integer, default=0)
    date_recorded = Column(DateTime(timezone=True), server_default=func.now())
    additional_data = Column(Text, nullable=True)  # JSON for extra metrics