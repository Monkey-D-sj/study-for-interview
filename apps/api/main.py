from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.api.core.config import ApiConfig
from apps.api.core.dependencies import db_dependencies
from apps.api.db.redis_client import redis_client
from apps.api.db.pg_client import pg_client
from apps.api.modules.chat.controller import chat_router
from apps.api.modules.pdf.controller import pdf_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = ApiConfig()

    # 连接 Redis
    redis_client.connect(config)
    db_dependencies.connect(redis_client.client)

    # 连接 PostgreSQL 并初始化表
    pg_client.connect(config.get_postgres_url())
    await pg_client.init_tables()

    yield

    # 关闭连接
    redis_client.close()
    await pg_client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(chat_router)
app.include_router(pdf_router)

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


