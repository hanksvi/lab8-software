"""Kafka messaging adapter."""

from rewards.application.use_cases import ProcessDinnerTransaction
from rewards.common.config import KafkaConfig
from rewards.common.events import TransactionEventCodec
from rewards.domain.models import DinnerTransaction


class KafkaPublisher:
    def __init__(self, config: KafkaConfig):
        from confluent_kafka import Producer

        self._producer = Producer({"bootstrap.servers": config.bootstrap_servers})
        self._topic = config.topic

    def publish_transaction(self, transaction: DinnerTransaction) -> None:
        self._producer.produce(self._topic, value=TransactionEventCodec.encode(transaction))
        self._producer.flush()

    def close(self) -> None:
        self._producer.flush()


class KafkaConsumer:
    def __init__(self, config: KafkaConfig, use_case: ProcessDinnerTransaction):
        from confluent_kafka import Consumer

        self._consumer = Consumer(
            {
                "bootstrap.servers": config.bootstrap_servers,
                "group.id": config.consumer_group,
                "auto.offset.reset": "earliest",
            }
        )
        self._topic = config.topic
        self._use_case = use_case

    def start(self) -> None:
        self._consumer.subscribe([self._topic])
        print(f'Waiting for Kafka messages in topic "{self._topic}". Press CTRL+C to exit.')
        while True:
            message = self._consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                print(f"Kafka error: {message.error()}")
                continue

            transaction = TransactionEventCodec.decode(message.value())
            reward = self._use_case.execute(transaction)
            print(f"Reward processed: {reward.points} points, cashback S/{reward.cashback}")

    def close(self) -> None:
        self._consumer.close()
