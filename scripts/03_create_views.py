import sqlite3
import re

# Connect to database
conn = sqlite3.connect('database/real_estate.db')
cursor = conn.cursor()


# Read the views.sql file
with open('sql/views.sql', 'r') as f:
    sql_script = f.read()

# Extract view names using regex
view_names = re.findall(r'CREATE VIEW (\w+) AS', sql_script)

# Drop existing views
for view_name in view_names:
    cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
    print(f"Dropped view: {view_name}")

print("\nDropped existing views")

# Execute all the CREATE VIEW statements
cursor.executescript(sql_script)

print("All views created successfully!")

# Verify views were created
print("\n=== Verifying Views ===")
for view_name in view_names:
    result = cursor.execute(f"SELECT COUNT(*) FROM {view_name}").fetchone()
    print(f"{view_name}: {result[0]} rows")

print("All views created and verified!")

# Commit and close
conn.commit()
conn.close()