"""Match local work excerpts to synthetic task titles without posting them."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    task_ref: str
    title: str
    keywords: tuple[str, ...] = ()


def title_keywords(title: str) -> set[str]:
    cleaned = re.sub(r"\[[^\]]*]", " ", title)
    return {
        token
        for token in re.split(r"[\s_·,/()]+", cleaned)
        if len(token) >= 2
    }


def match_excerpt(excerpt: str, tasks: list[Task]) -> list[str]:
    normalized = excerpt.casefold()
    scored: list[tuple[int, str]] = []
    for task in tasks:
        keywords = set(task.keywords) or title_keywords(task.title)
        score = sum(
            1 for keyword in keywords if keyword.casefold() in normalized
        )
        if score:
            scored.append((score, task.task_ref))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [task_ref for _, task_ref in scored]
