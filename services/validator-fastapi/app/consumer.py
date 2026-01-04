import os
import json
import threading
from confluent_kafka import Consumer
from sqlalchemy import text
from app.db import engine
from app.cache import cache_last2

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")



def persist_event(event: dict):
    payload = event.get("payload", {}) or {}
    with engine.begin() as conn:
        # Idempotent insert using unique event_id
        conn.execute(
            text("""
                INSERT INTO order_events
                (event_id, event_type, ts, order_id, user_id, amount, currency, raw_json)
                VALUES
                (:event_id, :event_type, :ts, :order_id, :user_id, :amount, :currency, CAST(:raw_json AS JSON))
                ON DUPLICATE KEY UPDATE event_id = event_id;
            """),
            {
                "event_id": event.get("event_id"),
                "event_type": event.get("type"),
                "ts": event.get("ts"),
                "order_id": event.get("order_id"),
                "user_id": payload.get("user_id"),
                "amount": payload.get("amount"),
                "currency": payload.get("currency"),
                "raw_json": json.dumps(event),
            }
        )


def start_consumer():
    c = Consumer({
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "validator-fastapi",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False
    })
    c.subscribe(["order.created"])

    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("kafka error:", msg.error())
            continue

        event = json.loads(msg.value().decode("utf-8"))
        
        try:
            persist_event(event)
            cache_last2(event)
            c.commit(message=msg)  # commit AFTER success
            print("persisted+cached order event:", event.get("order_id"))
        except Exception as e:
            print("failed to persist/cache:", e)
            # no commit -> message will be retrie


def run_in_thread():
    t = threading.Thread(target=start_consumer, daemon=True)
    t.start()
