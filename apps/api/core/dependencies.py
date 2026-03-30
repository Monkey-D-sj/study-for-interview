from langgraph.types import Checkpointer
from redis import Redis
from apps.api.db.redis_client import redis_client
from packages.infra.checkpointer import get_redis_checkpointer


def get_redis():
    return redis_client

class DbDependencies:
    def __init__(self):
        self.redis = None
        self.checkpointer = None

    def connect(self, redis: Redis):
        self.redis = redis
        self.checkpointer = get_redis_checkpointer(redis)
        self.checkpointer.setup()

    def get_checkpointer(self) -> Checkpointer:
        return self.checkpointer

db_dependencies = DbDependencies()
