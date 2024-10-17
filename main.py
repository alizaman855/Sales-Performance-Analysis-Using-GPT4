from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
from utils.data_loading import ingest_data
from utils.prompts import individual_sales_performance_prompt, gpt_data_analysis_assistant,create_team_performance_prompt, create_performance_trends_prompt

# Ingesting Data
data = ingest_data('data/sales_performance_data.csv','csv')


# Initialize FastAPI
app = FastAPI()

# Define the endpoint for individual sales representative performance analysis
@app.get("/api/rep_performance")
def get_rep_performance(rep_id: int):
    try:
        # Filter the data for the representative with the specified ID
        rep_data = data[data['employee_id'] == rep_id]
        if rep_data.empty:
            raise HTTPException(status_code=404, detail="Sales representative not found.")

        # Get the first row (since the filter returns a DataFrame)
        rep_data_row = rep_data.iloc[0]

        # Create the prompt using the specific row's data
        prompt = individual_sales_performance_prompt(rep_data_row)

        # Generate feedback using GPT-4o or any other specified model
        feedback = gpt_data_analysis_assistant(prompt)

        return {"rep_id": rep_id, "feedback": feedback}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
# Endpoint for overall sales team performance summary
@app.get("/api/team_performance")
def get_team_performance():
    try:
        # Create the prompt using the entire team's data
        prompt = create_team_performance_prompt(data)

        # Generate feedback using GPT-4o or any other specified model
        feedback = gpt_data_analysis_assistant(prompt)

        return {"team_performance_summary": feedback}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Endpoint for sales performance trends and forecasting
@app.get("/api/performance_trends")
def get_performance_trends(time_period: str = Query(..., regex="^(monthly|quarterly|yearly)$")):
    try:
        # Validate the time period input and create the prompt
        prompt = create_performance_trends_prompt(data, time_period)

        # Generate feedback using GPT-4o or any other specified model
        feedback = gpt_data_analysis_assistant(prompt)

        return {"time_period": time_period, "performance_trends": feedback}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
