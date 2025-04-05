import os
from twilio.rest import Client

def send_twilio_message(to_phone_number: str, message: str) -> bool:
    """
    Send an SMS message using Twilio.
    
    Args:
        to_phone_number (str): The recipient's phone number in E.164 format (e.g., +12125551234)
        message (str): The message to send
        
    Returns:
        bool: True if the message was sent successfully, False otherwise
    """
    try:
        # Get Twilio credentials from environment variables
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN") 
        from_phone = os.environ.get("TWILIO_PHONE_NUMBER")
        
        # Check if all required credentials are available
        if not all([account_sid, auth_token, from_phone]):
            print("Error: Missing Twilio credentials")
            return False
            
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send the message
        message = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone_number
        )
        
        print(f"Message sent successfully with SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False


def generate_portfolio_update_message(metrics):
    """
    Generate a formatted message with portfolio metrics.
    
    Args:
        metrics (dict): Dictionary containing portfolio metrics
        
    Returns:
        str: Formatted message for SMS
    """
    return (
        f"Portfolio Update:\n"
        f"Total Invested: ${metrics['total_invested']:,.2f}\n"
        f"Current Balance: ${metrics['current_balance']:,.2f}\n"
        f"Total Earnings: ${metrics['total_earnings']:,.2f}\n"
        f"Avg Monthly Earnings: ${metrics['avg_monthly_earnings']:,.2f}\n"
        f"Months Invested: {metrics['months_invested']}"
    )