-- mart_instructor_load
-- Instructor course load analysis by semester.
-- Identifies instructors who may be overloaded with too many course
-- assignments in a given semester (threshold: > 3 courses).



select
    i.instructor_id,
    concat(i.first_name, ' ', i.last_name) as instructor_name,
    c.semester_id,
    count(*) as courses_assigned,
    case when count(*) > 1 then 1 else 0 end as is_overloaded
from "analytics"."main"."stg_courses" c
inner join "analytics"."main"."stg_instructors" i
    on c.instructor_id = i.instructor_id
group by i.instructor_id, i.first_name, i.last_name, c.semester_id