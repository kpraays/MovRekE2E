import pandas as pd
import re

DATA_PATH = "dummy_data_test/ratings.csv"

def determine_format(dt_str):
    try:
        pd.to_datetime(dt_str, format="%Y-%m-%dT%H:%M:%S")
        return "%Y-%m-%dT%H:%M:%S"
    except:
        try:
            pd.to_datetime(dt_str, format="%Y-%m-%dT%H:%M")
            return "%Y-%m-%dT%H:%M"
        except:
            return None

def extract_ratings(data_path):
    # Load data
    df_all = pd.read_csv(data_path, names=['raw'], sep='\t')
    mask = df_all['raw'].str.contains(r"/rate")
    df = df_all[mask]
    print(df.head())

    # Splitting the raw data into separate columns
    df_split = df['raw'].str.split(',', expand=True)
    df_split.columns = ['time', 'userid', 'data']

    # Extract movie name and rating from the data column
    pattern = r'GET /rate/(.*?)=(\d)'
    df_split[['movieid', 'rating']] = df_split['data'].str.extract(pattern)
    df_split.drop(columns=['data'], inplace=True)
    df_split['time'] = df_split['time'].apply(lambda x: pd.to_datetime(x, format=determine_format(x), errors='coerce'))
    df_split.to_csv('cleaned_rating.csv', index=False)

    print(df_split.head())
    return "SUCCESS"

if __name__ == "__main__":
    extract_ratings(DATA_PATH)
