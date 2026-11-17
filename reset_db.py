"""Run before every demo:  python reset_db.py
Recreates tasks.db from schema.sql with fresh sample data."""
from app import init_db

init_db()
print("Database reset. Sample tasks loaded.")
