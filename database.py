from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set. Please check your .env file.")

_engine = None

def get_engine():
    """Get or create the database engine"""
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Verify connections before using them
            echo=False  # Set to True for SQL debugging
        )
    return _engine

def get_session_local():
    """Get the session factory"""
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine()
    )

# Base class for models
Base = declarative_base()


class Appointment(Base):
    """Appointment table"""
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), nullable=True)
    reason = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=True)
    canceled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    """Dependency for getting database session"""
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=get_engine())

init_db()