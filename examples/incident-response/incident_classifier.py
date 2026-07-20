"""Turn observations into a synthetic incident investigation plan."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    api_success: bool
    persisted_state_matches: bool
    network_reachable: bool
    worker_busy: bool


def investigation_steps(observation: Observation) -> list[str]:
    steps = ["freeze_writes", "capture_correlation_reference"]
    if observation.api_success and not observation.persisted_state_matches:
        steps.extend(["requery_source", "compare_business_result"])
    if not observation.network_reachable:
        steps.extend(["check_dns", "check_port", "check_proxy_policy"])
    if observation.worker_busy:
        steps.extend(["inspect_owned_process", "verify_single_worker_lease"])
    steps.extend(["minimal_reproduction", "recovery", "add_prevention_guard"])
    return steps
