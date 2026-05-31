from datetime import datetime, timezone
from decimal import Decimal
import unittest

from rewards.domain import DinnerTransaction, RewardPolicy


class RewardPolicyTest(unittest.TestCase):
    def test_calculates_points_and_cashback(self):
        transaction = DinnerTransaction.create(
            amount=Decimal("100.00"),
            card_number="4556737586899855",
            restaurant_code="rest-01",
            occurred_at=datetime(2026, 5, 16, tzinfo=timezone.utc),
        )

        reward = RewardPolicy().calculate(transaction)

        self.assertEqual(150, reward.points)
        self.assertEqual(Decimal("5.00"), reward.cashback)
        self.assertEqual("REST-01", reward.restaurant_code)

    def test_rejects_invalid_amount(self):
        with self.assertRaises(ValueError):
            DinnerTransaction.create(
                amount=Decimal("0"),
                card_number="4556737586899855",
                restaurant_code="REST-01",
            )


if __name__ == "__main__":
    unittest.main()
