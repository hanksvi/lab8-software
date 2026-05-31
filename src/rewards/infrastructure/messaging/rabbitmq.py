"""RabbitMQ messaging adapter."""

from rewards.application.use_cases import ProcessDinnerTransaction
from rewards.common.config import RabbitConfig
from rewards.common.events import TransactionEventCodec
from rewards.domain.models import DinnerTransaction


class RabbitPublisher:
    def __init__(self, config: RabbitConfig):
        import pika

        credentials = pika.PlainCredentials(config.username, config.password)
        parameters = pika.ConnectionParameters(config.host, config.port, config.virtual_host, credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._queue_name = config.queue_name
        self._channel.queue_declare(queue=self._queue_name, durable=True)

    def publish_transaction(self, transaction: DinnerTransaction) -> None:
        self._channel.basic_publish(
            exchange="",
            routing_key=self._queue_name,
            body=TransactionEventCodec.encode(transaction),
        )

    def close(self) -> None:
        if self._connection.is_open:
            self._connection.close()


class RabbitConsumer:
    def __init__(self, config: RabbitConfig, use_case: ProcessDinnerTransaction):
        import pika

        credentials = pika.PlainCredentials(config.username, config.password)
        parameters = pika.ConnectionParameters(config.host, config.port, config.virtual_host, credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._queue_name = config.queue_name
        self._use_case = use_case
        self._channel.queue_declare(queue=self._queue_name, durable=True)

    def start(self) -> None:
        def on_message(channel, method, properties, body) -> None:
            transaction = TransactionEventCodec.decode(body)
            reward = self._use_case.execute(transaction)
            print(f"Reward processed: {reward.points} points, cashback S/{reward.cashback}")
            channel.basic_ack(delivery_tag=method.delivery_tag)

        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(queue=self._queue_name, on_message_callback=on_message)
        print(f'Waiting for RabbitMQ messages in queue "{self._queue_name}". Press CTRL+C to exit.')
        self._channel.start_consuming()

    def close(self) -> None:
        if self._connection.is_open:
            self._connection.close()
