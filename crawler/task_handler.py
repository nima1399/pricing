import logging
from abc import abstractmethod

from celery import shared_task
from django.utils.timezone import now
import requests

from .crawl_services import NobitexCrawlService
from core.manager import ActiveManager
from .models import ValuableObject, CrawlConfig, ValuableRecord

logger = logging.getLogger(__name__)


class CrawlHandlerService:

    @staticmethod
    def crawl_handler():
        valuable_active_objects = ValuableObject.active_objects.all()
        for valuable_object in valuable_active_objects:
            crawl_configs = CrawlHandlerService.get_active_crawl_configs(
                valuable_object
            )
            CrawlHandlerService.create_valuable_record(crawl_configs)

    @staticmethod
    def get_active_crawl_configs(valuable_object):
        return (
            CrawlConfig.active_objects.filter(valuable_object=valuable_object)
            .filter(crawl_source__is_valid=True)
            .order_by("priority")
        )

    @staticmethod
    def create_valuable_record(crawl_configs):
        for crawl_config in crawl_configs:
            try:
                value = CrawlHandlerService.get_value(crawl_config.id)
                logger.info("Got value")

                ValuableRecord.active_objects.create(
                    crawl_config=crawl_config, date=now(), value=value
                ).save()
                logger.info("Created ValuableRecord")
                break
            except Exception as e:
                logger.error(f"Error in crawl task: {e}")
                crawl_config.increase_priority()
                crawl_config.save()

    @staticmethod
    def get_value(crawl_config_id):
        try:
            crawl_config = CrawlConfig.active_objects.get(id=crawl_config_id)
            if crawl_config.crawl_source.title == "Nobitex":
                return NobitexCrawlService(crawl_config).fetch()
        except Exception as e:
            logger.error(f"Error in get_value: {e}")
            raise e
