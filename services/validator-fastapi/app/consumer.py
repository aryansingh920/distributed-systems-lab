import os
import json
import threading
from confluent_kafka import Consumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")


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
        print("validator-fastapi consumed:", event)


def run_in_thread():
    t = threading.Thread(target=start_consumer, daemon=True)
    t.start()
