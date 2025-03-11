from fastapi import FastAPI
from src.anno import router as anno_router

app = FastAPI()

app.include_router(anno_router)