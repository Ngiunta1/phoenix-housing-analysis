import pandas as pd
import sqlite3

print("="*50)
print("LOADING DATA INTO SQL DATABASE")
print("="*50)

# Load the cleaned data
print("\nLoading cleaned CSV...")
df = pd.read_csv('data/cleaned/arizona_real_estate_cleaned.csv')
print(f"Loaded {len(df):,} rows")

# Create/connect to SQLite database
print("\nConnecting to database...")
conn = sqlite3.connect('data/real_estate.db')
print("Connected to: data/real_estate.db")