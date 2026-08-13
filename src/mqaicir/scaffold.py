"""Safe starter records for CLI and web creation."""

from datetime import datetime, timezone

from mqaicir.models.incident import Incident


def new_incident(incident_id: str, title: str = "New AI incident", system_name: str = "Unspecified AI system") -> Incident:
    now = datetime.now(timezone.utc)
    return Incident.model_validate(
        {
            "incident_id": incident_id,
            "title": title,
            "occurred_at": now,
            "event_state": "E0",
            "system": {"name": system_name},
            "authority": {"authorized": [], "actually_exercised": [], "unauthorized_exercised": []},
            "boundaries_crossed": ["none"],
            "harm": {"realized_level": "H0", "potential_level": "H0", "categories": []},
            "reversibility": "R0",
            "observability": {"level": "O4", "missing_evidence": ["Assessment not started"]},
            "blast_radius": "BR0",
            "corrective_actions_required": True,
        }
    )

