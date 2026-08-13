"""Generate the committed Draft 2020-12 schema from the canonical Pydantic model."""

from __future__ import annotations

import json
from pathlib import Path

from mqaicir.models.incident import Incident

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "schemas" / "ai-incident-1.0.schema.json"

DEFINITION_DESCRIPTIONS = {
    "EventState": "E0 Hazard; E1 Near Miss; E2 Boundary Violation; E3 Incident; E4 Serious/Systemic Incident. E4 is not a jurisdiction-specific legal conclusion.",
    "AuthorityClass": "READ, RECOMMEND, WRITE, EXECUTE, EXTERNALIZE, or AUTHORIZE authority class from Maple Quanta Agentic AI Containment Assurance.",
    "BoundaryType": "Machine identifiers for B0 None through B9 Third Party / External. See the MQ-AICIR taxonomy for code labels.",
    "AssetType": "Category of asset affected by the AI event.",
    "HarmLevel": "H0 No Realized Harm; H1 Negligible; H2 Material; H3 Major; H4 Severe/Systemic.",
    "ReversibilityLevel": "R0 No persistent consequence through R4 Irreversible.",
    "ObservabilityLevel": "O0 Fully reconstructed through O4 Unobservable. A larger number means worse observability.",
    "BlastRadius": "BR0 Single action/session through BR5 Potentially systemic.",
    "MCAILevel": "Maple Quanta Maximum Credible Agent Impact: A0 Informational through A4 Critical.",
    "Severity": "Rule-based operational severity. Values are never derived by averaging dimensions.",
    "LifecycleState": "DRAFT, TRIAGE, ACTIVE, CONTAINED, INVESTIGATION, REMEDIATION, REVALIDATION, or CLOSED.",
    "HandlingClassification": "Incident-level information handling marking.",
    "RootCauseCategory": "Structured primary or contributing root-cause category.",
}

PROPERTY_DESCRIPTIONS = {
    "framework": "Framework identity and semantic version; consumers must not silently reinterpret other versions.",
    "incident_id": "Organization-assigned identifier in MQ-YYYY-... form.",
    "event_state": "Event State (E) in the incident vector.",
    "authority": "Authorized, actually exercised, and unauthorized exercised Authority (A).",
    "boundaries_crossed": "One or more Boundary (B) identifiers; B0/none is exclusive.",
    "assets_affected": "Affected Assets (X), including owner and contextual criticality where known.",
    "harm": "Realized and credible potential Harm (H) are deliberately separate.",
    "reversibility": "Reversibility (R) of the consequence.",
    "observability": "Observability (O); O0 is best and O4 is worst.",
    "containment": "Containment (C), including the Intervention Time components, Damage Time, and contextual Containment Margin.",
    "severity_result": "Deterministic result including every decisive rule identifier and rationale.",
    "extensions": "Namespaced organization-specific data. MQ-AICIR public core does not interpret this object.",
}


def build_schema() -> dict[str, object]:
    schema = Incident.model_json_schema(mode="serialization")
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = "https://maplequanta.ca/schemas/ai-incident/1.0"
    schema["title"] = "Maple Quanta AI Incident Classification & Reporting Framework — Incident 1.0"
    schema["description"] = (
        "MQ-AICIR 1.0 incident, hazard, near-miss, or boundary-violation record. "
        "The $id identifies the schema; it does not assert that the URL currently hosts this file."
    )
    schema["version"] = "1.0.0"
    properties = schema.get("properties", {})
    if isinstance(properties, dict):
        for name, description in PROPERTY_DESCRIPTIONS.items():
            if isinstance(properties.get(name), dict):
                properties[name].setdefault("description", description)
    definitions = schema.get("$defs", {})
    if isinstance(definitions, dict):
        for name, description in DEFINITION_DESCRIPTIONS.items():
            if isinstance(definitions.get(name), dict):
                definitions[name]["description"] = description
    schema["examples"] = [
        {
            "framework": {"name": "Maple Quanta AI Incident Classification & Reporting Framework", "version": "1.0.0"},
            "incident_id": "MQ-2026-0042",
            "title": "Example boundary violation",
            "occurred_at": "2026-08-12T15:21:32Z",
            "event_state": "E2",
            "system": {"name": "Example Agent"},
            "authority": {"authorized": ["READ"], "actually_exercised": ["READ", "EXECUTE"], "unauthorized_exercised": ["EXECUTE"]},
            "boundaries_crossed": ["tool"],
            "harm": {"realized_level": "H0", "potential_level": "H3", "categories": []},
            "reversibility": "R0",
            "observability": {"level": "O1"},
            "blast_radius": "BR0"
        }
    ]
    return schema


if __name__ == "__main__":
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(build_schema(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(TARGET)

