import streamlit as st

def apply_custom_styles():
    # Custom CSS styles for the application
    st.markdown("""
        <style>
        .main {
            padding: 1rem;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #1f77b4;
        }
        .earnings-value {
            font-size: 24px;
            font-weight: bold;
            color: #2ecc71;  /* Green color for earnings */
        }
        .metric-label {
            font-size: 14px;
            color: #666;
        }
        .stDataFrame {
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)

def format_currency(value):
    return f"${value:,.2f}"
