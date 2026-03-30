from redis import from_url

from apps.api.core.config import ApiConfig
from packages.infra.checkpointer import get_redis_checkpointer


class RedisClient:
	def __init__(self):
		self.client = None
		self.checkpointer = None

	def connect(self, config: ApiConfig):
		self.client = from_url(
			f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}",
			encoding="utf-8",
			decode_responses=True,  # 自动解码为字符串
			max_connections=20,  # 连接池大小
			socket_timeout=5,  # 超时时间
		)
		print("Redis connected")

	def close(self):
		self.client.close()
		print("Redis closed")

	def init_checkpointer(self):
		if self.checkpointer is None:
			self.checkpointer = get_redis_checkpointer(self.client)

redis_client = RedisClient()
