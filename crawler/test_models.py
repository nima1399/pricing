from django.apps import apps
import pytest
from django.utils import timezone


@pytest.fixture
def create_models():
    valuable_group_module = apps.get_model("crawler", "ValuableGroup")
    valuable_object_module = apps.get_model("crawler", "ValuableObject")
    crawl_source_module = apps.get_model("crawler", "CrawlSource")
    crawl_config_module = apps.get_model("crawler", "CrawlConfig")
    valuable_record_module = apps.get_model("crawler", "ValuableRecord")

    # Create instances of models
    valuable_group = valuable_group_module.objects.create(
        title="cryptocurrency", description="Description 1"
    )
    valuable_object = valuable_object_module.objects.create(
        title="btc_irt", description="bitcoin to Iranian toman", group=valuable_group
    )
    crawl_source = crawl_source_module.objects.create(
        title="Nobitex", base_url="https://nobitex.ir/", is_valid=True, type="token"
    )
    crawl_config = crawl_config_module.objects.create(
        crawl_source=crawl_source,
        valuable_object=valuable_object,
        helper_data={"https://api.nobitex.ir/v2/orderbook/BTCIRT": {}},
        priority=1,
    )
    valuable_record = valuable_record_module.objects.create(
        crawl_config=crawl_config, date=timezone.now(), value=100.0
    )

    return {
        "valuable_group": valuable_group,
        "valuable_object": valuable_object,
        "crawl_source": crawl_source,
        "crawl_config": crawl_config,
        "valuable_record": valuable_record,
    }


@pytest.mark.django_db
def test_valuable_group(create_models):
    valuable_group = create_models["valuable_group"]
    assert valuable_group.title == "cryptocurrency"
    assert valuable_group.description == "Description 1"
    assert str(valuable_group) == "cryptocurrency"


@pytest.mark.django_db
def test_valuable_object(create_models):
    valuable_object = create_models["valuable_object"]
    assert valuable_object.title == "btc_irt"
    assert valuable_object.description == "bitcoin to Iranian toman"
    assert valuable_object.group.title == "cryptocurrency"
    assert str(valuable_object) == "btc_irt"


@pytest.mark.django_db
def test_crawl_source(create_models):
    crawl_source = create_models["crawl_source"]
    assert crawl_source.title == "Nobitex"
    assert crawl_source.base_url == "https://nobitex.ir/"
    assert crawl_source.is_valid is True
    assert crawl_source.type == "token"
    assert str(crawl_source) == "Nobitex"


@pytest.mark.django_db
def test_crawl_config(create_models):
    crawl_config = create_models["crawl_config"]
    assert crawl_config.crawl_source.title == "Nobitex"
    assert crawl_config.valuable_object.title == "btc_irt"
    assert crawl_config.helper_data == {
        "https://api.nobitex.ir/v2/orderbook/BTCIRT": {}
    }
    assert crawl_config.priority == 1
    assert str(crawl_config) == "Nobitex - btc_irt"


@pytest.mark.django_db
def test_valuable_record(create_models):
    valuable_record = create_models["valuable_record"]
    assert valuable_record.crawl_config.crawl_source.title == "Nobitex"
    assert valuable_record.value == 100.0
    assert str(valuable_record) == "Nobitex - btc_irt"


@pytest.mark.django_db
def test_delete_base_module(create_models):
    valuable_group_module = apps.get_model("crawler", "ValuableGroup")
    valuable_object_module = apps.get_model("crawler", "ValuableObject")
    crawl_source_module = apps.get_model("crawler", "CrawlSource")
    crawl_config_module = apps.get_model("crawler", "CrawlConfig")
    valuable_record_module = apps.get_model("crawler", "ValuableRecord")

    valuable_group_module.objects.all().delete()
    valuable_object_module.objects.all().delete()
    crawl_source_module.objects.all().delete()
    crawl_config_module.objects.all().delete()
    valuable_record_module.objects.all().delete()

    assert valuable_group_module.objects.count() == 0
    assert valuable_object_module.objects.count() == 0
    assert crawl_source_module.objects.count() == 0
    assert crawl_config_module.objects.count() == 0
    assert valuable_record_module.objects.count() == 0
