"""Select synthetic scheduled-alert candidates after prerequisite checks."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Candidate:
    subject_ref: str
    event_at: datetime
    classification_confirmed: bool
    recipient_ref: str | None
    source_synced_at: datetime


def select_candidates(
    candidates: list[Candidate],
    not_before: datetime,
) -> list[Candidate]:
    return [
        item
        for item in candidates
        if item.classification_confirmed
        and item.recipient_ref
        and item.source_synced_at >= not_before
        and item.event_at >= not_before
    ]
