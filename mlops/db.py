# mlops/db.py

import psycopg2
from datetime import datetime
import os


# ======================================================
# DATABASE CONFIG
# ======================================================

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


# ======================================================
# CONNECTION
# ======================================================

def get_conn():
    return psycopg2.connect(**DB_CONFIG)


# ======================================================
# INIT DATABASE
# ======================================================

def init_db():

    conn = get_conn()
    cur = conn.cursor()

    # ==================================================
    # USERS TABLE
    # ==================================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP
    );
    """)

    # ==================================================
    # MODELS TABLE
    # ==================================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS models (
        id SERIAL PRIMARY KEY,
        model_name TEXT,
        model_type TEXT,
        version INTEGER,
        created_at TIMESTAMP
    );
    """)

    # ==================================================
    # PREDICTIONS TABLE
    # ==================================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        model_name TEXT,
        input_type TEXT,
        prediction TEXT,
        time TIMESTAMP
    );
    """)

    # ==================================================
    # API USAGE TABLE
    # ==================================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS api_usage (
        id SERIAL PRIMARY KEY,
        endpoint TEXT,
        method TEXT,
        created_at TIMESTAMP
    );
    """)

    conn.commit()

    cur.close()
    conn.close()


# ======================================================
# USER FUNCTIONS
# ======================================================

def create_user(username, email, password):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO users (
        username,
        email,
        password,
        created_at
    )
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    """, (
        username,
        email,
        password,
        datetime.now()
    ))

    user_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return user_id


def get_user_by_email(email):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, username, email, password
    FROM users
    WHERE email=%s;
    """, (email,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


# ======================================================
# MODEL FUNCTIONS
# ======================================================

def insert_model(model_name, model_type, version):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO models (
        model_name,
        model_type,
        version,
        created_at
    )
    VALUES (%s, %s, %s, %s);
    """, (
        model_name,
        model_type,
        version,
        datetime.now()
    ))

    conn.commit()

    cur.close()
    conn.close()


# ======================================================
# PREDICTION FUNCTIONS
# ======================================================

def insert_prediction(model_name, input_type, prediction):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO predictions (
        model_name,
        input_type,
        prediction,
        time
    )
    VALUES (%s, %s, %s, %s);
    """, (
        model_name,
        input_type,
        str(prediction),
        datetime.now()
    ))

    conn.commit()

    cur.close()
    conn.close()


# ======================================================
# API USAGE FUNCTIONS
# ======================================================

def insert_api_usage(endpoint, method="GET"):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO api_usage (
        endpoint,
        method,
        created_at
    )
    VALUES (%s, %s, %s);
    """, (
        endpoint,
        method,
        datetime.now()
    ))

    conn.commit()

    cur.close()
    conn.close()