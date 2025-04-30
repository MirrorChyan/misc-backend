from fastapi import APIRouter
from loguru import logger
from time import time

from src.database import Plan

router = APIRouter()

CacheExpiration = 60  # 秒
plan_cache = None


@router.get("/plan")
async def query_anno(type_id: str = "GameTools"):
    logger.debug(f"type_id: {type_id}")

    if not type_id:
        logger.error(f"type_id is required")
        return {"ec": 400, "msg": "type_id is required"}

    now = time()
    global plan_cache
    if not plan_cache or (now - plan_cache[1] > CacheExpiration):
        plan_cache = (Plan.select().where(Plan.available == True).order_by(Plan.plan_index), now)

    data = {
        "home": [],
        "more": [],
    }

    for p in plan_cache[0]:
        if p.type_id == type_id:
            data["home"].append(
                {
                    "platform": p.platform,
                    "plan_id": p.plan_id,
                    "type_id": p.type_id,
                    "popular": p.popular,
                    "title": p.title,
                    "price": p.price,
                    "original_price": p.original_price,
                }
            )
        else:
            data["more"].append(
                {
                    "platform": p.platform,
                    "plan_id": p.plan_id,
                    "type_id": p.type_id,
                    "popular": p.popular,
                    "title": p.title,
                    "price": p.price,
                    "original_price": p.original_price,
                }
            )

    if not data["home"]:
        data["home"], data["more"] = data["more"], data["home"]

    return {"ec": 200, "data": data}
