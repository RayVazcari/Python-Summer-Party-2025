# Note: pandas and numpy are already imported as pd and np
# The following tables are loaded as pandas DataFrames with the same names: milkshake_ratings
# Please print your final result or dataframe

import pandas as pd
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

fct_trips = pd.read_csv('./fct_trips.csv')
fct_trips_df = fct_trips.copy()

print(fct_trips.info())
print()
print(fct_trips_df)
print()
print("=" * 150)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 1 of 3
# What is the average driver earnings per completed UberPool ride with more than two riders between July 1st and September 30th, 2024? This analysis will help isolate trips that meet specific rider thresholds to understand their impact on driver earnings.

# Fortunately it does not seem like we have any missing values in the dataset
# However we will begin by analyzing numerical and non numerical columns
# We will first however transform the date columns to datetime
fct_trips_df['trip_date'] = pd.to_datetime(fct_trips_df['trip_date'], format='%Y-%m-%d', errors='coerce')
print(fct_trips_df.info())
print()
print(fct_trips_df.head())
print()
print("=" * 150)

# Making a list of all categorical variables ()'object' or 'category')
cat_cols = fct_trips_df.select_dtypes(include=['object', 'category']).columns

# Iterate through each categorical column and print the count of unique categorical levels, followed by a separator line.
for column in cat_cols:
    print(fct_trips_df[column].value_counts())
    print("-" * 50)
print()
print("=" * 150)

# Making a list of all numerical variables ('int64', 'float64', 'complex')
num_cols = fct_trips_df.select_dtypes(include=['int64', 'float64', 'complex']).columns

# Iterate through each numerical column and print summary statistics, followed by a separator line.
for column in num_cols:
    print(fct_trips_df[column].describe())
    print("-" * 50)
print()
print("=" * 150)

# Checking missing values across each column
missing_values = fct_trips_df.isnull().sum()
print('The number of missing values on each column of the data set is:');
print(missing_values)
print()

# Check for complete duplicate records
duplicate_records = fct_trips_df.duplicated().sum()
print('The number of duplicate values on the data set is:', duplicate_records)
print()
print("=" * 150)

# Now we should begin by grouping rides dBetween July 1st 2024 and September 30 2024
julsept_fct_trips_df = fct_trips_df[(fct_trips_df['trip_date'] >= '2024-07-01') & (fct_trips_df['trip_date'] <= '2024-09-30')]
print(julsept_fct_trips_df.head())
print()
print(julsept_fct_trips_df.info())
print()
print("=" * 150)

# Now we group by ride_type (UberPool), rider_count(>2)
grouped_sep_jul_df =  julsept_fct_trips_df.query("(ride_type == 'UberPool') & (rider_count > 2)")
print(grouped_sep_jul_df)
print()
print("=" * 150)

# Now we calculate the average total_earnings
average_earnings_sep_jul = grouped_sep_jul_df['total_earnings'].mean()

# Answer to Question 1
print("\nThe average total earnings for UberPool rides with more than 2 riders between July 1st 2024 and September 30 2024 is:", average_earnings_sep_jul)
print()
print("=" * 150)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 2 of 3
# For completed UberPool rides between July 1st and September 30th, 2024, derive a new column calculating earnings per mile (total_earnings divided by total_distance) and then compute the average earnings per mile for rides with more than two riders. This calculation will reveal efficiency metrics for driver compensation.

# Display data again
print(julsept_fct_trips_df.head())
print()
print(julsept_fct_trips_df.info())
print()
print("=" * 150)

# Copy the dataframe to avoid overwriting
q2_julsept_fct_df = julsept_fct_trips_df.copy()

# Calculate earnings per mile
q2_julsept_fct_df['earnings_per_mile'] = q2_julsept_fct_df['total_earnings'] / q2_julsept_fct_df['total_distance']
print(q2_julsept_fct_df.head())
print()
print(q2_julsept_fct_df.info())
print()
print("=" * 150)

# Now we group by ride_type (UberPool), rider_count(>2)
q2_grouped_sep_jul_df =  q2_julsept_fct_df.query("(ride_type == 'UberPool') & (rider_count > 2)")
print(q2_grouped_sep_jul_df)
print()
print("=" * 150)

# Now we calculate the average total_earnings
q2_avg_earn_per_mile_sep_jul = q2_grouped_sep_jul_df['earnings_per_mile'].mean().round(2)

# Answer to Question 2
print("\nThe average total earnings for UberPool rides with more than 2 riders between July 1st 2024 and September 30 2024 is: $", q2_avg_earn_per_mile_sep_jul, "per mile")
print()
print("=" * 150)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 3 of 3
# Identify the combination of rider count and total distance that results in the highest average driver earnings per UberPool ride between July 1st and September 30th, 2024. This analysis directly recommends optimal trip combination strategies to maximize driver earnings.

# Copy the dataframe to avoid overwriting
q3_julsept_fct_df = q2_julsept_fct_df.copy()
print(q3_julsept_fct_df)
print()
print("=" * 150)

# Now we group by ride_type (UberPool), but not by rider_count
q3_grouped_sep_jul_df =  q3_julsept_fct_df.query("(ride_type == 'UberPool')")
print(q3_grouped_sep_jul_df)
print()
print("=" * 150)

# Now I need to narrow down the combinations on that data frame
# I will do that by first creating an index 
q3_rdrcount_earnings_df = (q3_grouped_sep_jul_df.groupby(['rider_count', 'total_distance']).agg(average_driver_earnings = ('total_earnings', 'mean'))).sort_values('average_driver_earnings', ascending=False).reset_index()
print("Table of combination of rider cound and total distance that results in the highest average driver earnings per UberPool ride between July 1st and September 30th, 2024");
print(q3_rdrcount_earnings_df)
print()
print("=" * 150)

# Now that this is sorted, we need to call out the highest average driver earnings per UberPool ride between July 1st and September 30th, 2024
# Answer to Question 3
print("The combination of rider count and total distance that results in the highest average driver earnings per UberPool ride between July 1st and September 30th, 2024 is:")
print(q3_rdrcount_earnings_df.nlargest(1, 'average_driver_earnings'))
print()
print("=" * 150)