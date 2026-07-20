"""Validate a synthetic vendor API contract and result counts."""

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Contract:
    required_request_fields: tuple[str, ...]
    allowed_statuses: frozenset[str]


def execute_contract(
    request: dict[str, Any],
    contract: Contract,
    query: Callable[[dict[str, Any]], list[dict[str, Any]]],
) -> dict[str, Any]:
    missing = [
        field
        for field in contract.required_request_fields
        if request.get(field) in (None, "")
    ]
    if missing:
        return {"ok": False, "error": "missing_fields", "fields": missing}

    rows = query(request)
    safe_rows = [
        row for row in rows if row.get("status") in contract.allowed_statuses
    ]
    if len(safe_rows) != len(rows):
        return {"ok": False, "error": "undefined_status", "rows": []}

    return {
        "ok": True,
        "count": len(safe_rows),
        "rows": safe_rows,
    }
