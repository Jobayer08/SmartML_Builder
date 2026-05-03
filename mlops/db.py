# mlops/db.py

import psycopg2
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "database": "smartml",
    "user": "postgres",
    "password": "postgres"
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
        time TIMESTAMP
    );
    """)

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


def insert_api_usage(endpoint):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO api_usage (endpoint, time)
    VALUES (%s, %s);
    """, (endpoint, datetime.now()))

    conn.commit()
    cur.close()
    conn.close()