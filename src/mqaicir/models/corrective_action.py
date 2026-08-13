"""Corrective action tracking models."""

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CorrectiveActionPriority(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CorrectiveActionStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    ACCEPTED_RISK = "accepted_risk"


class CorrectiveAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_id: str = Field(pattern=r"^CA-[A-Z0-9-]+$")
    finding: str = Field(min_length=1)
    recommended_action: str = Field(min_length=1)
    priority: CorrectiveActionPriority
    owner: str = ""
    due_date: date | None = None
    status: CorrectiveActionStatus = CorrectiveActionStatus.OPEN
    verification_required: bool = True
    verification_evidence: list[str] = Field(default_factory=list)

