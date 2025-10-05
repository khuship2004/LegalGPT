from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./legal_ai_database.db")

# Create SQLAlchemy engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database with default data"""
    create_tables()
    
    # Add default legal documents
    db = SessionLocal()
    try:
        from models.database import LegalDocument, SystemAnalytics
        
        # Check if documents already exist
        existing_docs = db.query(LegalDocument).count()
        if existing_docs == 0:
            default_documents = [
                {
                    "title": "Constitution of India",
                    "document_type": "Constitution",
                    "category": "Constitutional Law",
                    "year": 1950,
                    "content": "The Constitution of India is the supreme law of India. It lays down the framework defining fundamental political principles, establishes the structure, procedures, powers, and duties of government institutions.",
                    "official_url": "https://www.india.gov.in/my-government/constitution-india/constitution-india-full-text"
                },
                {
                    "title": "Indian Penal Code",
                    "document_type": "Act",
                    "category": "Criminal Law", 
                    "year": 1860,
                    "content": "The Indian Penal Code is the official criminal code of India. It covers all substantive aspects of criminal law.",
                    "official_url": "https://www.indiacode.nic.in/handle/123456789/2263"
                },
                {
                    "title": "Indian Contract Act",
                    "document_type": "Act",
                    "category": "Civil Law",
                    "year": 1872,
                    "content": "The Indian Contract Act, 1872 prescribes the law relating to contracts in India and is the key act regulating Indian contract law.",
                    "official_url": "https://www.indiacode.nic.in/handle/123456789/2268"
                },
                {
                    "title": "Consumer Protection Act",
                    "document_type": "Act", 
                    "category": "Consumer Law",
                    "year": 2019,
                    "content": "The Consumer Protection Act, 2019 is an Act of the Parliament of India which aims to give consumers rights and penalize businesses for exploiting consumers.",
                    "official_url": "https://www.indiacode.nic.in/handle/123456789/15397"
                },
                {
                    "title": "Surrogacy (Regulation) Act",
                    "document_type": "Act",
                    "category": "Family Law",
                    "year": 2021,
                    "content": "The Surrogacy (Regulation) Act, 2021 regulates surrogacy in India by allowing only altruistic surrogacy and prohibiting commercial surrogacy.",
                    "official_url": "https://www.indiacode.nic.in/handle/123456789/16806"
                }
            ]
            
            for doc_data in default_documents:
                doc = LegalDocument(**doc_data)
                db.add(doc)
            
            # Initialize system analytics
            analytics = [
                SystemAnalytics(metric_name="total_queries", metric_value=0),
                SystemAnalytics(metric_name="total_users", metric_value=0),
                SystemAnalytics(metric_name="total_sessions", metric_value=0)
            ]
            
            for analytic in analytics:
                db.add(analytic)
            
            db.commit()
            print("✅ Default legal documents and analytics initialized!")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error initializing database: {str(e)}")
    finally:
        db.close()