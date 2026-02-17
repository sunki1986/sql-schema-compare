# SQL Schema Compare

## Overview

SQL Schema Compare is a tool for comparing source and target SQL Server database schemas and generating deployment scripts. It is designed to automate the manual process of creating SQL scripts for database changes, making it especially useful for CI/CD pipelines.

## Features
- Compare SQL Server database schemas
- Generate deployment scripts for schema changes
- Automate SQL script generation for CI/CD

## Setup

### Requirements
- Python 3.8+
- `uv` utility for dependency management (https://github.com/astral-sh/uv)
- `sqlpackage` utility (required for extracting and comparing SQL Server schemas)

### Python Environment Setup

1. Install `uv`:
   ```shell
   pip install uv
   ```
2. Initialize the environment (creates `pyproject.toml` if not present):
   ```shell
   uv init
   ```
3. Sync dependencies:
   ```shell
   uv sync
   ```
4. Activate the virtual environment:
   ```shell
   source .venv/bin/activate
   ```

### Installing sqlpackage

#### Windows
1. Download the latest `sqlpackage` from the official Microsoft site:
   https://aka.ms/sqlpackage
2. Extract the zip file to a preferred location.
3. Add the extracted folder to your PATH environment variable.
4. Verify installation:
   ```shell
   sqlpackage /?
   ```

#### macOS
1. Download the latest `sqlpackage` for macOS from:
   https://aka.ms/sqlpackage
2. Extract the zip file:
   ```shell
   unzip sqlpackage-osx-x64-en.zip -d ~/sqlpackage
   ```
3. Add the extracted folder to your PATH:
   ```shell
   export PATH="$PATH:~/sqlpackage"
   ```
   (Add this line to your `.zshrc` or `.bash_profile` for persistence.)
4. Verify installation:
   ```shell
   sqlpackage /?
   ```

## Usage

1. Configure your source and target database connection details in `.env`.
2. Run the main script:
   ```shell
   python main.py
   ```
3. Generated deployment scripts will be available in the `output_sql/` directory.

