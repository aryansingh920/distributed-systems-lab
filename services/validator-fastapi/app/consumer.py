import os
import json
import threading
from confluent_kafka import Consumer
from sqlalchemy import text
from app.db import engine

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
        "auto.offset.reset": "earliest"
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
        persist_event(event)
        print("persisted order event:", event.get("order_id"))


def run_in_thread():
    t = threading.Thread(target=start_consumer, daemon=True)
    t.start()
