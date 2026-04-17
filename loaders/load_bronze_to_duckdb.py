import duckdb, os

DB_PATH = "db/analytics.duckdb"
BRONZE_PATH = "data/bronze"

tables = ["semesters","instructors","courses","students","prerequisites","enrollments"]

con = duckdb.connect(DB_PATH)
for table in tables:
    csv_path = os.path.join(BRONZE_PATH, f"{table}.csv").replace("\\", "/")
    con.execute(f"DROP TABLE IF EXISTS {table}")
    con.execute(f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto('{csv_path}')")
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {count} rows loaded")
con.close()
print("DuckDB load complete --> db/analytics.duckdb")
