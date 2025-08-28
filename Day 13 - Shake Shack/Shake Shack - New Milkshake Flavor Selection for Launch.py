# Note: pandas and numpy are already imported as pd and np
# The following tables are loaded as pandas DataFrames with the same names: milkshake_ratings
# Please print your final result or dataframe

import pandas as pd
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the CSV file into a DataFrame
milkshake_ratings = pd.read_csv('./milkshake_ratings.csv')
milkshake_ratings_df = milkshake_ratings.copy()
print(milkshake_ratings_df)
print()
print(milkshake_ratings_df.info())

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 1 of 3
# There was an error in our data collection process, and we unknowingly introduced duplciate rows into our data. Remove any duplicate entries in the customer ratings data to ensure the accuracy of the analysis.

# We can quickly do this by using .duplicated().sum()
duplicate_records = milkshake_ratings_df.duplicated().sum()
print('The number of duplicate values on the data set is:', duplicate_records)
print()

# Identify all duplicate rows, including the first occurrence
all_duplicate_rows = milkshake_ratings_df[milkshake_ratings_df.duplicated(keep=False)]
print('All duplicate rows in the data set are:') ; 
print(all_duplicate_rows)
print()

# Now that we have identified the duplicate rows, we can drop them
clean_milkshake_ratings_df = milkshake_ratings_df.drop_duplicates()
print(clean_milkshake_ratings_df.info())
print()
print("=" * 100)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 2 of 3
# CFor each milkshake flavor, calculate the average customer rating and append this as a new column to the milkshake_ratings DataFrame. Don't forget to clean the DataFrame first by dropping duplicate values.

# Before we work on this question we need to address the null values, we will be dropping them so they dont affect our analysis
clean_milkshake_ratings_df = clean_milkshake_ratings_df.dropna()
print(clean_milkshake_ratings_df.info())
print()
print("=" * 100)

# Now tat the null values are removed, we can work on this question
# We need to group the data by flavor and get the average rating for each flavor
flavor_ratings = clean_milkshake_ratings_df.groupby('flavor').agg({'rating': 'mean'}).round(2).rename(columns={'rating': 'avg_rating'})
print(flavor_ratings)
print()
print("=" * 100)

# Now we just need to append this data to the milkshake_ratings data set
append_milkshake_ratings_df = pd.merge(clean_milkshake_ratings_df, flavor_ratings, how='right', on='flavor').sort_values('customer_id').reset_index(drop=True)
print(append_milkshake_ratings_df.info())
print("\nAnswer 2: Cleaned dataframe with new 'avg_rating' column:")
print(append_milkshake_ratings_df)
print()
print("=" * 100)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 3 of 3
# For each row in the dataset, calculate the difference between that customer's rating and the average rating for the flavor. Don't forget to clean the DataFrame first by dropping duplicate values.

# Calculating and creating a new column with the difference between the rating and the average rating
append_milkshake_ratings_df['difference'] = append_milkshake_ratings_df['rating'] - append_milkshake_ratings_df['avg_rating']
print(append_milkshake_ratings_df)
print()
print("=" * 150)