"""Synthetic outbox pattern for threshold-based alerts."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    version: str
    minimum_score: float


@dataclass
class OutboxItem:
    event_ref: str
    rule_version: str
    delivered: bool = False


def evaluate(event_ref: str, score: float, rule: Rule) -> OutboxItem | None:
    if not 0 <= score <= 100:
        raise ValueError("score is out of range")
    if score < rule.minimum_score:
        return None
    return OutboxItem(event_ref=event_ref, rule_version=rule.version)


def pending(items: list[OutboxItem]) -> list[OutboxItem]:
    seen: set[tuple[str, str]] = set()
    output: list[OutboxItem] = []
    for item in items:
        key = (item.event_ref, item.rule_version)
        if not item.delivered and key not in seen:
            seen.add(key)
            output.append(item)
    return output
