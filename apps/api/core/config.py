import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class ApiConfig(BaseModel):
    """
    API 配置
    """
    # REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))

