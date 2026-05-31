"""Repository adapters."""

from rewards.domain.models import Reward


class InMemoryRewardRepository:
    def __init__(self) -> None:
        self._rewards: list[Reward] = []

    def save(self, reward: Reward) -> None:
        self._rewards.append(reward)

    def all(self) -> list[Reward]:
        return list(self._rewards)
