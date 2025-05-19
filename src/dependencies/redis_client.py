import os
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

cache = Redis(host = os.getenv('REDIS_HOST'), port = os.getenv('REDIS_PORT'),
              decode_responses = True)
print(cache.ping())