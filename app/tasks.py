import time
from app import celery


@celery.task
def example(duration):
    time.sleep(duration)
    return 'Task Completed'

