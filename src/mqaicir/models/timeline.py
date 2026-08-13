"""Incident chronology models."""

from datetime import datetime
from enum import StrEnum

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class TimelineEventType(StrEnum):
    INITIAL_TRIGGER = "initial_trigger"
    MODEL_ACTION = "model_action"
    TOOL_CALL = "tool_call"
    HUMAN_ACTION = "human_action"
    DETECTION = "detection"
    ALERT = "alert"
    CONTAINMENT = "containment"
    CREDENTIAL_REVOCATION = "credential_revocation"
    NETWORK_ISOLATION = "network_isolation"
    SHUTDOWN = "shutdown"
    NOTIFICATION = "notification"
    RECOVERY = "recovery"
    RETEST = "retest"
    CLOSURE = "closure"
    OTHER = "other"


class TimelineEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: AwareDatetime
    event_type: TimelineEventType
    actor: str = Field(min_length=1)
    description: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)

