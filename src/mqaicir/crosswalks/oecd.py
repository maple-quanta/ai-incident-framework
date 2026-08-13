"""OECD actual-harm and potential-harm terminology crosswalk."""

from mqaicir.crosswalks.common import references
from mqaicir.models.incident import CrosswalkReference, Incident
from mqaicir.models.taxonomy import EventState, HarmLevel


def suggest(incident: Incident) -> list[CrosswalkReference]:
    keys = {"realized_harm", "potential_harm"}
    if incident.event_state in {EventState.HAZARD, EventState.NEAR_MISS, EventState.BOUNDARY_VIOLATION}:
        keys.add("hazard")
    if incident.event_state in {EventState.INCIDENT, EventState.SERIOUS_SYSTEMIC_INCIDENT} and incident.harm.realized_level != HarmLevel.NONE:
        keys.add("incident")
    return references("oecd", keys)

