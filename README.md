# FixFinders

FixFinders is a service provider directory app, a Django-based backend application being developed to connect users with local service providers in Myanmar.  
It focuses on practical features like search, listings, and bookings tailored to the local context.
2026

---

## Tech Stack

- Python 3
- Django
- PostgreSQL (for production; SQLite may be used locally)
- uv (package and environment manager)
- Gunicorn (for production web server)
- Render (for hosting)

---

## Project Setup (from scratch)

> This section shows how the project was originally created using `uv` and Django.  
> You **do not** need to run these steps again if you already cloned this repo.

```bash
# 1. Create project directory
mkdir fix-finder
cd fix-finder

# 2. Initialize uv project (creates pyproject.toml and .python-version)
uv init

# 3. Create virtual environment (lightning fast)
uv venv

# 4. Activate virtual environment
# On Windows (Git Bash / PowerShell)
source .venv/Scripts/activate

# On Mac / Linux
source .venv/bin/activate

# 5. Add core dependencies (updates pyproject.toml & installs to venv)
uv add django psycopg2-binary pillow django-cleanup


