"""Aggregate synthetic container and process health without credentials."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceHealth:
    service_ref: str
    running: bool
    restart_count: int
    memory_percent: float


def summarize(
    services: list[ServiceHealth],
    restart_limit: int = 3,
    memory_limit: float = 90.0,
) -> dict:
    unhealthy = [
        service.service_ref
        for service in services
        if not service.running
        or service.restart_count > restart_limit
        or service.memory_percent > memory_limit
    ]
    return {
        "healthy": not unhealthy,
        "checked": len(services),
        "unhealthyServiceRefs": unhealthy,
    }
