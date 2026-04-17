import os
import sys
import sqlite3
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import BRONZE_PATH, DB_PATH

def load_bronze_to_sqlite():
    tables = [
        "semesters",
        "instructors",
        "courses",
        "students",
        "prerequisites",
        "enrollments"
    ]

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    for table in tables:
        csv_file = os.path.join(BRONZE_PATH, f"{table}.csv")
        if os.path.exists(csv_file):
            print(f"Loading '{table}' from {csv_file}...")
            df = pd.read_csv(csv_file)
            df.to_sql(table, conn, if_exists='replace', index=False)
            print(f"Successfully loaded {len(df)} records into '{table}'.")
        else:
            print(f"Warning: {csv_file} not found. Skipping '{table}'.")

    conn.close()
    print(f"\nAll Bronze CSVs loaded into SQLite Database -> {DB_PATH}")

if __name__ == "__main__":
    load_bronze_to_sqlite()
