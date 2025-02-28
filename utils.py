import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from typing import Tuple, Dict
from io import StringIO

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
            tickformat='%d/%m/%Y',  # Updated date format
            tickangle=45,
            dtick='M1',  # Show tick for every month
            tickmode='auto',
            nticks=20  # Maximum number of ticks to show
        )
    )

    return fig

def validate_input(date: str, amount: float, balance: float, account_type: str) -> Tuple[bool, str]:
    """Validate user input for new transactions"""
    try:
        datetime.strptime(date, '%d/%m/%Y')
    except ValueError:
        return False, "Invalid date format. Please use DD/MM/YYYY"

    if amount < 0:
        return False, "Investment amount cannot be negative"

    if balance < 0:
        return False, "Total balance cannot be negative"

    if not account_type:
        return False, "Account type is required"

    return True, ""

def import_csv_data(file_content: str) -> pd.DataFrame:
    """Import data from CSV content string"""
    try:
        # Create DataFrame from CSV content
        df = pd.read_csv(StringIO(file_content))

        # Verify required columns exist
        required_columns = ['Date', 'Investment', 'Total Balance', 'Account Type', 'Notes']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        # Convert date strings to datetime objects
        try:
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        except ValueError:
            raise ValueError("Date format should be DD/MM/YYYY")

        # Clean currency strings and convert to numeric
        for col in ['Investment', 'Total Balance']:
            df[col] = df[col].astype(str).str.replace('$', '').str.replace(',', '')
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].isna().any():
                raise ValueError(f"Invalid numeric values found in {col} column")

        # Fill NaN values with 0 for Investment column
        df['Investment'] = df['Investment'].fillna(0)

        # Validate Account Type values
        valid_account_types = ["RSP", "FHSA", "TFSA", "Slush Fund", "1/4ly Statement", "-"]
        invalid_types = df['Account Type'].unique().tolist()
        invalid_types = [t for t in invalid_types if t not in valid_account_types]
        if invalid_types:
            raise ValueError(f"Invalid account types found: {', '.join(map(str, invalid_types))}")

        return df
    except pd.errors.EmptyDataError:
        raise ValueError("The CSV file is empty")
    except pd.errors.ParserError:
        raise ValueError("Error parsing CSV file. Please ensure it's properly formatted")
    except Exception as e:
        raise ValueError(f"Error importing CSV data: {str(e)}")