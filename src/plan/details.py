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
    if not p:
        logger.error(f"plan_id not found")
        return {"ec": 404, "msg": "plan_id not found"}

    afdian_info = None
    if p.afdian_id:
        sp = [s.strip() for s in p.afdian_id.split(",")]
        if len(sp) != 2:
            logger.error(f"afdian_id is invalid")
            return {"ec": 500, "msg": "afdian_id is invalid"}

        afdian_info = {
            "plan_id": sp[0],
            "sku_id": sp[1],
        }

    return {
        "ec": 200,
        "data": {
            "title": p.title,
            "type_id": p.type_id,
            "price": p.price,
            "original_price": p.original_price,
            "checkout_price": p.checkout_price,
            "popular": p.popular,
            "afdian_info": afdian_info,
            "yimapay_id": p.yimapay_id,
            "weixin_id": p.weixin_id,
        },
    }
