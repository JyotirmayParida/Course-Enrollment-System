# Course Enrollment System — Data Engineering Pipeline

## Project Overview

An end-to-end data engineering pipeline built around a university course enrollment system. The project generates realistic synthetic data using Python and Faker, loads it into DuckDB as the Bronze layer, and applies a **Medallion Architecture (Bronze → Silver → Gold)** using dbt-core for layered transformations. The pipeline detects real-world edge cases such as prerequisite violations (~95% violation rate in synthetic data), over-capacity courses, and instructor overload, then exposes key analytics through a suite of SQL queries. Designed to demonstrate proficiency in data modeling, ELT pipelines, and analytics engineering.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.x** | Orchestration, data generation, loading |
| **Faker** | Synthetic data generation (students, courses, enrollments) |
| **Pandas** | Data manipulation and CSV I/O |
| **DuckDB** | Analytical database (replaces SQLite for OLAP workloads) |
| **dbt-core** | Data transformation framework (staging + mart layers) |
| **dbt-duckdb** | dbt adapter for DuckDB |
| **PyArrow** | Columnar data format support |
| **Rich** | Console formatting and UTF-8 output |

---

## Project Structure

```
Course Enrollment System/
│
├── run_pipeline.py                # Main orchestrator — runs the full pipeline
├── requirements.txt               # Python dependencies
├── setup.sh                       # Environment setup script
│
├── generators/                    # Synthetic data generation (Bronze)
│   ├── generate_semesters.py
│   ├── generate_instructors.py
│   ├── generate_courses.py
│   ├── generate_students.py
│   ├── generate_prerequisites.py
│   └── generate_enrollments.py
│
├── data/
│   └── bronze/                    # Raw CSV files (Bronze layer)
│       ├── semesters.csv
│       ├── instructors.csv
│       ├── courses.csv
│       ├── students.csv
│       ├── prerequisites.csv
│       └── enrollments.csv
│
├── loaders/                       # Data loading scripts
│   ├── load_bronze_to_duckdb.py   # CSV → DuckDB loader
│   └── load_bronze_to_sqlite.py   # CSV → SQLite loader (legacy)
│
├── db/
│   └── analytics.duckdb           # DuckDB database file
│
├── dbt_project/                   # dbt transformation project
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── sources.yml
│       ├── staging/               # Silver layer (cleaned views)
│       │   ├── stg_semesters.sql
│       │   ├── stg_instructors.sql
│       │   ├── stg_courses.sql
│       │   ├── stg_students.sql
│       │   ├── stg_prerequisites.sql
│       │   └── stg_enrollments.sql
│       └── marts/                 # Gold layer (business logic tables)
│           ├── mart_enrollment_summary.sql
│           ├── mart_course_capacity.sql
│           ├── mart_student_progress.sql
│           ├── mart_instructor_load.sql
│           └── mart_prerequisite_compliance.sql
│
├── analytics/                     # Analytical queries and runner
│   ├── queries.sql                # 6 analytics queries
│   └── run_queries.py             # Query executor with formatted output
│
└── config/
    └── settings.py                # Project configuration
```

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the full pipeline (Generate → Load → Transform)

```bash
python run_pipeline.py
```

This runs all four steps in sequence:
- **Step 1:** Load Bronze CSVs into DuckDB
- **Step 2:** dbt run — staging layer (6 Silver views)
- **Step 3:** dbt run — mart layer (5 Gold tables)
- **Step 4:** Pipeline summary with row counts

### 3. Run analytics queries

```bash
python analytics/run_queries.py
```

Executes 6 analytical queries against the Gold layer and prints formatted results.

---

## Key Features Demonstrated

- **Medallion Architecture** — Bronze (raw CSVs) → Silver (cleaned staging views) → Gold (business-logic mart tables)
- **Synthetic Data Generation** — 500 students, 60 courses, 20 instructors, 2,000 enrollments with realistic edge cases using Faker
- **Prerequisite Violation Detection** — Identifies students enrolled in courses without completing prerequisites (~95% violation rate in synthetic data)
- **Over-Capacity Detection** — Flags courses where enrolled students exceed seat capacity
- **Instructor Overload Analytics** — Detects instructors assigned more courses than the threshold per semester
- **Pass Rate Distribution** — Segments students into High/Mid/Low performance bands
- **Capacity Risk Ranking** — Ranks courses by fill rate with status labels (OVER CAPACITY, CRITICAL, HIGH, NORMAL)

