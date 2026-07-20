"""Parse a synthetic device file only after it becomes stable."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class FileSignature:
    size: int
    modified_ns: int


def signature(path: Path) -> FileSignature:
    stat = path.stat()
    return FileSignature(size=stat.st_size, modified_ns=stat.st_mtime_ns)


def is_stable(first: FileSignature, second: FileSignature) -> bool:
    return first == second and first.size > 0


def parse_measurement(
    lines: list[str],
    field_map: dict[str, str],
    convert: Callable[[str], float],
) -> dict[str, float]:
    output: dict[str, float] = {}
    for raw in lines:
        if "=" not in raw:
            continue
        key, value = (part.strip() for part in raw.split("=", 1))
        target = field_map.get(key)
        if target is not None:
            output[target] = convert(value)
    if not output:
        raise ValueError("no supported measurement")
    return output
