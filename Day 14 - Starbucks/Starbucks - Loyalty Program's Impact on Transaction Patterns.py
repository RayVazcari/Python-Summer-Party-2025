# Note: pandas and numpy are already imported as pd and np
# The following tables are loaded as pandas DataFrames with the same names: milkshake_ratings
# Please print your final result or dataframe

import pandas as pd
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the datasets and display them
fct_transactions = pd.read_csv('./fct_transactions.csv')
dim_customers = pd.read_csv('./dim_customers.csv')

fct_transactions_df = fct_transactions.copy()
dim_customers_df = dim_customers.copy()

print(fct_transactions_df.info())
print()
print(fct_transactions_df.head())
print()
print(dim_customers_df.info())
print()
print(dim_customers_df.head())
print()
print("=" * 150)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 1 of 3
# For the month of July 2024, how many transactions did loyalty program members and non-members make? Compare the transaction counts between these two groups.

# We are going to start by merging both dataframes into one for further analysis
merged_fct_df =pd.merge(fct_transactions_df, dim_customers_df, how='right', on='customer_id')
print(merged_fct_df.info())
print()
print(merged_fct_df)
print()
print("=" * 150)

# Now that we have merged the dataframes, we can start to look at the transaction patterns of our customers
# First lets transform the 'transaction_date' column to datetime format
merged_fct_df['transaction_date'] = pd.to_datetime(merged_fct_df['transaction_date'], format='%Y-%m-%d', errors='coerce')
print(merged_fct_df.info())
print()
print("=" * 150)

# Now lets filter the dataframe to include transactions for July 2024
jul_fct_df = merged_fct_df[(merged_fct_df['transaction_date'] >= '2024-07-01') & (merged_fct_df['transaction_date'] < '2024-08-01')]
print(jul_fct_df.info())
print()
print(jul_fct_df)
print()
print("=" * 150)

# Now we will count how many transaction did members with and without loyalty membership made in this month
print("Number of transactions made by members with and without loyalty membership:")
print(jul_fct_df['is_loyalty_member'].value_counts())

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 2 of 3
# What is the average transaction value for loyalty program members and non-members during July 2024? Use this to identify which group has a higher average transaction value.

# Since the data is already filtrered for July 2024, we can groupby loyalty membership and calculate the average transaction value
jul_avg_txn_value = jul_fct_df.groupby('is_loyalty_member')['transaction_value'].mean().reset_index(name='average_transaction_value').round(2)
print("Average transaction value for members with and without loyalty membership during July 2024:")
print(jul_avg_txn_value)
print()
print("=" * 150)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 3 of 3
# Determine the percentage difference in average transaction value between loyalty program members and non-members for July 2024.

# We can directly calculate the percentage difference in average transaction value between members and non-members by subtracting the average transaction value of non-members from the average transaction value of members and 
percentage_diff = (jul_avg_txn_value[jul_avg_txn_value['is_loyalty_member'] == True]['average_transaction_value'].values[0] - jul_avg_txn_value[jul_avg_txn_value['is_loyalty_member'] == False]['average_transaction_value'].values[0]) / jul_avg_txn_value[jul_avg_txn_value['is_loyalty_member'] == False]['average_transaction_value'].values[0] * 100
print("Percentage difference in average transaction value between members and non-members during July 2024:")
print(percentage_diff.round(2), "%")