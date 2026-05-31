"""Application ports."""

from typing import Protocol

from rewards.domain.models import DinnerTransaction, Reward


class RewardRepository(Protocol):
    def save(self, reward: Reward) -> None:
        """Persists the calculated reward."""


class EventPublisher(Protocol):
    def publish_transaction(self, transaction: DinnerTransaction) -> None:
        """Publishes a dinner transaction event."""

    def close(self) -> None:
        """Releases messaging resources."""
