import os
import urllib.parse

from dotenv import load_dotenv
from celery import Celery

load_dotenv()

REDIS_PASSWORD = urllib.parse.quote(os.environ.get("REDIS_PASSWORD", ""))

celery_app = Celery(
    "tasks",
    broker=f"redis://:{REDIS_PASSWORD}@redis:6379/0",
    backend=f"redis://:{REDIS_PASSWORD}@redis:6379/0",
)
celery_app.conf.task_track_started = True
# celery_app.conf.worker_redirect_stdouts = False
