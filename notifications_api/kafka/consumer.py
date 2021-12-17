from functools import lru_cache

from kafka import KafkaConsumer


@lru_cache()
def get_kafka_consumer() -> KafkaConsumer:
    return KafkaConsumer(bootstrap_servers="localhost:9093")
