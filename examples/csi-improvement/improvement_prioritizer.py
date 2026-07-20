"""Prioritize synthetic improvement candidates."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Improvement:
    improvement_ref: str
    frequency: int
    minutes_per_case: int
    error_risk: int
    implementation_effort: int


def score(item: Improvement) -> float:
    benefit = item.frequency * item.minutes_per_case * (1 + item.error_risk)
    effort = max(item.implementation_effort, 1)
    return benefit / effort


def prioritize(items: list[Improvement]) -> list[Improvement]:
    return sorted(items, key=lambda item: (-score(item), item.improvement_ref))
