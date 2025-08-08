# Project Structure

## Core Application Files

### `main.py`
- **Purpose**: Main Streamlit application entry point
- **Key Functions**:
  - Data loading from Google Sheets
  - UI components and layout
  - Transaction management
  - Portfolio insights integration
- **Dependencies**: All other modules

### `utils.py`
- **Purpose**: Utility functions for data processing and visualization
- **Key Functions**:
  - `calculate_metrics()`: Portfolio calculations
  - `create_combo_chart()`: Interactive Plotly visualizations
  - `validate_input()`: Data validation
- **Dependencies**: pandas, plotly

### `styles.py`
- **Purpose**: CSS styling and UI formatting
- **Key Functions**:
  - `apply_custom_styles()`: Streamlit CSS injection
  - `format_currency()`: Number formatting
- **Dependencies**: streamlit

### `gsheets.py`
- **Purpose**: Google Sheets integration
- **Key Functions**:
  - `load_data_from_sheet()`: Fetch data from public Google Sheet
  - Data parsing and column mapping
- **Dependencies**: gspread, pandas

### `local_insights.py`
- **Purpose**: Portfolio analysis and insights generation
- **Key Functions**:
  - `generate_local_insights()`: Creates portfolio analysis
  - Performance calculations
  - Growth trend analysis
- **Dependencies**: pandas, datetime

## Configuration Files

### `.streamlit/config.toml`
- **Purpose**: Streamlit server configuration
- **Settings**: Port, address, headless mode

### `github_requirements.txt`
- **Purpose**: Python package dependencies
- **Note**: Rename to `requirements.txt` when deploying

### `.gitignore`
- **Purpose**: Git exclusion rules
- **Excludes**: Local data, API keys, IDE files

## Documentation Files

### `README.md`
- **Purpose**: Project overview and setup instructions
- **Sections**: Features, installation, usage, file structure

### `DEPLOYMENT.md`
- **Purpose**: Deployment instructions for various platforms
- **Covers**: Streamlit Cloud, local development, configuration

### `LICENSE`
- **Purpose**: MIT License for open source distribution

### `sample_data.csv`
- **Purpose**: Example data format for testing
- **Format**: Date, Investment, Total Balance, Account Type, Notes

## Data Flow

1. **Data Source**: Google Sheets (primary) → CSV backup (fallback)
2. **Processing**: Raw data → Pandas DataFrame → Metrics calculation
3. **Visualization**: Processed data → Plotly charts → Streamlit UI
4. **Analysis**: Historical data → Local insights → User display

## Key Features

- **Real-time sync** with Google Sheets
- **Automatic backup** to local CSV
- **Interactive charts** with date-based filtering
- **Portfolio insights** without external API dependencies
- **Multi-account support** (RSP, TFSA, FHSA, etc.)
- **Data import/export** functionality

## Security Considerations

- No API keys required for core functionality
- Google Sheets used in read-only mode
- Local data backup for offline access
- Sensitive data excluded from version control