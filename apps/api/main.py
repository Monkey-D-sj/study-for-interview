from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.api.core.config import ApiConfig
from apps.api.core.dependencies import db_dependencies
from apps.api.db.redis_client import redis_client
from apps.api.modules.chat.controller import chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client.connect(ApiConfig())
    db_dependencies.connect(redis_client.client)
    yield
    redis_client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Interview API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "interview-api"}


