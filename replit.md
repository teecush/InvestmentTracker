# Investment Portfolio Tracker - Project Documentation

## Project Overview
An intelligent, user-friendly investment tracking web application that empowers users to manage and visualize their financial investments with precision and ease. Built with Streamlit, it integrates directly with Google Sheets for real-time data synchronization and provides comprehensive portfolio analysis.

## Recent Changes
- **2025-02**: Created GitHub-ready package with comprehensive documentation
- **2025-02**: Implemented Smart Insights feature with local analytics (no API required)
- **2025-02**: Fixed encoding issues and removed API dependency for core functionality
- **2025-02**: Moved Portfolio Insights section above Transaction Log per user request
- **2025-02**: Added proper file structure and deployment documentation

## Key Technologies
- **Frontend**: Streamlit web framework
- **Backend**: Python 3.11
- **Data Processing**: Pandas for data manipulation
- **Visualization**: Plotly for interactive charts
- **Storage**: Google Sheets integration with CSV backup
- **Analytics**: Built-in local insights engine

## Core Features
1. **Real-time Google Sheets Integration** - Automatic data sync
2. **Interactive Visualizations** - Combined bar/line charts
3. **Smart Portfolio Insights** - Local analysis without external APIs
4. **Multi-Account Support** - RSP, TFSA, FHSA, Slush Fund tracking
5. **Data Import/Export** - CSV backup and restore
6. **Responsive Design** - Works on all devices

## File Structure
```
├── main.py                 # Main Streamlit application
├── utils.py                # Data processing and chart utilities
├── styles.py               # CSS styling and formatting
├── gsheets.py              # Google Sheets integration
├── local_insights.py       # Portfolio analysis engine
├── .streamlit/config.toml  # Streamlit configuration
├── README.md               # Project documentation
├── DEPLOYMENT.md           # Deployment instructions
├── PROJECT_STRUCTURE.md    # Detailed file descriptions
├── LICENSE                 # MIT License
├── .gitignore              # Git exclusion rules
├── github_requirements.txt # Python dependencies
└── sample_data.csv         # Example data format
```

## User Preferences
- **Date Format**: MM/DD/YYYY for all inputs and displays
- **Currency Display**: Formatted with dollar signs and appropriate scaling (K, M)
- **Insights**: Prefers built-in analytics over API-dependent features
- **Layout**: Portfolio Insights above Transaction Log
- **Data Source**: Google Sheets integration with CSV backup

## Data Structure
- **Date**: Transaction date (MM/DD/YYYY)
- **Investment**: Amount invested (numeric)
- **Total Balance**: Current portfolio balance (numeric)
- **Account Type**: RSP, FHSA, TFSA, Slush Fund, 1/4ly Statement, "-"
- **Notes**: Transaction descriptions

## Key Metrics Tracked
- Total Invested
- Current Balance
- Total Earnings (gains/losses)
- Average Monthly Earnings
- Investment Duration (months)

## Project Architecture
- **Data Flow**: Google Sheets → Pandas DataFrame → Plotly Charts → Streamlit UI
- **Backup Strategy**: Primary data from Google Sheets, fallback to local CSV
- **Analysis Engine**: Local calculations for ROI, growth trends, projections
- **Visualization**: Combined bar chart (investments) + line chart (total value)

## Deployment Configuration
- **Streamlit Cloud**: Ready for one-click deployment
- **Local Development**: Full setup instructions provided
- **Google Sheets**: Public read-only access configured
- **Dependencies**: All packages specified in requirements file

## GitHub Package Contents
Essential files for GitHub upload:
1. Core application files (main.py, utils.py, styles.py, etc.)
2. Configuration files (.streamlit/config.toml, .gitignore)
3. Documentation (README.md, DEPLOYMENT.md, PROJECT_STRUCTURE.md)
4. Dependencies (github_requirements.txt - rename to requirements.txt)
5. Sample data and license files

## Development Notes
- Encoding issues resolved with local insights implementation
- Type hints present but minor LSP warnings don't affect functionality
- Optimized for Replit deployment with 0.0.0.0:5000 configuration
- Smart Insights feature provides comprehensive analysis without external APIs