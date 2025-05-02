from fastapi import APIRouter
from loguru import logger
from time import time

from .cache import get_plan_cache

router = APIRouter()

@router.get("/plan")
async def query_plan(type_id: str = "GameTools"):
    logger.debug(f"type_id: {type_id}")

    if not type_id:
        logger.error(f"type_id is required")
        return {"ec": 400, "msg": "type_id is required"}

    data = {
        "home": [],
        "more": [],
    }

    for p in get_plan_cache():
        if not p.available:
            continue

        if p.type_id == type_id:
            data["home"].append(
                {
                    "title": p.title,
                    "price": p.price,
                    "original_price": p.original_price,
                    "popular": p.popular,
                    "plan_id": p.plan_id,
                }
            )
        else:
            data["more"].append(
                {
                    "title": p.title,
                    "price": p.price,
                    "original_price": p.original_price,
                    "popular": p.popular,
                    "plan_id": p.plan_id,
                }
            )

    if not data["home"]:
        data["home"], data["more"] = data["more"], data["home"]

    return {"ec": 200, "data": data}
