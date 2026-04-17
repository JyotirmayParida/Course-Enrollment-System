-- mart_prerequisite_compliance
-- Identifies students enrolled in courses without completing prerequisites.
-- Helps detect prerequisite violations where students may need intervention
-- or should not have been allowed to enroll.

{{ config(materialized='table') }}

with student_completed_courses as (
    select distinct
        student_id,
        course_id
    from {{ ref('stg_enrollments') }}
    where grade not in ('F', 'W')
),
enrollments_with_prereqs as (
    select
        e.student_id,
        e.course_id,
        p.prerequisite_course_id
    from {{ ref('stg_enrollments') }} e
    inner join {{ ref('stg_prerequisites') }} p
        on e.course_id = p.course_id
)
select
    ep.student_id,
    ep.course_id,
    ep.prerequisite_course_id,
    case when scc.student_id is not null then 1 else 0 end as has_completed_prereq,
    case when scc.student_id is null then 1 else 0 end as is_violation
from enrollments_with_prereqs ep
left join student_completed_courses scc
    on ep.student_id = scc.student_id
    and ep.prerequisite_course_id = scc.course_id
