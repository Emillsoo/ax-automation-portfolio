"""Single-worker lease for browser automation."""

import threading
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class WorkerState:
    task_ref: str | None = None


class SingleWorker:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.state = WorkerState()

    @contextmanager
    def lease(self, task_ref: str):
        if not self._lock.acquire(blocking=False):
            raise RuntimeError("browser worker is busy")
        self.state.task_ref = task_ref
        try:
            yield self.state
        finally:
            self.state.task_ref = None
            self._lock.release()
