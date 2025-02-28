import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from typing import Tuple, Dict

def calculate_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate key investment metrics"""
    total_invested = df['Investment'].sum()
    current_balance = df['Total Balance'].iloc[-1] if not df.empty else 0
    total_earnings = current_balance - total_invested
    
    # Calculate months invested
    if not df.empty:
        start_date = pd.to_datetime(df['Date'].min())
        end_date = pd.to_datetime(df['Date'].max())
        months_invested = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        avg_monthly_earnings = total_earnings / max(months_invested, 1)
    else:
        months_invested = 0
        avg_monthly_earnings = 0

    return {
        'total_invested': total_invested,
        'current_balance': current_balance,
        'total_earnings': total_earnings,
        'avg_monthly_earnings': avg_monthly_earnings,
        'months_invested': months_invested
    }

def create_combo_chart(df: pd.DataFrame) -> go.Figure:
    """Create combination chart with bars for investments and line for total balance"""
    fig = go.Figure()

    # Add bar chart for investments
    fig.add_trace(
        go.Bar(
            x=df['Date'],
            y=df['Investment'],
            name='Investment',
            marker_color='#2ecc71'
        )
    )

    # Add line chart for total balance
    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Total Balance'],
            name='Total Balance',
            line=dict(color='#3498db', width=2),
            mode='lines+markers'
        )
    )

    # Update layout
    fig.update_layout(
        title='Investment History and Balance Over Time',
        xaxis_title='Date',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        showlegend=True,
        template='plotly_white',
        height=500,
        xaxis=dict(
            type='date',
            tickformat='%Y-%m-%d',
            tickangle=45
        )
    )

    return fig

def validate_input(date: str, amount: float, balance: float, account_type: str) -> Tuple[bool, str]:
    """Validate user input for new transactions"""
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD"
    
    if amount < 0:
        return False, "Investment amount cannot be negative"
    
    if balance < 0:
        return False, "Total balance cannot be negative"
    
    if not account_type:
        return False, "Account type is required"
    
    return True, ""
