"""
User Management Routes

This module handles user-related operations including user creation,
profile management, and user data retrieval. It provides endpoints
for managing user accounts and personal information.

Features:
- User registration
- Profile retrieval
- Profile updates
- User data validation
- Authentication integration
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.routes.auth import get_password_hash, get_current_user
from app.database import get_db

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.
    
    Args:
        user: User creation data containing:
            - email: User's email address
            - password: User's password
            - first_name: User's first name
            - last_name: User's last name
        db: Database session
        
    Returns:
        User: Created user object
        
    Raises:
        HTTPException: If email is already registered
    """
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/users/me", response_model=schemas.User)
def read_user_me(current_user: models.User = Depends(get_current_user)):
    """
    Get the current user's profile.
    
    Args:
        current_user: The authenticated user object
        
    Returns:
        User: Current user's profile data
    """
    return current_user

@router.put("/users/me", response_model=schemas.User)
def update_user(
    user_update: schemas.UserBase,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the current user's profile.
    
    Args:
        user_update: Updated user data containing:
            - email: Updated email address
            - first_name: Updated first name
            - last_name: Updated last name
        current_user: The authenticated user object
        db: Database session
        
    Returns:
        User: Updated user profile
    """
    current_user.email = user_update.email
    current_user.first_name = user_update.first_name
    current_user.last_name = user_update.last_name
    
    db.commit()
    db.refresh(current_user)
    
    return current_user