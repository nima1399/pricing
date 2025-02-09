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
        title="Group 1", description="Description 1"
    )
    valuable_object = valuable_object_module.objects.create(
        title="Object 1", description="Description 1", group=valuable_group
    )
    crawl_source = crawl_source_module.objects.create(
        title="Source 1", base_url="http://example.com", is_valid=True, type="ws"
    )
    crawl_config = crawl_config_module.objects.create(
        crawl_source=crawl_source,
        valuable_object=valuable_object,
        helper_data={"http://example.com": "data"},
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
    assert valuable_group.title == "Group 1"
    assert valuable_group.description == "Description 1"


@pytest.mark.django_db
def test_valuable_object(create_models):
    valuable_object = create_models["valuable_object"]
    assert valuable_object.title == "Object 1"
    assert valuable_object.description == "Description 1"
    assert valuable_object.group.title == "Group 1"


@pytest.mark.django_db
def test_crawl_source(create_models):
    crawl_source = create_models["crawl_source"]
    assert crawl_source.title == "Source 1"
    assert crawl_source.base_url == "http://example.com"
    assert crawl_source.is_valid is True
    assert crawl_source.type == "ws"


@pytest.mark.django_db
def test_crawl_config(create_models):
    crawl_config = create_models["crawl_config"]
    assert crawl_config.crawl_source.title == "Source 1"
    assert crawl_config.valuable_object.title == "Object 1"
    assert crawl_config.helper_data == {"http://example.com": "data"}
    assert crawl_config.priority == 1


@pytest.mark.django_db
def test_valuable_record(create_models):
    valuable_record = create_models["valuable_record"]
    assert valuable_record.crawl_config.crawl_source.title == "Source 1"
    assert valuable_record.value == 100.0
