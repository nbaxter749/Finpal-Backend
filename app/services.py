from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

# Security configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password handling
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# User authentication
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
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

# Account services
def get_accounts(db: Session, user_id: int):
    return db.query(models.Account).filter(models.Account.user_id == user_id).all()

def get_account(db: Session, account_id: int, user_id: int):
    return db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.user_id == user_id
    ).first()

def create_account(db: Session, account: schemas.AccountCreate, user_id: int):
    db_account = models.Account(**account.dict(), user_id=user_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_account(db: Session, account_id: int, account: schemas.AccountCreate, user_id: int):
    db_account = get_account(db, account_id, user_id)
    if not db_account:
        return None
    
    for key, value in account.dict().items():
        setattr(db_account, key, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

def delete_account(db: Session, account_id: int, user_id: int):
    db_account = get_account(db, account_id, user_id)
    if not db_account:
        return False
    
    db.delete(db_account)
    db.commit()
    return True

# Expense services
def get_expenses(db: Session, user_id: int):
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).all()

def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    db_expense = models.Expense(**expense.dict(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# Income services
def get_incomes(db: Session, user_id: int):
    return db.query(models.Income).filter(models.Income.user_id == user_id).all()

def create_income(db: Session, income: schemas.IncomeCreate, user_id: int):
    db_income = models.Income(**income.dict(), user_id=user_id)
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

# Debt services
def get_debts(db: Session, user_id: int):
    return db.query(models.Debt).filter(models.Debt.user_id == user_id).all()

def create_debt(db: Session, debt: schemas.DebtCreate, user_id: int):
    db_debt = models.Debt(**debt.dict(), user_id=user_id)
    db.add(db_debt)
    db.commit()
    db.refresh(db_debt)
    return db_debt

# Goal services
def get_goals(db: Session, user_id: int):
    return db.query(models.Goal).filter(models.Goal.user_id == user_id).all()

def create_goal(db: Session, goal: schemas.GoalCreate, user_id: int):
    db_goal = models.Goal(**goal.dict(), user_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal(db: Session, goal_id: int, goal: schemas.GoalCreate, user_id: int):
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
def get_financial_summary(db: Session, user_id: int):
    expenses = get_expenses(db, user_id)
    incomes = get_incomes(db, user_id)
    debts = get_debts(db, user_id)
    
    # Calculate totals
    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.amount for expense in expenses)
    
    # Calculate savings rate
    savings_rate = 0 if total_income == 0 else ((total_income - total_expenses) / total_income) * 100
    
    # Generate expense breakdown by category
    expense_breakdown = {}
    for expense in expenses:
        if expense.category in expense_breakdown:
            expense_breakdown[expense.category] += expense.amount
        else:
            expense_breakdown[expense.category] = expense.amount
    
    # Prepare spending data for analysis
    spending_data = [{
        "amount": expense.amount,
        "category": expense.category,
        "date": expense.date,
        "description": expense.description
    } for expense in expenses]
    
    from app.ml.budget_analyzer import analyze_spending_patterns, generate_recommendations
    
    # Analyze spending patterns
    spending_patterns = analyze_spending_patterns(spending_data)
    
    # Generate budget recommendations
    recommendations = generate_recommendations(
        spending_patterns, 
        total_income, 
        total_expenses, 
        debts
    )
    
    # Format recommendations
    formatted_recommendations = [
        schemas.BudgetRecommendation(
            category=category,
            recommended_amount=amount,
            reason=reason
        )
        for category, amount, reason in recommendations
    ]
    
    # Create financial report
    financial_report = schemas.FinancialReport(
        total_income=total_income,
        total_expenses=total_expenses,
        savings_rate=savings_rate,
        debt_overview=debts,
        expense_breakdown=expense_breakdown,
        recommendations=formatted_recommendations
    )
    
    return financial_report