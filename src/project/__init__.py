from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel
from time import time

from src.config import settings
from src.database import Project, db

router = APIRouter()

CacheExpiration = 60  # 秒
project_cache = None


class ReorderRequest(BaseModel):
    rid_list: list[str]


class CreateProjectRequest(BaseModel):
    rid: str
    name: str
    desc: str
    image: str = ""
    url: str
    platform: str
    type_id: str = "GameTools"
    download: bool = True
    available: bool = True


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
            "download": p.download,
        }
        for p in sorted(project_cache[0], key=lambda p: p.type_id != type_id)
    ]

    return {"ec": 200, "data": data}


@router.post("/project/reorder")
async def reorder_project(req: ReorderRequest):
    all_projects = list(Project.select())
    db_rids = {p.rid for p in all_projects}

    ordered_rids = [rid for rid in req.rid_list if rid in db_rids]
    remaining_rids = [p.rid for p in sorted(all_projects, key=lambda p: p.proj_index) if p.rid not in set(ordered_rids)]
    final_order = ordered_rids + remaining_rids

    with db.atomic():
        for idx, rid in enumerate(final_order):
            Project.update(proj_index=idx).where(Project.rid == rid).execute()

    global project_cache
    project_cache = None

    return {"ec": 200, "msg": "ok"}


@router.post("/project/create")
async def create_project(req: CreateProjectRequest):
    max_index = Project.select(Project.proj_index).order_by(Project.proj_index.desc()).limit(1).scalar() or 0

    Project.create(
        type_id=req.type_id,
        proj_index=max_index + 1,
        rid=req.rid,
        name=req.name,
        desc=req.desc,
        image=req.image,
        url=req.url,
        platform=req.platform,
        download=req.download,
        available=req.available,
    )

    global project_cache
    project_cache = None

    return {"ec": 200, "msg": "ok"}
