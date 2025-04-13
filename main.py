from fastapi import FastAPI
from src.anno import router as anno_router
from src.plan import router as plan_router
from src.health_check import router as health_check_router
from src.project import router as project_router

app = FastAPI()

app.include_router(anno_router)
app.include_router(plan_router)
app.include_router(health_check_router)
app.include_router(project_router)

