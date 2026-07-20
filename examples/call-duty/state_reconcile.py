"""Synthetic call-forwarding state reconciliation.

The adapter is injected. No real telephony URL, account, or number is used.
"""

from dataclasses import dataclass
from typing import Protocol


class ForwardingAdapter(Protocol):
    def read_destination(self, line_ref: str) -> str | None: ...
    def change_destination(self, line_ref: str, destination: str) -> None: ...


@dataclass(frozen=True)
class ReconcileResult:
    line_ref: str
    before: str | None
    after: str | None
    changed: bool
    verified: bool


def reconcile(
    adapter: ForwardingAdapter,
    line_ref: str,
    expected_destination: str,
) -> ReconcileResult:
    if not line_ref.strip() or not expected_destination.strip():
        raise ValueError("line_ref and destination are required")

    before = adapter.read_destination(line_ref)
    changed = before != expected_destination
    if changed:
        adapter.change_destination(line_ref, expected_destination)

    after = adapter.read_destination(line_ref)
    return ReconcileResult(
        line_ref=line_ref,
        before=before,
        after=after,
        changed=changed,
        verified=after == expected_destination,
    )
