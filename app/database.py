"""
Database Configuration Module

This module handles database connection and session management using SQLAlchemy.
It provides the core database functionality for the application including:
- Database engine configuration
- Session management
- Base model declaration
- Database connection handling

Features:
- SQLAlchemy ORM integration
- Environment-based configuration
- Session pooling
- Connection management
- Database URL configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finpal.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Database session dependency for FastAPI endpoints.
    
    Yields:
        Session: SQLAlchemy database session
        
    Note:
        Automatically closes the session after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()