from fastapi import Request, APIRouter
from aiohttp import ClientSession
from loguru import logger

from src.config import settings

router = APIRouter()

@router.post("/notify_admin")
async def notify_admin(request: Request):
    body = await request.json()
    logger.info(str(body))

    try:
        async with ClientSession() as session:
            async with session.post(
                settings.notify_admin_url, json=body
            ) as response:
                pass
    except Exception as e:
        logger.error(f"notify_admin error: {e}, body: f{body}")
