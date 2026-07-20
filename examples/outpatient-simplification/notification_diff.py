"""Compare baseline and candidate notification targets."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Target:
    target_ref: str
    channel: str


def compare(
    baseline: list[Target],
    candidate: list[Target],
) -> dict[str, set[tuple[str, str]]]:
    baseline_set = {(item.target_ref, item.channel) for item in baseline}
    candidate_set = {(item.target_ref, item.channel) for item in candidate}
    return {
        "missing": baseline_set - candidate_set,
        "unexpected": candidate_set - baseline_set,
        "unchanged": baseline_set & candidate_set,
    }
