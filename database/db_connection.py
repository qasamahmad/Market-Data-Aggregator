import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Return a PostgreSQL connection using DATABASE_URL."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set")
    return psycopg.connect(db_url)