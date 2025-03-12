from logger import logger
from services.kafka_service import KafkaService
import os

CURRENCIES_KAFKA_TOPIC = os.getenv("CURRENCIES_KAFKA_TOPIC")

class TaskHandler:
    @classmethod
    async def notify_handler(cls):
        logger.info("Notify handler started")
        if KafkaService.has_running_consumer:
            raise Exception("Consumer is already running!")
        await KafkaService.consume_messages(CURRENCIES_KAFKA_TOPIC)
