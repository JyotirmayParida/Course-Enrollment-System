
  
  create view "analytics"."main"."stg_prerequisites__dbt_tmp" as (
    -- stg_prerequisites - Silver layer cleaned view


with source as (
    select * from main.prerequisites
),
staged as (
    select
        prerequisite_id,
        course_id,
        prerequisite_course_id,
        cast(created_at as timestamp) as created_at
    from source
)
select * from staged
  );
