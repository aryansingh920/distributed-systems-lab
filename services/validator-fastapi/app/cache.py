import os
import json
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
KEY_LAST2 = "orders:last2"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def cache_last2(event: dict):
    # store JSON string
    r.lpush(KEY_LAST2, json.dumps(event))
    # keep only 2 most recent
    r.ltrim(KEY_LAST2, 0, 1)
