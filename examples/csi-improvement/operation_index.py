"""Search a synthetic screen-to-service operation index."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationIndexEntry:
    screen_keyword: str
    service_ref: str
    data_domain: str
    evidence_ref: str


def find_candidates(
    query: str,
    entries: list[OperationIndexEntry],
) -> list[OperationIndexEntry]:
    normalized = query.casefold()
    return [
        entry
        for entry in entries
        if entry.screen_keyword.casefold() in normalized
        or normalized in entry.screen_keyword.casefold()
    ]
