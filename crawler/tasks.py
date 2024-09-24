import logging

from celery import shared_task
from django.utils.timezone import now
import requests

from .crawl_services import NobitexCrawlService
from .models import ValuableObject, CrawlConfig, ValuableRecord

logger = logging.getLogger(__name__)

@shared_task
def crawl():
    valuable_objects = ValuableObject.objects.all()
    for valuable_object in valuable_objects:
        crawl_configs = CrawlConfig.objects.filter(valuable_object=valuable_object).filter(crawl_source__is_valid=True).order_by('priority')
        for crawl_config in crawl_configs:
            try:
                value = get_value(crawl_config.id)
                logger.info("Got value")

                ValuableRecord.objects.create(crawl_config=crawl_config, date=now(), value=value)
                logger.info("Created ValuableRecord")
                break
            except Exception as e:
                logger.error(f"Error in crawl task: {e}")
                crawl_config.priority += 1
                crawl_config.save()

@shared_task
def get_value(crawl_config_id):
    try:
        crawl_config = CrawlConfig.objects.get(id=crawl_config_id)
        if crawl_config.crawl_source.title == "Nobitex":
            return NobitexCrawlService.fetch(crawl_config_id)
    except Exception as e:
        logger.error(f"Error in get_value: {e}")
        raise