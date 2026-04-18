import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Pull the database URL from the .env file and try to connect
DB_URI = os.getenv('DATABASE_URL')
engine = None

if DB_URI:
    try:
        engine = create_engine(DB_URI)
        with engine.connect() as conn:
            pass
        print("[SUCCESS] Connected to database.")
    except Exception as e:
        print(f"[WARNING] DB connection failed: {e}")
else:
    print("[WARNING] No DATABASE_URL found — running without DB connection.")


def db_ready():
    # Returns True only if a database connection was established
    return engine is not None


def mask_ip(ip):
    # Hides the last octet of an IP to avoid exposing specific addresses
    # e.g. 192.168.0.123 becomes 192.168.0.x
    parts = str(ip).split('.')
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.{parts[2]}.x"
    return "x.x.x.x"