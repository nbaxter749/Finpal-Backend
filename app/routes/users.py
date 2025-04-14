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
from app.routes.auth import get_current_user
from app.services import create_user as service_create_user
from app.services import get_user_by_email as service_get_user_by_email
from app.services import update_user as service_update_user
from app.database import get_db

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account by calling the user service.
    
    Args:
        user: User creation data
        db: Database session
        
    Returns:
        User: Created user object
        
    Raises:
        HTTPException: If email is already registered
    """
    db_user = service_get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return service_create_user(db=db, user=user)

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
    Update the current user's profile by calling the user service.
    
    Args:
        user_update: Updated user data (email, first_name, last_name)
        current_user: The authenticated user object
        db: Database session
        
    Returns:
        User: Updated user profile
        
    Raises:
        HTTPException: If update fails (e.g., email conflict if implemented in service)
    """
    updated_user = service_update_user(db=db, user_id=current_user.id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated_user