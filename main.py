import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

    # Convert date input to DD/MM/YYYY format
    date_str = st.text_input("Date (DD/MM/YYYY)", datetime.today().strftime('%d/%m/%Y'))
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
            date = datetime.strptime(date_str, '%d/%m/%Y')
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

    # CSV Upload
    st.sidebar.markdown("---")
    st.sidebar.header("Import Data")
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])

    if uploaded_file is not None:
        try:
            # Read the uploaded file
            csv_content = uploaded_file.getvalue().decode('utf-8')
            imported_df = import_csv_data(csv_content)

            # Update the session state with imported data
            st.session_state.transactions = imported_df
            st.sidebar.success("Data imported successfully!")
        except Exception as e:
            st.sidebar.error(f"Error importing data: {str(e)}")


def import_csv_data(csv_content):
    try:
        df = pd.read_csv(pd.compat.StringIO(csv_content))
        #Basic data type validation.  More robust validation would be needed in a production system.
        for col in ['Date', 'Investment', 'Total Balance']:
            if df[col].dtype != 'object' and df[col].dtype != 'float64' and df[col].dtype != 'int64':
                raise ValueError(f"Column '{col}' has an unexpected data type.")
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
        return df
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty.")
    except pd.errors.ParserError:
        raise ValueError("Error parsing CSV file. Please check the file format.")
    except KeyError as e:
        raise ValueError(f"Missing column in CSV file: {e}")
    except ValueError as e:
        raise


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
    )

    # Display transaction table with formatting
    displayed_transactions = sorted_transactions.copy()
    displayed_transactions['Date'] = displayed_transactions['Date'].dt.strftime('%d/%m/%Y')

    st.dataframe(
        displayed_transactions.style.format({
            'Investment': '${:,.2f}',
            'Total Balance': '${:,.2f}'
        }),
        use_container_width=True
    )
else:
    st.info("No transactions yet. Add your first transaction using the sidebar!")

# Footer
st.markdown("---")
st.markdown(
    "💡 Track your investments across different account types and visualize your "
    "portfolio growth over time."
)