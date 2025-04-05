import os
import json
from datetime import datetime
import pandas as pd
from openai import OpenAI

# We'll get the API key from the app instead of environment variable
def get_openai_client(api_key=None):
    """
    Creates and returns an OpenAI client with the given API key.
    Falls back to environment variable if api_key is None.
    """
    if api_key:
        return OpenAI(api_key=api_key)
    else:
        return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_portfolio_insights(df: pd.DataFrame, metrics: dict, api_key=None) -> str:
    """
    Generate AI-powered insights about the investment portfolio.
    
    Args:
        df (pd.DataFrame): Transaction data
        metrics (dict): Portfolio metrics
        api_key (str, optional): OpenAI API key to use
        
    Returns:
        str: AI-generated insights
    """
    try:
        # Get OpenAI client with the provided API key
        client = get_openai_client(api_key)
        
        # Format transaction data into a readable format
        transactions_text = format_transactions_for_ai(df)
        
        # Format metrics into a readable format
        metrics_text = format_metrics_for_ai(metrics)
        
        # Current date for context
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Create prompt for OpenAI
        prompt = f"""
As an investment analysis AI, review this portfolio data and provide 3-5 key insights.
Today's date: {current_date}

PORTFOLIO METRICS:
{metrics_text}

TRANSACTION HISTORY:
{transactions_text}

Provide specific, data-driven insights about:
1. Performance trends and patterns
2. Growth rate and return on investment
3. Distribution across different account types
4. Suggestions for portfolio optimization

Format your response in bullet points starting with emoji icons.
Keep your analysis concise but insightful (max 250 words).
"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[
                {"role": "system", "content": "You are a financial analyst AI that provides concise, insightful analysis of investment portfolios."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        # Extract and return the insights
        insights = response.choices[0].message.content.strip()
        return insights
        
    except Exception as e:
        # Return error message if something goes wrong
        return f"⚠️ Could not generate insights: {str(e)}"

def format_transactions_for_ai(df: pd.DataFrame) -> str:
    """Format transaction data for the AI prompt"""
    if df.empty:
        return "No transaction data available."
        
    # Sort by date (newest to oldest)
    sorted_df = df.sort_values('Date', ascending=False).head(10)  # Only include the most recent 10 transactions
    
    # Format transactions as text
    transactions_text = ""
    for _, row in sorted_df.iterrows():
        date = row['Date'].strftime('%m/%d/%Y')
        investment = f"${row['Investment']:,.2f}" if pd.notna(row['Investment']) and row['Investment'] != 0 else "No investment"
        balance = f"${row['Total Balance']:,.2f}"
        account_type = row['Account Type'] if pd.notna(row['Account Type']) else '-'
        notes = row['Notes'] if pd.notna(row['Notes']) else ''
        
        transactions_text += f"Date: {date}, Investment: {investment}, Balance: {balance}, Account: {account_type}, Notes: {notes}\n"
    
    return transactions_text

def format_metrics_for_ai(metrics: dict) -> str:
    """Format portfolio metrics for the AI prompt"""
    return f"""
Total Invested: ${metrics['total_invested']:,.2f}
Current Balance: ${metrics['current_balance']:,.2f}
Total Earnings: ${metrics['total_earnings']:,.2f}
Average Monthly Earnings: ${metrics['avg_monthly_earnings']:,.2f}
Months Invested: {metrics['months_invested']}
"""