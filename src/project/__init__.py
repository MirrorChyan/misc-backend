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
    type_id: str
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


class UpdateProjectRequest(BaseModel):
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
            .order_by(Project.type_id, Project.proj_index),
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


@router.get("/project/list")
async def list_projects(type_id: str = ""):
    query = Project.select()
    if type_id:
        query = query.where(Project.type_id == type_id)
    query = query.order_by(Project.type_id, Project.proj_index)

    data = [
        {
            "type_id": p.type_id,
            "proj_index": p.proj_index,
            "rid": p.rid,
            "name": p.name,
            "desc": p.desc,
            "image": p.image,
            "url": p.url,
            "platform": p.platform,
            "download": p.download,
            "available": p.available,
        }
        for p in query
    ]

    return {"ec": 200, "data": data}


@router.post("/project/reorder")
async def reorder_project(req: ReorderRequest):
    type_id = req.type_id
    rid_list = req.rid_list

    if not type_id:
        return {"ec": 400, "msg": "type_id is required"}
    if not rid_list:
        return {"ec": 400, "msg": "rid_list is required"}
    if len(rid_list) != len(set(rid_list)):
        return {"ec": 400, "msg": "rid_list contains duplicates"}

    db_rids = {p.rid for p in Project.select(Project.rid).where(Project.type_id == type_id)}
    if set(rid_list) != db_rids:
        return {"ec": 400, "msg": "rid_list must exactly match all rids of this type_id"}

    with db.atomic():
        for idx, rid in enumerate(rid_list):
            Project.update(proj_index=idx).where(Project.rid == rid).execute()

    global project_cache
    project_cache = None

    return {"ec": 200, "msg": "ok"}


@router.post("/project/update")
async def update_project(req: UpdateProjectRequest):
    project = Project.get_or_none(Project.rid == req.rid)
    if project is None:
        logger.error(f"project not found: {req.rid}")
        return {"ec": 404, "msg": "project not found"}

    moved = req.type_id != project.type_id

    project.type_id = req.type_id
    project.name = req.name
    project.desc = req.desc
    project.image = req.image
    project.url = req.url
    project.platform = req.platform
    project.download = req.download
    project.available = req.available
    if moved:
        max_index = (
            Project.select(Project.proj_index)
            .where((Project.type_id == req.type_id) & (Project.rid != req.rid))
            .order_by(Project.proj_index.desc())
            .limit(1)
            .scalar()
        )
        project.proj_index = (max_index + 1) if max_index is not None else 0
    project.save()

    global project_cache
    project_cache = None

    return {"ec": 200, "msg": "ok"}


@router.post("/project/create")
async def create_project(req: CreateProjectRequest):
    if Project.get_or_none(Project.rid == req.rid) is not None:
        logger.error(f"rid already exists: {req.rid}")
        return {"ec": 400, "msg": "rid already exists"}

    with db.atomic():
        max_index = (
            Project.select(Project.proj_index)
            .where(Project.type_id == req.type_id)
            .order_by(Project.proj_index.desc())
            .limit(1)
            .scalar()
        )
        new_index = (max_index + 1) if max_index is not None else 0
        project = Project.create(
            type_id=req.type_id,
            proj_index=new_index,
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

    return {
        "ec": 200,
        "data": {
            "type_id": project.type_id,
            "proj_index": project.proj_index,
            "rid": project.rid,
            "name": project.name,
            "desc": project.desc,
            "image": project.image,
            "url": project.url,
            "platform": project.platform,
            "download": project.download,
            "available": project.available,
        },
    }
