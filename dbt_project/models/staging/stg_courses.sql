-- stg_courses - Silver layer cleaned view
{{ config(materialized='view') }}

with source as (
    select * from {{ source('main', 'courses') }}
),
staged as (
    select
        course_id,
        name as course_name,
        upper(department) as department_name,
        cast(credit_hours as integer) as credit_hours,
        instructor_id,
        cast(capacity as integer) as capacity,
        semester_id,
        cast(created_at as timestamp) as created_at
    from source
)
select * from staged
