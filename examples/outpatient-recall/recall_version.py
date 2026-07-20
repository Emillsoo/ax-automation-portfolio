"""Version repeated recall events without real patient identifiers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RecallState:
    visit_ref: str
    version: int
    waiting: bool


def request_recall(
    state: RecallState,
    request_key: str,
    processed_keys: set[str],
) -> RecallState:
    if request_key in processed_keys:
        return state
    if not state.waiting:
        raise ValueError("visit is not in a recallable state")
    processed_keys.add(request_key)
    return RecallState(
        visit_ref=state.visit_ref,
        version=state.version + 1,
        waiting=True,
    )
