from pydantic import BaseModel


class ApiConfig(BaseModel):
    """
    API 配置
    """
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

