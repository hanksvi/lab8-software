"""Command helpers for the demo scripts."""

from datetime import datetime, timezone
from decimal import Decimal

from rewards.application.use_cases import ProcessDinnerTransaction
from rewards.domain.models import DinnerTransaction, RewardPolicy
from rewards.infrastructure.repositories import InMemoryRewardRepository


def sample_transaction() -> DinnerTransaction:
    return DinnerTransaction.create(
        amount=Decimal("120.50"),
        card_number="4556737586899855",
        restaurant_code="REST-UTEC-01",
        occurred_at=datetime.now(timezone.utc),
    )


def build_process_use_case() -> ProcessDinnerTransaction:
    return ProcessDinnerTransaction(RewardPolicy(), InMemoryRewardRepository())
