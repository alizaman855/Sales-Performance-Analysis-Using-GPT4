import pandas as pd
import json

def ingest_data(file_path, file_type='csv'):
    """
    Ingests sales data from a file and returns a Pandas DataFrame.
    
    Parameters:
    file_path (str): Path to the sales data file.
    file_type (str): The type of the file ('csv' or 'json').
    
    Returns:
    pd.DataFrame: A Pandas DataFrame containing the sales data.
    """
    if file_type == 'csv':
        try:
            # Ingest CSV file
            data = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")
        
    elif file_type == 'json':
        try:
            # Ingest JSON file
            with open(file_path, 'r') as file:
                json_data = json.load(file)
            data = pd.json_normalize(json_data)
        except Exception as e:
            raise ValueError(f"Error reading JSON file: {str(e)}")
        
    else:
        raise ValueError("Unsupported file type. Use 'csv' or 'json'.")
    
    return data


# Function to return a DataFrame with a specific representative's data
def get_sales_data_by_rep_id(df, rep_id):
    """
    Filters the sales data by the provided representative ID.
    
    Parameters:
    df (pd.DataFrame): The sales data DataFrame.
    rep_id (int): The representative ID to filter.
    
    Returns:
    pd.DataFrame: A DataFrame containing only the data for the given rep_id.
    """
    rep_data = df[df['employee_id'] == rep_id]
    if rep_data.empty:
        return f"No data found for rep_id: {rep_id}"
    return rep_data