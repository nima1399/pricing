from django.apps import apps
import pytest
from crawler.crawl_services import NobitexCrawlService


@pytest.fixture
def create_config():
    valuable_group_module = apps.get_model("crawler", "ValuableGroup")
    valuable_object_module = apps.get_model("crawler", "ValuableObject")
    crawl_source_module = apps.get_model("crawler", "CrawlSource")
    crawl_config_module = apps.get_model("crawler", "CrawlConfig")

    valuable_group = valuable_group_module.objects.create(
        title="Group 1", description="Description 1"
    )
    valuable_object = valuable_object_module.objects.create(
        title="Object 1", description="Description 1", group=valuable_group
    )
    crawl_source = crawl_source_module.objects.create(
        title="Source 1", base_url="https://nobitex.ir/", is_valid=True, type="token"
    )
    crawl_config = crawl_config_module.objects.create(
        crawl_source=crawl_source,
        valuable_object=valuable_object,
        helper_data={"https://api.nobitex.ir/v2/orderbook/BTCIRT": {}},
        priority=1,
    )

    return crawl_config


@pytest.mark.django_db
def test_nobitex_crawl_service(create_config):
    crawl_config = create_config
    nobitex_crawl_service = NobitexCrawlService(crawl_config)
    price = nobitex_crawl_service.fetch()
    assert isinstance(price, float)
