import os
from dotenv import load_dotenv
import redis
load_dotenv()

class RedisClient():
    _client = None
    @classmethod
    #连接redis
    def get_redis_conn(cls) -> redis.Redis:
        if cls._client is None:
            cls._client = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=int(os.getenv("REDIS_PORT")),
                db=int(os.getenv("REDIS_DB")),
                decode_responses=True,
                max_connections=50, #限制池大小
            )
        return cls._client