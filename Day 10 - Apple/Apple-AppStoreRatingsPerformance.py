# Note: pandas and numpy are already imported as pd and np
# The following tables are loaded as pandas DataFrames with the same names: app_ratings
# Please print your final result or dataframe

import pandas as pd
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 1 of 3 
# There are some data inconsistencies in the 'rating' column, specifically: leading or trailing white space, decimals represented by commas instead of decimal points (eg. 4,2 instead of 4.2), and non-numeric values. Clean up these data issues and convert the column to a numeric data type.

# Load the CSV file into a DataFrame and display it
app_ratings = pd.read_csv('./app_ratings.csv')
app_ratings_df = app_ratings.copy()
print(app_ratings_df)
print()
print(app_ratings_df.info())
print()
print("=" * 150)

# Lets first find out these inconsistencies by checking the unique values in the user_id column
print(app_ratings_df['rating'].unique())
print()
print("=" * 150)

# Yeah, we can confirm there are leading and trailing spaces, missing values, the datatype is object instead of numeric, and there are some invalid entries like 'five' and 'not available'.
# Lets start cleaning the data by removing leading and trailing spaces, converting to numeric and handling missing and invalid values.
# While we are at it we can also convert the review_date to datetime format

# Normalizing and cleaning rating column
app_ratings_df['rating'] = app_ratings_df['rating'].str.lower()
app_ratings_df['rating'] = app_ratings_df['rating'].str.lower().str.strip()
print("'rating' with leading and trailing spaces removed and converted to lowercase:")
print(app_ratings_df['rating'].unique())
print()
print("=" * 150)

# We got rid of the leading and trailing spaces. Now lets convert to numeric, and transform the commas to dots
app_ratings_df['rating'] = app_ratings_df['rating'].str.replace(',', '.')
print("'rating' with commas replaced by dots:")
print(app_ratings_df['rating'].unique())
print()
print("=" * 150)

# Converting rating to numeric, setting errors to NaN we will not be filling them with 0 because it is possible that some apps have not been rated yet
app_ratings_df['rating'] = pd.to_numeric(app_ratings_df['rating'], errors='coerce')
print(app_ratings_df.info())
print("'rating' after converting to numeric and setting errors to NaN:")
print(app_ratings_df['rating'].unique())
print()
print("=" * 150)

# Converting review_date to datetime format
app_ratings_df['review_date'] = pd.to_datetime(app_ratings_df['review_date'], format='%Y-%m-%d', errors='coerce')
print("'review_date' after converting to datetime format:")
print(app_ratings_df.info())
print()
print()
print("=" * 150)

# Cleaned dataframe
cleaned_app_ratings_df = app_ratings_df.copy()
print("Answer 1: Cleaned dataframe with normalized 'rating' column and 'review_date' in datetime format:")
print(cleaned_app_ratings_df)
print()
print(cleaned_app_ratings_df.info())
print()
print("=" * 150)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 2 of 3 
# Using the cleaned dataset, display the first and last five entries to get an overview of the app ratings across different categories.

# This can easily be achieved by using .head and .tail 
print("Showing first 5 entries:")
print(cleaned_app_ratings_df.head(5))
print()
print("Showing last 5 entries:")
print(cleaned_app_ratings_df.tail(5))
print()
print("=" * 150)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 3 of 3
# Calculate the basic summary statistics (mean, median, standard deviation) of app ratings for each category to identify variations and performance patterns.

# For this first we need to group the data by category and then calculate the statistics for each category

# Group the data by category and calculate the mean rating for each category
grouped_app_ratings_df = cleaned_app_ratings_df.groupby('category')['rating'].describe(include="all")
print("Descriptive statistics:")
print(grouped_app_ratings_df)
