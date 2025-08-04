"""
OpenAI Budget Analyzer Module

This module provides AI-powered financial analysis and budgeting recommendations
using the OpenAI API. It analyzes spending patterns, identifies trends, and 
generates personalized recommendations based on financial best practices.

Features:
- Spending pattern analysis
- Trend identification
- Category-based spending analysis
- Personalized budget recommendations
- Savings rate optimization
- Debt management guidance

Usage:
```python
# Import the main analysis function
from app.ml.openai_budget_analyzer import analyze_finances 

# Prepare data (example)
spending_data = [...] 
total_income = 5000
total_expenses = 4000
debts_list = [...] # List of SQLAlchemy Debt objects

# Get the combined financial analysis and recommendations
analysis_results = analyze_finances(
    spending_data=spending_data,
    total_income=total_income,
    total_expenses=total_expenses,
    debts=debts_list
)

# Access results
spending_patterns = analysis_results.get("spending_patterns")
recommendations = analysis_results.get("recommendations") # List of tuples: (category, amount, reason)
```
"""

import os
import json
import requests
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def analyze_finances(
    spending_data: List[Dict[str, Any]],
    total_income: float,
    total_expenses: float,
    debts: List
) -> Dict[str, Any]:
    """
    Analyze financial data and generate recommendations in a single API call.
    
    Args:
        spending_data: List of expense dictionaries
        total_income: Total monthly income
        total_expenses: Total monthly expenses
        debts: List of debt objects
        
    Returns:
        Dictionary containing:
            - spending_patterns: Analysis of spending
            - recommendations: Budget recommendations
    """
    if not spending_data:
        return {
            "spending_patterns": {
                "patterns": {},
                "trends": {},
                "average_spending": {}
            },
            "recommendations": [],
            "forecasting": {
                "month1": {},
                "month2": {},
                "month3": {}
            }
        }
    
    # Format expense data for the API
    formatted_expenses = ""
    for expense in spending_data:
        formatted_expenses += f"Date: {expense['date']}, Category: {expense['category']}, Amount: £{expense['amount']}, Description: {expense['description']}\n"
    
    # Format debt information
    debt_info = ""
    for i, debt in enumerate(debts):
        debt_info += f"Debt {i+1}: Amount: £{debt.amount}, Monthly Payment: £{debt.minimum_payment}\n"
    
    try:
        print("PROMPT SENT TO OPENAI:")
        print("""System prompt: You are a financial expert. Analyze the spending data and provide:
        1. Analysis of spending patterns
        2. Personalized budget recommendations based on individual spending patterns
        3. Expense forecasting for the next 3 months
        
        Follow these guidelines for recommendations:
        - Use the 50/30/20 rule (50% needs, 30% wants, 20% savings)
        - Housing costs should be below 35% of income
        - Debt payments should be below 20% of income
        - Tailor recommendations to actual spending habits and needs
        
        You MUST return your response as a JSON object structured exactly as follows:
        {
            "spending_patterns": {
                "patterns": {
                    "category1": {"proportion": float, "monthly_average": float},
                    "category2": {"proportion": float, "monthly_average": float}
                },
                "trends": {
                    "category1": {"direction": "increasing|decreasing|stable", "rate": float},
                    "category2": {"direction": "increasing|decreasing|stable", "rate": float}
                },
                "average_spending": {
                    "category1": float,
                    "category2": float
                }
            },
            "recommendations": [
                {
                    "category": "string",
                    "recommended_amount": float,
                    "reason": "string"
                },
                {
                    "category": "string",
                    "recommended_amount": float,
                    "reason": "string"
                }
            ],
            "forecasting": {
                "month1": {
                    "category1": float,
                    "category2": float,
                    "total": float
                },
                "month2": {
                    "category1": float,
                    "category2": float,
                    "total": float
                },
                "month3": {
                    "category1": float,
                    "category2": float,
                    "total": float
                }
            }
        }
        """)
        
        print(f"""User prompt: Analyze these financial details and provide both spending patterns analysis and budget recommendations:

        Monthly Income: £{total_income}
        Monthly Expenses: £{total_expenses}
        
        Expenses:
        {formatted_expenses}
        
        Debts:
        {debt_info}""")
        
        # Get API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Make direct API call using requests
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system", 
                    "content": """You are a financial expert. Analyze the spending data and provide:
                    1. Analysis of spending patterns
                    2. Personalized budget recommendations based on individual spending patterns
                    3. Expense forecasting for the next 3 months
                    
                    Follow these guidelines for recommendations:
                    - Use the 50/30/20 rule (50% needs, 30% wants, 20% savings)
                    - Housing costs should be below 35% of income
                    - Debt payments should be below 20% of income
                    - Tailor recommendations to actual spending habits and needs
                    
                    You MUST return your response as a JSON object structured exactly as follows:
                    {
                        "spending_patterns": {
                            "patterns": {
                                "category1": {"proportion": float, "monthly_average": float},
                                "category2": {"proportion": float, "monthly_average": float}
                            },
                            "trends": {
                                "category1": {"direction": "increasing|decreasing|stable", "rate": float},
                                "category2": {"direction": "increasing|decreasing|stable", "rate": float}
                            },
                            "average_spending": {
                                "category1": float,
                                "category2": float
                            }
                        },
                        "recommendations": [
                            {
                                "category": "string",
                                "recommended_amount": float,
                                "reason": "string"
                            },
                            {
                                "category": "string",
                                "recommended_amount": float,
                                "reason": "string"
                            }
                        ],
                        "forecasting": {
                            "month1": {
                                "category1": float,
                                "category2": float,
                                "total": float
                            },
                            "month2": {
                                "category1": float,
                                "category2": float,
                                "total": float
                            },
                            "month3": {
                                "category1": float,
                                "category2": float,
                                "total": float
                            }
                        }
                    }
                    """
                },
                {
                    "role": "user",
                    "content": f"""Analyze these financial details and provide both spending patterns analysis and budget recommendations:

                    Monthly Income: £{total_income}
                    Monthly Expenses: £{total_expenses}
                    
                    Expenses:
                    {formatted_expenses}
                    
                    Debts:
                    {debt_info}"""
                }
            ],
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            print(f"OpenAI API error: {response.status_code} - {response.text}")
            raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
        
        response_data = response.json()
        
        # Log the OpenAI response
        print("\nOPENAI RESPONSE (Complete Financial Analysis):")
        print(response_data["choices"][0]["message"]["content"])
        
        result = json.loads(response_data["choices"][0]["message"]["content"])
        
        # Extract recommendations in the expected tuple format
        recommendations = []
        for rec in result.get("recommendations", []):
            if isinstance(rec, dict) and "category" in rec and "recommended_amount" in rec and "reason" in rec:
                recommendations.append((
                    rec["category"],
                    float(rec["recommended_amount"]),
                    rec["reason"]
                ))
        
        return {
            "spending_patterns": result.get("spending_patterns", {
                "patterns": {},
                "trends": {},
                "average_spending": {}
            }),
            "recommendations": recommendations,
            "forecasting": result.get("forecasting", {
                "month1": {},
                "month2": {},
                "month3": {}
            })
        }
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # Return default values in case of error
        return {
            "spending_patterns": {
                "patterns": {},
                "trends": {},
                "average_spending": {}
            },
            "recommendations": [
                ("Savings", total_income * 0.2, "Try to save at least 20% of your income."),
                ("Expenses", total_income * 0.8, "Try to keep expenses below 80% of your income.")
            ],
            "forecasting": {
                "month1": {},
                "month2": {},
                "month3": {}
            }
        }
