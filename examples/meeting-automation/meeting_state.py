"""Finite-state workflow for a synthetic meeting."""

from dataclasses import dataclass
from enum import Enum


class MeetingState(str, Enum):
    READY = "ready"
    RUNNING = "running"
    ENDED = "ended"
    SUMMARIZED = "summarized"


ALLOWED_TRANSITIONS = {
    MeetingState.READY: {MeetingState.RUNNING},
    MeetingState.RUNNING: {MeetingState.ENDED},
    MeetingState.ENDED: {MeetingState.SUMMARIZED},
    MeetingState.SUMMARIZED: set(),
}


@dataclass
class Meeting:
    meeting_ref: str
    state: MeetingState = MeetingState.READY


def transition(meeting: Meeting, target: MeetingState) -> Meeting:
    if target not in ALLOWED_TRANSITIONS[meeting.state]:
        raise ValueError(f"invalid transition: {meeting.state} -> {target}")
    meeting.state = target
    return meeting


def next_facilitator(
    candidate_refs: list[str],
    excluded_refs: set[str],
    recent_refs: list[str],
) -> str:
    eligible = [ref for ref in candidate_refs if ref not in excluded_refs]
    if not eligible:
        raise ValueError("no eligible facilitator")
    recent_rank = {ref: index for index, ref in enumerate(recent_refs)}
    return min(eligible, key=lambda ref: recent_rank.get(ref, -1))
