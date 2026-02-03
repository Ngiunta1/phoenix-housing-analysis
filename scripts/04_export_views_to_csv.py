import pandas as pd
import sqlite3
import re

# Connect to database
conn = sqlite3.connect('database/real_estate.db')

# Get view names from views.sql
with open('sql/views.sql', 'r') as f:
    sql_script = f.read()

view_names = re.findall(r'CREATE VIEW (\w+) AS', sql_script)


for view_name in view_names:
    df = pd.read_sql(f"SELECT * FROM {view_name}", conn)
    df.to_csv(f"powerbi/data/{view_name}.csv", index = False)
    print(f"Exported {view_name}")
