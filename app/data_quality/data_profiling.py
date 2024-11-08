import numpy as np
import pandas as pd
import glob
from ydata_profiling import ProfileReport

def load_smaller_data_files(source='../extracted'):
    # get only smaller files
    csv_files = glob.glob(f"{source}/*.csv")
    return csv_files

def load_compressed_data():
# get only smaller files
    directory_with_data = '../extracted'
    csv_files = glob.glob(f"{directory_with_data}/*.tsv")
    return csv_files

def make_reports(csv_files, tab=False, location="profile_reports"):
    # create the report for each csv
    for file in csv_files:
        if tab:
            df1 = pd.read_csv(file, sep='\t')
        else:
            df1 = pd.read_csv(file)
        print(df1.head())
        title = file.split("/")[-1]
        print(title)
        profile = ProfileReport(df1, title=f"Profiling Report: {title}")
        profile.to_file(f"{location}/data-profile-{title}.html")

if __name__ == "__main__":
    # make_reports(load_smaller_data_files())
    make_reports(load_compressed_data(), True)