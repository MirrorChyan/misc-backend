from fastapi import APIRouter, Request
from loguru import logger
from time import time
import asyncio

from src.database import ContactUs

router = APIRouter()

CacheExpiration = 600  # 秒
cache = None
cache_lock = asyncio.Lock()


async def get_cache():
    global cache

    async with cache_lock:
        now = time()
        if not cache or (now - cache[1] > CacheExpiration):
            cache = (list(ContactUs.select()), now)
    return cache[0]


@router.get("/contact_us")
async def contact_us():
    data = {}
    for c in await get_cache():
        data[c.channel] = c.detail

    return {"ec": 200, "code": 0, "data": data}
