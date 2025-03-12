import pytest

from crawler.crawl_services import NobitexCrawlService
from crawler.task_handler import CrawlHandlerService
from crawler.tests.test_models import create_models  # noqa: F401


@pytest.mark.django_db
def test_nobitex_crawl_service(create_models):  # noqa: F811
    crawl_config = create_models["crawl_config"]
    nobitex_crawl_service = NobitexCrawlService(crawl_config)
    price = nobitex_crawl_service.fetch()
    assert isinstance(price, float)

    crawl_config.helper_data = {}
    crawl_config.save()


@pytest.mark.django_db
def test_get_value_exception(create_models):  # noqa: F811
    crawl_config = create_models["crawl_config"]
    crawl_config.helper_data = {}
    nobitex_crawl_service = NobitexCrawlService(crawl_config)
    with pytest.raises(Exception):
        nobitex_crawl_service.fetch()


@pytest.mark.django_db
def test_create_valuable_record_exception(create_models):  # noqa: F811
    crawl_config = create_models["crawl_config"]
    crawl_config.helper_data = {}
    crawl_config.save()
    priority = crawl_config.priority
    CrawlHandlerService.create_valuable_record([crawl_config])
    assert crawl_config.priority == priority - 1
