import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

celery_app = Celery(__name__,
                    broker = f'redis://{os.getenv('REDIS_HOST')}:6379/0',
                    include = ['src.dependencies.tasks'],
                    broker_connection_retry_on_startup = True)

