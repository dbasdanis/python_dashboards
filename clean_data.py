import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('internet_usage_dirty.csv',delimiter=';')

# Remove columns with "_notes" or "_source" in the header description
df = df.loc[:, ~df.columns.str.contains('_notes|_source')]

# Remove "_value" text from header names
df.columns = df.columns.str.replace('_value', '')

# Remove the first and last columns
df = df.iloc[:, 1:-1]

# Change the second column heading from "Economy" to "Country"
df = df.rename(columns={'Economy': 'Country'})

# Save the cleaned data to a new CSV file
df.to_csv('internet_usage_clean.csv', index=False)
