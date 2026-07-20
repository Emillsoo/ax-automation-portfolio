"""Reconcile synthetic notification requests with delivery receipts."""

from dataclasses import dataclass
from enum import Enum


class DeliveryState(str, Enum):
    DELIVERED = "delivered"
    FAILED = "failed"
    PENDING = "pending"
    MISSING = "missing"


@dataclass(frozen=True)
class Request:
    request_ref: str
    recipient_ref: str


@dataclass(frozen=True)
class Receipt:
    request_ref: str
    delivered: bool
    final: bool


def reconcile(
    requests: list[Request],
    receipts: list[Receipt],
) -> dict[str, DeliveryState]:
    receipt_by_ref = {item.request_ref: item for item in receipts}
    if len(receipt_by_ref) != len(receipts):
        raise ValueError("duplicate receipt reference")

    result: dict[str, DeliveryState] = {}
    for request in requests:
        receipt = receipt_by_ref.get(request.request_ref)
        if receipt is None:
            result[request.request_ref] = DeliveryState.MISSING
        elif not receipt.final:
            result[request.request_ref] = DeliveryState.PENDING
        elif receipt.delivered:
            result[request.request_ref] = DeliveryState.DELIVERED
        else:
            result[request.request_ref] = DeliveryState.FAILED
    return result
