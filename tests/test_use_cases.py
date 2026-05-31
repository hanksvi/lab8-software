from datetime import datetime, timezone
from decimal import Decimal
import unittest

from rewards.application.use_cases import ProcessDinnerTransaction
from rewards.domain import DinnerTransaction, RewardPolicy
from rewards.infrastructure.repositories import InMemoryRewardRepository


class ProcessDinnerTransactionTest(unittest.TestCase):
    def test_processes_and_persists_reward(self):
        repository = InMemoryRewardRepository()
        use_case = ProcessDinnerTransaction(RewardPolicy(), repository)
        transaction = DinnerTransaction.create(
            amount=Decimal("40.00"),
            card_number="4556737586899855",
            restaurant_code="REST-03",
            occurred_at=datetime(2026, 5, 16, tzinfo=timezone.utc),
        )

        reward = use_case.execute(transaction)

        self.assertEqual(60, reward.points)
        self.assertEqual([reward], repository.all())


if __name__ == "__main__":
    unittest.main()
