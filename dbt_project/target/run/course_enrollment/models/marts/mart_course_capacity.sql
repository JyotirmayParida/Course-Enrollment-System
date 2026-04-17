
  
    
    

    create  table
      "analytics"."main"."mart_course_capacity__dbt_tmp"
  
    as (
      -- mart_course_capacity
-- Course capacity analysis showing enrolled vs available seats.
-- Identifies courses that are at or over capacity to help with
-- enrollment management and resource planning.



select
    c.course_id,
    c.course_name,
    c.department_name,
    c.capacity,
    count(e.enrollment_id) as enrolled_count,
    greatest(c.capacity - count(e.enrollment_id), 0) as seats_remaining,
    case when count(e.enrollment_id) > c.capacity then 1 else 0 end as is_over_capacity
from "analytics"."main"."stg_courses" c
left join "analytics"."main"."stg_enrollments" e
    on c.course_id = e.course_id
group by c.course_id, c.course_name, c.department_name, c.capacity
    );
  
  