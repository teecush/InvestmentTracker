# Deployment Guide

## Quick Deploy on Streamlit Cloud

1. **Upload to GitHub**:
   - Create a new repository on GitHub
   - Upload all files from this project
   - Rename `github_requirements.txt` to `requirements.txt`

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `main.py`
   - Click "Deploy"

## Local Development

1. **Setup Environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Run Application**:
```bash
streamlit run main.py
```

## Google Sheets Configuration

1. **Make Sheet Public**:
   - Open your Google Sheet
   - Click "Share" → "Change to anyone with the link"
   - Set permission to "Viewer"
   - Copy the share URL

2. **Update Configuration**:
   - Edit `main.py`
   - Replace `SHEET_URL` with your sheet URL
   - Ensure sheet has required columns: Date, Investment, Total Balance, Account Type, Notes

## Environment Variables (Optional)

For enhanced security in production:

```bash
# .streamlit/secrets.toml
SHEET_URL = "your-google-sheet-url"
OPENAI_API_KEY = "your-openai-key"  # Optional for AI insights
```

## Troubleshooting

**Common Issues**:
- **Google Sheets Access**: Ensure sheet is publicly readable
- **Date Format**: Use MM/DD/YYYY format in your sheet
- **Missing Data**: Check column names match exactly
- **Deployment Errors**: Verify all dependencies in requirements.txt

**Performance Tips**:
- Keep sheet data under 10,000 rows for optimal performance
- Use the refresh button to update data from sheets
- CSV backup ensures data persistence