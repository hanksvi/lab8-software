from datetime import datetime, timezone
from decimal import Decimal
import unittest

from rewards.common.events import RewardEventCodec, TransactionEventCodec
from rewards.domain import DinnerTransaction, Reward


class EventCodecTest(unittest.TestCase):
    def test_transaction_roundtrip(self):
        transaction = DinnerTransaction.create(
            amount=Decimal("80.75"),
            card_number="4556737586899855",
            restaurant_code="REST-02",
            occurred_at=datetime(2026, 5, 16, 20, 30, tzinfo=timezone.utc),
        )

        decoded = TransactionEventCodec.decode(TransactionEventCodec.encode(transaction))

        self.assertEqual(transaction, decoded)

    def test_reward_event_contains_result(self):
        reward = Reward(
            card_number="4556737586899855",
            points=120,
            cashback=Decimal("4.00"),
            restaurant_code="REST-02",
        )

        encoded = RewardEventCodec.encode(reward).decode("utf-8")

        self.assertIn('"points": 120', encoded)
        self.assertIn('"cashback": "4.00"', encoded)


if __name__ == "__main__":
    unittest.main()
