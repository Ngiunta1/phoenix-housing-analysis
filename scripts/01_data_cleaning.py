import pandas as pd
import numpy as np

save_location = 'data/cleaned/arizona_real_estate_cleaned.csv'

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
df_clean = df_clean[~((df_clean['city'] == 'Congress') & (df_clean['price'] >= 25000000))]

df_clean = df_clean[df_clean['price'] >= 70000]
print(f"\nAfter removing prices under $70k: {len(df_clean):,} rows")

# Check smallest and largest listings based on house size
print("Smallest houses:")
print(df_clean.nsmallest(10, 'house_size')[['house_size', 'price', 'city']],"\n")

print("Largest houses:")
print(df_clean.nlargest(10, 'house_size')[['house_size', 'price', 'city']])

# Removing unrealistic house sizes

df_clean['price_per_sqft'] = df_clean['price'] / df_clean['house_size']

print("\nLargest houses with price/sqft:")
print(df_clean.nlargest(10, 'house_size')[['house_size', 'price', 'city', 'price_per_sqft']])

df_clean = df_clean[(df_clean['price_per_sqft'] >= 20) & (df_clean['price_per_sqft'] <= 1500)]

print(f"\nAfter removing unrealistic price/sqft: {len(df_clean):,} rows")

# Categorize price ranges
def categorize_price(price):
    if price < 300000:
        return 'Budget'
    elif price < 600000:
        return 'Mid-Range'
    else:
        return 'Luxury'

df_clean['price_category'] = df_clean['price'].apply(categorize_price)

# Distribution
print("\nPrice category distribution:")
print(df_clean['price_category'].value_counts())

# Final Dataset Info
print("\n" + "="*50)
print("FINAL CLEANED DATASET")
print("="*50)
print(f"\nTotal rows: {len(df_clean):,}")
print(f"Total columns: {len(df_clean.columns)}")

print("\nColumns:")
print(df_clean.columns.tolist())

print("\nMissing values:")
print(df_clean.isnull().sum())

print("\nBasic statistics")
print(df_clean[['price', 'bed', 'bath', 'house_size', 'price_per_sqft']].describe())

print("\nSample data:")
print(df_clean.head(10))

# Save cleaned data
print("\n" + "="*50)
print("SAVING CLEANED DATA")
print("="*50)

df_clean.to_csv(save_location, index=False)
print(f"\nCleaned data saved to: {save_location}")

print("\n DATA CLEANING COMPLETE!")
print(f"Final dataset: {len(df_clean):,} rows * {len(df_clean.columns)} columns")
