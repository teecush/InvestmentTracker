"""
Investment Portfolio Tracker
A comprehensive Streamlit application for tracking and analyzing investment portfolios.

Author: TeeCush Portfolio Tracker
License: MIT
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Local imports
from utils import calculate_metrics, create_combo_chart, validate_input
from styles import apply_custom_styles, format_currency
from gsheets import load_data_from_sheet
from local_insights import generate_local_insights

# Page configuration
st.set_page_config(
    page_title="TeeCush Portfolio Tracker",
    page_icon="📈",
    layout="wide"
)

# Apply custom styles
apply_custom_styles()

# File path for persistent storage (as backup)
DATA_FILE = "transactions.csv"

# Google Sheet URL - Replace with your own publicly accessible Google Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1kD7e6Naq9dEIF1BaIZIQ31G5k7F_jqXP6IZQ4ZxZcIM/edit?usp=sharing"

# Initialize or load transactions data
if 'transactions' not in st.session_state or st.button("🔄 Refresh Data"):
    try:
        # Try to load from Google Sheets
        with st.spinner("Loading data from Google Sheets..."):
            df = load_data_from_sheet()
            if df is not None and not df.empty:
                st.session_state.transactions = df
                st.success("Data loaded successfully from Google Sheet!")
                
                # Save a backup to CSV file
                save_df = df.copy()
                save_df['Date'] = save_df['Date'].dt.strftime('%m/%d/%Y')
                save_df.to_csv(DATA_FILE, index=False)
            else:
                raise Exception("Failed to load data from Google Sheet")
    except Exception as e:
        st.error(f"Error loading data from Google Sheets: {str(e)}")
        # Fall back to local CSV if available
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
            st.session_state.transactions = df
            st.warning("Loaded data from local backup. Google Sheets connection failed.")
        else:
            # Initialize empty DataFrame
            st.session_state.transactions = pd.DataFrame(
                columns=['Date', 'Investment', 'Total Balance', 'Account Type', 'Notes']
            )
            st.warning("Could not load data from Google Sheets or local backup. Starting with empty data.")

# Main title
st.title("📊 TeeCush Portfolio Tracker")

# Info about data source
st.info("Data is being loaded directly from Google Sheets. Changes made in the connected spreadsheet will be reflected when you refresh the data.")

# Main content area
if not st.session_state.transactions.empty:
    # Calculate metrics
    metrics = calculate_metrics(st.session_state.transactions)

    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_currency(metrics["total_invested"])}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Invested</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_currency(metrics["current_balance"])}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Current Balance</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="earnings-value">{format_currency(metrics["total_earnings"])}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Earnings</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_currency(metrics["avg_monthly_earnings"])}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Avg Monthly Earnings</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{metrics["months_invested"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Months Invested</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Display combination chart
    st.plotly_chart(
        create_combo_chart(st.session_state.transactions),
        use_container_width=True
    )
    
    # Portfolio Insights Section
    st.header("🧠 Portfolio Insights")
    
    if st.button("✨ Generate Smart Insights"):
        with st.spinner("Analyzing your portfolio data..."):
            try:
                # Generate local insights that don't require an API
                insights = generate_local_insights(
                    st.session_state.transactions,
                    metrics
                )
                
                # Display insights in a nice looking container
                st.markdown(f'<div class="insights-container">{insights}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")
    else:
        st.info("Click the button above to generate data-driven insights about your investment portfolio.")
    
    # Transaction log
    st.header("Transaction Log")

    # Sort transactions by date
    sorted_transactions = st.session_state.transactions.sort_values(
        by='Date',
        ascending=False
    ).reset_index()  # Reset index for proper row deletion

    # Display transaction table with formatting and delete buttons
    for idx, row in sorted_transactions.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 3, 1])

        with col1:
            st.write(row['Date'].strftime('%m/%d/%Y'))
        with col2:
            st.write(format_currency(row['Investment']))
        with col3:
            st.write(format_currency(row['Total Balance']))
        with col4:
            st.write(row['Account Type'])
        with col5:
            st.write(row['Notes'] if pd.notna(row['Notes']) else '')
        with col6:
            if st.button('🗑️', key=f'delete_{idx}'):
                st.session_state.transactions = st.session_state.transactions.drop(row['index']).reset_index(drop=True)
                # Save to CSV file after deletion
                save_df = st.session_state.transactions.copy()
                save_df['Date'] = save_df['Date'].dt.strftime('%m/%d/%Y')
                save_df.to_csv(DATA_FILE, index=False)
                st.rerun()

    # Data Import/Export section
    st.subheader("Import/Export Data")
    col1, col2 = st.columns(2)

    with col1:
        # Download button
        download_df = st.session_state.transactions.copy()
        download_df['Date'] = download_df['Date'].dt.strftime('%m/%d/%Y')
        csv = download_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Transactions Data",
            data=csv,
            file_name="investment_transactions.csv",
            mime="text/csv",
        )

    with col2:
        # Upload button
        uploaded_file = st.file_uploader("📤 Import Previous Data (CSV)", type="csv")
        if uploaded_file is not None:
            try:
                imported_df = pd.read_csv(uploaded_file)
                imported_df['Date'] = pd.to_datetime(imported_df['Date'], format='%m/%d/%Y')

                # Combine with existing data
                st.session_state.transactions = pd.concat(
                    [st.session_state.transactions, imported_df],
                    ignore_index=True
                ).drop_duplicates()

                # Sort and save
                st.session_state.transactions = st.session_state.transactions.sort_values('Date')
                save_df = st.session_state.transactions.copy()
                save_df['Date'] = save_df['Date'].dt.strftime('%m/%d/%Y')
                save_df.to_csv(DATA_FILE, index=False)
                st.success("Data imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error importing data: Please ensure the CSV file matches the expected format")

else:
    st.info("No transactions yet. Add your first transaction using the sidebar!")

# Footer
st.markdown("---")
st.markdown(
    "💡 Track your investments across different account types and visualize your "
    "portfolio growth over time."
)