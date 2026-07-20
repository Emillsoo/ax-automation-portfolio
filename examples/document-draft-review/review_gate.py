"""Human-review gate for a synthetic document drafting workflow.

The model output remains a draft until a reviewer explicitly approves it.
No clinical decision or production integration is included.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DraftState(str, Enum):
    CREATED = "created"
    REVIEW_REQUIRED = "review_required"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class Evidence:
    section: str
    source_text: str


@dataclass
class Draft:
    document_id: str
    sections: dict[str, str]
    evidence: list[Evidence]
    state: DraftState = DraftState.CREATED
    reviewer_note: str | None = None


REQUIRED_SECTIONS = {"summary", "process", "next_step"}


def prepare_for_review(draft: Draft) -> Draft:
    missing = REQUIRED_SECTIONS - draft.sections.keys()
    if missing:
        raise ValueError(f"missing sections: {sorted(missing)}")
    if not draft.evidence:
        raise ValueError("source evidence is required")

    unsupported = [
        section
        for section, text in draft.sections.items()
        if text.strip() and not any(item.section == section for item in draft.evidence)
    ]
    if unsupported:
        raise ValueError(f"sections without evidence: {unsupported}")

    draft.state = DraftState.REVIEW_REQUIRED
    return draft


def review(draft: Draft, approved: bool, reviewer_note: str) -> Draft:
    if draft.state != DraftState.REVIEW_REQUIRED:
        raise ValueError("draft is not ready for review")
    if not reviewer_note.strip():
        raise ValueError("reviewer note is required")

    draft.reviewer_note = reviewer_note.strip()
    draft.state = DraftState.APPROVED if approved else DraftState.REJECTED
    return draft


def can_publish(draft: Draft) -> bool:
    return draft.state == DraftState.APPROVED

