"""Domain model and reward rules."""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN


@dataclass(frozen=True)
class DinnerTransaction:
    amount: Decimal
    card_number: str
    restaurant_code: str
    occurred_at: datetime

    @classmethod
    def create(
        cls,
        amount: Decimal,
        card_number: str,
        restaurant_code: str,
        occurred_at: datetime | None = None,
    ) -> "DinnerTransaction":
        if amount <= Decimal("0"):
            raise ValueError("amount must be greater than zero")
        if len(card_number.strip()) < 8:
            raise ValueError("card number must have at least 8 characters")
        if not restaurant_code.strip():
            raise ValueError("restaurant code is required")

        return cls(
            amount=amount,
            card_number=card_number.strip(),
            restaurant_code=restaurant_code.strip().upper(),
            occurred_at=occurred_at or datetime.now(timezone.utc),
        )


@dataclass(frozen=True)
class Reward:
    card_number: str
    points: int
    cashback: Decimal
    restaurant_code: str


class RewardPolicy:
    """Calculates rewards without depending on infrastructure."""

    def __init__(self, points_per_currency_unit: Decimal = Decimal("1.5"), cashback_rate: Decimal = Decimal("0.05")):
        self.points_per_currency_unit = points_per_currency_unit
        self.cashback_rate = cashback_rate

    def calculate(self, transaction: DinnerTransaction) -> Reward:
        points = int((transaction.amount * self.points_per_currency_unit).to_integral_value(rounding=ROUND_DOWN))
        cashback = (transaction.amount * self.cashback_rate).quantize(Decimal("0.01"))
        return Reward(
            card_number=transaction.card_number,
            points=points,
            cashback=cashback,
            restaurant_code=transaction.restaurant_code,
        )
