# Note: pandas and numpy are already imported as pd and np
# The following tables are loaded as pandas DataFrames with the same names: fct_transactions, dim_risk_flags
# Please print your final result or dataframe

import pandas as pd
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the CSV file into a DataFrame and display it
customer_returns = pd.read_csv('./customer_returns.csv')
customer_returns_df = customer_returns.copy()
print(customer_returns_df)
print()
print(customer_returns_df.info())

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 1 of 2
# Identify and list all unique customer IDs who have made returns between July 1st 2024 and June 30th 2025. This will help us understand the base set of customers involved in returns during the specified period.

# We first need to convert the 'return_date' column to datetime format
customer_returns_df['order_date'] = pd.to_datetime(customer_returns_df['order_date'], format='%Y-%m-%d', errors='coerce')
print("'order_date' after converting to datetime format:")
print(customer_returns_df.head())
print()
print(customer_returns_df.info())
print()
print("=" * 150)

# Now we filter for transaction between July 1, 2024 and June 30, 2025.
jul_jun_ustomer_returns_df = customer_returns_df[(customer_returns_df['order_date'] >= '2024-07-01') & (customer_returns_df['order_date'] <= '2025-06-30')]
print(jul_jun_ustomer_returns_df)
print(jul_jun_ustomer_returns_df.info())
print()
print("=" * 150)

# Now we group by all transaction where the return flag is True
grouped_customer_returns_df = jul_jun_ustomer_returns_df[jul_jun_ustomer_returns_df['return_flag'] == True]
print(grouped_customer_returns_df)
print()
print(grouped_customer_returns_df.info())
print("\nThe unique customer_ids who have made returns between July 1st 2024 and June 30th 2025 is:");
print(grouped_customer_returns_df['customer_id'].unique())
print()
print("=" * 150)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 2 of 2
# Convert the 'order_date' column to a datetime format and create a MultiIndex with 'customer_id' and 'order_date'. Then, calculate the total number of returns per customer for each month. This will provide insights into monthly return patterns for each customer.

# Since we already converted the 'order_date' column to datetime format, we can now create a MultiIndex with 'customer_id' and 'order_date'.
customer_returns_df = customer_returns_df.set_index(['customer_id', 'order_date']).sort_index()
print(customer_returns_df)
print()
print("=" * 150)

# Now we group by monthly totals 
# Now we group by monthly totals 
montly_returns = (customer_returns_df.groupby(['customer_id', pd.Grouper(level='order_date', freq='ME')]).agg(total_returns=('return_flag', 'sum')))
print("The total number of returns per customer for each month is:");
print(montly_returns)