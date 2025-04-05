import pandas as pd
import os
import json
from datetime import datetime

# Google Sheet ID 
SHEET_ID = "1kD7e6Naq9dEIF1BaIZIQ31G5k7F_jqXP6IZQ4ZxZcIM"

def load_data_from_sheet():
    """
    Load data from a publicly shared Google Sheet.
    Returns a pandas DataFrame with the investment data.
    """
    try:
        # URL for the published CSV version of the sheet
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
        
        # Read the data into a pandas DataFrame
        df = pd.read_csv(url)
        
        # Process/clean the data
        df = process_sheet_data(df)
        
        return df
    except Exception as e:
        print(f"Error loading data from Google Sheet: {str(e)}")
        return None

def process_sheet_data(df):
    """
    Process and clean the data from the Google Sheet.
    Handles column naming, date formatting, and data type conversions.
    """
    try:
        # Make a copy to avoid SettingWithCopyWarning
        df = df.copy()
        
        # Print the column names for debugging
        print(f"Original columns: {list(df.columns)}")
        
        # Rename columns (assuming the sheet has headers)
        expected_columns = ['Date', 'Investment', 'Total Balance', 'Account Type', 'Notes']
        
        # Check if the DataFrame has expected number of columns
        if len(df.columns) >= 5:
            # Rename columns to match the expected format
            df.columns = expected_columns + list(df.columns[5:])
            
            # Print first few rows for debugging
            print("Sample data after column renaming:")
            print(df.head())
            
            # Convert date strings to datetime objects
            df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
            
            # Drop rows with invalid dates
            df = df.dropna(subset=['Date'])
            
            # Clean financial columns (remove '$' and ',' characters)
            df['Investment'] = df['Investment'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
            df['Total Balance'] = df['Total Balance'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
            
            # Convert to numeric
            df['Investment'] = pd.to_numeric(df['Investment'], errors='coerce')
            df['Total Balance'] = pd.to_numeric(df['Total Balance'], errors='coerce')
            
            # Fill NaN in text columns with empty string
            df['Account Type'] = df['Account Type'].fillna('-')
            df['Notes'] = df['Notes'].fillna('')
            
            # Sort by date
            df = df.sort_values('Date')
            
            # Print sample of processed data
            print("Processed data:")
            print(df.head())
            
            return df
        else:
            print(f"Sheet does not have expected columns. Found: {list(df.columns)}")
            return pd.DataFrame(columns=expected_columns)
    except Exception as e:
        print(f"Error processing sheet data: {str(e)}")
        return pd.DataFrame(columns=expected_columns)