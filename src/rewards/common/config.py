"""Application configuration."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class RabbitConfig:
    host: str = "213.199.42.57"
    port: int = 5672
    username: str = "students"
    password: str = ""
    virtual_host: str = "/"
    queue_name: str = "laboratorio_1"

    @classmethod
    def from_env(cls) -> "RabbitConfig":
        password = os.getenv("RABBIT_PASSWORD", cls.password)
        if not password:
            raise ValueError("RABBIT_PASSWORD environment variable is required")

        return cls(
            host=os.getenv("RABBIT_HOST", cls.host),
            port=int(os.getenv("RABBIT_PORT", str(cls.port))),
            username=os.getenv("RABBIT_USER", cls.username),
            password=password,
            virtual_host=os.getenv("RABBIT_VHOST", cls.virtual_host),
            queue_name=os.getenv("RABBIT_QUEUE", cls.queue_name),
        )


@dataclass(frozen=True)
class KafkaConfig:
    bootstrap_servers: str = "213.199.42.57:9092"
    topic: str = "laboratorio_1"
    consumer_group: str = "grupo_estudiantes_1"

    @classmethod
    def from_env(cls) -> "KafkaConfig":
        return cls(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", cls.bootstrap_servers),
            topic=os.getenv("KAFKA_TOPIC", cls.topic),
            consumer_group=os.getenv("KAFKA_CONSUMER_GROUP", cls.consumer_group),
        )
