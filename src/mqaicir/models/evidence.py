"""Evidence preservation records."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class EvidenceType(StrEnum):
    AGENT_TRACE = "agent_trace"
    PROMPT = "prompt"
    SYSTEM_PROMPT = "system_prompt"
    TOOL_CALL = "tool_call"
    TOOL_RESPONSE = "tool_response"
    NETWORK_LOG = "network_log"
    IAM_LOG = "iam_log"
    CLOUD_LOG = "cloud_log"
    APPLICATION_LOG = "application_log"
    MODEL_VERSION = "model_version"
    SYSTEM_CONFIGURATION = "system_configuration"
    POLICY_VERSION = "policy_version"
    CREDENTIALS_AVAILABLE = "credentials_available_to_agent"
    AFFECTED_FILE = "affected_file"
    SCREENSHOT = "screenshot"
    FORENSIC_IMAGE = "forensic_image"
    HUMAN_COMMUNICATION = "human_communication"
    INCIDENT_TICKET = "incident_ticket"
    OTHER = "other"


class CustodyEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: AwareDatetime
    actor: str = Field(min_length=1)
    action: str = Field(min_length=1)
    notes: str | None = None


class Evidence(BaseModel):
    """A reference to preserved evidence; never embed credentials or secrets."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(pattern=r"^EV-[A-Z0-9-]+$")
    type: EvidenceType
    description: str
    location: str = Field(description="Reference or controlled location, not the evidence secret itself.")
    hash: str | None = Field(default=None, description="Optional digest including algorithm, e.g. sha256:...")
    collected_at: AwareDatetime | None = None
    collected_by: str | None = None
    chain_of_custody: list[CustodyEvent] = Field(default_factory=list)
    redacted: bool = False

