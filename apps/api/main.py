from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.api.core.config import ApiConfig
from apps.api.db.redis_client import redis_client
from apps.api.modules.chat.controller import chat_router
from packages.infra.checkpointer import get_redis_checkpointer

redis_checkpointer = get_redis_checkpointer(redis_client.client)
@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client.connect(ApiConfig())
    yield
    redis_client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(chat_router)


