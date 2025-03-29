"""
Budget Analyzer Module

This module provides AI-powered financial analysis and budgeting recommendations.
It analyzes spending patterns, identifies trends, and generates personalized
recommendations based on financial best practices.

Features:
- Spending pattern analysis
- Trend identification
- Category-based spending analysis
- Personalized budget recommendations
- Savings rate optimization
- Debt management guidance
- Category-specific spending thresholds

Usage:
```python
from app.ml.budget_analyzer import analyze_spending_patterns, generate_recommendations

# Analyze spending patterns
patterns = analyze_spending_patterns(spending_data)

# Generate recommendations
recommendations = generate_recommendations(
    patterns,
    total_income=5000,
    total_expenses=4000,
    debts=debts_list
)
```
"""

from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from collections import defaultdict

def analyze_spending_patterns(spending_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze spending patterns from historical expense data.
    
    This function processes historical spending data to identify:
    - Monthly spending averages by category
    - Spending trends (increasing/decreasing)
    - Category-wise spending proportions
    - Overall spending patterns
    
    Args:
        spending_data: List of expense dictionaries containing:
            - amount: float
            - category: str
            - date: str (YYYY-MM-DD)
            - description: str
        
    Returns:
        Dictionary containing:
            - patterns: Category-wise spending patterns and proportions
            - trends: Category-wise spending trends
            - average_spending: Monthly averages by category
    """
    if not spending_data:
        return {
            "patterns": {},
            "trends": {},
            "average_spending": {}
        }
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(spending_data)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.strftime('%Y-%m')
    
    # Calculate monthly averages by category
    monthly_avg = df.groupby(['category', 'month'])['amount'].sum().groupby('category').mean()
    monthly_avg = monthly_avg.to_dict()
    
    # Identify spending trends (increasing or decreasing)
    trends = {}
    categories = df['category'].unique()
    
    for category in categories:
        category_data = df[df['category'] == category].sort_values('date')
        if len(category_data) >= 3:  # Need at least 3 data points for trend
            amounts = category_data['amount'].values
            if len(amounts) > 1:
                # Simple trend calculation
                trend = np.polyfit(range(len(amounts)), amounts, 1)[0]
                direction = "increasing" if trend > 0 else "decreasing" if trend < 0 else "stable"
                trends[category] = {
                    "direction": direction,
                    "rate": abs(trend)
                }
    
    # Calculate overall spending pattern
    patterns = defaultdict(dict)
    
    # Proportion of spending by category
    total_spending = df['amount'].sum()
    for category in categories:
        category_total = df[df['category'] == category]['amount'].sum()
        patterns[category]["proportion"] = (category_total / total_spending) * 100 if total_spending > 0 else 0
        patterns[category]["monthly_average"] = monthly_avg.get(category, 0)
    
    return {
        "patterns": dict(patterns),
        "trends": trends,
        "average_spending": monthly_avg
    }

def generate_recommendations(
    spending_patterns: Dict[str, Any],
    total_income: float,
    total_expenses: float,
    debts: List
) -> List[Tuple[str, float, str]]:
    """
    Generate budgeting recommendations based on spending patterns.
    
    This function analyzes financial data and generates personalized
    recommendations based on:
    - 50/30/20 budgeting rule
    - Category-specific spending thresholds
    - Debt-to-income ratios
    - Savings rate optimization
    
    Args:
        spending_patterns: Output from analyze_spending_patterns
        total_income: Total monthly income
        total_expenses: Total monthly expenses
        debts: List of debt objects containing:
            - amount: float
            - minimum_payment: float
        
    Returns:
        List of tuples containing:
            - category: str (category name)
            - recommended_amount: float (suggested spending amount)
            - reason: str (explanation of recommendation)
    """
    recommendations = []
    patterns = spending_patterns.get("patterns", {})
    trends = spending_patterns.get("trends", {})
    
    # Calculate recommended savings (20% of income as a rule of thumb)
    recommended_savings = total_income * 0.2
    current_savings = total_income - total_expenses
    
    if current_savings < recommended_savings:
        savings_gap = recommended_savings - current_savings
        recommendations.append(
            ("Savings", recommended_savings, 
             f"Try to save at least 20% of your income (£{recommended_savings:.2f}). "
             f"You're currently saving £{current_savings:.2f}, which is "
             f"£{savings_gap:.2f} less than recommended.")
        )
    
    # Calculate debt payments (should be around 15-20% max of income)
    total_debt = sum(debt.amount for debt in debts)
    total_min_payments = sum(debt.minimum_payment for debt in debts)
    
    if total_min_payments > total_income * 0.2:
        recommendations.append(
            ("Debt Payments", total_income * 0.2,
             f"Your debt payments are too high relative to your income. "
             f"Try to keep debt payments below 20% of your income.")
        )
    
    # Check high-spending categories
    for category, details in patterns.items():
        proportion = details.get("proportion", 0)
        
        # Different thresholds for different categories
        threshold = 0
        reason = ""
        
        if category.lower() == "rent" or category.lower() == "housing":
            threshold = 35  # 35% of total spending
            reason = "Housing costs should ideally be below 35% of your total spending."
        elif category.lower() == "food" or category.lower() == "groceries":
            threshold = 15  # 15% of total spending
            reason = "Food costs should ideally be around 10-15% of your total spending."
        elif category.lower() in ["entertainment", "dining out", "shopping"]:
            threshold = 10  # 10% of total spending
            reason = f"{category} spending should ideally be kept under 10% of your total spending."
        elif category.lower() in ["utilities", "transportation"]:
            threshold = 10  # 10% of total spending
            reason = f"{category} costs should ideally be kept under 10% of your total spending."
        
        if threshold > 0 and proportion > threshold:
            monthly_avg = details.get("monthly_average", 0)
            recommended_amount = (threshold / 100) * total_expenses
            
            if category in trends and trends[category]["direction"] == "increasing":
                reason += f" This category is trending upward, which is concerning."
            
            recommendations.append(
                (category, recommended_amount,
                 f"Your {category} spending is {proportion:.1f}% of your total expenses, "
                 f"which is higher than the recommended {threshold}%. {reason} "
                 f"Consider reducing to around £{recommended_amount:.2f} per month.")
            )
    
    return recommendations