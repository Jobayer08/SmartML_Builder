# app/tracker.py

from mlops.db import insert_api_usage


def log_api_usage(endpoint, method):
    """Log API endpoint usage to database"""
    try:
        insert_api_usage(endpoint, method)
    except Exception as e:
        print(f"Failed to log API usage: {e}")
