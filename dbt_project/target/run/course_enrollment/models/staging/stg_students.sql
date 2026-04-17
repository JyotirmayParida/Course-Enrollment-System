
  
  create view "analytics"."main"."stg_students__dbt_tmp" as (
    -- stg_students - Silver layer cleaned view


with source as (
    select * from main.students
),
staged as (
    select
        student_id,
        first_name,
        last_name,
        lower(email) as email,
        cast(enrollment_date as date) as enrollment_date,
        upper(major) as major,
        cast(created_at as timestamp) as created_at
    from source
)
select * from staged
  );
