"""Canonical MQ-AICIR incident record model."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator, model_validator

from mqaicir._version import INCIDENT_SCHEMA_VERSION
from mqaicir.models.corrective_action import CorrectiveAction
from mqaicir.models.evidence import Evidence
from mqaicir.models.taxonomy import (
    AssetType,
    AuthorityClass,
    BlastRadius,
    BoundaryType,
    ClassificationIndicator,
    EventState,
    HandlingClassification,
    HarmCategory,
    HarmLevel,
    LifecycleState,
    MCAILevel,
    ObservabilityLevel,
    ReversibilityLevel,
    RootCauseCategory,
    Severity,
)
from mqaicir.models.timeline import TimelineEvent

FRAMEWORK_NAME = "Maple Quanta AI Incident Classification & Reporting Framework"
FRAMEWORK_VERSION = INCIDENT_SCHEMA_VERSION


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True, use_enum_values=False)


class FrameworkInfo(StrictModel):
    name: Literal["Maple Quanta AI Incident Classification & Reporting Framework"] = FRAMEWORK_NAME
    version: str = Field(default=FRAMEWORK_VERSION, pattern=r"^\d+\.\d+\.\d+$")

    @field_validator("version")
    @classmethod
    def supported_version(cls, value: str) -> str:
        if value != FRAMEWORK_VERSION:
            raise ValueError(
                f"framework version {value!r} is not interpreted by MQ-AICIR {FRAMEWORK_VERSION}; migrate explicitly"
            )
        return value


class Handling(StrictModel):
    classification: HandlingClassification = HandlingClassification.CONFIDENTIAL
    distribution: list[str] = Field(default_factory=list)
    retention_policy: str | None = None


class RegulatoryStatus(StrEnum):
    YES = "yes"
    NO = "no"
    PENDING = "pending"
    NOT_ASSESSED = "not_assessed"


class RegulatorySeriousIncident(StrictModel):
    status: RegulatoryStatus = RegulatoryStatus.NOT_ASSESSED
    framework: str | None = None
    notes: str | None = None


class AuthorityAssessment(StrictModel):
    authorized: list[AuthorityClass] = Field(default_factory=list)
    actually_exercised: list[AuthorityClass] = Field(default_factory=list)
    unauthorized_exercised: list[AuthorityClass] = Field(default_factory=list)

    @model_validator(mode="after")
    def authority_sets_are_consistent(self) -> "AuthorityAssessment":
        for field_name in ("authorized", "actually_exercised", "unauthorized_exercised"):
            values = getattr(self, field_name)
            if len(values) != len(set(values)):
                raise ValueError(f"authority.{field_name} must not contain duplicates")
        if not set(self.unauthorized_exercised).issubset(self.actually_exercised):
            raise ValueError("unauthorized_exercised must be a subset of actually_exercised")
        return self


class AssetCriticality(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AffectedAsset(StrictModel):
    type: AssetType
    name: str = Field(min_length=1)
    owner: str | None = None
    criticality: AssetCriticality = AssetCriticality.MEDIUM
    description: str = ""


class HarmAssessment(StrictModel):
    realized_level: HarmLevel
    potential_level: HarmLevel
    categories: list[HarmCategory] = Field(default_factory=list)
    description: str = ""

    @field_validator("categories")
    @classmethod
    def unique_categories(cls, values: list[HarmCategory]) -> list[HarmCategory]:
        if len(values) != len(set(values)):
            raise ValueError("harm categories must not contain duplicates")
        return values


class ObservabilityAssessment(StrictModel):
    level: ObservabilityLevel = Field(
        description="O0 is best and O4 is worst; unlike most dimensions, a larger number means poorer observability."
    )
    evidence_sources: list[str] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    tamper_risk: bool = False


class ContainmentMetrics(StrictModel):
    detection_time_seconds: float | None = Field(default=None, ge=0)
    decision_time_seconds: float | None = Field(default=None, ge=0)
    enforcement_time_seconds: float | None = Field(default=None, ge=0)
    intervention_time_seconds: float | None = Field(default=None, ge=0)
    damage_time_seconds: float | None = Field(default=None, ge=0)
    containment_margin: float | None = Field(default=None, ge=0)
    metric_misleading: bool = False
    instantaneous_action: bool = False
    not_applicable_reason: str | None = None
    documentation: str = ""
    preventive_control: str | None = None

    @model_validator(mode="after")
    def calculate_metrics(self) -> "ContainmentMetrics":
        parts = (self.detection_time_seconds, self.decision_time_seconds, self.enforcement_time_seconds)
        if all(value is not None for value in parts):
            object.__setattr__(self, "intervention_time_seconds", sum(value for value in parts if value is not None))
        else:
            object.__setattr__(self, "intervention_time_seconds", None)

        reason: str | None = None
        if self.metric_misleading:
            reason = self.not_applicable_reason or "Containment Margin would be misleading for this pathway."
        elif self.instantaneous_action or self.damage_time_seconds == 0:
            reason = self.not_applicable_reason or "The action is effectively instantaneous; prevention is the relevant control."
        elif self.damage_time_seconds is None:
            reason = self.not_applicable_reason or "Damage Time is unavailable."
        elif self.intervention_time_seconds is None:
            reason = self.not_applicable_reason or "Intervention Time is unavailable because one or more components are missing."
        elif self.intervention_time_seconds == 0:
            reason = self.not_applicable_reason or "Intervention Time is zero; a meaningful ratio cannot be calculated."

        if reason:
            object.__setattr__(self, "containment_margin", None)
            object.__setattr__(self, "not_applicable_reason", reason)
        else:
            object.__setattr__(self, "containment_margin", self.damage_time_seconds / self.intervention_time_seconds)  # type: ignore[operator]
            object.__setattr__(self, "not_applicable_reason", None)
        return self


class MCAIAssessment(StrictModel):
    pre_incident_assessed: MCAILevel | None = None
    post_incident_reassessed: MCAILevel | None = None


class ControlStatus(StrEnum):
    EFFECTIVE = "effective"
    PARTIALLY_EFFECTIVE = "partially_effective"
    FAILED = "failed"
    NOT_TESTED = "not_tested"
    NOT_APPLICABLE = "not_applicable"
    UNKNOWN = "unknown"


class ControlPerformance(StrictModel):
    control_id: str = Field(min_length=1)
    control_name: str = Field(min_length=1)
    expected_behavior: str = Field(min_length=1)
    observed_behavior: str = Field(min_length=1)
    status: ControlStatus
    evidence: list[str] = Field(default_factory=list)


class RootCauseAnalysis(StrictModel):
    primary_root_cause: RootCauseCategory
    contributing_factors: list[RootCauseCategory] = Field(default_factory=list)
    analysis: str = ""


class NotificationDecision(StrEnum):
    YES = "yes"
    NO = "no"
    PENDING = "pending"


class Notifications(StrictModel):
    affected_internal_teams: list[str] = Field(default_factory=list)
    affected_third_parties: list[str] = Field(default_factory=list)
    regulators: list[str] = Field(default_factory=list)
    law_enforcement: list[str] = Field(default_factory=list)
    contractual_notification_required: NotificationDecision = NotificationDecision.PENDING
    regulatory_notification_required: NotificationDecision = NotificationDecision.PENDING
    legal_review_required: bool = True


class SeverityAssessment(StrictModel):
    severity: Severity
    triggered_rules: list[str] = Field(min_length=1)
    rationale: list[str] = Field(min_length=1)
    ruleset_version: str = "1.0.0"


class CrosswalkReference(StrictModel):
    identifier: str | None = None
    title: str
    relationship: str
    source_version: str
    verified_at: str | None = None


class Crosswalks(StrictModel):
    safe: list[CrosswalkReference] = Field(default_factory=list)
    mitre_atlas: list[CrosswalkReference] = Field(default_factory=list)
    nist: list[CrosswalkReference] = Field(default_factory=list)
    oecd: list[CrosswalkReference] = Field(default_factory=list)


class AISystemInfo(StrictModel):
    name: str = Field(min_length=1)
    model: str | None = None
    model_version: str | None = None
    provider: str | None = None
    owner: str | None = None
    deployment_environment: str | None = None
    assurance_boundary: str | None = None
    description: str = ""


class LifecycleOverride(StrictModel):
    responsible_person: str = Field(min_length=1)
    timestamp: AwareDatetime
    rationale: str = Field(min_length=1)


class Incident(StrictModel):
    """The complete, multidimensional MQ-AICIR incident record."""

    framework: FrameworkInfo = Field(default_factory=FrameworkInfo)
    incident_id: str = Field(pattern=r"^MQ-\d{4}-[A-Z0-9-]+$")
    title: str = Field(min_length=1)
    description: str = ""
    executive_summary: str = ""
    handling: Handling = Field(default_factory=Handling)
    created_at: AwareDatetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    occurred_at: AwareDatetime
    discovered_at: AwareDatetime | None = None
    lifecycle_status: LifecycleState = LifecycleState.DRAFT
    event_state: EventState
    regulatory_serious_incident: RegulatorySeriousIncident = Field(default_factory=RegulatorySeriousIncident)
    system: AISystemInfo
    authority: AuthorityAssessment
    boundaries_crossed: list[BoundaryType]
    assets_affected: list[AffectedAsset] = Field(default_factory=list)
    harm: HarmAssessment
    reversibility: ReversibilityLevel
    observability: ObservabilityAssessment
    containment: ContainmentMetrics = Field(default_factory=ContainmentMetrics)
    blast_radius: BlastRadius
    mcai: MCAIAssessment = Field(default_factory=MCAIAssessment)
    classification_indicators: list[ClassificationIndicator] = Field(default_factory=list)
    root_cause: RootCauseAnalysis | None = None
    control_performance: list[ControlPerformance] = Field(default_factory=list)
    timeline: list[TimelineEvent] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    notifications: Notifications = Field(default_factory=Notifications)
    corrective_actions_required: bool = True
    corrective_actions: list[CorrectiveAction] = Field(default_factory=list)
    revalidation: str = ""
    closure_rationale: str | None = None
    lifecycle_override: LifecycleOverride | None = None
    severity_result: SeverityAssessment | None = None
    crosswalks: Crosswalks = Field(default_factory=Crosswalks)
    extensions: dict[str, object] = Field(
        default_factory=dict,
        description="Namespaced hook for organization-specific policy; public core does not interpret it.",
    )

    @field_validator("boundaries_crossed")
    @classmethod
    def validate_boundaries(cls, values: list[BoundaryType]) -> list[BoundaryType]:
        if not values:
            raise ValueError("at least one boundary value is required; use 'none' for B0")
        if len(values) != len(set(values)):
            raise ValueError("boundaries_crossed must not contain duplicates")
        if BoundaryType.NONE in values and len(values) > 1:
            raise ValueError("B0/none cannot be combined with crossed boundaries")
        return values

    @field_validator("classification_indicators")
    @classmethod
    def unique_indicators(cls, values: list[ClassificationIndicator]) -> list[ClassificationIndicator]:
        if len(values) != len(set(values)):
            raise ValueError("classification_indicators must not contain duplicates")
        return values

    @model_validator(mode="after")
    def normalize_and_validate(self) -> "Incident":
        object.__setattr__(self, "timeline", sorted(self.timeline, key=lambda event: event.timestamp))
        evidence_ids = [item.id for item in self.evidence]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("evidence ids must be unique")
        known_evidence = set(evidence_ids)
        referenced = {
            ref
            for event in self.timeline
            for ref in event.evidence_refs
        } | {
            ref
            for action in self.corrective_actions
            for ref in action.verification_evidence
        }
        unknown = referenced - known_evidence
        if unknown:
            raise ValueError(f"unknown evidence references: {', '.join(sorted(unknown))}")
        if self.lifecycle_status == LifecycleState.CLOSED and self.lifecycle_override is None:
            errors: list[str] = []
            if self.root_cause is None:
                errors.append("root cause must be recorded (use 'unknown' when appropriate)")
            if not self.containment.documentation.strip():
                errors.append("containment documentation is required")
            if self.corrective_actions_required and not self.corrective_actions:
                errors.append("required corrective actions must be assigned")
            if any(not action.owner.strip() for action in self.corrective_actions):
                errors.append("every corrective action must have an owner")
            if not (self.closure_rationale and self.closure_rationale.strip()):
                errors.append("closure rationale is required")
            if errors:
                raise ValueError("CLOSED lifecycle requirements not met: " + "; ".join(errors))
        return self


Incident.model_rebuild()