---

## Sample Outputs

### Pipeline Run (`python run_pipeline.py`)

```
══════════════════════════════════════════════════
  COURSE ENROLLMENT SYSTEM — PIPELINE RUN
  2026-04-17 10:54:36
══════════════════════════════════════════════════

──────────────────────────────────────────────────
  STEP: Load Bronze → DuckDB
──────────────────────────────────────────────────
  semesters: 6 rows loaded
  instructors: 20 rows loaded
  courses: 60 rows loaded
  students: 500 rows loaded
  prerequisites: 80 rows loaded
  enrollments: 2000 rows loaded
  ✅  Done in 0.72s

──────────────────────────────────────────────────
  STEP: dbt run — mart layer
──────────────────────────────────────────────────
  •  1 of 5 OK created sql table model main.mart_course_capacity      [OK in 0.13s]
  •  2 of 5 OK created sql table model main.mart_enrollment_summary   [OK in 0.05s]
  •  3 of 5 OK created sql table model main.mart_instructor_load      [OK in 0.06s]
  •  4 of 5 OK created sql table model main.mart_prerequisite_compliance [OK in 0.06s]
  •  5 of 5 OK created sql table model main.mart_student_progress     [OK in 0.05s]
  •  Done. PASS=5 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=5
  ✅  Done in 5.98s

──────────────────────────────────────────────────
  PIPELINE SUMMARY
──────────────────────────────────────────────────
  Bronze (source tables)
  •  semesters                                     6 rows
  •  instructors                                  20 rows
  •  courses                                      60 rows
  •  students                                    500 rows
  •  prerequisites                                80 rows
  •  enrollments                                2000 rows

  Silver (staging views)
  •  stg_semesters                                 6 rows
  •  stg_instructors                              20 rows
  •  stg_courses                                  60 rows
  •  stg_students                                500 rows
  •  stg_prerequisites                            80 rows
  •  stg_enrollments                            2000 rows

  Gold (mart tables)
  •  mart_course_capacity                         60 rows
  •  mart_enrollment_summary                     360 rows
  •  mart_instructor_load                         45 rows
  •  mart_prerequisite_compliance               2685 rows
  •  mart_student_progress                       489 rows

══════════════════════════════════════════════════
  ✅ PIPELINE COMPLETE — 12.07s total
══════════════════════════════════════════════════
```

### Analytics Report — Course Capacity Risk Ranking (Q5)

```
course_id                                   course_name  department_name  capacity  enrolled_count  fill_rate_pct capacity_status
 CRS-0047            Polarized value-added solution 101 COMPUTER SCIENCE        27              47          174.1   OVER CAPACITY
 CRS-0012    Secured foreground process improvement 101      MATHEMATICS        26              45          173.1   OVER CAPACITY
 CRS-0042            Phased cohesive implementation 101         BUSINESS        29              43          148.3   OVER CAPACITY
 CRS-0058              Balanced directional toolset 101         BUSINESS        27              39          144.4   OVER CAPACITY
 CRS-0044 Ameliorated homogeneous Internet solution 101      ENGINEERING        25              36          144.0   OVER CAPACITY
```

### Analytics Report — Instructor Overload Summary (Q6)

```
instructor_id  instructor_name  semesters_active  total_courses  avg_courses_per_semester  overloaded_semesters
      INS-016        Sonya Lee                 4            6.0                       1.5                   2.0
      INS-002 Jennifer Perkins                 3            5.0                       1.7                   2.0
      INS-010    Samantha Paul                 4            5.0                       1.3                   1.0
      INS-012   Patrick Harris                 3            5.0                       1.7                   2.0
      INS-013   Tonya Humphrey                 3            5.0                       1.7                   2.0
```

---

## Future Improvements

- **Data Quality Checks** — Integrate [Great Expectations](https://greatexpectations.io/) or dbt tests for automated data validation at each layer
- **Real-Time Streaming** — Replace batch CSV ingestion with a Kafka/Spark Streaming pipeline for live enrollment events
- **Dashboard Layer** — Connect a BI tool (Metabase, Superset, or Streamlit) to the Gold layer for interactive visualizations
- **CI/CD Integration** — Add GitHub Actions to run `dbt build` and analytics queries on every push

---

## License

This project is for educational and portfolio demonstration purposes.
