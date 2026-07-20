"""Public reconstruction of an RPA task manager.

This is not production source. It demonstrates lifecycle, timeout,
cancellation, and evidence handling without real systems or credentials.
"""

from __future__ import annotations

import subprocess
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Sequence


class TaskState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"


@dataclass
class Task:
    task_id: str
    state: TaskState = TaskState.QUEUED
    current_step: str = "waiting"
    error: str | None = None
    evidence_files: list[str] = field(default_factory=list)


class TaskManager:
    """Run one predefined automation command with observable state."""

    def __init__(
        self,
        command_factory: Callable[[str], Sequence[str]],
        evidence_dir: Path,
        timeout_seconds: int = 300,
    ) -> None:
        self._command_factory = command_factory
        self._evidence_dir = evidence_dir
        self._timeout_seconds = timeout_seconds
        self._tasks: dict[str, Task] = {}
        self._processes: dict[str, subprocess.Popen[str]] = {}
        self._lock = threading.Lock()

    def create(self, task_id: str) -> Task:
        with self._lock:
            if task_id in self._tasks:
                raise ValueError("task_id already exists")
            task = Task(task_id=task_id)
            self._tasks[task_id] = task
            return task

    def run(self, task_id: str) -> Task:
        task = self._require(task_id)
        command = list(self._command_factory(task_id))
        if not command:
            raise ValueError("predefined command is empty")

        self._set_state(task, TaskState.RUNNING, "starting automation")
        started_at = time.monotonic()

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
        )
        with self._lock:
            self._processes[task_id] = process

        try:
            while process.poll() is None:
                if time.monotonic() - started_at > self._timeout_seconds:
                    process.terminate()
                    self._set_state(task, TaskState.TIMED_OUT, "timeout")
                    self._collect_evidence(task)
                    return task
                time.sleep(0.2)

            if task.state == TaskState.CANCELLED:
                return task
            if process.returncode == 0:
                self._set_state(task, TaskState.SUCCEEDED, "completed")
            else:
                task.error = f"automation exited with code {process.returncode}"
                self._set_state(task, TaskState.FAILED, "failed")
                self._collect_evidence(task)
            return task
        finally:
            with self._lock:
                self._processes.pop(task_id, None)

    def cancel(self, task_id: str) -> Task:
        task = self._require(task_id)
        with self._lock:
            process = self._processes.get(task_id)
            if process is not None and process.poll() is None:
                process.terminate()
            task.state = TaskState.CANCELLED
            task.current_step = "cancelled by user"
        self._collect_evidence(task)
        return task

    def _collect_evidence(self, task: Task) -> None:
        candidate = self._evidence_dir / f"{task.task_id}-failure.png"
        if candidate.exists():
            task.evidence_files.append(candidate.name)

    def _require(self, task_id: str) -> Task:
        with self._lock:
            if task_id not in self._tasks:
                raise KeyError("unknown task_id")
            return self._tasks[task_id]

    def _set_state(self, task: Task, state: TaskState, step: str) -> None:
        with self._lock:
            task.state = state
            task.current_step = step

