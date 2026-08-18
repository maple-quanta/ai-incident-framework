import json
from pathlib import Path

from jsonschema import Draft202012Validator

from mqaicir._version import INCIDENT_SCHEMA_VERSION, SOFTWARE_VERSION
from mqaicir.classification.severity import classify_severity
from mqaicir.io import load_incident

ROOT = Path(__file__).resolve().parents[1]


def test_at_least_six_synthetic_examples_validate_and_classify() -> None:
    paths = sorted((ROOT / "examples" / "incidents").glob("*.json"))
    assert len(paths) >= 6
    for path in paths:
        incident = load_incident(path)
        result = classify_severity(incident)
        assert result.triggered_rules and result.rationale


def test_patch_release_accepts_every_v1_0_0_record() -> None:
    assert SOFTWARE_VERSION == "1.0.1"
    assert INCIDENT_SCHEMA_VERSION == "1.0.0"
    schema_path = ROOT / "schemas" / "ai-incident-1.0.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for path in sorted((ROOT / "examples" / "incidents").glob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        declared_version = document.get("framework", {}).get("version", INCIDENT_SCHEMA_VERSION)
        assert declared_version == INCIDENT_SCHEMA_VERSION
        validator.validate(document)
        assert load_incident(path).framework.version == INCIDENT_SCHEMA_VERSION


def test_examples_do_not_contain_live_credential_shapes() -> None:
    forbidden = ("-----BEGIN PRIVATE KEY-----", "ghp_", "AKIA", "Bearer eyJ")
    for path in (ROOT / "examples" / "incidents").glob("*.json"):
        text = path.read_text(encoding="utf-8")
        assert not any(value in text for value in forbidden)
