from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest, REGISTRY
from prometheus_client import CollectorRegistry
from prometheus_client import multiprocess  # harmless if unused
from prometheus_client import start_http_server  # not used

app = FastAPI()


@app.get("/health")
def health():
    return {"ok": True, "service": "validator-fastapi"}


@app.get("/metrics")
def metrics():
    data = generate_latest(REGISTRY)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
