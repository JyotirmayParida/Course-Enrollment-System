-- mart_student_progress
-- Student academic progress tracking with credits attempted and earned.
-- Calculates pass rate based on successfully completed coursework
-- (excluding failures and withdrawals).

{{ config(materialized='table') }}

select
    e.student_id,
    concat(s.first_name, ' ', s.last_name) as student_name,
    count(*) as total_enrollments,
    sum(c.credit_hours) as credits_attempted,
    sum(case when e.grade not in ('F', 'W') then c.credit_hours else 0 end) as credits_earned,
    sum(case when e.grade not in ('F', 'W') then c.credit_hours else 0 end)
        / nullif(sum(c.credit_hours), 0) as pass_rate
from {{ ref('stg_enrollments') }} e
inner join {{ ref('stg_students') }} s
    on e.student_id = s.student_id
inner join {{ ref('stg_courses') }} c
    on e.course_id = c.course_id
group by e.student_id, s.first_name, s.last_name
