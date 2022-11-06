import redis
from redis_lru import RedisLRU
from datetime import datetime
from timeit import timeit

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client, max_size=256)


@cache
def fibonacci(n):
    if n < 1:
        return 0
    if n == 1:
        return 1
    else:
        return (fibonacci(n - 1)) + fibonacci(n - 2)


script_start = datetime.now()
print('Результат 1:', fibonacci(200))
script_end = datetime.now()
print('час:', (script_end - script_start).total_seconds())


script_start = datetime.now()
print('Результат 2:', fibonacci(200))
script_end = datetime.now()
print('час:', (script_end - script_start).total_seconds())


