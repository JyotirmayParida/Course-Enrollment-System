
  
  create view "analytics"."main"."stg_instructors__dbt_tmp" as (
    -- stg_instructors - Silver layer cleaned view


with source as (
    select * from main.instructors
),
staged as (
    select
        instructor_id,
        first_name,
        last_name,
        lower(email) as email,
        upper(department) as department_name,
        cast(hire_date as date) as hire_date,
        cast(created_at as timestamp) as created_at
    from source
)
select * from staged
  );
