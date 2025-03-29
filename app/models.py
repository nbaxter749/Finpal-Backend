"""
Database Models Module

This module defines the SQLAlchemy ORM models for the application.
It contains all database table definitions and their relationships.

Models:
- User: Core user account information
- Account: Financial accounts (savings, checking)
- Expense: User expenses and recurring payments
- Income: User income sources and recurring income
- Debt: User debts and loans
- Goal: Financial goals and savings targets

Features:
- SQLAlchemy ORM models
- Table relationships and foreign keys
- Data validation constraints
- Default values
- Timestamps and audit fields
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    """
    User model representing application users.
    
    Attributes:
        id (int): Primary key
        email (str): Unique email address
        hashed_password (str): Securely hashed password
        is_active (bool): Account status
        first_name (str): User's first name
        last_name (str): User's last name
        created_at (datetime): Account creation timestamp
        
    Relationships:
        accounts: One-to-many with Account
        expenses: One-to-many with Expense
        incomes: One-to-many with Income
        debts: One-to-many with Debt
        goals: One-to-many with Goal
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    
    accounts = relationship("Account", back_populates="owner")
    expenses = relationship("Expense", back_populates="owner")
    incomes = relationship("Income", back_populates="owner")
    debts = relationship("Debt", back_populates="owner")
    goals = relationship("Goal", back_populates="owner")

class Account(Base):
    """
    Account model representing financial accounts.
    
    Attributes:
        id (int): Primary key
        name (str): Account name
        type (str): Account type (savings, checking)
        balance (float): Current balance
        currency (str): Account currency (default: USD)
        user_id (int): Foreign key to User
        
    Relationships:
        owner: Many-to-one with User
    """
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # savings, checking, etc.
    balance = Column(Float)
    currency = Column(String, default="USD")
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="accounts")

class Expense(Base):
    """
    Expense model representing user expenses.
    
    Attributes:
        id (int): Primary key
        amount (float): Expense amount
        category (str): Expense category
        description (str): Expense description
        date (date): Transaction date
        is_recurring (bool): Recurring status
        recurring_period (str): Recurrence period
        user_id (int): Foreign key to User
        
    Relationships:
        owner: Many-to-one with User
    """
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    category = Column(String)  # food, rent, utilities, etc.
    description = Column(String)
    date = Column(Date)
    is_recurring = Column(Boolean, default=False)
    recurring_period = Column(String, nullable=True)  # monthly, weekly, etc.
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="expenses")

class Income(Base):
    """
    Income model representing user income sources.
    
    Attributes:
        id (int): Primary key
        amount (float): Income amount
        source (str): Income source
        description (str): Income description
        date (date): Receipt date
        is_recurring (bool): Recurring status
        recurring_period (str): Recurrence period
        user_id (int): Foreign key to User
        
    Relationships:
        owner: Many-to-one with User
    """
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    source = Column(String)  # job, scholarship, etc.
    description = Column(String)
    date = Column(Date)
    is_recurring = Column(Boolean, default=False)
    recurring_period = Column(String, nullable=True)  # monthly, weekly, etc.
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="incomes")

class Debt(Base):
    """
    Debt model representing user debts and loans.
    
    Attributes:
        id (int): Primary key
        name (str): Debt name
        amount (float): Total debt amount
        interest_rate (float): Annual interest rate
        minimum_payment (float): Minimum payment amount
        due_date (date): Payment due date
        type (str): Debt type (student loan, credit card)
        user_id (int): Foreign key to User
        
    Relationships:
        owner: Many-to-one with User
    """
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    amount = Column(Float)
    interest_rate = Column(Float)
    minimum_payment = Column(Float)
    due_date = Column(Date)
    type = Column(String)  # student loan, credit card, etc.
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="debts")

class Goal(Base):
    """
    Goal model representing financial goals.
    
    Attributes:
        id (int): Primary key
        name (str): Goal name
        target_amount (float): Target savings amount
        current_amount (float): Current progress
        deadline (date): Goal deadline
        description (str): Goal description
        user_id (int): Foreign key to User
        
    Relationships:
        owner: Many-to-one with User
    """
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    target_amount = Column(Float)
    current_amount = Column(Float, default=0)
    deadline = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="goals")