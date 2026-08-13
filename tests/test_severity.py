from __future__ import annotations

from pathlib import Path

from mqaicir.classification.severity import classify_severity, load_rules
from mqaicir.models.incident import Incident
from mqaicir.models.taxonomy import Severity


def with_updates(example: Incident, **updates: object) -> Incident:
    data = example.model_dump(mode="python")
    data.update(updates)
    data["severity_result"] = None
    return Incident.model_validate(data)


def test_realized_h4_is_critical(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["harm"]["realized_level"] = "H4"
    result = classify_severity(Incident.model_validate(data))
    assert result.severity == Severity.CRITICAL
    assert "SR-CRITICAL-001" in result.triggered_rules


def test_critical_infrastructure_destructive_action_is_critical(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["classification_indicators"] = ["destructive_action"]
    data["boundaries_crossed"] = ["privilege"]
    data["assets_affected"] = [{"type": "CRITICAL_INFRASTRUCTURE", "name": "Synthetic grid", "criticality": "critical"}]
    result = classify_severity(Incident.model_validate(data))
    assert result.severity == Severity.CRITICAL
    assert result.triggered_rules == ["SR-CRITICAL-002"]


def test_external_unauthorized_action_is_high(example: Incident) -> None:
    result = classify_severity(example)
    assert result.severity == Severity.HIGH
    assert "SR-HIGH-001" in result.triggered_rules


def test_low_fallback_is_explicit(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["event_state"] = "E0"
    data["authority"] = {"authorized": ["READ"], "actually_exercised": ["READ"], "unauthorized_exercised": []}
    data["boundaries_crossed"] = ["none"]
    data["harm"] = {"realized_level": "H0", "potential_level": "H1", "categories": [], "description": ""}
    data["observability"]["level"] = "O1"
    data["containment"] = {"documentation": "No event occurred."}
    data["classification_indicators"] = []
    result = classify_severity(Incident.model_validate(data))
    assert result.severity == Severity.LOW
    assert result.triggered_rules == ["SR-LOW-001"]


def test_result_always_has_rule_and_rationale(example: Incident) -> None:
    result = classify_severity(example)
    assert result.triggered_rules
    assert result.rationale
    assert len(result.triggered_rules) == len(result.rationale)


def test_rules_are_conditions_not_weighted_average() -> None:
    document = load_rules()
    text = Path(__file__).resolve().parents[1].joinpath("config/severity_rules.yaml").read_text().lower()
    assert "weight" not in text
    assert "average" in document["ruleset"]["description"].lower()
    assert all("all" in rule and "score" not in rule for rule in document["rules"])

