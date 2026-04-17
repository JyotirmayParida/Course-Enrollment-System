
  
  create view "analytics"."main"."stg_enrollments__dbt_tmp" as (
    -- stg_enrollments - Silver layer cleaned view


with source as (
    select * from main.enrollments
),
staged as (
    select
        enrollment_id,
        student_id,
        course_id,
        semester_id,
        upper(grade) as grade,
        cast(created_at as timestamp) as created_at
    from source
)
select * from staged
  );
