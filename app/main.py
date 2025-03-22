from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, get_db
from app import models, schemas, services
from app.routes import auth, users, finances, reports

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinPal API",
    description="AI-Powered Student Financial Manager",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, tags=["Users"])
app.include_router(finances.router, tags=["Finances"])
app.include_router(reports.router, tags=["Reports"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FinPal API"}