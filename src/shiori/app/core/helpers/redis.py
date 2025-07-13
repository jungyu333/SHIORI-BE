from redis import asyncio as redis

from shiori.app.core import get_settings

config = get_settings()


redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)
