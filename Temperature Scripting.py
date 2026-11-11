import random, sqlite3, time #regular imports
import pandas as pd
from datetime import datetime 

db = sqlite3.connect("temps.db") #this sets the variable db to a file temps.db
db.execute("""CREATE TABLE IF NOT EXISTS readings ( 
    id INTEGER PRIMARY KEY,
    temp_c REAL,
    taken_at TEXT)""")
# 
temp = 22.0
for _ in range(5):
    temp += random.uniform(-0.3,0.3)
    db.execute ("INSERT INTO readings (temp_c) VALUES (?)",
                (round(temp, 2),))
    db.commit()
    print(f"{temp:.2f} C")
    time.sleep(1)

readings = pd.read_sql_query("SELECT * FROM readings", db)

summary = pd.read_sql_query(
    "SELECT MIN(temp_c) AS temp_c, MAX(temp_c) AS max_c, AVG(temp_c) AS avg_c FROM readings",
    db)

with pd.ExcelWriter("temps.xlsx") as writer:
    readings.to_excel(writer, sheet_name="Readings", index=False)
    summary.to_excel(writer, sheet_name="Summary", index=False)

print(summary)