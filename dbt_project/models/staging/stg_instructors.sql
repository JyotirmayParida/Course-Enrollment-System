-- stg_instructors - Silver layer cleaned view
{{ config(materialized='view') }}

with source as (
    select * from {{ source('main', 'instructors') }}
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
