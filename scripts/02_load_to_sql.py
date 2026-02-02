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
conn = sqlite3.connect('database/real_estate.db')
print("Connected to: database/real_estate.db")

# Set table name to be loaded
tbl_name = 'properties'

# Load data into database
print("\nLoading data into 'properties' table...")
df.to_sql(tbl_name, conn, if_exists = 'replace', index = False)
print(f"Loaded {len(df):,} rows into {tbl_name} table")

# Check to see that the data was correctly loaded into the sql db

result = pd.read_sql("SELECT COUNT(*) FROM properties", conn)

print(result)

result = pd.read_sql("SELECT * FROM properties LIMIT 5",conn)
print(result)

conn.close()

print("\n ✅ Loading Completed Successfully") 