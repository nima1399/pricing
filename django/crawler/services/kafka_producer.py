import json
import logging
import os
import time

from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
CURRENCIES_KAFKA_TOPIC = os.getenv("CURRENCIES_KAFKA_TOPIC")


class KafkaService:
    @staticmethod
    def get_kafka_producer():
        return KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            key_serializer=lambda k: str(k).encode("utf-8"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    @classmethod
    def send_message(cls, currency, price):
        timestamp = int(time.time())
        logger.info(
            f"Kafka : Sending {currency} | timestamp: {timestamp} | Value: {price}"
        )

        producer = cls.get_kafka_producer()

        try:
            producer.send(
                topic=CURRENCIES_KAFKA_TOPIC,
                key=currency,
                value={"timestamp": timestamp, "price": price},
            )
        except Exception as e:
            logger.error(f"Kafka : Error in sending message: {e}")

        producer.flush()
        logger.info(
            f"Kafka : Sent {currency} | timestamp_ms: {timestamp} | Value: {price}"
        )
