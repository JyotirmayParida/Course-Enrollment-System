import subprocess
import sys
import time
import duckdb
from datetime import datetime

# Force UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def log(msg, symbol="•"):
    print(f"  {symbol}  {msg}")

def run_step(label, func):
    print(f"\n{'─'*50}")
    print(f"  STEP: {label}")
    print(f"{'─'*50}")
    start = time.time()
    try:
        func()
        elapsed = round(time.time() - start, 2)
        log(f"Done in {elapsed}s", "✅")
        return True
    except Exception as e:
        log(f"FAILED: {e}", "❌")
        return False

def step_load_duckdb():
    result = subprocess.run(
        [sys.executable, "loaders/load_bronze_to_duckdb.py"],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0:
        raise RuntimeError(result.stderr)

def step_dbt_staging():
    """Run dbt staging models (stg_*)"""
    result = subprocess.run(
        ["dbt", "run", "--select", "stg_*",
         "--project-dir", "dbt_project",
         "--profiles-dir", "dbt_project"],
        capture_output=True, text=True
    )
    # Parse and display key lines from dbt output
    _print_dbt_summary(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-500:])

def step_dbt_marts():
    """Run dbt mart models (marts*)"""
    result = subprocess.run(
        ["dbt", "run", "--select", "marts*",
         "--project-dir", "dbt_project",
         "--profiles-dir", "dbt_project"],
        capture_output=True, text=True
    )
    _print_dbt_summary(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-500:])

def _print_dbt_summary(output):
    """Extract and print clean dbt run summary lines."""
    for line in output.splitlines():
        line_stripped = line.strip()
        # Show model run lines and the final summary
        if any(kw in line_stripped for kw in [
            "OK created", "ERROR creating",
            "PASS=", "Finished running",
            "Found", "Concurrency"
        ]):
            # Remove the timestamp prefix (e.g., "05:10:57  ")
            parts = line_stripped.split("  ", 1)
            clean = parts[1] if len(parts) > 1 else line_stripped
            log(clean)

def step_summary():
    con = duckdb.connect("db/analytics.duckdb")
    layers = {
        "Bronze (source tables)": [
            "semesters", "instructors", "courses",
            "students", "prerequisites", "enrollments"
        ],
        "Silver (staging views)": [
            "stg_semesters", "stg_instructors", "stg_courses",
            "stg_students", "stg_prerequisites", "stg_enrollments"
        ],
        "Gold (mart tables)": [
            "mart_course_capacity", "mart_enrollment_summary",
            "mart_instructor_load", "mart_prerequisite_compliance",
            "mart_student_progress"
        ],
    }
    print(f"\n{'─'*50}")
    print(f"  PIPELINE SUMMARY — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'─'*50}")
    for layer, tables in layers.items():
        print(f"\n  {layer}")
        for t in tables:
            try:
                count = con.execute(
                    f"SELECT COUNT(*) FROM {t}"
                ).fetchone()[0]
                log(f"{t:<40} {count:>6} rows")
            except Exception:
                log(f"{t:<40}  NOT FOUND", "⚠️")
    con.close()

def main():
    print(f"\n{'═'*50}")
    print(f"  COURSE ENROLLMENT SYSTEM — PIPELINE RUN")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'═'*50}")

    pipeline_start = time.time()
    steps = [
        ("Load Bronze → DuckDB",      step_load_duckdb),
        ("dbt run — staging layer",    step_dbt_staging),
        ("dbt run — mart layer",       step_dbt_marts),
        ("Pipeline summary",           step_summary),
    ]

    for label, func in steps:
        success = run_step(label, func)
        if not success:
            print(f"\n❌ Pipeline aborted at: {label}")
            sys.exit(1)

    total = round(time.time() - pipeline_start, 2)
    print(f"\n{'═'*50}")
    print(f"  ✅ PIPELINE COMPLETE — {total}s total")
    print(f"{'═'*50}\n")

if __name__ == "__main__":
    main()
