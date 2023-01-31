import pandas as pd

def process_csv(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    # Store the first column as a list of integers
    first_column = df.iloc[:, 0].values.tolist()
    return first_column
