from unittest.mock import patch

import pytest
from django.apps import apps
from django.utils import timezone

from crawler.tasks import crawl
from crawler.tests.test_models import create_models  # noqa: F401


@pytest.mark.django_db
@patch("crawler.task_handler.KafkaService.send_message")
def test_crawl_task(mock_send_message, create_models):  # noqa: F811
    before = timezone.now()
    crawl()
    valuable_record = apps.get_model("crawler", "ValuableRecord")

    filtered_records = valuable_record.active_objects.filter(date__gte=before)
    print(filtered_records)  # Debugging line

    assert filtered_records.exists()

    last_record = valuable_record.active_objects.get(date__gte=before)
    assert isinstance(last_record.value, float)

    # Assert that KafkaService.send_message was called
    mock_send_message.assert_called()
