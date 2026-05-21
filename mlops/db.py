# mlops/db.py

import psycopg2
from datetime import datetime
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT")
if not DB_PORT:
    DB_PORT = "5433" if DB_HOST in ("localhost", "127.0.0.1") else "5432"

DB_CONFIG = {
    "host": DB_HOST,
    "database": os.getenv("DB_NAME", "smartml"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "port": DB_PORT
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)


# ---------------------------------------------------
# 🧱 TABLE CREATE (RUN ONCE)
# ---------------------------------------------------
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS models (
        id SERIAL PRIMARY KEY,
        model_name TEXT,
        model_type TEXT,
        version INTEGER,
        created_at TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        model_name TEXT,
        input_type TEXT,
        prediction TEXT,
        time TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS api_usage (
        id SERIAL PRIMARY KEY,
        endpoint TEXT,
        method TEXT,
        created_at TIMESTAMP
    );
    """)

    # Add missing API usage columns for existing schema versions
    cur.execute("ALTER TABLE api_usage ADD COLUMN IF NOT EXISTS method TEXT;")

    conn.commit()
    cur.close()
    conn.close()


# ---------------------------------------------------
# 📦 INSERT FUNCTIONS
# ---------------------------------------------------
def insert_model(model_name, model_type, version):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO models (model_name, model_type, version, created_at)
    VALUES (%s, %s, %s, %s);
    """, (model_name, model_type, version, datetime.now()))

    conn.commit()
    cur.close()
    conn.close()


def insert_prediction(model_name, input_type, prediction):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO predictions (model_name, input_type, prediction, time)
    VALUES (%s, %s, %s, %s);
    """, (model_name, input_type, str(prediction), datetime.now()))

    conn.commit()
    cur.close()
    conn.close()



def insert_api_usage(endpoint, method="GET"):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO api_usage (endpoint, method, created_at)
    VALUES (%s, %s, %s);
    """, (endpoint, method, datetime.now()))

    conn.commit()
    cur.close()
    conn.close()
