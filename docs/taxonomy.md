# MQ-AICIR taxonomy 1.0

All codes below are part of framework version 1.0.0. A future incompatible change requires a new semantic version and explicit migration.

## E — Event State

| Code | Label | Definition |
|---|---|---|
| E0 | Hazard | A credible failure pathway exists, but no event occurred. |
| E1 | Near Miss | A failure condition occurred or nearly occurred, but preventive or containment controls prevented consequential impact. |
| E2 | Boundary Violation | The AI system crossed a defined authorization, technical, security, organizational, or environmental boundary, whether or not harm occurred. |
| E3 | Incident | AI activity caused an actual adverse operational, security, financial, privacy, legal, human, or third-party consequence. |
| E4 | Serious/Systemic Incident | Severe, widespread, critical-infrastructure, physical, fundamental-rights, or potentially systemic consequences. |

`E4` does not automatically equal a jurisdiction's legal definition of a serious incident. Use `regulatory_serious_incident.status`, `framework`, and `notes` for that separate assessment.

## A — Authority Exercised

Multiple classes may apply.

| Class | Definition |
|---|---|
| READ | Obtain information. |
| RECOMMEND | Generate a proposed action or decision. |
| WRITE | Modify data, files, records, or configuration. |
| EXECUTE | Trigger a system action or code execution. |
| EXTERNALIZE | Communicate data or action outside the defined assurance boundary. |
| AUTHORIZE | Approve, initiate, or commit consequential actions. |

Every record has three lists:

- `authorized` — authority classes allowed in the relevant context.
- `actually_exercised` — authority demonstrated by the event.
- `unauthorized_exercised` — exercised authority not authorized for the purpose, target, scope, time, or conditions.

An authority class can appear in all three where, for example, `EXECUTE` was authorized in an evaluation but the same class was exercised against a real target. `unauthorized_exercised` must always be a subset of `actually_exercised`.

## B — Boundary Crossed

Records store the machine identifier while reports render the code and label.

| Code | Identifier | Label |
|---|---|---|
| B0 | `none` | None |
| B1 | `instruction_policy` | Instruction / Policy |
| B2 | `data` | Data |
| B3 | `tool` | Tool |
| B4 | `credential` | Identity / Credential |
| B5 | `privilege` | Privilege |
| B6 | `network` | Network / Environment |
| B7 | `tenant` | Tenant / Organizational |
| B8 | `evaluation_real_world` | Evaluation / Real World |
| B9 | `third_party` | Third Party / External |

Multiple boundaries may be selected. `B0` is exclusive. A token used from an evaluation against an actual external repository can be `B4`, `B5`, `B8`, and `B9` even if those crossings happen in one action.

## X — Asset Affected

Supported categories are `DATA`, `IDENTITY`, `MODEL`, `TOOL`, `CODE`, `INFRASTRUCTURE`, `FINANCIAL`, `OPERATIONS`, `HUMAN`, `RIGHTS`, `PHYSICAL`, `CRITICAL_INFRASTRUCTURE`, and `THIRD_PARTY`.

Each asset can record a contextual name, owner, `low|medium|high|critical` criticality, and description. Criticality is not converted into a weighted score. It is context available to rules and reviewers.

## H — Harm

| Code | Label |
|---|---|
| H0 | No Realized Harm |
| H1 | Negligible |
| H2 | Material |
| H3 | Major |
| H4 | Severe/Systemic |

`realized_level` records what occurred. `potential_level` records the greater credible outcome supported by the pathway and controls in place. Categories are confidentiality, integrity, availability, financial, privacy, legal, reputational, human safety, fundamental rights, environmental, critical infrastructure, and third party.

Potential harm is not a prediction and does not replace scenario analysis. Realized and potential values must never be collapsed into one value.

## R — Reversibility

| Code | Label | Definition |
|---|---|---|
| R0 | No persistent consequence | No meaningful persistent effect. |
| R1 | Automatically reversible | Existing technical controls automatically restore the system. |
| R2 | Operator reversible | Human intervention can fully restore the prior state. |
| R3 | Partially reversible | Recovery is possible but leaves cost, delay, residual exposure, third-party consequence, or another permanent effect. |
| R4 | Irreversible | The consequence cannot realistically be undone. |

Examples of `R4` include public disclosure of a secret, a completed non-recallable external transfer, irreversible physical harm, unrecoverable deletion, and a consequential third-party action that cannot be recalled.

## O — Observability

| Code | Label | Meaning |
|---|---|---|
| O0 | Fully reconstructed | A complete, independently supported reconstruction is available. |
| O1 | Strong | Material actions and decisions are attributable with only minor gaps. |
| O2 | Partial | Important evidence exists but some material gaps remain. |
| O3 | Weak | Reconstruction depends heavily on incomplete, agent-controlled, or indirect evidence. |
| O4 | Unobservable | Consequential behaviour cannot be reliably reconstructed. |

Unlike most dimensions, **a larger Observability number is worse**. Evidence sources, missing evidence, and tamper risk must be recorded rather than inferred from the code alone.

## C — Containment

Containment records Detection Time, Decision Time, Enforcement Time, calculated Intervention Time, Damage Time, optional Containment Margin, an explicit non-applicability reason, containment documentation, and the relevant preventive control. See [containment-metrics.md](containment-metrics.md).

## Blast Radius

| Code | Label |
|---|---|
| BR0 | Single action/session |
| BR1 | Single user/system |
| BR2 | Multiple organizational systems |
| BR3 | Organization-wide |
| BR4 | Multiple organizations / third parties |
| BR5 | Potentially systemic |

## Maximum Credible Agent Impact

| Code | Label |
|---|---|
| A0 | Informational |
| A1 | Local |
| A2 | Organizational |
| A3 | External / Significant |
| A4 | Critical |

The record keeps `pre_incident_assessed` and `post_incident_reassessed` values to compare expected consequence space with demonstrated capability.

## Root cause and contributing factors

Structured categories are:

`model_behavior`, `prompt_injection`, `indirect_prompt_injection`, `tool_injection`, `credential_exposure`, `excessive_privilege`, `network_misconfiguration`, `sandbox_failure`, `identity_failure`, `approval_bypass`, `logging_failure`, `monitoring_failure`, `human_error`, `unsafe_delegation`, `agent_to_agent_failure`, `supply_chain`, `model_configuration`, `orchestration_failure`, `data_poisoning`, `retrieval_poisoning`, `policy_failure`, `unknown`, and `other`.

One primary category and multiple contributing factors are supported. Free-text analysis supplements rather than replaces structure. `unknown` is an explicit recorded outcome and satisfies the root-cause closure gate; absence of root cause does not.

## Handling markings

`PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, and `RESTRICTED` are incident-level information handling markings. They do not substitute for jurisdiction-specific classification or records-management rules. Distribution and retention policy remain organization-defined.

