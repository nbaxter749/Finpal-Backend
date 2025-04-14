"""
Financial Reports Routes

This module handles all routes related to financial reporting and analysis.
It provides endpoints for generating comprehensive financial reports that include
spending patterns, budget recommendations, and financial health metrics.

Features:
- Financial summary generation (delegated to service layer)
- Spending pattern analysis (handled by service layer)
- Budget recommendations (handled by service layer)
- Expense breakdown by category (handled by service layer)
- Debt overview (handled by service layer)
- Savings rate calculation (handled by service layer)
- AI-powered insights (handled by service layer)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.routes.auth import get_current_user
from app.database import get_db
from app.services import get_financial_summary as service_get_financial_summary

router = APIRouter()

@router.get("/reports/financial_summary", response_model=schemas.FinancialReport)
def get_financial_summary(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a comprehensive financial summary report for the current user
    by calling the financial service.
    
    Args:
        current_user: The authenticated user object (from dependency)
        db: Database session (passed to service)
        
    Returns:
        FinancialReport: A comprehensive financial report including AI insights.
        
    Raises:
        HTTPException: If the report generation fails in the service layer.
    """
    # Call the service function to get the financial summary
    try:
        financial_report = service_get_financial_summary(db=db, user_id=current_user.id)
        if financial_report is None:
            # Handle cases where the service might return None (e.g., user not found, though unlikely here)
            raise HTTPException(status_code=404, detail="Could not generate report for user")
        return financial_report
    except Exception as e:
        # Catch potential errors during report generation in the service layer
        # Log the error e
        print(f"Error generating financial summary: {e}") # Basic logging
        raise HTTPException(status_code=500, detail="Internal server error while generating financial report")
