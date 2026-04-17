-- mart_enrollment_summary
-- Aggregated enrollment metrics by course and semester, including pass/fail/withdraw counts.
-- This model joins enrollments with courses and semesters to provide a comprehensive
-- view of course enrollment performance for each semester.

{{ config(materialized='table') }}

select
    c.course_id,
    c.course_name,
    e.semester_id,
    count(*) as total_enrollments,
    sum(case when e.grade not in ('F', 'W') then 1 else 0 end) as pass_count,
    sum(case when e.grade = 'F' then 1 else 0 end) as fail_count,
    sum(case when e.grade = 'W' then 1 else 0 end) as withdraw_count
from {{ ref('stg_enrollments') }} e
inner join {{ ref('stg_courses') }} c
    on e.course_id = c.course_id
group by c.course_id, c.course_name, e.semester_id
