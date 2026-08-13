from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from mqaicir.models.incident import Incident


def test_timeline_is_sorted_automatically(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["timeline"] = list(reversed(data["timeline"]))
    parsed = Incident.model_validate(data)
    assert parsed.timeline == sorted(parsed.timeline, key=lambda event: event.timestamp)


def test_unauthorized_authority_must_have_been_exercised(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["authority"]["unauthorized_exercised"] = ["AUTHORIZE"]
    with pytest.raises(ValidationError, match="subset"):
        Incident.model_validate(data)


def test_authority_class_can_be_authorized_in_one_scope_and_unauthorized_in_another(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["authority"] = {
        "authorized": ["EXECUTE"],
        "actually_exercised": ["EXECUTE"],
        "unauthorized_exercised": ["EXECUTE"],
    }
    assert Incident.model_validate(data).authority.unauthorized_exercised


def test_none_boundary_is_exclusive(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["boundaries_crossed"] = ["none", "tool"]
    with pytest.raises(ValidationError, match="cannot be combined"):
        Incident.model_validate(data)


def test_framework_versions_are_not_silently_reinterpreted(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["framework"]["version"] = "1.1.0"
    with pytest.raises(ValidationError, match="migrate explicitly"):
        Incident.model_validate(data)


def test_unknown_evidence_reference_is_rejected(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["timeline"][0]["evidence_refs"] = ["EV-NOT-FOUND"]
    with pytest.raises(ValidationError, match="unknown evidence"):
        Incident.model_validate(data)

