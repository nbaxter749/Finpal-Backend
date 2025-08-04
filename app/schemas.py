"""
Pydantic Schemas Module

This module defines Pydantic models for request/response validation and serialization.
It contains all data schemas used for API input/output validation and documentation.

Schema Categories:
- User: User account and authentication schemas
- Account: Financial account schemas
- Expense: Expense tracking schemas
- Income: Income tracking schemas
- Debt: Debt management schemas
- Goal: Financial goal schemas
- Token: Authentication token schemas
- Report: Financial reporting schemas

Features:
- Input validation
- Response serialization
- OpenAPI documentation
- Type hints
- Default values
- Optional fields
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime

# User Schemas
class UserBase(BaseModel):
    """
    Base schema for user data.
    
    Attributes:
        email (EmailStr): User's email address
        first_name (str): User's first name
        last_name (str): User's last name
    """
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    """
    Schema for creating a new user, extends UserBase.
    
    Attributes:
        password (str): User's password (plain text)
    """
    password: str

class User(UserBase):
    """
    Schema for user responses, extends UserBase.
    
    Attributes:
        id (int): User ID
        is_active (bool): Account status
        created_at (datetime): Account creation timestamp
    """
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True 

# Account Schemas
class AccountBase(BaseModel):
    """
    Base schema for financial accounts.
    
    Attributes:
        name (str): Account name
        type (str): Account type (savings, checking)
        balance (float): Current balance
        currency (str): Account currency, defaults to USD
    """
    name: str
    type: str
    balance: float
    currency: str = "USD"

class AccountCreate(AccountBase):
    """Schema for creating a new account, extends AccountBase."""
    pass

class Account(AccountBase):
    """
    Schema for account responses, extends AccountBase.
    
    Attributes:
        id (int): Account ID
        user_id (int): Owner's user ID
    """
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Expense Schemas
class ExpenseBase(BaseModel):
    """
    Base schema for expenses.
    
    Attributes:
        amount (float): Expense amount
        category (str): Expense category
        description (str): Expense description
        date (date): Transaction date
        is_recurring (bool): Whether the expense recurs
        recurring_period (str, optional): Recurrence period
    """
    amount: float
    category: str
    description: str
    date: date
    is_recurring: bool = False
    recurring_period: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense, extends ExpenseBase."""
    pass

class Expense(ExpenseBase):
    """
    Schema for expense responses, extends ExpenseBase.
    
    Attributes:
        id (int): Expense ID
        user_id (int): Owner's user ID
    """
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Income Schemas
class IncomeBase(BaseModel):
    """
    Base schema for income entries.
    
    Attributes:
        amount (float): Income amount
        source (str): Income source
        description (str): Income description
        date (date): Receipt date
        is_recurring (bool): Whether the income recurs
        recurring_period (str, optional): Recurrence period
    """
    amount: float
    source: str
    description: str
    date: date
    is_recurring: bool = False
    recurring_period: Optional[str] = None

class IncomeCreate(IncomeBase):
    """Schema for creating a new income entry, extends IncomeBase."""
    pass

class Income(IncomeBase):
    """
    Schema for income responses, extends IncomeBase.
    
    Attributes:
        id (int): Income ID
        user_id (int): Owner's user ID
    """
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Debt Schemas
class DebtBase(BaseModel):
    """
    Base schema for debts.
    
    Attributes:
        name (str): Debt name
        amount (float): Total debt amount
        interest_rate (float): Annual interest rate
        minimum_payment (float): Minimum payment amount
        due_date (date): Payment due date
        type (str): Debt type (student loan, credit card)
    """
    name: str
    amount: float
    interest_rate: float
    minimum_payment: float
    due_date: date
    type: str

class DebtCreate(DebtBase):
    """Schema for creating a new debt, extends DebtBase."""
    pass

class Debt(DebtBase):
    """
    Schema for debt responses, extends DebtBase.
    
    Attributes:
        id (int): Debt ID
        user_id (int): Owner's user ID
    """
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Goal Schemas
class GoalBase(BaseModel):
    """
    Base schema for financial goals.
    
    Attributes:
        name (str): Goal name
        target_amount (float): Target savings amount
        current_amount (float): Current progress
        deadline (date, optional): Goal deadline
        description (str, optional): Goal description
    """
    name: str
    target_amount: float
    current_amount: float = 0
    deadline: Optional[date] = None
    description: Optional[str] = None

class GoalCreate(GoalBase):
    """Schema for creating a new goal, extends GoalBase."""
    pass

class Goal(GoalBase):
    """
    Schema for goal responses, extends GoalBase.
    
    Attributes:
        id (int): Goal ID
        user_id (int): Owner's user ID
    """
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    """
    Schema for authentication tokens.
    
    Attributes:
        access_token (str): JWT access token
        token_type (str): Token type (e.g., "bearer")
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for token payload data.
    
    Attributes:
        email (str, optional): User's email from token
    """
    email: Optional[str] = None

# Report Schemas
class BudgetRecommendation(BaseModel):
    """
    Schema for budget recommendations.
    
    Attributes:
        category (str): Expense category
        recommended_amount (float): Recommended spending amount
        reason (str): Explanation for the recommendation
    """
    category: str
    recommended_amount: float
    reason: str

class FinancialReport(BaseModel):
    """
    Schema for comprehensive financial reports.
    
    Attributes:
        total_income (float): Total income amount
        total_expenses (float): Total expenses amount
        savings_rate (float): Savings rate percentage
        debt_overview (List[Debt]): List of all debts
        expense_breakdown (dict): Category-wise expenses
        recommendations (List[BudgetRecommendation]): Budget recommendations
        forecasting (dict): Expense forecasting for next three months
    """
    total_income: float
    total_expenses: float
    savings_rate: float
    debt_overview: List[Debt]
    expense_breakdown: dict
    recommendations: List[BudgetRecommendation]
    forecasting: dict = {}