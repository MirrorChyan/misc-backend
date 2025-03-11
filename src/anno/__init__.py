from datetime import datetime
from fastapi import APIRouter, Request
from loguru import logger

from src.database import Anno
from src.config import settings

router = APIRouter()

@router.get("/anno")
async def query_anno():
    now = datetime.now()
    anno = Anno.get_or_none(
        Anno.start < now,
        Anno.end > now,
    )

    if not anno:
        logger.trace(f"Anno not found, {now}")
        return {"ec": 404, "msg": "Not Found"}

    logger.info(f"Anno: {now}, {anno.title}")
    return {
        "ec": 200,
        "data": {
            "title": anno.title,
            "detail": anno.detail,
        }
    }