from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from app import models, schemas
from app.routes.auth import get_current_user
from app.database import get_db
from app.ml.budget_analyzer import analyze_spending_patterns, generate_recommendations

router = APIRouter()

@router.get("/reports/financial_summary", response_model=schemas.FinancialReport)
def get_financial_summary(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get user's financial data
    expenses = db.query(models.Expense).filter(models.Expense.user_id == current_user.id).all()
    incomes = db.query(models.Income).filter(models.Income.user_id == current_user.id).all()
    debts = db.query(models.Debt).filter(models.Debt.user_id == current_user.id).all()
    
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
    
    # Get spending patterns and recommendations
    spending_data = [{
        "amount": expense.amount,
        "category": expense.category,
        "date": expense.date,
        "description": expense.description
    } for expense in expenses]
    
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
