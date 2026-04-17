-- stg_enrollments - Silver layer cleaned view
{{ config(materialized='view') }}

with source as (
    select * from {{ source('main', 'enrollments') }}
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
