"""Fail-safe planning for a synthetic payment batch.

No real account, billing code, amount, or production API is represented.
The function creates a plan only; it does not perform a write.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Candidate:
    record_id: str
    category: str
    outstanding: Decimal
    requested: Decimal
    already_processed: bool


@dataclass(frozen=True)
class PaymentPlan:
    record_ids: tuple[str, ...]
    total: Decimal
    dry_run: bool = True


ALLOWED_CATEGORY = "demo-receivable"


def build_safe_plan(server_rows: list[Candidate]) -> PaymentPlan:
    """Apply a second filter and abort the whole batch on any unsafe row."""

    second_filter = [
        row
        for row in server_rows
        if row.category == ALLOWED_CATEGORY and not row.already_processed
    ]

    if len(second_filter) != len(server_rows):
        raise ValueError("double-filter mismatch: abort entire batch")

    unsafe_amounts = [
        row.record_id
        for row in second_filter
        if row.outstanding <= 0 or row.requested != row.outstanding
    ]
    if unsafe_amounts:
        raise ValueError("partial or invalid amount: abort entire batch")

    unique_ids = tuple(dict.fromkeys(row.record_id for row in second_filter))
    if len(unique_ids) != len(second_filter):
        raise ValueError("duplicate record_id: abort entire batch")

    return PaymentPlan(
        record_ids=unique_ids,
        total=sum((row.requested for row in second_filter), Decimal("0")),
        dry_run=True,
    )

