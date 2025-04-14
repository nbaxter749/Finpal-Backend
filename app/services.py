"""
Service Layer Module

This module provides business logic and database operations for the application.
It handles all interactions between the API routes and the database models.

Service Categories:
- Authentication: Password handling and JWT token management
- Users: User account management
- Accounts: Financial account operations
- Expenses: Expense tracking operations
- Income: Income tracking operations
- Debts: Debt management operations
- Goals: Financial goal operations
- Financial Analysis: Summary and reporting operations

Features:
- Password hashing and verification
- JWT token generation and validation
- Database CRUD operations
- Business logic implementation
- Data aggregation and analysis
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app import models, schemas
from app.database import get_db

# Load environment variables
load_dotenv()

# Security configuration - Load from environment variables
# Ensure these are set securely in your production .env file
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
# Convert expire minutes to int, provide default
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Check if the default secret key is being used and print a warning if so
if SECRET_KEY == "your-secret-key-change-in-production":
    print("WARNING: Using default SECRET_KEY. Please set a strong secret key in your .env file for production.")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password handling
def verify_password(plain_password, hashed_password):
    """
    Verify a password against its hash.
    
    Args:
        plain_password: The password to verify
        hashed_password: The hash to verify against
        
    Returns:
        bool: True if password matches hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Generate a password hash.
    
    Args:
        password: The password to hash
        
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)

# User authentication
def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user by email and password.
    
    Args:
        db: Database session
        email: User's email
        password: User's password
        
    Returns:
        User: The authenticated user or False if authentication fails
    """
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Get the current authenticated user from a JWT token.
    
    Args:
        db: Database session
        token: JWT token
        
    Returns:
        User: The current user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

# User services
def get_user_by_email(db: Session, email: str):
    """
    Get a user by email address.
    
    Args:
        db: Database session
        email: User's email
        
    Returns:
        User: The user or None if not found
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    """
    Get a user by ID.
    
    Args:
        db: Database session
        user_id: User's ID
        
    Returns:
        User: The user or None if not found
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user.
    
    Args:
        db: Database session
        user: User creation data
        
    Returns:
        User: The created user
    """
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

def update_user(db: Session, user_id: int, user_update: schemas.UserBase):
    """
    Update an existing user's profile information.

    Args:
        db: Database session
        user_id: ID of the user to update
        user_update: Pydantic schema with updated user data (email, first_name, last_name)

    Returns:
        User: The updated user object or None if not found.
    """
    db_user = get_user_by_id(db, user_id=user_id)
    if not db_user:
        return None

    # Optional: Add check for email uniqueness if email is changing
    # existing_user = get_user_by_email(db, email=user_update.email)
    # if existing_user and existing_user.id != user_id:
    #     raise HTTPException(status_code=400, detail="Email already registered by another user")

    # Update fields from the UserBase schema
    db_user.email = user_update.email
    db_user.first_name = user_update.first_name
    db_user.last_name = user_update.last_name

    db.commit()
    db.refresh(db_user)
    return db_user

# Account services
def get_accounts(db: Session, user_id: int):
    """
    Get all accounts for a user.
    
    Args:
        db: Database session
        user_id: User's ID
        
    Returns:
        List[Account]: List of user's accounts
    """
    return db.query(models.Account).filter(models.Account.user_id == user_id).all()

def get_account(db: Session, account_id: int, user_id: int):
    """
    Get a specific account by ID.
    
    Args:
        db: Database session
        account_id: Account's ID
        user_id: Owner's user ID
        
    Returns:
        Account: The account or None if not found
    """
    return db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.user_id == user_id
    ).first()

