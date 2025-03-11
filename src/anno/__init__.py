from datetime import datetime
from fastapi import APIRouter, Request
from loguru import logger

from src.database import Anno
from src.config import settings

router = APIRouter()


@router.get("/anno")
async def query_anno(lang: str):
    if not lang:
        logger.error(f"lang is required")
        return {"ec": 400, "msg": "lang is required"}

    now = datetime.now()
    anno = Anno.get_or_none(
        Anno.language == lang,
        Anno.start < now,
        Anno.end > now,
    )

    if not anno:
        logger.trace(f"Anno not found, {now}, {lang}")
        return {"ec": 404, "msg": "Not Found"}

    logger.info(f"Anno: {now}, {lang}, {anno.summary}")
    return {
        "ec": 200,
        "msg": "OK",
        "data": {
            "summary": anno.summary,
            "details": anno.details,
        },
    }
