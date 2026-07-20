"""Build a review-only reconciliation plan from synthetic rows."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PaymentRow:
    external_ref: str
    amount: Decimal


@dataclass(frozen=True)
class Receivable:
    internal_ref: str
    external_ref: str
    outstanding: Decimal


def plan(
    payments: list[PaymentRow],
    receivables: list[Receivable],
) -> tuple[list[tuple[str, str, Decimal]], list[str]]:
    by_external: dict[str, list[Receivable]] = {}
    for item in receivables:
        by_external.setdefault(item.external_ref, []).append(item)

    matched: list[tuple[str, str, Decimal]] = []
    exceptions: list[str] = []
    for payment in payments:
        candidates = by_external.get(payment.external_ref, [])
        exact = [
            item for item in candidates if item.outstanding == payment.amount
        ]
        if len(exact) != 1:
            exceptions.append(payment.external_ref)
            continue
        matched.append(
            (payment.external_ref, exact[0].internal_ref, payment.amount)
        )
    return matched, exceptions
