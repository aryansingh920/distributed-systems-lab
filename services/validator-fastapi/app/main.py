"""
Created on 04/01/2026

@author: Aryan

Filename: main.py

Relative Path: services/validator-fastapi/app/main.py
"""

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest, REGISTRY

from app.consumer import run_in_thread
from app.db import init_db_with_retry

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db_with_retry()
    run_in_thread()


@app.get("/health")
def health():
    return {"ok": True, "service": "validator-fastapi"}


@app.get("/metrics")
def metrics():
    data = generate_latest(REGISTRY)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
