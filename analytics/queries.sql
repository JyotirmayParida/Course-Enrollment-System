-- ============================================================
-- COURSE ENROLLMENT SYSTEM — ANALYTICS QUERIES
-- Target: db/analytics.duckdb
-- Run with: python analytics/run_queries.py
-- ============================================================

-- Q1: Enrollment by Department
SELECT
    c.department_name,
    COUNT(*) AS total_enrollments,
    SUM(CASE WHEN e.grade NOT IN ('F','W') THEN 1 ELSE 0 END) AS passed,
    SUM(CASE WHEN e.grade = 'F' THEN 1 ELSE 0 END) AS failed,
    SUM(CASE WHEN e.grade = 'W' THEN 1 ELSE 0 END) AS withdrawn
FROM stg_enrollments e
JOIN stg_courses c ON e.course_id = c.course_id
GROUP BY c.department_name
ORDER BY total_enrollments DESC;

-- Q2: Top 10 Courses by Enrollment
SELECT
    course_id,
    course_name,
    department_name,
    capacity,
    enrolled_count,
    seats_remaining,
    is_over_capacity
FROM mart_course_capacity
ORDER BY enrolled_count DESC
LIMIT 10;

-- Q3: Weekly Enrollment Trend
SELECT
    strftime(created_at, '%Y-%W') AS year_week,
    COUNT(*) AS enrollments_that_week,
    SUM(COUNT(*)) OVER (ORDER BY strftime(created_at, '%Y-%W')) AS cumulative_enrollments
FROM stg_enrollments
GROUP BY strftime(created_at, '%Y-%W')
ORDER BY year_week;

-- Q4: Student Pass Rate Distribution
SELECT
    CASE
        WHEN pass_rate >= 0.8 THEN 'High (>=80%)'
        WHEN pass_rate >= 0.5 THEN 'Mid (50-79%)'
        ELSE 'Low (<50%)'
    END AS pass_rate_band,
    COUNT(*) AS student_count,
    ROUND(AVG(total_enrollments), 1) AS avg_courses,
    ROUND(AVG(credits_attempted), 1) AS avg_credits_attempted,
    ROUND(AVG(credits_earned), 1) AS avg_credits_earned
FROM mart_student_progress
GROUP BY pass_rate_band
ORDER BY pass_rate_band;

-- Q5: Course Capacity Risk Ranking
SELECT
    course_id,
    course_name,
    department_name,
    capacity,
    enrolled_count,
    ROUND(enrolled_count * 100.0 / NULLIF(capacity, 0), 1) AS fill_rate_pct,
    CASE
        WHEN enrolled_count >= capacity THEN 'OVER CAPACITY'
        WHEN enrolled_count >= capacity * 0.8 THEN 'CRITICAL'
        WHEN enrolled_count >= capacity * 0.6 THEN 'HIGH'
        ELSE 'NORMAL'
    END AS capacity_status
FROM mart_course_capacity
ORDER BY fill_rate_pct DESC
LIMIT 15;

-- Q6: Instructor Overload Summary
SELECT
    instructor_id,
    instructor_name,
    COUNT(DISTINCT semester_id) AS semesters_active,
    SUM(courses_assigned) AS total_courses,
    ROUND(AVG(courses_assigned), 1) AS avg_courses_per_semester,
    SUM(is_overloaded) AS overloaded_semesters
FROM mart_instructor_load
GROUP BY instructor_id, instructor_name
ORDER BY total_courses DESC
LIMIT 10;
