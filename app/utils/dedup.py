import os
from dotenv import load_dotenv
from upstash_redis import Redis

load_dotenv()

redis = Redis(
    url=os.getenv("UPSTASH_REDIS_URL"),
    token=os.getenv("UPSTASH_REDIS_TOKEN")
)

SEEN_TTL_SECONDS = 60 * 60 * 24 * 7

def is_seen(url: str) -> bool:
    return redis.exists(f"seen:{url}") == 1

def mark_seen(url: str):
    redis.setex(f"seen:{url}", SEEN_TTL_SECONDS, "1")
