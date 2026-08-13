from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from mqaicir.models.incident import Incident

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "ai-incident-1.0.schema.json"


@pytest.fixture(scope="module")
def schema() -> dict:
    value = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(value)
    return value


def test_schema_declares_draft_id_version_and_examples(schema: dict) -> None:
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["$id"] == "https://maplequanta.ca/schemas/ai-incident/1.0"
    assert schema["version"] == "1.0.0"
    assert schema["description"]
    assert schema["examples"]


def test_every_example_is_schema_valid(schema: dict) -> None:
    validator = Draft202012Validator(schema)
    for path in sorted((ROOT / "examples" / "incidents").glob("*.json")):
        validator.validate(json.loads(path.read_text(encoding="utf-8")))


def test_malformed_incident_is_rejected(schema: dict, example_path: Path) -> None:
    document = json.loads(example_path.read_text())
    document["containment"]["detection_time_seconds"] = -1
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(document)


def test_enum_is_enforced(schema: dict, example_path: Path) -> None:
    document = json.loads(example_path.read_text())
    document["event_state"] = "E9"
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(document)


def test_required_field_is_enforced(schema: dict, example_path: Path) -> None:
    document = json.loads(example_path.read_text())
    del document["incident_id"]
    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(document)


def test_schema_and_model_have_same_required_core(schema: dict) -> None:
    expected = {
        "incident_id", "title", "occurred_at", "event_state", "system", "authority",
        "boundaries_crossed", "harm", "reversibility", "observability", "blast_radius",
    }
    assert expected.issubset(set(schema["required"]))
    assert expected.issubset(Incident.model_fields)

