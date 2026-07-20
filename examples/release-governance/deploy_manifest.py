"""Validate a synthetic deployment manifest before release."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DeployManifest:
    commit_sha: str
    approved: bool
    monitoring_ready: bool
    rollback_ref: str
    validation_mismatches: int


def validate(manifest: DeployManifest) -> None:
    if len(manifest.commit_sha) < 7:
        raise ValueError("commit_sha is required")
    if not manifest.approved:
        raise ValueError("approval is required")
    if not manifest.monitoring_ready:
        raise ValueError("monitoring must be deployed together")
    if not manifest.rollback_ref.strip():
        raise ValueError("rollback reference is required")
    if manifest.validation_mismatches != 0:
        raise ValueError("triangulation mismatch must be zero")
