"""Auditable incident lifecycle transitions."""

from copy import deepcopy

from mqaicir.models.incident import Incident, LifecycleOverride
from mqaicir.models.taxonomy import LifecycleState

ALLOWED_TRANSITIONS: dict[LifecycleState, set[LifecycleState]] = {
    LifecycleState.DRAFT: {LifecycleState.TRIAGE},
    LifecycleState.TRIAGE: {LifecycleState.ACTIVE, LifecycleState.CONTAINED},
    LifecycleState.ACTIVE: {LifecycleState.CONTAINED, LifecycleState.INVESTIGATION},
    LifecycleState.CONTAINED: {LifecycleState.INVESTIGATION, LifecycleState.REMEDIATION},
    LifecycleState.INVESTIGATION: {LifecycleState.REMEDIATION, LifecycleState.ACTIVE},
    LifecycleState.REMEDIATION: {LifecycleState.REVALIDATION, LifecycleState.ACTIVE},
    LifecycleState.REVALIDATION: {LifecycleState.CLOSED, LifecycleState.REMEDIATION},
    LifecycleState.CLOSED: set(),
}


def transition_incident(
    incident: Incident,
    target: LifecycleState,
    *,
    override: LifecycleOverride | None = None,
) -> Incident:
    """Return a new validated record in ``target`` or raise ``ValueError``."""

    if target not in ALLOWED_TRANSITIONS[incident.lifecycle_status] and override is None:
        raise ValueError(f"invalid lifecycle transition: {incident.lifecycle_status} -> {target}")
    data = deepcopy(incident.model_dump(mode="python"))
    data["lifecycle_status"] = target
    if override is not None:
        data["lifecycle_override"] = override.model_dump(mode="python")
    return Incident.model_validate(data)

