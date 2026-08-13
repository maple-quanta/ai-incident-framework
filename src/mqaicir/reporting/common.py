"""Shared report context construction."""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from mqaicir.classification.containment import interpret_margin
from mqaicir.classification.severity import classify_severity
from mqaicir.models.incident import Incident
from mqaicir.models.taxonomy import BOUNDARY_CODES, coded_boundary, label_for
from mqaicir.redaction import redact_value

LEGAL_NOTICE = (
    "Regulatory notification requirements depend on jurisdiction, system classification, "
    "contractual obligations, and applicable law. This framework assists classification "
    "but does not provide legal advice."
)


def environment(*, html: bool) -> Environment:
    template_dir = Path(str(files("mqaicir.reporting").joinpath("templates")))
    return Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(enabled_extensions=("html", "xml"), default_for_string=html, default=html),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def report_context(incident: Incident, custom_redaction_patterns: list[str] | None = None) -> dict[str, Any]:
    severity = incident.severity_result or classify_severity(incident)
    data = redact_value(incident.model_dump(mode="json"), custom_redaction_patterns)
    data["severity_result"] = severity.model_dump(mode="json")
    boundaries = [f"{coded_boundary(value)} {label_for(value)}" for value in incident.boundaries_crossed]
    authorities = [value.value for value in incident.authority.actually_exercised]
    asset_types = [value.type.value for value in incident.assets_affected]
    cm = "N/A" if incident.containment.containment_margin is None else f"{incident.containment.containment_margin:.2f}"
    vector = (
        f"[{incident.event_state.value} | {', '.join(authorities) or 'NONE'} | "
        f"{','.join(coded_boundary(value) for value in incident.boundaries_crossed)} | "
        f"{','.join(asset_types) or 'NONE'} | {incident.harm.realized_level.value}/"
        f"{incident.harm.potential_level.value} | {incident.reversibility.value} | "
        f"{incident.observability.level.value} | CM={cm}]"
    )
    return {
        "incident": data,
        "severity": severity.model_dump(mode="json"),
        "vector": vector,
        "boundary_labels": boundaries,
        "label": label_for,
        "boundary_code": lambda raw: BOUNDARY_CODES[raw],
        "containment_interpretation": interpret_margin(incident.containment),
        "legal_notice": LEGAL_NOTICE,
    }

