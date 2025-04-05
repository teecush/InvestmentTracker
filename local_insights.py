import pandas as pd
from datetime import datetime
import calendar
import math

def generate_local_insights(df: pd.DataFrame, metrics: dict) -> str:
    """
    Generate insights about the investment portfolio using local analysis.
    
    Args:
        df (pd.DataFrame): Transaction data
        metrics (dict): Portfolio metrics
        
    Returns:
        str: Generated insights
    """
    insights = []
    
    # Get basic data
    months_invested = metrics['months_invested']
    total_invested = metrics['total_invested']
    current_balance = metrics['current_balance']
    total_earnings = metrics['total_earnings']
    avg_monthly_earnings = metrics['avg_monthly_earnings']
    
    # 1. Overall performance insight
    roi_percent = (total_earnings / total_invested) * 100 if total_invested > 0 else 0
    annualized_roi = (roi_percent / months_invested) * 12 if months_invested > 0 else 0
    
    if roi_percent > 15:
        performance_insight = f"💰 Excellent performance! Your portfolio has earned {roi_percent:.1f}% returns " \
                             f"({annualized_roi:.1f}% annualized), which is significantly above average market returns."
    elif roi_percent > 8:
        performance_insight = f"📈 Good performance! Your portfolio has earned {roi_percent:.1f}% returns " \
                             f"({annualized_roi:.1f}% annualized), which is above average market returns."
    elif roi_percent > 0:
        performance_insight = f"✅ Your portfolio is showing positive returns of {roi_percent:.1f}% " \
                             f"({annualized_roi:.1f}% annualized), which is a good foundation."
    else:
        performance_insight = f"⚠️ Your portfolio is currently showing {roi_percent:.1f}% returns. " \
                             f"This might improve with more time in the market."
    
    insights.append(performance_insight)
    
    # 2. Growth trend insight
    if len(df) >= 3:
        # Get first and last balance entries with timestamps at least 1 month apart
        sorted_df = df.sort_values('Date')
        first_date = sorted_df.iloc[0]['Date']
        last_date = sorted_df.iloc[-1]['Date']
        
        # Only calculate growth if we have at least one month of data
        if (last_date - first_date).days >= 30:
            first_balance = sorted_df.iloc[0]['Total Balance']
            last_balance = sorted_df.iloc[-1]['Total Balance']
            
            # Calculate monthly growth rate
            months_between = (last_date.year - first_date.year) * 12 + (last_date.month - first_date.month)
            if months_between > 0:
                monthly_growth_rate = ((last_balance / first_balance) ** (1/months_between) - 1) * 100
                
                if monthly_growth_rate > 3:
                    growth_insight = f"🚀 Impressive growth rate! Your portfolio is growing at approximately {monthly_growth_rate:.1f}% per month."
                elif monthly_growth_rate > 1:
                    growth_insight = f"📈 Solid growth rate! Your portfolio is growing at approximately {monthly_growth_rate:.1f}% per month."
                elif monthly_growth_rate > 0:
                    growth_insight = f"📊 Your portfolio is growing steadily at approximately {monthly_growth_rate:.1f}% per month."
                else:
                    growth_insight = f"📉 Your portfolio has shown a change of {monthly_growth_rate:.1f}% per month over the analyzed period."
                
                insights.append(growth_insight)
    
    # 3. Account distribution insight
    account_distribution = {}
    for _, row in df.iterrows():
        if pd.notna(row['Account Type']) and row['Account Type'] != '-':
            if row['Account Type'] not in account_distribution:
                account_distribution[row['Account Type']] = 0
            
            # Add investments to the account type
            if pd.notna(row['Investment']) and row['Investment'] > 0:
                account_distribution[row['Account Type']] += row['Investment']
    
    # Generate insight based on the distribution
    if len(account_distribution) > 1:
        # Find the account with the most investment
        max_account = max(account_distribution.items(), key=lambda x: x[1])
        percentage = (max_account[1] / total_invested) * 100 if total_invested > 0 else 0
        
        if percentage > 80:
            distribution_insight = f"⚖️ Your portfolio is heavily concentrated in {max_account[0]} ({percentage:.1f}%). " \
                                 f"Consider diversifying across different account types."
        elif percentage > 60:
            distribution_insight = f"📊 Your portfolio has a significant allocation to {max_account[0]} ({percentage:.1f}%). " \
                                 f"This shows clear focus while maintaining some diversification."
        else:
            distribution_insight = f"🔄 Your portfolio has a balanced distribution across different account types, " \
                                 f"with {max_account[0]} representing {percentage:.1f}% of your investments."
        
        insights.append(distribution_insight)
    
    # 4. Future projection insight
    if months_invested > 0 and avg_monthly_earnings > 0:
        years_to_double = math.log(2) / math.log(1 + (avg_monthly_earnings / current_balance))
        years_to_double = years_to_double * (1/12)  # Convert from months to years
        
        future_insight = f"🔮 At your current average monthly return rate, your portfolio could double in approximately " \
                       f"{years_to_double:.1f} years."
        insights.append(future_insight)
    
    # 5. Current month performance (if we have data from previous months)
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Check if we have data for the current month
    current_month_data = df[
        (df['Date'].dt.month == current_month) & 
        (df['Date'].dt.year == current_year)
    ]
    
    if not current_month_data.empty:
        # Find the previous month's last balance
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_year = current_year if current_month > 1 else current_year - 1
        
        previous_month_data = df[
            (df['Date'].dt.month == previous_month) & 
            (df['Date'].dt.year == previous_year)
        ]
        
        if not previous_month_data.empty:
            prev_balance = previous_month_data['Total Balance'].iloc[-1]
            current_balance = current_month_data['Total Balance'].iloc[-1]
            
            month_growth = ((current_balance - prev_balance) / prev_balance) * 100
            month_name = calendar.month_name[current_month]
            
            if month_growth > 5:
                month_insight = f"✨ Outstanding performance in {month_name}! Your portfolio has grown by {month_growth:.1f}% this month."
            elif month_growth > 2:
                month_insight = f"🌟 Strong performance in {month_name}! Your portfolio has grown by {month_growth:.1f}% this month."
            elif month_growth > 0:
                month_insight = f"👍 Positive growth in {month_name}. Your portfolio has increased by {month_growth:.1f}% this month."
            else:
                month_insight = f"📊 Your portfolio has changed by {month_growth:.1f}% in {month_name}."
            
            insights.append(month_insight)
    
    # Join insights and return
    return "\n\n".join(insights)