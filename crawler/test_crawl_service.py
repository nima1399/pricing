import pytest
from crawler.crawl_services import NobitexCrawlService
from crawler.test_models import create_models  # noqa: F401


@pytest.mark.django_db
def test_nobitex_crawl_service(create_models):  # noqa: F811
    crawl_config = create_models["crawl_config"]
    nobitex_crawl_service = NobitexCrawlService(crawl_config)
    price = nobitex_crawl_service.fetch()
    assert isinstance(price, float)
