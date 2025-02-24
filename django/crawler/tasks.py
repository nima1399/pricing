import logging

from celery import shared_task

from crawler.task_handler import CrawlHandlerService

logger = logging.getLogger(__name__)


@shared_task
def crawl():
    logger.info("Crawl task started")
    CrawlHandlerService.crawl_handler()
