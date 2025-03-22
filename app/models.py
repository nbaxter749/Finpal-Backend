from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
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
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # savings, checking, etc.
    balance = Column(Float)
    currency = Column(String, default="USD")
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="accounts")

class Expense(Base):
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
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    target_amount = Column(Float)
    current_amount = Column(Float, default=0)
    deadline = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="goals")