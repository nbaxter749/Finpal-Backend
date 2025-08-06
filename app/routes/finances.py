from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.routes.auth import get_current_user
from app.database import get_db
# Import service functions
from app.services import (
    create_account as service_create_account,
    get_accounts as service_get_accounts,
    get_account as service_get_account,
    update_account as service_update_account,
    delete_account as service_delete_account,
    create_expense as service_create_expense,
    get_expenses as service_get_expenses,
    create_income as service_create_income,
    get_incomes as service_get_incomes,
    create_debt as service_create_debt,
    get_debts as service_get_debts,
    get_debt as service_get_debt,
    update_debt as service_update_debt,
    delete_debt as service_delete_debt,
    create_goal as service_create_goal,
    get_goals as service_get_goals,
    update_goal as service_update_goal
)

router = APIRouter()

# Account routes
@router.post("/accounts/", response_model=schemas.Account)
def create_account(
    account: schemas.AccountCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create an account using the account service."""
    return service_create_account(db=db, account=account, user_id=current_user.id)

@router.get("/accounts/", response_model=List[schemas.Account])
def read_accounts(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Read accounts using the account service."""
    return service_get_accounts(db=db, user_id=current_user.id)

@router.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(
    account_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Read a specific account using the account service."""
    account = service_get_account(db=db, account_id=account_id, user_id=current_user.id)
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
    """Update an account using the account service."""
    updated_account = service_update_account(db=db, account_id=account_id, account=account, user_id=current_user.id)
    if not updated_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated_account

@router.delete("/accounts/{account_id}", status_code=200)
def delete_account(
    account_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an account using the account service."""
    success = service_delete_account(db=db, account_id=account_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"detail": "Account deleted successfully"}

# Expense routes
@router.post("/expenses/", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create an expense using the expense service."""
    return service_create_expense(db=db, expense=expense, user_id=current_user.id)

@router.get("/expenses/", response_model=List[schemas.Expense])
def read_expenses(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Read expenses using the expense service."""
    return service_get_expenses(db=db, user_id=current_user.id)

# Income routes
@router.post("/incomes/", response_model=schemas.Income)
def create_income(
    income: schemas.IncomeCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create an income entry using the income service."""
    return service_create_income(db=db, income=income, user_id=current_user.id)

@router.get("/incomes/", response_model=List[schemas.Income])
def read_incomes(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Read income entries using the income service."""
    return service_get_incomes(db=db, user_id=current_user.id)

# Debt routes
@router.post("/debts/", response_model=schemas.Debt)
def create_debt(
    debt: schemas.DebtCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a debt entry using the debt service."""
    return service_create_debt(db=db, debt=debt, user_id=current_user.id)

@router.get("/debts/", response_model=List[schemas.Debt])
def read_debts(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Read debt entries using the debt service."""
    return service_get_debts(db=db, user_id=current_user.id)

@router.get("/debts/{debt_id}", response_model=schemas.Debt)
def read_debt(
    debt_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Read a specific debt using the debt service."""
    debt = service_get_debt(db=db, debt_id=debt_id, user_id=current_user.id)
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    return debt

@router.put("/debts/{debt_id}", response_model=schemas.Debt)
def update_debt(
    debt_id: int,
    debt: schemas.DebtCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a debt using the debt service."""
    updated_debt = service_update_debt(db=db, debt_id=debt_id, debt=debt, user_id=current_user.id)
    if not updated_debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    return updated_debt

@router.delete("/debts/{debt_id}", status_code=200)
def delete_debt(
    debt_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a debt using the debt service."""
    success = service_delete_debt(db=db, debt_id=debt_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Debt not found")
    return {"detail": "Debt deleted successfully"}

# Goal routes
@router.post("/goals/", response_model=schemas.Goal)
def create_goal(
    goal: schemas.GoalCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a goal using the goal service."""
    return service_create_goal(db=db, goal=goal, user_id=current_user.id)

@router.get("/goals/", response_model=List[schemas.Goal])
def read_goals(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Read goals using the goal service."""
    return service_get_goals(db=db, user_id=current_user.id)

@router.put("/goals/{goal_id}", response_model=schemas.Goal)
def update_goal(
    goal_id: int,
    goal: schemas.GoalCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a goal using the goal service."""
    updated_goal = service_update_goal(db=db, goal_id=goal_id, goal=goal, user_id=current_user.id)
    if not updated_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return updated_goal