from unittest.mock import PropertyMock

import pytest
from unittest import mock
from rest_framework.exceptions import ValidationError
import time
from task_handler import TaskHandler


@pytest.mark.asyncio
async def test_notify_handler():
    with (
        mock.patch("task_handler.DjangoService.get_currencies") as get_currencies,
        mock.patch("services.django_service.DjangoService.get_emails") as get_emails,
        mock.patch(
            "task_handler.KafkaService.has_running_consumer", new_callable=PropertyMock
        ) as has_running_consumer,
        mock.patch("services.kafka_service.KafkaConsumer") as KafkaConsumer,
        mock.patch("services.email_service.EmailManager.send_email") as send_email,
    ):
        get_currencies.return_value = ["btc_irt"]
        has_running_consumer.return_value = True
        with pytest.raises(ValidationError):
            await TaskHandler.notify_handler()

        has_running_consumer.return_value = False
        mock_messages = iter(
            [mock.MagicMock(topic="btc_irt", key=int(time.time()), value=1000000000)]
        )
        get_emails.return_value = ["test@gmail.com"]
        KafkaConsumer.return_value.__iter__.return_value = mock_messages

        await TaskHandler.notify_handler()
        send_email.assert_called()
        get_currencies.assert_called()
        has_running_consumer.assert_called()
