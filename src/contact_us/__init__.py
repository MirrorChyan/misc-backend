from fastapi import APIRouter, Request
from loguru import logger
from time import time

from src.database import ContactUs

router = APIRouter()

CacheExpiration = 600  # 秒
cache = None

def get_cache():
    now = time()
    
    global cache
    if not cache or (now - cache[1] > CacheExpiration):
        cache = (list(ContactUs.select()), now)

    return cache[0]

@router.get("/contact_us")
async def contact_us():
    data = {}
    for c in get_cache():
        data[c.channel] = c.detail

    return {
        "ec": 200,
        "code": 0,
        "data": data
    }