"""MQ-AICIR 1.0 taxonomy enumerations and display metadata."""

from __future__ import annotations

from enum import StrEnum


class EventState(StrEnum):
    HAZARD = "E0"
    NEAR_MISS = "E1"
    BOUNDARY_VIOLATION = "E2"
    INCIDENT = "E3"
    SERIOUS_SYSTEMIC_INCIDENT = "E4"


class AuthorityClass(StrEnum):
    READ = "READ"
    RECOMMEND = "RECOMMEND"
    WRITE = "WRITE"
    EXECUTE = "EXECUTE"
    EXTERNALIZE = "EXTERNALIZE"
    AUTHORIZE = "AUTHORIZE"


class BoundaryType(StrEnum):
    NONE = "none"
    INSTRUCTION_POLICY = "instruction_policy"
    DATA = "data"
    TOOL = "tool"
    CREDENTIAL = "credential"
    PRIVILEGE = "privilege"
    NETWORK = "network"
    TENANT = "tenant"
    EVALUATION_REAL_WORLD = "evaluation_real_world"
    THIRD_PARTY = "third_party"


class AssetType(StrEnum):
    DATA = "DATA"
    IDENTITY = "IDENTITY"
    MODEL = "MODEL"
    TOOL = "TOOL"
    CODE = "CODE"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    FINANCIAL = "FINANCIAL"
    OPERATIONS = "OPERATIONS"
    HUMAN = "HUMAN"
    RIGHTS = "RIGHTS"
    PHYSICAL = "PHYSICAL"
    CRITICAL_INFRASTRUCTURE = "CRITICAL_INFRASTRUCTURE"
    THIRD_PARTY = "THIRD_PARTY"


class HarmLevel(StrEnum):
    NONE = "H0"
    NEGLIGIBLE = "H1"
    MATERIAL = "H2"
    MAJOR = "H3"
    SEVERE_SYSTEMIC = "H4"


class HarmCategory(StrEnum):
    CONFIDENTIALITY = "confidentiality"
    INTEGRITY = "integrity"
    AVAILABILITY = "availability"
    FINANCIAL = "financial"
    PRIVACY = "privacy"
    LEGAL = "legal"
    REPUTATIONAL = "reputational"
    HUMAN_SAFETY = "human_safety"
    FUNDAMENTAL_RIGHTS = "fundamental_rights"
    ENVIRONMENTAL = "environmental"
    CRITICAL_INFRASTRUCTURE = "critical_infrastructure"
    THIRD_PARTY = "third_party"


class ReversibilityLevel(StrEnum):
    NO_PERSISTENT_CONSEQUENCE = "R0"
    AUTOMATICALLY_REVERSIBLE = "R1"
    OPERATOR_REVERSIBLE = "R2"
    PARTIALLY_REVERSIBLE = "R3"
    IRREVERSIBLE = "R4"


class ObservabilityLevel(StrEnum):
    FULLY_RECONSTRUCTED = "O0"
    STRONG = "O1"
    PARTIAL = "O2"
    WEAK = "O3"
    UNOBSERVABLE = "O4"


class BlastRadius(StrEnum):
    SINGLE_ACTION_SESSION = "BR0"
    SINGLE_USER_SYSTEM = "BR1"
    MULTIPLE_ORG_SYSTEMS = "BR2"
    ORGANIZATION_WIDE = "BR3"
    MULTIPLE_ORGANIZATIONS = "BR4"
    POTENTIALLY_SYSTEMIC = "BR5"


class MCAILevel(StrEnum):
    INFORMATIONAL = "A0"
    LOCAL = "A1"
    ORGANIZATIONAL = "A2"
    EXTERNAL_SIGNIFICANT = "A3"
    CRITICAL = "A4"


class Severity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class LifecycleState(StrEnum):
    DRAFT = "DRAFT"
    TRIAGE = "TRIAGE"
    ACTIVE = "ACTIVE"
    CONTAINED = "CONTAINED"
    INVESTIGATION = "INVESTIGATION"
    REMEDIATION = "REMEDIATION"
    REVALIDATION = "REVALIDATION"
    CLOSED = "CLOSED"


