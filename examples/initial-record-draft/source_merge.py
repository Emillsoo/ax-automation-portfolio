"""Normalize multiple synthetic record sources before drafting."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceFragment:
    source_type: str
    occurred_at: str
    text: str


ALLOWED_SOURCE_TYPES = {"outpatient", "emergency", "inpatient"}


def merge_fragments(fragments: list[SourceFragment]) -> str:
    accepted = [
        fragment
        for fragment in fragments
        if fragment.source_type in ALLOWED_SOURCE_TYPES
        and fragment.occurred_at.strip()
        and fragment.text.strip()
    ]
    accepted.sort(key=lambda item: (item.occurred_at, item.source_type))

    seen: set[tuple[str, str, str]] = set()
    output: list[str] = []
    for item in accepted:
        key = (item.source_type, item.occurred_at, item.text.strip())
        if key in seen:
            continue
        seen.add(key)
        output.append(
            f"[{item.occurred_at} | {item.source_type}] {item.text.strip()}"
        )
    if not output:
        raise ValueError("no supported source text")
    return "\n".join(output)
