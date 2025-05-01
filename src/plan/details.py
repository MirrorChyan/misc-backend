from fastapi import APIRouter
from loguru import logger

from .cache import get_plan_cache

router = APIRouter()


@router.get("/plan/{plan_id}")
async def query_details(plan_id: str):
    logger.debug(f"plan_id: {plan_id}")

    if not plan_id:
        logger.error(f"plan_id is required")
        return {"ec": 400, "msg": "plan_id is required"}

    p = next((p for p in get_plan_cache() if p.plan_id == plan_id), None)
    if not plan_id:
        logger.error(f"plan_id not found")
        return {"ec": 404, "msg": "plan_id not found"}

    return {
        "ec": 200,
        "data": {
            "title": p.title,
            "price": p.price,
            "original_price": p.original_price,
            "popular": p.popular,
            "afdian_id": p.afdian_id,
            "yimapay_id": p.yimapay_id,
        },
    }
