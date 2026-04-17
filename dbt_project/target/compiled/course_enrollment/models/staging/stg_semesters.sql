-- stg_semesters - Silver layer cleaned view


with source as (
    select * from main.semesters
),
staged as (
    select
        semester_id,
        name as semester_name,
        cast(start_date as date) as start_date,
        cast(end_date as date) as end_date,
        cast(created_at as timestamp) as created_at
    from source
)
select * from staged