class HandlingClassification(StrEnum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class RootCauseCategory(StrEnum):
    MODEL_BEHAVIOR = "model_behavior"
    PROMPT_INJECTION = "prompt_injection"
    INDIRECT_PROMPT_INJECTION = "indirect_prompt_injection"
    TOOL_INJECTION = "tool_injection"
    CREDENTIAL_EXPOSURE = "credential_exposure"
    EXCESSIVE_PRIVILEGE = "excessive_privilege"
    NETWORK_MISCONFIGURATION = "network_misconfiguration"
    SANDBOX_FAILURE = "sandbox_failure"
    IDENTITY_FAILURE = "identity_failure"
    APPROVAL_BYPASS = "approval_bypass"
    LOGGING_FAILURE = "logging_failure"
    MONITORING_FAILURE = "monitoring_failure"
    HUMAN_ERROR = "human_error"
    UNSAFE_DELEGATION = "unsafe_delegation"
    AGENT_TO_AGENT_FAILURE = "agent_to_agent_failure"
    SUPPLY_CHAIN = "supply_chain"
    MODEL_CONFIGURATION = "model_configuration"
    ORCHESTRATION_FAILURE = "orchestration_failure"
    DATA_POISONING = "data_poisoning"
    RETRIEVAL_POISONING = "retrieval_poisoning"
    POLICY_FAILURE = "policy_failure"
    UNKNOWN = "unknown"
    OTHER = "other"


class ClassificationIndicator(StrEnum):
    """Analyst-attested facts used by transparent severity rules."""

    DESTRUCTIVE_ACTION = "destructive_action"
    CROSS_TENANT_COMPROMISE = "cross_tenant_compromise"
    AUTONOMOUS_OFFENSIVE_CYBER = "autonomous_offensive_cyber"
    CREDENTIAL_PROPAGATION = "credential_propagation"
    BROAD_PRIVILEGED_ACCESS = "broad_privileged_access"
    PERSISTENT_UNAUTHORIZED_ACCESS = "persistent_unauthorized_access"
    SENSITIVE_DATA_EXPOSURE = "sensitive_data_exposure"
    PRODUCTION_IMPACT = "production_impact"
    APPROVAL_BYPASS = "approval_bypass"
    EXTERNAL_ACTION = "external_action"
    CRITICAL_ACTION = "critical_action"
    PREVENTIVE_CONTROL_ABSENT = "preventive_control_absent"
    THIRD_PARTY_IMPACT = "third_party_impact"


EVENT_STATE_LABELS = {
    "E0": "Hazard",
    "E1": "Near Miss",
    "E2": "Boundary Violation",
    "E3": "Incident",
    "E4": "Serious/Systemic Incident",
}
EVENT_STATE_DEFINITIONS = {
    "E0": "A credible failure pathway exists, but no event occurred.",
    "E1": "A failure condition occurred or nearly occurred, but controls prevented consequential impact.",
    "E2": "The AI system crossed a defined authorization, technical, security, organizational, or environmental boundary.",
    "E3": "AI activity caused an actual adverse consequence.",
    "E4": "Severe, widespread, critical-infrastructure, physical, fundamental-rights, or potentially systemic consequences.",
}
AUTHORITY_LABELS = {
    "READ": "Obtain information",
    "RECOMMEND": "Generate a proposed action or decision",
    "WRITE": "Modify data, files, records, or configuration",
    "EXECUTE": "Trigger a system action or code execution",
    "EXTERNALIZE": "Communicate data or action outside the assurance boundary",
    "AUTHORIZE": "Approve, initiate, or commit consequential actions",
}
BOUNDARY_CODES = {
    "none": "B0",
    "instruction_policy": "B1",
    "data": "B2",
    "tool": "B3",
    "credential": "B4",
    "privilege": "B5",
    "network": "B6",
    "tenant": "B7",
    "evaluation_real_world": "B8",
    "third_party": "B9",
}
BOUNDARY_LABELS = {
    "none": "None",
    "instruction_policy": "Instruction / Policy",
    "data": "Data",
    "tool": "Tool",
    "credential": "Identity / Credential",
    "privilege": "Privilege",
    "network": "Network / Environment",
    "tenant": "Tenant / Organizational",
    "evaluation_real_world": "Evaluation / Real World",
    "third_party": "Third Party / External",
}
HARM_LABELS = {
    "H0": "No Realized Harm",
    "H1": "Negligible",
    "H2": "Material",
    "H3": "Major",
    "H4": "Severe/Systemic",
}
REVERSIBILITY_LABELS = {
    "R0": "No persistent consequence",
    "R1": "Automatically reversible",
    "R2": "Operator reversible",
    "R3": "Partially reversible",
    "R4": "Irreversible",
}
OBSERVABILITY_LABELS = {
    "O0": "Fully reconstructed",
    "O1": "Strong",
    "O2": "Partial",
    "O3": "Weak",
    "O4": "Unobservable",
}
BLAST_RADIUS_LABELS = {
    "BR0": "Single action/session",
    "BR1": "Single user/system",
    "BR2": "Multiple organizational systems",
    "BR3": "Organization-wide",
    "BR4": "Multiple organizations / third parties",
    "BR5": "Potentially systemic",
}
MCAI_LABELS = {
    "A0": "Informational",
    "A1": "Local",
    "A2": "Organizational",
    "A3": "External / Significant",
    "A4": "Critical",
}


def coded_boundary(value: BoundaryType | str) -> str:
    raw = value.value if isinstance(value, BoundaryType) else value
    return BOUNDARY_CODES[raw]


def label_for(value: StrEnum | str) -> str:
    raw = value.value if isinstance(value, StrEnum) else value
    for labels in (
        EVENT_STATE_LABELS,
        AUTHORITY_LABELS,
        BOUNDARY_LABELS,
        HARM_LABELS,
        REVERSIBILITY_LABELS,
        OBSERVABILITY_LABELS,
        BLAST_RADIUS_LABELS,
        MCAI_LABELS,
    ):
        if raw in labels:
            return labels[raw]
    return raw.replace("_", " ").title()
