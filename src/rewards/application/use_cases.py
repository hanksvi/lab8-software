"""Application use cases."""

from rewards.application.ports import RewardRepository
from rewards.domain.models import DinnerTransaction, Reward, RewardPolicy


class ProcessDinnerTransaction:
    def __init__(self, policy: RewardPolicy, repository: RewardRepository):
        self._policy = policy
        self._repository = repository

    def execute(self, transaction: DinnerTransaction) -> Reward:
        reward = self._policy.calculate(transaction)
        self._repository.save(reward)
        return reward
