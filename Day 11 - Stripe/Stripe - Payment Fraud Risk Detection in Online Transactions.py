# Note: pandas and numpy are already imported as pd and np
# The following tables are loaded as pandas DataFrames with the same names: fct_transactions, dim_risk_flags
# Please print your final result or dataframe

import pandas as pd
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the CSV file into a DataFrame and display it
fct_transactions = pd.read_csv('./fct_transactions.csv')
dim_risk_flags = pd.read_csv('./dim_risk_flags.csv')

fct_transactions_df = fct_transactions.copy()
dim_risk_flags_df = dim_risk_flags.copy()

print(fct_transactions_df.info())
print()
print(fct_transactions_df.head())
print()
print(dim_risk_flags_df.info())
print()
print(dim_risk_flags_df.head())
print()

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 1 of 3
# How many transactions in October 2024 have a customer email ending with a domain other than 'gmail.com', 'yahoo.com', or 'hotmail.com'? This metric will help us identify transactions associated with less common email providers that may indicate emerging risk patterns.

# First we need to normalize and transform the 'transaction_date' column to datetime format
fct_transactions_df['transaction_date'] = pd.to_datetime(fct_transactions_df['transaction_date'], format='%Y-%m-%d', errors='coerce')
print("'transaction_date' after converting to datetime format:")
print(fct_transactions_df.info())
print()

# Lets find inconsistencies in 'customer_email'
print(fct_transactions_df['customer_email'].unique())
print()
print("=" * 150)

# 'customer_email' is clean, no inconsistencies
# Now we will have to group the data by transaction_date
fct_oct_transactions_df = fct_transactions_df[(fct_transactions_df['transaction_date'] >= '2024-10-01') & (fct_transactions_df['transaction_date'] < '2024-11-01')]
print(fct_oct_transactions_df.info()) 
print(fct_oct_transactions_df.head())
print()
print("=" * 150)

# We will now find transactions with a domain other than 'gmail.com', 'yahoo.com', or 'hotmail.com'
# To do that we need to define a tuple of valid domains
valid_domains = ('@gmail.com', '@yahoo.com', '@hotmail.com')

# Then we will find the transactions using '~' as negation and the 'str.endswith' method
fct_oct_trans_val_email_df = fct_oct_transactions_df[~fct_oct_transactions_df['customer_email'].str.endswith(valid_domains, na=False)]
print(fct_oct_trans_val_email_df)
print()
print("=" * 150)

# Now we display the count of transactions by customer_email
print("There are only", fct_oct_trans_val_email_df.shape[0], "transactions with with a domain other than 'gmail.com', 'yahoo.com', or 'hotmail.com'")
print()
print("=" * 150)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 2 of 3
# For transactions occurring in November 2024, what is the average transaction amount, using 0 as a default for any missing values? This calculation will help us detect abnormal transaction amounts that could be related to fraudulent activity.

# We will need to re-filter the date to include november 2024
fct_nov_transactions_df = fct_transactions_df[(fct_transactions_df['transaction_date'] >= '2024-11-01') & (fct_transactions_df['transaction_date'] < '2024-12-01')]
print(fct_nov_transactions_df.info()) 
print()
print(fct_nov_transactions_df.head())
print()
print("=" * 150)

# We can see that there is one null value for transaction_ammount so we will be replacinging it with 0
fct_nov_transactions_df = fct_nov_transactions_df.copy()
fct_nov_transactions_df['transaction_amount'] = pd.to_numeric(fct_nov_transactions_df['transaction_amount'], errors='coerce').fillna(0)
print(fct_nov_transactions_df.info())
print()
print("=" * 150)

# Now that we got rid of the null values we can proceed and calculate the average transaction amount for the whole month
fct_nov_avg_transaction_df = fct_nov_transactions_df['transaction_amount'].mean()
print("The average transaction amount for the whole month of November 2024 is:", fct_nov_avg_transaction_df)
print()
print("=" * 150)

################################################################################
print()
print("=" * 150)
print("=" * 150)
print()
################################################################################
# Question 3 of 3
# Among transactions flagged as 'High' risk in December 2024, which day of the week recorded the highest number of such transactions? This analysis is intended to pinpoint specific days with concentrated high-risk activity and support the development of our preliminary fraud detection score.

# We start again by filtering for transactions in December 2024
fct_dec_transactions_df = fct_transactions_df[(fct_transactions_df['transaction_date'] >= '2024-12-01') & (fct_transactions_df['transaction_date'] < '2025-01-01')]
print(fct_dec_transactions_df.info()) 
print(fct_dec_transactions_df.head())
print()
print("=" * 150)

# Then we will need to append the 'dim_risk_flags' DataFrame to the 'fct_transactions' DataFrame
fct_dec_tran_risk_df = pd.merge(fct_dec_transactions_df, dim_risk_flags_df, how='left', on='transaction_id')
print(fct_dec_tran_risk_df.info())
print(fct_dec_tran_risk_df)
print()
print("=" * 150)

# Filter for high risk transactions
dec_high_risk = fct_dec_tran_risk_df[(fct_dec_tran_risk_df['risk_level'] == 'High')].copy()
print(dec_high_risk.info())
print()
print("=" * 150)

# Add weekday column
dec_high_risk['day_of_week'] = dec_high_risk['transaction_date'].dt.day_name()
print(dec_high_risk.info())
print()
print(dec_high_risk.head())
print()
print("=" * 150)

# Count by weekday
weekday_counts = dec_high_risk.groupby('day_of_week').size().reset_index(name='transaction_count')

# Find the max
max_day = weekday_counts.sort_values('transaction_count', ascending=False).head(1)

# Answer to question 3 
print("\nWeekdays with high-risk activity in Dec 2024:")
print(weekday_counts)
print("\nDay with highest high-risk activity in Dec 2024:")
print(max_day)