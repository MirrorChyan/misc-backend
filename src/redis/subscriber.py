from loguru import logger

from src.contact_us import clean_contact_cache
from src.plan.cache import clean_plan_cache
from src.redis.client import rds

channel = "misc"


async def cache_clear_subscriber():
    try:
        pubsub = await rds.subscribe(channel)
        if not pubsub:
            logger.error("pubsub is None")
            return

        logger.info("start subscribe misc cache listener")

        async for message in pubsub.listen():
            if message["type"] == "message":
                logger.info("evict message received: {}".format(message))
                await clean_plan_cache()
                await clean_contact_cache()

    except Exception as e:
        logger.error(f"subscribe with error: {e}")
    finally:
        if rds.pubsub:
            await rds.pubsub.unsubscribe(channel)
            logger.info(f"unsubscribe: {channel}")
