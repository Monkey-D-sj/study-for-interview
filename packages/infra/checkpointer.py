from langgraph.checkpoint.redis import RedisSaver
from redis import Redis

def get_redis_checkpointer(redis_client: Redis):
    return RedisSaver(redis_client=redis_client)
