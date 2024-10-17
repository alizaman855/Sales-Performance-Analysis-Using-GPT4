# 📊 Sales Performance Analysis API
This project provides a FastAPI-based service to analyze sales performance for individual representatives and overall team performance. The service includes several endpoints for generating feedback, sales trends, and forecasting, powered by OpenAI's language models.
# 📑 Table of Contents
- [Project Overview](https://github.com/alizaman855/Sales-Performance-Analysis-Using-GPT4/tree/main?tab=readme-ov-file#-project-overview)
- [Features](https://github.com/alizaman855/Sales-Performance-Analysis-Using-GPT4/tree/main?tab=readme-ov-file#-key-features)
- [Technologies Used](https://github.com/alizaman855/Sales-Performance-Analysis-Using-GPT4/tree/main?tab=readme-ov-file#%EF%B8%8F-technologies-used)
- [Setup Instructions](https://github.com/alizaman855/Sales-Performance-Analysis-Using-GPT4/tree/main?tab=readme-ov-file#%EF%B8%8F-setup-instructions)
- [Running the Application](https://github.com/alizaman855/Sales-Performance-Analysis-Using-GPT4/tree/main?tab=readme-ov-file#-running-the-application)
- [API Endpoints](https://github.com/alizaman855/Sales-Performance-Analysis-Using-GPT4/tree/main?tab=readme-ov-file#-api-endpoints)
- [Docker Deployment](https://github.com/alizaman855/Sales-Performance-Analysis-Using-GPT4/tree/main?tab=readme-ov-file#-docker-deployment-1)



# 📖 Project Overview

This project is designed to ingest sales data, perform analysis, and return detailed performance feedback for sales representatives and teams. It leverages OpenAI's GPT models to generate insights based on various sales metrics, and it is deployed using FastAPI.
# ✨ Key Features:
- 📊 Individual sales performance analysis for representatives.
- 👥 Team performance summary.
- 📈 Sales trends analysis and future forecasting

# 🛠️ Technologies Used
- 🚀 FastAPI: For building the API endpoints.
- 🤖 OpenAI GPT Models: Used for generating sales performance insights and forecasting.
- 🐳 Docker: For containerizing the application.
- 🐼 Pandas: For handling sales data ingestion and analysis.
- 🔐 dotenv: For managing environment variables securely.
# ⚙️ Setup Instructions
## 📋 Prerequisites
Ensure you have the following installed:

- 🐍 Python 3.11+
- 🐳 Docker (for containerization)
- 🔑 OpenAI API Key (you will need to set this up)

# Steps



1. 📥 Clone this repository:
```bash
git clone https://github.com/alizaman855/Sales-Performance-Analysis-Using-GPT4
cd sales-performance-analysis
```
2. 📦 Install the required Python packages:
```bash
pip install -r requirements.txt
```
3. 🗂️ Create a .env file in the root directory and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```
4. 🗄️ **Ingest sales data** into the application by placing your sales data in the data/ folder:

- Data format should be in CSV or JSON.
- Ensure the required sales metrics are present (e.g., employee_id, lead_taken, tours_booked, etc.).

# 🚀 Running the Application
## 💻 Locally
You can run the FastAPI server locally using the following command:

```bash
uvicorn main:app --reload
```
This will start the FastAPI server on http://localhost:8000.

## 🐳 Docker Deployment
1. Build the Docker image:
```bash
docker build -t fastapi-sales-app .
```
2. Run the Docker container:
```bash
docker run -d -p 8000:8000 --env-file .env fastapi-sales-app
```
The application will be available at http://localhost:8000.

# 📡 API Endpoints
## 🔍 Individual Sales Representative Performance Analysis

- Endpoint: /api/rep_performance
- URL: http://localhost:8000/api/rep_performance?rep_id=<id>
- Method: GET
- Parameters: rep_id (the unique identifier for the sales representative)
- Function: Returns detailed performance analysis and feedback for the specified sales representative.
**Use Case**

## 📊 Overall Sales Team Performance Summary

- Endpoint: /api/team_performance
- URL: http://localhost:8000/api/team_performance
- Method: GET
- Function: Provides a summary of the sales team's overall performance.
## 📅 Sales Performance Trends and Forecasting

- Endpoint: /api/performance_trends
- URL: http://localhost:8000/api/performance_trends?time_period=<time_period>
- Method: GET
- Parameters: time_period (e.g., monthly, quarterly)
- Function: Analyzes sales data over the specified time period to identify trends and forecast future performance.


# 🐳 Docker Deployment
To deploy the FastAPI application using Docker, follow these steps:

1. Build the Docker image:
```bash
docker build -t fastapi-sales-app .
```
2. Run the Docker container:
```bash
docker run -d -p 8000:8000 --env-file .env fastapi-sales-app
```
This will run the application in a Docker container, making it available at http://localhost:8000.