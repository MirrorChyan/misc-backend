from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config import settings

from src.anno import router as anno_router
from src.plan.summary import router as plan_router
from src.plan.details import router as plan_details_router
from src.health_check import router as health_check_router
from src.project import router as project_router
from src.ICP import router as icp_router

app = FastAPI()

if settings.static_app_dir:
    app.mount("/static", StaticFiles(directory=settings.static_app_dir), name="static")

app.include_router(anno_router)
app.include_router(plan_router)
app.include_router(plan_details_router)
app.include_router(health_check_router)
app.include_router(project_router)
app.include_router(icp_router)