def create_account(db: Session, account: schemas.AccountCreate, user_id: int):
    """
    Create a new account.
    
    Args:
        db: Database session
        account: Account creation data
        user_id: Owner's user ID
        
    Returns:
        Account: The created account
    """
    db_account = models.Account(**account.dict(), user_id=user_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_account(db: Session, account_id: int, account: schemas.AccountCreate, user_id: int):
    """
    Update an existing account.
    
    Args:
        db: Database session
        account_id: Account's ID
        account: Updated account data
        user_id: Owner's user ID
        
    Returns:
        Account: The updated account or None if not found
    """
    db_account = get_account(db, account_id, user_id)
    if not db_account:
        return None
    
    for key, value in account.dict().items():
        setattr(db_account, key, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

def delete_account(db: Session, account_id: int, user_id: int):
    """
    Delete an account.
    
    Args:
        db: Database session
        account_id: Account's ID
        user_id: Owner's user ID
        
    Returns:
        bool: True if deleted, False if not found
    """
    db_account = get_account(db, account_id, user_id)
    if not db_account:
        return False
    
    db.delete(db_account)
    db.commit()
    return True

# Expense services
def get_expenses(db: Session, user_id: int):
    """
    Get all expenses for a user.
    
    Args:
        db: Database session
        user_id: User's ID
        
    Returns:
        List[Expense]: List of user's expenses
    """
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).all()

def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    """
    Create a new expense.
    
    Args:
        db: Database session
        expense: Expense creation data
        user_id: Owner's user ID
        
    Returns:
        Expense: The created expense
    """
    db_expense = models.Expense(**expense.dict(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# Income services
def get_incomes(db: Session, user_id: int):
    """
    Get all income entries for a user.
    
    Args:
        db: Database session
        user_id: User's ID
        
    Returns:
        List[Income]: List of user's income entries
    """
    return db.query(models.Income).filter(models.Income.user_id == user_id).all()

def create_income(db: Session, income: schemas.IncomeCreate, user_id: int):
    """
    Create a new income entry.
    
    Args:
        db: Database session
        income: Income creation data
        user_id: Owner's user ID
        
    Returns:
        Income: The created income entry
    """
    db_income = models.Income(**income.dict(), user_id=user_id)
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

# Debt services
def get_debts(db: Session, user_id: int):
    """
    Get all debts for a user.
    
    Args:
        db: Database session
        user_id: User's ID
        
    Returns:
        List[Debt]: List of user's debts
    """
    return db.query(models.Debt).filter(models.Debt.user_id == user_id).all()

def create_debt(db: Session, debt: schemas.DebtCreate, user_id: int):
    """
    Create a new debt.
    
    Args:
        db: Database session
        debt: Debt creation data
        user_id: Owner's user ID
        
    Returns:
        Debt: The created debt
    """
    db_debt = models.Debt(**debt.dict(), user_id=user_id)
    db.add(db_debt)
    db.commit()
    db.refresh(db_debt)
    return db_debt

# Goal services
def get_goals(db: Session, user_id: int):
    """
    Get all financial goals for a user.
    
    Args:
        db: Database session
        user_id: User's ID
        
    Returns:
        List[Goal]: List of user's goals
    """
    return db.query(models.Goal).filter(models.Goal.user_id == user_id).all()

def create_goal(db: Session, goal: schemas.GoalCreate, user_id: int):
    """
    Create a new financial goal.
    
    Args:
        db: Database session
        goal: Goal creation data
        user_id: Owner's user ID
        
    Returns:
        Goal: The created goal
    """
    db_goal = models.Goal(**goal.dict(), user_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal(db: Session, goal_id: int, goal: schemas.GoalCreate, user_id: int):
    """
    Update an existing financial goal.
    
    Args:
        db: Database session
        goal_id: Goal's ID
        goal: Updated goal data
        user_id: Owner's user ID
        
    Returns:
        Goal: The updated goal or None if not found
    """
    db_goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id,
        models.Goal.user_id == user_id
    ).first()
    
    if not db_goal:
        return None
    
    for key, value in goal.dict().items():
        setattr(db_goal, key, value)
    
    db.commit()
    db.refresh(db_goal)
    return db_goal

# Financial analysis services
def get_financial_summary(db: Session, user_id: int) -> Optional[schemas.FinancialReport]:
    """
    Generate a comprehensive financial summary for a user, including AI analysis.
    
    Args:
        db: Database session
        user_id: User's ID
        
    Returns:
        FinancialReport: Financial summary object or None if data retrieval fails.
    """
    try:
        expenses = get_expenses(db, user_id)
        incomes = get_incomes(db, user_id)
        debts = get_debts(db, user_id)
    except Exception as e:
        print(f"Error fetching financial data for user {user_id}: {e}")
        return None # Or raise a specific service layer exception

    # Calculate totals
    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.amount for expense in expenses)
    
    # Calculate savings rate
    savings_rate = 0
    if total_income > 0:
        savings_rate = ((total_income - total_expenses) / total_income) * 100
    
    # Generate expense breakdown by category
    expense_breakdown = {}
    for expense in expenses:
        expense_breakdown[expense.category] = expense_breakdown.get(expense.category, 0) + expense.amount
    
    # Prepare spending data for analysis
    spending_data = [{
        "amount": expense.amount,
        "category": expense.category,
        "date": expense.date,
        "description": expense.description
    } for expense in expenses]
    
    # Import the correct AI analysis function
    from app.ml.openai_budget_analyzer import analyze_finances

    # Initialize recommendations list
    formatted_recommendations = []
    
    # Call the AI analysis function
    try:
        financial_analysis = analyze_finances(
            spending_data,
            total_income,
            total_expenses,
            debts # Pass the list of SQLAlchemy debt models
        )
        
        # Extract and format recommendations from the AI response
        # The AI function now returns recommendations as [(category, amount, reason)]
        recommendations_list = financial_analysis.get("recommendations", [])
        formatted_recommendations = [
            schemas.BudgetRecommendation(
                category=category,
                recommended_amount=amount,
                reason=reason
            )
            for category, amount, reason in recommendations_list
        ]
        
    except Exception as e:
        print(f"Error during financial analysis for user {user_id}: {e}")
        # Proceed without AI recommendations if analysis fails
        # Optionally add a default recommendation or note about the failure
        formatted_recommendations.append(schemas.BudgetRecommendation(
            category="General", 
            recommended_amount=0,
            reason="AI analysis failed. Unable to provide specific recommendations."
        ))

    # Convert SQLAlchemy Debt objects to Pydantic Debt schemas for the report
    formatted_debts = [
        schemas.Debt.from_orm(debt)
        for debt in debts
    ]
    
    # Create financial report
    financial_report = schemas.FinancialReport(
        total_income=total_income,
        total_expenses=total_expenses,
        savings_rate=savings_rate,
        debt_overview=formatted_debts, # Use formatted Pydantic schemas
        expense_breakdown=expense_breakdown,
        recommendations=formatted_recommendations
    )
    
    return financial_report