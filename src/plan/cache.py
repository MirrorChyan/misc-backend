from time import time
from src.database import Plan
import asyncio

CacheExpiration = 600  # 秒
_plan_cache = None
cache_lock = asyncio.Lock()


async def get_plan_cache():
    global _plan_cache

    async with cache_lock:
        now = time()
        if not _plan_cache or (now - _plan_cache[1] > CacheExpiration):
            _plan_cache = (list(Plan.select().order_by(Plan.plan_index)), now)

    return _plan_cache[0]


async def clean_plan_cache():
    global _plan_cache

    async with cache_lock:
        _plan_cache = None
