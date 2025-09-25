from fastapi import Request, APIRouter, HTTPException
from aiohttp import ClientSession
from loguru import logger

from src.config import settings

router = APIRouter()

@router.post("/notify_admin")
async def notify_admin(request: Request):
    try:
        body = await request.json()
    except Exception as e:
        logger.error(f"notify_admin invalid json: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")

    logger.info(str(body))

    if not settings.notify_admin_url:
        logger.warning("no notify_admin_url, ignore")
        return

    try:
        async with ClientSession() as session:
            async with session.post(
                settings.notify_admin_url, json=body
            ) as response:
                if response.status < 200 or response.status >= 300:
                    logger.warning(f"notify_admin failed with status {response.status}, body: {body}")
    except Exception as e:
        logger.error(f"notify_admin error: {e}, body: {body}")
