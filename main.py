from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from src.config import settings
from src.redis import start_subscriber, rds

from src.anno import router as anno_router
from src.plan.summary import router as plan_router
from src.plan.details import router as plan_details_router
from src.health_check import router as health_check_router
from src.project import router as project_router
from src.icp import router as icp_router
from src.notify_admin import router as notify_admin_router
from src.contact_us import router as contact_us_router


@asynccontextmanager
async def lifespan(a: FastAPI):
    await start_subscriber()
    yield
    await rds.close()


app = FastAPI(lifespan=lifespan)

if settings.static_app_dir:
    app.mount("/static", StaticFiles(directory=settings.static_app_dir), name="static")

app.include_router(anno_router)
app.include_router(plan_router)
app.include_router(plan_details_router)
app.include_router(health_check_router)
app.include_router(project_router)
app.include_router(icp_router)
app.include_router(notify_admin_router)
app.include_router(contact_us_router)
