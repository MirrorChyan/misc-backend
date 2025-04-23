from datetime import datetime
from fastapi import APIRouter, Request
from loguru import logger

from src.config import settings

router = APIRouter()


@router.get("/icp")
async def query_icp(lang: str):
    return {
        "icp_beian": settings.icp_beian,
        "icp_url": settings.icp_url,
    }
