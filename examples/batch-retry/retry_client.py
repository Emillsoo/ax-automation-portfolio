"""Bounded retry policy for a synthetic internal API client.

The client accepts an injected request function and contains no endpoint,
credential, or production system detail.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar


T = TypeVar("T")


class PermanentFailure(RuntimeError):
    pass


class TemporaryFailure(RuntimeError):
    pass


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    initial_delay_seconds: float = 1.0
    multiplier: float = 2.0

    def validate(self) -> None:
        if self.max_attempts < 1 or self.max_attempts > 5:
            raise ValueError("max_attempts must be between 1 and 5")
        if self.initial_delay_seconds < 0:
            raise ValueError("initial delay must not be negative")
        if self.multiplier < 1:
            raise ValueError("multiplier must be at least 1")


class RetryClient(Generic[T]):
    def __init__(
        self,
        request: Callable[[], T],
        is_success: Callable[[T], bool],
        policy: RetryPolicy | None = None,
    ) -> None:
        self._request = request
        self._is_success = is_success
        self._policy = policy or RetryPolicy()
        self._policy.validate()

    def execute(self) -> T:
        delay = self._policy.initial_delay_seconds
        last_error: Exception | None = None

        for attempt in range(1, self._policy.max_attempts + 1):
            try:
                result = self._request()
                if self._is_success(result):
                    return result
                raise PermanentFailure("business result indicates failure")
            except PermanentFailure:
                raise
            except TemporaryFailure as exc:
                last_error = exc
                if attempt == self._policy.max_attempts:
                    break
                time.sleep(delay)
                delay *= self._policy.multiplier

        raise TemporaryFailure(
            f"request failed after {self._policy.max_attempts} attempts"
        ) from last_error

