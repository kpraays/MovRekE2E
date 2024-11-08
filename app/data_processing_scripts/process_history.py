import pandas as pd
import re
from dateutil import parser

DATA_PATH = "dummy_data_test/history1.csv"

def extract_history(DATA_PATH):
    # Load data
    df_all = pd.read_csv(DATA_PATH, names=['raw'], sep='\t')
    print(df_all.head())

    mask = df_all['raw'].str.contains(r"/data/m")
    df = df_all[mask]
    print(df.head())

    # Split the data
    df_split = df['raw'].str.split(',', expand=True)
    print(df_split.head())
    df_split.columns = ['time', 'userid', 'data']

    # Extract movie name and minute from the data column
    pattern = r'GET /data/m/(.*?)/(\d+)\.mpg'
    df_split[['movieid', 'minute']] = df_split['data'].str.extract(pattern)
    df_split.drop(columns=['data', 'time'], inplace=True)
    df_split = df_split.iloc[::-1]
    df_split.drop_duplicates(subset=['userid', 'movieid'], inplace=True)

    # Write to CSV
    df_split.to_csv('cleaned_history.csv', index=False)

    print(df_split.head())
    return "SUCCESS"

# if __name__ == "__main__":
#     extract_history(DATA_PATH)