import redis
import os


class RedisManager:

    __client = None
    __host_name = os.environ.get('REDIS_HOST')
    __port = os.environ.get('REDIS_PORT')
    __password = os.environ.get('REDIS_PASSWORD')

    def __new__(cls):
        if cls.__client is None:
            cls.__client = redis.StrictRedis(
                host=cls.__host_name, port=cls.__port, password=cls.__password)
        return super().__new__(cls)

    def __init__(self):
        self.redis = self.__client

    def set(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        return self.redis.get(key)

    def delete(self, key):
        self.redis.delete(key)

    def exists(self, key):
        return self.redis.exists(key)

    def keys(self, pattern):
        return self.redis.keys(pattern)

    def flushdb(self):
        self.redis.flushdb()

    def flushall(self):
        self.redis.flushall()
