"""
Main Application Module

This module serves as the entry point for the FastAPI application.
It configures the application, sets up middleware, and includes all routers.

Features:
- FastAPI application configuration
- CORS middleware setup
- Database initialization
- Router registration
- API documentation setup

Configuration:
- API title and version
- CORS settings
- Database table creation
- Route organization
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from app.database import engine, get_db
from app import models, schemas, services
from app.routes import auth, users, finances, reports

# Load environment variables
load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinPal API",
    description="AI-Powered Student Financial Manager",
    version="0.1.0"
)

# Configure CORS - Load allowed origins from environment variable
# Expects a comma-separated string of origins in the .env file
# Defaults to ["*"] for development if not set
cors_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in cors_origins_str.split(",")]

if "*" in allowed_origins and len(allowed_origins) > 1:
    print("WARNING: CORS_ALLOWED_ORIGINS contains '*' along with other origins. Allowing all origins.")
    allowed_origins = ["*"]
elif cors_origins_str == "*":
    print("INFO: Allowing all origins for CORS (development setting).")
else:
    print(f"INFO: Allowing specific CORS origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins, # Use the loaded origins
    allow_credentials=True,
    allow_methods=["*"], # Allow all standard methods
    allow_headers=["*"], # Allow all standard headers
)

# Include routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(finances.router, tags=["Finances"])
app.include_router(reports.router, tags=["Reports"])

@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: Welcome message
    """
    return {"message": "Welcome to FinPal API"}