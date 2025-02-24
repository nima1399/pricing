import pytest

from crawler.tasks import crawl
from crawler.tests.test_models import create_models  # noqa: F401
from django.utils import timezone
from django.apps import apps


@pytest.mark.django_db
def test_crawl_task(create_models):  # noqa: F811
    before = timezone.now()
    crawl()
    valuable_record = apps.get_model("crawler", "ValuableRecord")

    assert valuable_record.active_objects.filter(date__gte=before).exists()

    last_record = valuable_record.active_objects.get(date__gte=before)
    assert isinstance(last_record.value, float)
