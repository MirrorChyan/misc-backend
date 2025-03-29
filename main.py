from fastapi import FastAPI
from src.anno import router as anno_router
from src.plan import router as plan_router

app = FastAPI()

app.include_router(anno_router)
app.include_router(plan_router)
