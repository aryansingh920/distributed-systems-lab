"""
Created on 04/01/2026

@author: Aryan

Filename: db.py

Relative Path: services/validator-fastapi/app/db.py
"""

import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "orders_db")
DB_USER = os.getenv("DB_USER", "app")
DB_PASS = os.getenv("DB_PASS", "app")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS order_events (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                event_id VARCHAR(64) NOT NULL UNIQUE,
                event_type VARCHAR(64) NOT NULL,
                ts VARCHAR(64) NOT NULL,
                order_id VARCHAR(64) NOT NULL,
                user_id VARCHAR(64) NULL,
                amount DECIMAL(18,4) NULL,
                currency VARCHAR(8) NULL,
                raw_json JSON NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))


def init_db_with_retry(max_attempts=30, sleep_seconds=2):
    last = None
    for i in range(1, max_attempts + 1):
        try:
            init_db()
            print("DB ready")
            return
        except OperationalError as e:
            last = e
            print(f"DB not ready (attempt {i}/{max_attempts}), retrying...")
            time.sleep(sleep_seconds)
    raise last
