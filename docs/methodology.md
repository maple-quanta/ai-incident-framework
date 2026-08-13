# MQ-AICIR methodology

## Purpose

The Maple Quanta AI Incident Classification & Reporting Framework (MQ-AICIR) makes events involving agentic AI systems classifiable, comparable, auditable, and actionable. It covers credible hazards, near misses, boundary violations, realized incidents, and serious or systemic outcomes.

The method is designed around a central observation: loss of information is only one possible consequence of agentic activity. An agent may exercise unauthorized authority without stealing data; cross an evaluation boundary without immediate harm; commit a reversible financial action; create persistent infrastructure; affect a third party; or act so quickly that reactive containment is irrelevant. Those differences must remain visible.

MQ-AICIR is a Maple Quanta technical assurance and governance framework. It is not an international standard, regulatory certification, legal opinion, or automated determination that an external framework applies.

## Unit of analysis

The unit of analysis is a recordable event or credible failure pathway involving the development, use, orchestration, tooling, environment, or malfunction of one or more AI systems. The record may begin before all facts are known. Unknown, pending, and not-assessed states are preferable to unsupported conclusions.

The incident profile is:

`I = (E, A, B, X, H, R, O, C)`

| Dimension | Question |
|---|---|
| E — Event State | What happened: hazard, near miss, boundary violation, incident, or serious/systemic incident? |
| A — Authority Exercised | What action class was authorized, actually exercised, and exercised without authorization in this context? |
| B — Boundary Crossed | Which policy, data, tool, identity, privilege, network, tenant, evaluation, or third-party boundary was crossed? |
| X — Asset Affected | Which data, identity, model, tool, code, infrastructure, financial, operational, human, rights, physical, critical-infrastructure, or third-party asset was affected? |
| H — Harm | What harm was realized, and what greater harm remained credibly possible? |
| R — Reversibility | Can the consequence be undone, and with what residual effects? |
| O — Observability | Can the consequential behaviour be independently attributed and reconstructed? |
| C — Containment | Could detection, decision, and enforcement stop the defined damage pathway in time? |

The vector is never averaged. A profile such as high authority, credential and privilege boundary crossings, no realized harm, major potential harm, operator reversibility, and weak observability has a risk shape that an average would obscure.

## Classification workflow

1. Preserve volatile evidence and assign a handling marking before broad distribution.
2. Define the AI system and assurance boundary in effect at the time.
3. Establish the event state from facts, not intent or the operator's belief that a target was simulated.
4. Record authorized, actually exercised, and unauthorized authority. Authorization is contextual: the same authority class can be authorized for one target and unauthorized for another.
5. Select every crossed boundary and affected asset. `B0` is used only when no boundary was crossed.
6. Assess realized and credible potential harm separately.
7. Assess reversibility and residual consequence.
8. Assess observability from independent evidence, including missing sources and tamper risk. `O0` is best and `O4` is worst.
9. Calculate Intervention Time and, only where meaningful, Containment Margin.
10. Record structured root cause, contributing factors, expected and observed control performance, and corrective actions.
11. Run the deterministic severity rules and retain decisive rule IDs and rationale.
12. Assess notifications with legal, privacy, contractual, security, and affected-party stakeholders. Do not automate the legal conclusion.
13. Revalidate corrective controls before closure or record an accountable exception override.

## Event state and severity are different

Event State describes what kind of event occurred. Severity describes the operational escalation required under explicit rules. An `E2` boundary violation can be `HIGH` because an unauthorized external action occurred even where realized harm is `H0`. An `E1` near miss can require meaningful escalation when potential harm was major and only a deterministic preventive control avoided consequence.

Similarly, `E4` does not establish a jurisdiction-specific legal serious-incident classification. That assessment is recorded separately with the external framework, status, and notes.

## Analyst-attested indicators

Some escalation conditions cannot be derived safely from taxonomy codes alone. For example, `EXECUTE` does not prove destructive action, and a credential boundary does not prove broad privileged propagation. MQ-AICIR therefore uses typed `classification_indicators` for analyst-attested facts such as `destructive_action`, `approval_bypass`, `persistent_unauthorized_access`, and `preventive_control_absent`.

Indicators are evidence-backed inputs to public rules. They are not model-generated scores. Reports expose the resulting rule rationale, and incident evidence should support each material indicator.

## Feedback to containment assurance

MQ-AICIR complements Maple Quanta Agentic AI Containment Assurance:

```text
Containment Assurance
        ↓
      Deploy
        ↓
     Observe
        ↓
 Incident / Near Miss
        ↓
   Classification
        ↓
 Root Cause Analysis
        ↓
 Corrective Controls
        ↓
    Revalidation
        ↓
 Re-Assurance
```

The shared vocabulary is intentional:

- Authority describes action classes and delegated operational power.
- MCAI compares expected maximum credible impact before deployment with demonstrated capability after the event.
- Intervention Time is Detection Time plus Decision Time plus Enforcement Time.
- Damage Time is the shortest credible time to first material or irreversible consequence.
- Containment Margin compares the damage pathway with effective intervention only where the ratio is meaningful.
- Observability asks whether consequential behaviour can be independently reconstructed.

The incident framework does not duplicate or redefine private containment tests. It provides evidence that informs re-assurance.

## Public core and organization policy

The public core can include taxonomy, schema, public severity rules, report format, synthetic examples, crosswalk architecture, and methodology. It intentionally excludes adversarial playbooks, client-specific thresholds, private exploit procedures, assessor calibration, proprietary engagement scoring, and confidential control tests.

Organizations can add namespaced data under `extensions`, supply a separate severity rules file, and maintain private evidence/control catalogs. The public engine does not dynamically execute extension data or user-provided expressions.

## Interpretation discipline

- Classify from evidence and explicitly identify uncertainty.
- Do not infer authorization from technical ability.
- Do not infer harmlessness from a blocked outcome.
- Do not infer legal reportability from MQ-AICIR event state or severity.
- Do not claim compliance or exact equivalence through a crosswalk.
- Reassess the record as facts change; preserve revision history in the surrounding case-management system.

