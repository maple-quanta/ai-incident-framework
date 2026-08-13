"""Shared AI Findings Exchange (SAFE) proposed-RFC crosswalk."""

from mqaicir.crosswalks.common import references
from mqaicir.models.incident import CrosswalkReference, Incident


def suggest(incident: Incident) -> list[CrosswalkReference]:
    keys = {"incident_near_miss", "operating_stack"}
    if incident.evidence or incident.timeline:
        keys.add("evidence")
    if incident.corrective_actions:
        keys.add("corrective_actions")
    if incident.notifications.affected_third_parties or incident.notifications.regulators:
        keys.add("notification")
    return references("safe", keys)

