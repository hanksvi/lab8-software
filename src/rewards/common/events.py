"""Event serialization for producer and consumer adapters."""

from datetime import datetime
from decimal import Decimal
import json

from rewards.domain.models import DinnerTransaction, Reward


class TransactionEventCodec:
    @staticmethod
    def encode(transaction: DinnerTransaction) -> bytes:
        payload = {
            "amount": str(transaction.amount),
            "card_number": transaction.card_number,
            "restaurant_code": transaction.restaurant_code,
            "occurred_at": transaction.occurred_at.isoformat(),
        }
        return json.dumps(payload, ensure_ascii=False).encode("utf-8")

    @staticmethod
    def decode(message: bytes | str) -> DinnerTransaction:
        raw_message = message.decode("utf-8") if isinstance(message, bytes) else message
        payload = json.loads(raw_message)
        return DinnerTransaction.create(
            amount=Decimal(payload["amount"]),
            card_number=payload["card_number"],
            restaurant_code=payload["restaurant_code"],
            occurred_at=datetime.fromisoformat(payload["occurred_at"]),
        )


class RewardEventCodec:
    @staticmethod
    def encode(reward: Reward) -> bytes:
        payload = {
            "card_number": reward.card_number,
            "points": reward.points,
            "cashback": str(reward.cashback),
            "restaurant_code": reward.restaurant_code,
        }
        return json.dumps(payload, ensure_ascii=False).encode("utf-8")
