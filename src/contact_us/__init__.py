from fastapi import APIRouter
from time import time
import asyncio

from src.database import ContactUs

router = APIRouter()

CacheExpiration = 600
cache = None
cache_lock = asyncio.Lock()


async def get_contact_cache():
    global cache

    async with cache_lock:
        now = time()
        if not cache or (now - cache[1] > CacheExpiration):
            cache = (list(ContactUs.select()), now)
    return cache[0]


async def clean_contact_cache():
    global cache
    async with cache_lock:
        cache = None


@router.get("/contact_us")
async def contact_us():
    data = {}
    for c in await get_contact_cache():
        data[c.channel] = c.detail

    return {"ec": 200, "code": 0, "data": data}
