import pandas as pd

# Read the CSV file into a DataFrame
df1 = pd.read_csv('../data/movie_cleaned_1.csv')
df2 = pd.read_csv('../data/movie_cleaned_2.csv')

df = pd.concat([df1, df2])
print(df.head())
df.columns = ['userid', 'movieid', 'minute']
# Remove rows with duplicate entries in all columns
df = df.drop_duplicates(subset=["movieid"])

# Save the updated DataFrame to a new CSV file
df.to_csv('final_cleaned_movie_list.csv', index=False)
