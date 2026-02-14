# Create project directory

mkdir fix-finder
cd fix-finder

# Initialize uv project (creates pyproject.toml and .python-version)

uv init

# Create virtual environment (lightning fast)

uv venv

# Add dependencies (updates pyproject.toml & installs to venv)

uv add django psycopg2-binary pillow django-cleanup

# Activate on Windows (Git Bash/PowerShell)

source .venv/Scripts/activate

# OR on Mac/Linux

source .venv/bin/activate

# Create Django project

django-admin startproject config .
