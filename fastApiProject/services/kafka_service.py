import json
from kafka import KafkaConsumer
from decouple import config
from logger import logger
from message_handler import MessageHandler

KAFKA_BROKER = config("KAFKA_BROKER")


class KafkaService:
    has_running_consumer = False

    @classmethod
    async def consume_messages(cls, currency_topic):
        if cls.has_running_consumer:
            raise Exception("Consumer is already running!")

        consumer = KafkaConsumer(
            currency_topic,
            bootstrap_servers=KAFKA_BROKER,
            key_deserializer=lambda k: k.decode("utf-8") if k else None,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="latest",
            enable_auto_commit=True,
            group_id="crypto_price_group",
        )

        consumer.poll(timeout_ms=1000)
        consumer.seek_to_end()

        logger.info("Kafka Consumer is running...")
        for message in consumer:
            logger.info(
                f"Received {message.key} | Timestamp: {message.value['timestamp']} | Price: {message.value['price']}"
            )
            MessageHandler.handle_message(message)
