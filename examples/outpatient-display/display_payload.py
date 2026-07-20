"""Build a minimal display payload for synthetic waiting-room data."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Notice:
    text: str
    starts_at: datetime
    ends_at: datetime


def build_payload(
    room_ref: str,
    delay_minutes: int,
    notice: Notice | None,
    recall_version: int,
    now: datetime,
) -> dict:
    if delay_minutes < 0 or delay_minutes > 600:
        raise ValueError("delay_minutes is out of range")
    active_notice = (
        notice.text
        if notice and notice.starts_at <= now <= notice.ends_at
        else ""
    )
    return {
        "roomRef": room_ref,
        "delayMinutes": delay_minutes,
        "notice": active_notice,
        "recallVersion": max(recall_version, 0),
    }
