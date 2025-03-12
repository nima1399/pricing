import logging

from django.db.models import QuerySet
from django.utils.timezone import now

from crawler.crawl_services import NobitexCrawlService
from crawler.models import CrawlConfig, ValuableObject, ValuableRecord
from crawler.services.kafka_producer import KafkaService

logger = logging.getLogger(__name__)


class CrawlHandlerService:
    @staticmethod
    def crawl_handler() -> None:
        valuable_active_objects = ValuableObject.active_objects.all()
        for valuable_object in valuable_active_objects:
            crawl_configs = CrawlHandlerService.get_active_crawl_configs(
                valuable_object
            )
            value = CrawlHandlerService.create_valuable_record(crawl_configs)
            KafkaService.send_message(valuable_object.title, value)

    @staticmethod
    def get_active_crawl_configs(
        valuable_object: ValuableObject,
    ) -> QuerySet[CrawlConfig]:
        return (
            CrawlConfig.active_objects.filter(valuable_object=valuable_object)
            .filter(crawl_source__is_valid=True)
            .order_by("priority")
            .reverse()
        )

    @staticmethod
    def create_valuable_record(crawl_configs: QuerySet[CrawlConfig]):
        for crawl_config in crawl_configs:
            try:
                value = CrawlHandlerService.get_value(crawl_config.id)
            except Exception as e:
                logger.error(f"Error in crawl task: {e}")
                crawl_config.decrease_priority()
                crawl_config.save()
                continue

            logger.info("Got value")
            ValuableRecord.active_objects.create(
                crawl_config=crawl_config, date=now(), value=value
            ).save()
            logger.info("Created ValuableRecord")
            return value

    @staticmethod
    def get_value(crawl_config_id):
        try:
            crawl_config = CrawlConfig.active_objects.get(id=crawl_config_id)
            if crawl_config.crawl_source.title == "Nobitex":
                return NobitexCrawlService(crawl_config).fetch()
        except Exception as e:
            logger.error(f"Error in get_value: {e}")
            raise e
