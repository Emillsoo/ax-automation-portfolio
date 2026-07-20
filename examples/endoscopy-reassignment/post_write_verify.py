"""Verify a synthetic reservation change by reading the source again."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Reservation:
    reservation_ref: str
    slot_ref: str
    revision: int


class ReservationAdapter(Protocol):
    def read(self, reservation_ref: str) -> Reservation: ...
    def reassign(self, reservation_ref: str, slot_ref: str) -> None: ...


def reassign_and_verify(
    adapter: ReservationAdapter,
    reservation_ref: str,
    target_slot_ref: str,
) -> Reservation:
    before = adapter.read(reservation_ref)
    if before.slot_ref == target_slot_ref:
        return before

    adapter.reassign(reservation_ref, target_slot_ref)
    after = adapter.read(reservation_ref)

    if after.slot_ref != target_slot_ref:
        raise RuntimeError("write response did not match persisted state")
    if after.revision <= before.revision:
        raise RuntimeError("revision did not advance")
    return after
