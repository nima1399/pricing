from aiokafka import AIOKafkaConsumer
import asyncio
from decouple import config

TOPIC = config("TOPIC")
GROUP_ID = config("GROUP_ID")
BOOTSTRAP_SERVERS = "localhost:9092"


class KafkaService:
    @classmethod
    async def consume(cls):
        while True:
            consumer = AIOKafkaConsumer(
                TOPIC,
                bootstrap_servers=BOOTSTRAP_SERVERS,
                group_id=GROUP_ID,
                enable_auto_commit=True
            )

            await consumer.start()
            try:
                async for msg in consumer:
                    print(f"Received message: {msg.value.decode()}")
            except Exception as e:
                print(f"Error in consumer: {e}, restarting...")
            finally:
                await consumer.stop()
                await asyncio.sleep(5)  # Small delay before restarting


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(KafkaService.consume())