from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from mqaicir.classification.lifecycle import transition_incident
from mqaicir.models.incident import Incident, LifecycleOverride
from mqaicir.models.taxonomy import LifecycleState
from mqaicir.scaffold import new_incident


def test_invalid_transition_is_rejected() -> None:
    with pytest.raises(ValueError, match="invalid lifecycle transition"):
        transition_incident(new_incident("MQ-2026-9001"), LifecycleState.CLOSED)


def test_valid_transition_path() -> None:
    item = new_incident("MQ-2026-9002")
    for target in (
        LifecycleState.TRIAGE, LifecycleState.ACTIVE, LifecycleState.CONTAINED,
        LifecycleState.INVESTIGATION, LifecycleState.REMEDIATION, LifecycleState.REVALIDATION,
    ):
        item = transition_incident(item, target)
    assert item.lifecycle_status == LifecycleState.REVALIDATION


def test_cannot_close_incomplete_incident() -> None:
    data = new_incident("MQ-2026-9003").model_dump(mode="python")
    data["lifecycle_status"] = "REVALIDATION"
    item = Incident.model_validate(data)
    with pytest.raises(ValidationError, match="CLOSED lifecycle requirements"):
        transition_incident(item, LifecycleState.CLOSED)


def test_complete_incident_can_close(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["lifecycle_status"] = "REVALIDATION"
    data["closure_rationale"] = "Controls revalidated and remaining risk accepted by the incident owner."
    item = Incident.model_validate(data)
    closed = transition_incident(item, LifecycleState.CLOSED)
    assert closed.lifecycle_status == LifecycleState.CLOSED


def test_explicit_override_records_person_time_and_rationale() -> None:
    override = LifecycleOverride(
        responsible_person="Accountable Executive",
        timestamp=datetime.now(timezone.utc),
        rationale="Emergency administrative closure pending retrospective documentation.",
    )
    closed = transition_incident(new_incident("MQ-2026-9004"), LifecycleState.CLOSED, override=override)
    assert closed.lifecycle_override == override

