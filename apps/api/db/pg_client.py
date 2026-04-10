from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Optional

Base = declarative_base()


class PGClient:
    """PostgreSQL 客户端"""

    def __init__(self):
        self.engine: Optional[create_async_engine] = None
        self.async_session: Optional[sessionmaker] = None

    def connect(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def init_tables(self):
        """初始化表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        """获取会话"""
        if not self.async_session:
            raise ValueError("未连接数据库")
        return self.async_session()

    async def close(self):
        """关闭连接"""
        if self.engine:
            await self.engine.dispose()


pg_client = PGClient()
