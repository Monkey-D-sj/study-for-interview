from apps.api.db.redis_client import redis_client


def get_redis():
    return redis_client

