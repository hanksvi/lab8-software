"""Command line entrypoint for messaging demos."""

import argparse

from rewards.common.config import KafkaConfig, RabbitConfig
from rewards.infrastructure.messaging.kafka import KafkaConsumer, KafkaPublisher
from rewards.infrastructure.messaging.rabbitmq import RabbitConsumer, RabbitPublisher
from rewards.services.factory import build_process_use_case, sample_transaction


def publish_to_rabbit() -> None:
    publisher = RabbitPublisher(RabbitConfig.from_env())
    try:
        transaction = sample_transaction()
        publisher.publish_transaction(transaction)
        print(f"Transaction sent to RabbitMQ: {transaction}")
    finally:
        publisher.close()


def consume_from_rabbit() -> None:
    consumer = RabbitConsumer(RabbitConfig.from_env(), build_process_use_case())
    try:
        consumer.start()
    finally:
        consumer.close()


def publish_to_kafka() -> None:
    publisher = KafkaPublisher(KafkaConfig.from_env())
    try:
        transaction = sample_transaction()
        publisher.publish_transaction(transaction)
        print(f"Transaction sent to Kafka: {transaction}")
    finally:
        publisher.close()


def consume_from_kafka() -> None:
    consumer = KafkaConsumer(KafkaConfig.from_env(), build_process_use_case())
    try:
        consumer.start()
    finally:
        consumer.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Rewards event processing")
    parser.add_argument(
        "command",
        choices=["rabbit-producer", "rabbit-consumer", "kafka-producer", "kafka-consumer"],
    )
    args = parser.parse_args()

    commands = {
        "rabbit-producer": publish_to_rabbit,
        "rabbit-consumer": consume_from_rabbit,
        "kafka-producer": publish_to_kafka,
        "kafka-consumer": consume_from_kafka,
    }
    commands[args.command]()


if __name__ == "__main__":
    main()
