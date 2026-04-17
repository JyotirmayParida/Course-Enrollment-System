#!/bin/bash

# Create data directories
mkdir -p data/{bronze,silver,gold}

# Create source code directories
mkdir -p src/{ingestion,transformation,quality,orchestration}

# Create dbt directories
mkdir -p dbt_project/models/{staging,mart}
mkdir -p dbt_project/{tests,macros}

# Create other directories
mkdir -p docs analytics

echo "Directory structure created successfully."
