"""
Database migration script to add user_id columns to tables
for multi-user SaaS support.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "smartml_user"),
        password=os.getenv("DB_PASSWORD", "smartml_password"),
        database=os.getenv("DB_NAME", "smartml_db"),
        port=os.getenv("DB_PORT", 5432)
    )

def run_migrations():
    """Run all pending migrations"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        print("Starting migrations...")
        
        # Check if user_id column exists in models table
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'models' AND column_name = 'user_id'
        """)
        if not cur.fetchone():
            print("Adding user_id column to models table...")
            cur.execute("""
                ALTER TABLE models 
                ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1,
                ADD CONSTRAINT fk_models_user_id FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            print("✓ Added user_id to models table")
        else:
            print("✓ user_id column already exists in models table")
        
        # Check if user_id column exists in datasets table
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'datasets' AND column_name = 'user_id'
        """)
        if not cur.fetchone():
            print("Adding user_id column to datasets table...")
            cur.execute("""
                ALTER TABLE datasets 
                ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1,
                ADD CONSTRAINT fk_datasets_user_id FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            print("✓ Added user_id to datasets table")
        else:
            print("✓ user_id column already exists in datasets table")
        
        # Check if user_id column exists in predictions table
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'predictions' AND column_name = 'user_id'
        """)
        if not cur.fetchone():
            print("Adding user_id column to predictions table...")
            cur.execute("""
                ALTER TABLE predictions 
                ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1,
                ADD CONSTRAINT fk_predictions_user_id FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            print("✓ Added user_id to predictions table")
        else:
            print("✓ user_id column already exists in predictions table")
        
        # Check if user_id column exists in api_usage table
        cur.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'api_usage' AND column_name = 'user_id'
        """)
        if not cur.fetchone():
            print("Adding user_id column to api_usage table...")
            cur.execute("""
                ALTER TABLE api_usage 
                ADD COLUMN user_id INTEGER DEFAULT 1,
                ADD CONSTRAINT fk_api_usage_user_id FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            print("✓ Added user_id to api_usage table")
        else:
            print("✓ user_id column already exists in api_usage table")
        
        conn.commit()
        print("\n✓ All migrations completed successfully!")
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_migrations()
