-- stg_prerequisites - Silver layer cleaned view
{{ config(materialized='view') }}

with source as (
    select * from {{ source('main', 'prerequisites') }}
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
