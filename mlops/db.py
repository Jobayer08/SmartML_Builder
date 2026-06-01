# mlops/db.py

import psycopg2
from psycopg2.extras import RealDictCursor
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

        user_id INTEGER REFERENCES users(id),

        model_name TEXT,
        model_type TEXT,

        version INTEGER,

        file_path TEXT,

        created_at TIMESTAMP
    );
    """)

    # ==================================================
    # PREDICTIONS TABLE
    # ==================================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (

        id SERIAL PRIMARY KEY,

        user_id INTEGER REFERENCES users(id),

        model_name TEXT,

        input_type TEXT,

        prediction TEXT,

        created_at TIMESTAMP
    );
    """)

    # ==================================================
    # API USAGE TABLE
    # ==================================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS api_usage (

        id SERIAL PRIMARY KEY,

        user_id INTEGER,

        endpoint TEXT,

        method TEXT,

        created_at TIMESTAMP
    );
    """)

    # Ensure older DB schemas include user_id in api_usage
    cur.execute("""
    ALTER TABLE api_usage
    ADD COLUMN IF NOT EXISTS user_id INTEGER;
    """)

    # ==================================================
    # DATASETS TABLE
    # ==================================================

    cur.execute("""
    CREATE TABLE IF NOT EXISTS datasets (

        id SERIAL PRIMARY KEY,

        user_id INTEGER REFERENCES users(id),

        dataset_name TEXT,

        dataset_type TEXT,

        file_path TEXT,

        file_size_mb FLOAT,

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

    cur = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cur.execute("""
    SELECT *
    FROM users
    WHERE email=%s;
    """, (email,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


def get_user_by_id(user_id):

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cur.execute("""
    SELECT *
    FROM users
    WHERE id=%s;
    """, (user_id,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


# ======================================================
# MODEL FUNCTIONS
# ======================================================

def insert_model(
    user_id,
    model_name,
    model_type,
    version,
    file_path
):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO models (

        user_id,
        model_name,
        model_type,
        version,
        file_path,
        created_at

    )
    VALUES (%s, %s, %s, %s, %s, %s);
    """, (

        user_id,
        model_name,
        model_type,
        version,
        file_path,
        datetime.now()

    ))

    conn.commit()

    cur.close()
    conn.close()


def get_user_models(user_id):

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cur.execute("""
    SELECT *
    FROM models
    WHERE user_id=%s
    ORDER BY created_at DESC;
    """, (user_id,))

    models = cur.fetchall()

    cur.close()
    conn.close()

    return models


def get_model_by_name(user_id, model_name):

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cur.execute("""
    SELECT *
    FROM models
    WHERE user_id=%s
    AND model_name=%s;
    """, (

        user_id,
        model_name

    ))

    model = cur.fetchone()

    cur.close()
    conn.close()

    return model


# ======================================================
# VERSIONING FUNCTIONS
# ======================================================

def get_next_version(model_name):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT MAX(version)
    FROM models
    WHERE model_name=%s;
    """, (model_name,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    if result is None:
        return 1

    return result + 1


# ======================================================
# PREDICTION FUNCTIONS
# ======================================================

def insert_prediction(
    user_id,
    model_name,
    input_type,
    prediction
):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO predictions (

        user_id,
        model_name,
        input_type,
        prediction,
        created_at

    )
    VALUES (%s, %s, %s, %s, %s);
    """, (

        user_id,
        model_name,
        input_type,
        str(prediction),
        datetime.now()

    ))

    conn.commit()

    cur.close()
    conn.close()


def get_api_usage(user_id):

    conn = get_conn()
    cur = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cur.execute("""
    SELECT *
    FROM api_usage
    WHERE user_id=%s
    ORDER BY created_at DESC;
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def get_user_predictions(user_id):

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cur.execute("""
    SELECT *
    FROM predictions
    WHERE user_id=%s
    ORDER BY created_at DESC;
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


# ======================================================
# API USAGE FUNCTIONS
# ======================================================

def insert_api_usage(
    endpoint,
    method="GET",
    user_id=None
):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO api_usage (

        user_id,
        endpoint,
        method,
        created_at

    )
    VALUES (%s, %s, %s, %s);
    """, (

        user_id,
        endpoint,
        method,
        datetime.now()

    ))

    conn.commit()

    cur.close()
    conn.close()


# ======================================================
# DASHBOARD ANALYTICS
# ======================================================

def total_models():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT COUNT(*)
    FROM models;
    """)

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count


def total_predictions():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT COUNT(*)
    FROM predictions;
    """)

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count


def most_used_models():

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cur.execute("""
    SELECT
        model_name,
        COUNT(*) as usage_count

    FROM predictions

    GROUP BY model_name

    ORDER BY usage_count DESC

    LIMIT 10;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

# ======================================================
# DATASET FUNCTIONS
# ======================================================

def insert_dataset(
    user_id,
    dataset_name,
    dataset_type,
    file_path,
    file_size_mb
):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO datasets (

        user_id,
        dataset_name,
        dataset_type,
        file_path,
        file_size_mb,
        created_at

    )
    VALUES (%s, %s, %s, %s, %s, %s);
    """, (

        user_id,
        dataset_name,
        dataset_type,
        file_path,
        file_size_mb,
        datetime.now()

    ))

    conn.commit()

    cur.close()
    conn.close()


def get_user_datasets(user_id):

    conn = get_conn()

    cur = conn.cursor(
        cursor_factory=RealDictCursor
    )

    cur.execute("""
    SELECT *
    FROM datasets
    WHERE user_id=%s
    ORDER BY created_at DESC;
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows