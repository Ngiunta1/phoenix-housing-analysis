import pandas as pd
import numpy as np

# Load data into a data frame
print("Loading data...")
df = pd.read_csv('data/raw/realtor-data.csv')
print(f"Original dataset: {len(df):,} rows, {len(df.columns)} columns")

# Filter the dataframe to show only Arizona data
df_az = df[df['state'] == 'Arizona']
print(f"Arizona rows: {len(df_az):,}")

# Filter to show only Phoenix data
df_phoenix = df_az[df_az['city'].str.contains('___', case=False, na=False)]

print("\nTop 10 Arizona cities:")
print(df_az['city'].value_counts().head(10))

# Unique cities in Arizona
print(f"\nUnique Arizona cities: {df_az['city'].nunique()}")

# Use only Arizona data
df_filtered = df_az.copy()
print(f"\nWorking with Arizona data: {len(df_filtered):,} rows")

# Drop rows where price is or house_size is null
df_clean = df_filtered.dropna(subset=['price', 'house_size', 'bed', 'bath'])
print(f"\nCleaned data: {len(df_clean):,} rows")

# Drop unneccessary columns before importing to database (Less data so Queries can run faster later)
df_clean = df_clean.drop(columns=['brokered_by', 'street'])

# Check for outliers that must be input errors
print("\nPrice statistics:")
print(df_clean['price'].describe())

print("\nTop 10 most expensive:")
print(df_clean.nlargest(10, 'price')[['price', 'city', 'bed', 'bath', 'house_size']])

print("\nBottom 10 most expensive:")
print(df_clean.nsmallest(50, 'price')[['price', 'city', 'bed', 'bath', 'house_size']])

# Check price distribution by percentiles
print("\nPrice percentiles:")
print(df_clean['price'].quantile([0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]))

# Drop unrealistic outliers (Too cheap ~Under $50,000 and too expensive)
df_clean = df_clean[~((df_clean['city'] == 'congress') & (df_clean['price'] >= 25,000,000))]