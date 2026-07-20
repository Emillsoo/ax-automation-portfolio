"""Minimal OCR benchmark metrics for synthetic ground truth."""

from dataclasses import dataclass


def levenshtein(left: str, right: str) -> int:
    previous = list(range(len(right) + 1))
    for i, left_char in enumerate(left, start=1):
        current = [i]
        for j, right_char in enumerate(right, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[j] + 1,
                    previous[j - 1] + (left_char != right_char),
                )
            )
        previous = current
    return previous[-1]


def error_rate(expected: list[str], actual: list[str]) -> float:
    denominator = max(len(expected), 1)
    return levenshtein("\n".join(expected), "\n".join(actual)) / denominator


@dataclass(frozen=True)
class BenchmarkResult:
    engine: str
    character_error_rate: float
    elapsed_ms: int
    external_transfer: bool
