import streamlit as st
import pandas as pd
from datetime import datetime
from utils import calculate_metrics, create_combo_chart, validate_input
from styles import apply_custom_styles, format_currency

# Page configuration
st.set_page_config(
    page_title="Investment Tracker",
    page_icon="📈",
    layout="wide"
)

# Apply custom styles
apply_custom_styles()

# Initialize session state for data storage
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(
        columns=['Date', 'Investment', 'Total Balance', 'Account Type', 'Notes']
    )

# Main title
st.title("📊 Investment Portfolio Tracker")

# Sidebar for adding new transactions
with st.sidebar:
    st.header("Add New Transaction")

    # Convert date input to MM/DD/YYYY format
    date_str = st.text_input("Date (MM/DD/YYYY)", datetime.today().strftime('%m/%d/%Y'))
    investment = st.number_input("Investment Amount", min_value=0.0, step=100.0)
    total_balance = st.number_input("Total Balance", min_value=0.0, step=100.0)
    account_type = st.selectbox(
        "Account Type",
        options=["RSP", "FHSA", "TFSA", "Slush Fund", "1/4ly Statement", "-"]
    )
    notes = st.text_area("Notes")

    if st.button("Add Transaction"):
        valid, message = validate_input(
            date_str,
            investment,
            total_balance,
            account_type
        )

        if valid:
            # Convert date string to datetime object
            date = datetime.strptime(date_str, '%m/%d/%Y')
            new_transaction = pd.DataFrame([{
                'Date': date,
                'Investment': investment,
                'Total Balance': total_balance,
                'Account Type': account_type,
                'Notes': notes
            }])

            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, new_transaction],
                ignore_index=True
            )
            st.success("Transaction added successfully!")
        else:
            st.error(message)

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
        st.markdown(f'<div class="metric-value">{format_currency(metrics["total_earnings"])}</div>', unsafe_allow_html=True)
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
                st.rerun()

else:
    st.info("No transactions yet. Add your first transaction using the sidebar!")

# Footer
st.markdown("---")
st.markdown(
    "💡 Track your investments across different account types and visualize your "
    "portfolio growth over time."
)