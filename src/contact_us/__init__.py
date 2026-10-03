from fastapi import APIRouter
from loguru import logger
from pydantic import BaseModel
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


async def invalidate_cache():
    global cache

    async with cache_lock:
        cache = None


@router.get("/contact_us")
async def contact_us():
    data = {}
    for c in await get_cache():
        data[c.channel] = c.detail

    return {"ec": 200, "code": 0, "data": data}


class UpsertContactRequest(BaseModel):
    channel: str
    detail: str


class DeleteContactRequest(BaseModel):
    channel: str


@router.get("/contact_us/list")
async def list_contacts():
    data = [
        {"channel": c.channel, "detail": c.detail}
        for c in ContactUs.select().order_by(ContactUs.channel)
    ]
    return {"ec": 200, "data": data}


@router.post("/contact_us/update")
async def update_contact(req: UpsertContactRequest):
    """管理端：按 channel upsert，存在则更新 detail，不存在则新建。"""
    channel = req.channel.strip()
    if not channel:
        logger.error("channel is required")
        return {"ec": 400, "msg": "channel is required"}

    row = ContactUs.get_or_none(ContactUs.channel == channel)
    if row is None:
        row = ContactUs.create(channel=channel, detail=req.detail)
        logger.info(f"contact created: {channel}")
    else:
        row.detail = req.detail
        row.save()
        logger.info(f"contact updated: {channel}")

    await invalidate_cache()
    return {"ec": 200, "msg": "ok", "data": {"channel": channel, "detail": row.detail}}


@router.post("/contact_us/delete")
async def delete_contact(req: DeleteContactRequest):
    channel = req.channel.strip()
    row = ContactUs.get_or_none(ContactUs.channel == channel)
    if row is None:
        logger.error(f"channel not found: {channel}")
        return {"ec": 404, "msg": "channel not found"}

    row.delete_instance()
    logger.info(f"contact deleted: {channel}")
    await invalidate_cache()
    return {"ec": 200, "msg": "ok"}
