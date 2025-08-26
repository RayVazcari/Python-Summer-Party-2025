# Note: pandas and numpy are already imported as pd and np
# The following tables are loaded as pandas DataFrames with the same names: stories_data
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
# Take a look at the data in the `story_date column`. Correct any data type inconsistencies in that column.

# Load the CSV file into a DataFrame and display it
stories_data = pd.read_csv('./stories_data.csv')
stories_df = stories_data.copy()
print(stories_df)
print("=" * 150)
print()

# We can see that there are a total of 60 rows and all three columns have missing values.
# But first lets change the story_date column to datetime format
stories_df['story_date'] = pd.to_datetime(stories_df['story_date'], format='%Y-%m-%d')
print(stories_df.info())
print("=" * 150)
print()

# Answer to Question 1: The number of missing values on "story_date" column of the data set is:
sd_missing_values = stories_df["story_date"].isnull().sum()
print('The number of missing values on "story_date" column of the data set is:', sd_missing_values)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 2 of 3
# Calculate the 25th, 50th, and 75th percentiles of the number of stories created per user per day.

# Printing the dataframe to see the data
print(stories_df)
print("=" * 150)
print()

# Normalizing and cleaning the data
stories_df['user_id'] = stories_df['user_id'].str.lower()
stories_df['user_id'] = stories_df['user_id'].str.lower().str.strip()
print(stories_df['user_id'].unique())
print("=" * 150)
print()

# Keep rows we can measure on (drop missing user_id or date for this metric)
clean = stories_df.dropna(subset=['user_id', 'story_date']).copy()

# Make sure story_count is numeric (and treat NaN as 0 stories)
clean['story_count'] = pd.to_numeric(clean['story_count'], errors='coerce').fillna(0)
print(clean.info())
print()
print(clean)
print("=" * 150)
print()

# We can start by doing a groupby operation on user_id and story_date to count the number of stories created by each user on each day
stories_per_user_per_day = clean.groupby(['user_id', 'story_date']).agg(total_story_count = ('story_count', 'sum')).reset_index().sort_values(by=['user_id', 'story_date'], ascending=[True, True])
print(stories_per_user_per_day)
print("=" * 150)
print()

# Now we can calculate the 25th, 50th, and 75th percentiles of the number of stories created per user per day
percentiles = stories_per_user_per_day['total_story_count'].quantile([0.25, 0.5, 0.75])
percentiles.index = ['25th', '50th', '75th']
print("\nThe 25th, 50th, and 75th percentiles of the number of stories created per user per day are:")
print(percentiles)
print("=" * 150)
print()

per_user_percentiles = (
    stories_per_user_per_day
    .groupby('user_id')['total_story_count']
    .quantile([0.25, 0.5, 0.75])
    .unstack()              # columns: 0.25, 0.5, 0.75
    .rename(columns={0.25:'p25', 0.5:'p50', 0.75:'p75'})
    .reset_index()
)
print(per_user_percentiles.head())
print("=" * 150)
print()

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 3 of 3

# Display the dataframe to see the data again
print(stories_per_user_per_day)
print("=" * 150)
print()

# Here we need to first group by user_id and total_story_count to find users who have had at least one day where they posted more than 10 stories on that day
users_with_more_than_10_stories = stories_per_user_per_day[stories_per_user_per_day['total_story_count'] > 10]['user_id'].nunique()
print('The number of users who have had at least one day where they posted more than 10 stories on that day is:', users_with_more_than_10_stories)
print()

# Now we can calculate the percentage of users who have had at least one day where they posted more than 10 stories on that day
total_users = stories_per_user_per_day['user_id'].nunique()
percentage = (users_with_more_than_10_stories / total_users) * 100
print(f"\nThe percentage of users who have had at least one day where they posted more than 10 stories on that day is: {percentage:.2f}%")
print("=" * 150)
print()
