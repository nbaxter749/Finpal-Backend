from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.routes.auth import get_current_user
from app.database import get_db

router = APIRouter()

# Account routes
@router.post("/accounts/", response_model=schemas.Account)
def create_account(
    account: schemas.AccountCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_account = models.Account(**account.dict(), user_id=current_user.id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/accounts/", response_model=List[schemas.Account])
def read_accounts(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    accounts = db.query(models.Account).filter(models.Account.user_id == current_user.id).all()
    return accounts

@router.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(
    account_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return account

@router.put("/accounts/{account_id}", response_model=schemas.Account)
def update_account(
    account_id: int,
    account: schemas.AccountCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.user_id == current_user.id
    ).first()
    
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    for key, value in account.dict().items():
        setattr(db_account, key, value)
    
    db.commit()
    db.refresh(db_account)
    
    return db_account

@router.delete("/accounts/{account_id}")
def delete_account(
    account_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.user_id == current_user.id
    ).first()
    
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(db_account)
    db.commit()
    
    return {"detail": "Account deleted successfully"}

# Expense routes
@router.post("/expenses/", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_expense = models.Expense(**expense.dict(), user_id=current_user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/expenses/", response_model=List[schemas.Expense])
def read_expenses(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expenses = db.query(models.Expense).filter(models.Expense.user_id == current_user.id).all()
    return expenses

# Income routes
@router.post("/incomes/", response_model=schemas.Income)
def create_income(
    income: schemas.IncomeCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_income = models.Income(**income.dict(), user_id=current_user.id)
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

@router.get("/incomes/", response_model=List[schemas.Income])
def read_incomes(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    incomes = db.query(models.Income).filter(models.Income.user_id == current_user.id).all()
    return incomes

# Debt routes
@router.post("/debts/", response_model=schemas.Debt)
def create_debt(
    debt: schemas.DebtCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_debt = models.Debt(**debt.dict(), user_id=current_user.id)
    db.add(db_debt)
    db.commit()
    db.refresh(db_debt)
    return db_debt

@router.get("/debts/", response_model=List[schemas.Debt])
def read_debts(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    debts = db.query(models.Debt).filter(models.Debt.user_id == current_user.id).all()
    return debts

# Goal routes
@router.post("/goals/", response_model=schemas.Goal)
def create_goal(
    goal: schemas.GoalCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_goal = models.Goal(**goal.dict(), user_id=current_user.id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.get("/goals/", response_model=List[schemas.Goal])
def read_goals(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    goals = db.query(models.Goal).filter(models.Goal.user_id == current_user.id).all()
    return goals