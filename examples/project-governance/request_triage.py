"""Classify a synthetic integration request before implementation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectRequest:
    request_ref: str
    business_rule_confirmed: bool
    source_measured: bool
    owner_confirmed: bool
    vendor_dependency: bool
    monitoring_defined: bool


def blockers(request: ProjectRequest) -> list[str]:
    result: list[str] = []
    if not request.business_rule_confirmed:
        result.append("business_rule")
    if not request.source_measured:
        result.append("measured_source")
    if not request.owner_confirmed:
        result.append("owner")
    if request.vendor_dependency:
        result.append("vendor_dependency")
    if not request.monitoring_defined:
        result.append("monitoring")
    return result
