import logging

from celery import shared_task

from task_handler import crawl_handler
logger = logging.getLogger(__name__)

@shared_task
def crawl():
    crawl_handler()

