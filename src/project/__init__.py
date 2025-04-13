from fastapi import APIRouter
from loguru import logger
from time import time

from src.database import Project

router = APIRouter()

CacheExpiration = 60  # 秒
project_cache = None


@router.get("/project")
async def query_project(type_id: str = "GameTools"):
    logger.debug(f"type_id: {type_id}")

    if not type_id:
        logger.error(f"type_id is required")
        return {"ec": 400, "msg": "type_id is required"}

    now = time()
    global project_cache
    if not project_cache or (now - project_cache[1] > CacheExpiration):
        project_cache = (
            Project.select()
            .where(
                Project.available == True,
            )
            .order_by(Project.proj_index),
            now,
        )

    data = [
        {
            "type_id": p.type_id,
            "resource": p.rid,
            "name": p.name,
            "desc": p.desc,
            "image": p.image,
            "url": p.url,
            "support": [
                platform.strip() for platform in p.platform.split(",") if platform.strip()
            ],
        }
        for p in project_cache[0]
        if p.type_id == type_id
    ]

    return {"ec": 200, "data": data}
