# Investment Portfolio Tracker

A comprehensive, user-friendly investment tracking web application built with Streamlit that helps you manage and visualize your financial investments with precision and ease.

## Features

- **Real-time Data Integration**: Connects directly to Google Sheets for automatic data synchronization
- **Interactive Visualizations**: Combined bar and line charts showing investment contributions and portfolio growth
- **Smart Portfolio Insights**: Built-in analysis providing performance metrics and growth projections
- **Multiple Account Types**: Support for RSP, TFSA, FHSA, and other investment accounts
- **Data Import/Export**: CSV-based backup and restore functionality
- **Responsive Design**: Clean, professional interface that works on all devices

## Technologies Used

- **Frontend**: Streamlit web framework
- **Backend**: Python 3.11
- **Data Processing**: Pandas for data manipulation
- **Visualization**: Plotly for interactive charts
- **Storage**: Google Sheets integration with CSV backup
- **Deployment**: Optimized for Replit hosting

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd investment-portfolio-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Sheets:
   - Create a publicly accessible Google Sheet
   - Update the `SHEET_URL` variable in `main.py` with your sheet URL

4. Configure Streamlit:
```bash
mkdir .streamlit
```
Create `.streamlit/config.toml` with:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## Usage

1. Run the application:
```bash
streamlit run main.py
```

2. Access the app at `http://localhost:5000`

3. The app will automatically load data from your connected Google Sheet

## Data Format

Your Google Sheet should have the following columns:
- **Date**: Transaction date (MM/DD/YYYY format)
- **Investment**: Amount invested (numeric)
- **Total Balance**: Current portfolio balance (numeric)
- **Account Type**: Type of account (RSP, TFSA, FHSA, etc.)
- **Notes**: Additional transaction notes

## Key Metrics Tracked

- Total Amount Invested
- Current Portfolio Balance
- Total Earnings (gains/losses)
- Average Monthly Earnings
- Investment Duration (months)

## Smart Insights Features

The built-in analytics provide:
- Performance analysis and ROI calculations
- Growth trend identification
- Account distribution insights
- Future projection estimates
- Monthly performance tracking

## File Structure

```
├── main.py              # Main Streamlit application
├── utils.py             # Utility functions for calculations and charts
├── styles.py            # CSS styling and formatting
├── gsheets.py           # Google Sheets integration
├── local_insights.py    # Portfolio analysis engine
├── .streamlit/
│   └── config.toml      # Streamlit configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on GitHub or contact the maintainer.