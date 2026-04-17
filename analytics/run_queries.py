import sys
import duckdb

DB_PATH = "db/analytics.duckdb"
SQL_FILE = "analytics/queries.sql"

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    con = duckdb.connect(DB_PATH)
    print(f"\n{'═'*60}")
    print(f"  COURSE ENROLLMENT SYSTEM — ANALYTICS REPORT")
    print(f"{'═'*60}")

    try:
        with open(SQL_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read {SQL_FILE}: {e}")
        return

    # Split the file by queries
    blocks = content.split(";")
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # extract title
        lines = block.split('\n')
        title = "Query"
        sql_lines = []
        for line in lines:
            if line.startswith("-- Q"):
                title = line.strip("-- ").strip()
            elif not line.startswith("--") and line.strip():
                sql_lines.append(line)
        
        # Skip if block was only comments (e.g. the header at the top)
        if not sql_lines:
            continue
            
        sql = "\n".join(sql_lines).strip()
        
        print(f"\n{'─'*60}")
        print(f"  {title}")
        print(f"{'─'*60}")
        try:
            df = con.execute(sql).df()
            print(df.to_string(index=False))
        except Exception as e:
            print(f"  ERROR: {e}")

    con.close()
    print(f"\n{'═'*60}")
    print(f"  ✅ All queries complete")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    main()
