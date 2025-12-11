from redis import asyncio as aioredis
from loguru import logger
from src.config import settings
import asyncio


class RedisClient:
    def __init__(self):
        self.redis = None
        self.pubsub = None

    async def connect(self):
        try:
            redis_url = f"redis://:{settings.redis_password}@{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"
            if not settings.redis_password:
                redis_url = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"

            self.redis = aioredis.from_url(redis_url, decode_responses=True)
            logger.info(f"rds connect: {settings.redis_host}:{settings.redis_port}")
            return True
        except Exception as e:
            logger.error(f"rds connect: {e}")
            return False

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def publish(self, channel: str, message: str):
        if not self.redis:
            logger.warning("rds is None")
            return False

        try:
            await self.redis.publish(channel, message)
            logger.info(f"publish {channel}: {message}")
            return True
        except Exception as e:
            logger.error(f"publish error: {e}")
            return False

    async def subscribe(self, channel: str):
        if not self.redis:
            logger.warning("rds is None")
            return None

        try:
            self.pubsub = self.redis.pubsub()
            await self.pubsub.subscribe(channel)
            logger.info(f"subscribe: {channel}")
            return self.pubsub
        except Exception as e:
            logger.error(f"subscribe: {e}")
            return None


rds = RedisClient()


async def start_subscriber():
    from .subscriber import cache_clear_subscriber

    if not await rds.connect():
        logger.error("rds connect failed")
        return

    asyncio.create_task(cache_clear_subscriber())
