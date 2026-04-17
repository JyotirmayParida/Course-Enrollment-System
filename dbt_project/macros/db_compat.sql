{% macro source(source_name, table_name) %}
    {{ return(source_name ~ '.' ~ table_name) }}
{% endmacro %}
