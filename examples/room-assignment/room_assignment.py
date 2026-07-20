"""Create a dry-run room assignment from synthetic capacity data."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Admission:
    admission_ref: str
    required_zone: str
    isolation_required: bool


@dataclass(frozen=True)
class Room:
    room_ref: str
    zone: str
    available_beds: int
    supports_isolation: bool
    priority: int


def choose_room(admission: Admission, rooms: list[Room]) -> str | None:
    candidates = [
        room
        for room in rooms
        if room.zone == admission.required_zone
        and room.available_beds > 0
        and (not admission.isolation_required or room.supports_isolation)
    ]
    candidates.sort(key=lambda room: (room.priority, room.room_ref))
    return candidates[0].room_ref if candidates else None
