from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True 

# Account Schemas
class AccountBase(BaseModel):
    name: str
    type: str
    balance: float
    currency: str = "USD"

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Expense Schemas
class ExpenseBase(BaseModel):
    amount: float
    category: str
    description: str
    date: date
    is_recurring: bool = False
    recurring_period: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Income Schemas
class IncomeBase(BaseModel):
    amount: float
    source: str
    description: str
    date: date
    is_recurring: bool = False
    recurring_period: Optional[str] = None

class IncomeCreate(IncomeBase):
    pass

class Income(IncomeBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Debt Schemas
class DebtBase(BaseModel):
    name: str
    amount: float
    interest_rate: float
    minimum_payment: float
    due_date: date
    type: str

class DebtCreate(DebtBase):
    pass

class Debt(DebtBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Goal Schemas
class GoalBase(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0
    deadline: Optional[date] = None
    description: Optional[str] = None

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Report Schemas
class BudgetRecommendation(BaseModel):
    category: str
    recommended_amount: float
    reason: str

class FinancialReport(BaseModel):
    total_income: float
    total_expenses: float
    savings_rate: float
    debt_overview: List[Debt]
    expense_breakdown: dict
    recommendations: List[BudgetRecommendation]