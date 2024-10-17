from typing import List
from utils.data_loading import ingest_data
import dotenv
import openai
import os
import pandas as pd
from openai import OpenAI


# Load environment variables from a .env file
dotenv.load_dotenv()

# Access the OpenAI API key from the .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

# Make sure the key is loaded before proceeding
if not openai_api_key:
    raise ValueError("OpenAI API Key not found. Please set it in the .env file.")

# Set the API key for OpenAI
openai.api_key = openai_api_key

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai_api_key,
)

# Function to call OpenAI's gpt-4o or similar chat-based models
def gpt_data_analysis_assistant(prompt, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    # Return the generated response
    return response.choices[0].message.content.strip()

def individual_sales_performance_prompt(sales_data_row):
    # Comprehensive and detailed prompt
    prompt = f"""
    I am providing you with the performance metrics for a sales representative. Please analyze their sales performance, identify strengths, weaknesses, and suggest actionable strategies for improvement. Also, compare their performance against the average team performance in relevant metrics, and provide a detailed breakdown.

    ### Sales Representative Information:
    - **Employee Name**: {sales_data_row['employee_name']}
    - **Employee ID**: {sales_data_row['employee_id']}
    - **Lead Taken**: {sales_data_row['lead_taken']}
    - **Tours Booked**: {sales_data_row['tours_booked']}
    - **Applications Submitted**: {sales_data_row['applications']}
    - **Tours per Lead**: {sales_data_row['tours_per_lead']}
    - **Applications per Tour**: {sales_data_row['apps_per_tour']}
    - **Applications per Lead**: {sales_data_row['apps_per_lead']}
    - **Confirmed Revenue**: ${sales_data_row['revenue_confirmed']}
    - **Pending Revenue**: ${sales_data_row['revenue_pending']}
    - **Revenue Runrate**: ${sales_data_row['revenue_runrate']}
    - **Estimated Revenue**: ${sales_data_row['estimated_revenue']}
    - **Average Deal Value (Last 30 Days)**: ${sales_data_row['avg_deal_value_30_days']}
    - **Average Close Rate (Last 30 Days)**: {sales_data_row['avg_close_rate_30_days']}%

    ### Expected Analysis:
    1. **Overall Sales Performance**: Analyze how the sales representative performed in terms of revenue generation, deal closures, and applications submitted. Focus on the efficiency in terms of tours per lead, applications per tour, and applications per lead. 

    2. **Strengths**: Highlight areas where the representative excels. For example, strong revenue generation, high conversion rates, or excellent deal value. Compare these strengths to the team's average performance where applicable.

    3. **Weaknesses and Areas for Improvement**: Identify any areas where the representative could improve. This could include things like lead generation, applications, or tours. Provide suggestions on how to improve performance in these areas, such as strategies for better lead nurturing or conversion techniques.

    4. **Comparison to Team Performance**: Compare the representative’s key metrics (leads, applications, revenue) with the average team performance. Explain whether the representative is outperforming or underperforming compared to their peers.

    5. **Suggested Actions**:
        - **Lead Generation Strategies**: If the representative is behind in lead generation, recommend strategies for improving lead acquisition. This may include specific outreach techniques, networking strategies, or the use of lead generation tools.
        - **Sales Funnel Optimization**: Suggest ways the representative could improve the conversion of leads to applications or booked tours. For example, focusing on follow-ups, better qualification of leads, or improving tour presentations.
        - **Revenue Enhancement**: If applicable, suggest how the representative can improve their revenue generation, including upselling strategies or increasing the average deal value.

    6. **General Sales Strategy**: Provide high-level suggestions that the sales representative can incorporate into their day-to-day work to improve overall performance. This could include time management techniques, pipeline management, or team collaboration.

    Based on this data, please give a thorough analysis of the representative's performance, comparing it with team averages, and provide actionable insights for improving future performance.
    """
    return prompt

# Function to create a team performance summary prompt without industry benchmarks
def create_team_performance_prompt(team_data):
    # Calculate aggregate metrics
    total_leads = team_data['lead_taken'].sum()
    total_tours = team_data['tours_booked'].sum()
    total_applications = team_data['applications'].sum()
    total_revenue_confirmed = team_data['revenue_confirmed'].sum()
    total_pending_revenue = team_data['revenue_pending'].sum()
    total_estimated_revenue = team_data['estimated_revenue'].sum()
    avg_deal_value = team_data['avg_deal_value_30_days'].mean()
    avg_close_rate = team_data['avg_close_rate_30_days'].mean()

    # Structure the prompt without external comparison
    prompt = f"""
    Please analyze the performance of the entire sales team based on the following aggregated metrics:

    ### Team Sales Data:
    - **Total Leads Taken**: {total_leads}
    - **Total Tours Booked**: {total_tours}
    - **Total Applications Submitted**: {total_applications}
    - **Total Confirmed Revenue**: ${total_revenue_confirmed}
    - **Total Pending Revenue**: ${total_pending_revenue}
    - **Total Estimated Revenue**: ${total_estimated_revenue}
    - **Average Deal Value (Last 30 Days)**: ${avg_deal_value}
    - **Average Close Rate (Last 30 Days)**: {avg_close_rate}%

    ### Analysis Required:
    1. **Overall Team Performance**: Please analyze the overall team performance, including key performance indicators like leads, tours, applications, and revenue generation. Highlight any notable trends within the team.

    2. **Team Strengths**: Identify key strengths of the team. For example, strong revenue generation, efficient conversion rates, or excellent deal value.

    3. **Areas for Improvement**: Identify areas where the team may need improvement, such as lead generation, applications per tour, or pending revenue conversion.

    4. **Detailed Breakdown by Metric**:
        - **Lead Generation**: Assess whether the team is generating enough leads and suggest strategies to improve lead generation if necessary.
        - **Tours and Applications**: Examine the efficiency of the sales pipeline from tours to applications. If there are gaps, suggest ways to optimize the funnel and increase conversion rates.
        - **Revenue Performance**: Analyze the overall revenue generation, including confirmed and pending revenue. Are there delays in closing deals, and what steps can be taken to accelerate revenue realization?
    
    5. **Suggested Team Strategies**:
        - **Boost Lead Generation**: Recommend strategies to increase lead generation, such as new outreach methods, enhanced marketing efforts, or the use of lead generation tools.
        - **Sales Funnel Optimization**: Provide actionable suggestions on how the team can optimize the sales funnel, reduce drop-offs, and convert more leads into successful applications and tours.
        - **Revenue Enhancement**: Suggest strategies to improve revenue generation, including upselling, cross-selling, and increasing the average deal value.
    
    6. **Team Collaboration and Development**: Suggest ways the team can collaborate more effectively, including sharing successful strategies among team members, improving communication, and developing cross-functional training programs.
    
    7. **Future Outlook and Forecasting**: Based on the current data, provide insights into future performance. Highlight key trends and provide recommendations for maintaining or improving the team's performance in the next quarter.
    """
    return prompt

# Function to create performance trends and forecasting prompt
# Function to ensure monthly breakdown and create performance trends and forecasting prompt
def create_performance_trends_prompt(team_data, time_period):
    # Ensure that the 'dated' column is in proper datetime format
    team_data['dated'] = pd.to_datetime(team_data['dated'], errors='coerce')

    # Select only numeric columns for aggregation, excluding 'dated' and other non-numeric columns
    numeric_columns = team_data.select_dtypes(include=['number']).columns

    if time_period == 'monthly':
        team_data['month'] = team_data['dated'].dt.to_period('M')
        grouped_data = team_data.groupby('month')[numeric_columns].sum()
    elif time_period == 'quarterly':
        team_data['quarter'] = team_data['dated'].dt.to_period('Q')
        grouped_data = team_data.groupby('quarter')[numeric_columns].sum()
    elif time_period == 'yearly':
        team_data['year'] = team_data['dated'].dt.to_period('Y')
        grouped_data = team_data.groupby('year')[numeric_columns].sum()
    else:
        raise ValueError("Invalid time period. Please choose 'monthly', 'quarterly', or 'yearly'.")

    if grouped_data.empty:
        raise ValueError(f"No {time_period} data available for analysis.")

    # Extract key metrics over the selected time period
    total_leads = grouped_data['lead_taken'].sum()
    total_tours = grouped_data['tours_booked'].sum()
    total_applications = grouped_data['applications'].sum()
    total_revenue_confirmed = grouped_data['revenue_confirmed'].sum()
    total_pending_revenue = grouped_data['revenue_pending'].sum()
    total_estimated_revenue = grouped_data['estimated_revenue'].sum()

    # Explicitly mention the time period in the prompt
    prompt = f"""
    You are provided with sales data broken down by {time_period}. Analyze the sales trends and forecast future performance based on the historical data.

    ### {time_period.capitalize()} Aggregated Sales Data:
    - **Total Leads Taken**: {total_leads}
    - **Total Tours Booked**: {total_tours}
    - **Total Applications Submitted**: {total_applications}
    - **Total Confirmed Revenue**: ${total_revenue_confirmed}
    - **Total Pending Revenue**: ${total_pending_revenue}
    - **Total Estimated Revenue**: ${total_estimated_revenue}

    ### Analysis Required:
    1. **Sales Trends**: Identify key trends in lead generation, tours booked, applications, and revenue generation over the selected {time_period}.
    
    2. **Performance Forecasting**: Based on these trends, provide a detailed forecast of future performance for the next {time_period}. Focus on leads, tours, applications, and revenue.
    
    3. **Key Insights**: Provide insights into significant patterns in the data (e.g., seasonal changes, consistent growth/decline) and the reasons behind these trends.
    
    4. **Suggested Strategies**: Suggest actionable strategies that the sales team can implement to optimize performance based on the identified trends and forecast.
    """
    
    return prompt
