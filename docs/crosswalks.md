# External framework crosswalks

MQ-AICIR crosswalks are informative relationships. They do not establish exact equivalence, conformity, certification, legal coverage, or compliance. External frameworks have different purposes, scopes, units of analysis, and change cadences.

Machine-readable sources are in `config/crosswalks/`; typed suggestion modules are in `mqaicir.crosswalks`. Suggested references include a source version and verification date and can be copied into an incident only after analyst review.

## Shared AI Findings Exchange (SAFE)

SAFE is labelled `draft / RFC / evolving`. The checked proposal describes a Shared AI Findings Exchange for confidential collection and analysis of incidents and near misses, affected-party notification, evidence preservation, operating-stack review, and incident-driven corrective controls.

MQ-AICIR maps:

- event states to incident/near-miss learning concepts;
- its evidence and timeline model to preservation concepts;
- authority, boundaries, root cause, control performance, and observability to operating-stack review;
- structured notification assessment to notification workflows; and
- corrective actions and revalidation to lessons-to-controls workflows.

MQ-AICIR does not embed the proposal's notification timelines as legal or universal deadlines. SAFE had no stable release identifier when checked.

## MITRE ATLAS

ATLAS is a living knowledge base of adversary tactics and techniques against AI-enabled systems. MQ-AICIR uses ATLAS only for applicable attack mechanism or technique context. ATLAS does not determine whether an event is `E2` or `E3`, whether an action was authorized, or what MQ-AICIR severity applies.

Verified mappings in the 1.0 crosswalk include:

| MQ-AICIR fact | ATLAS identifier | Technique |
|---|---|---|
| prompt injection | AML.T0051 | LLM Prompt Injection |
| indirect prompt injection | AML.T0051.001 | LLM Prompt Injection: Indirect |
| agent tool action | AML.T0053 | AI Agent Tool Invocation |
| tool injection/poisoning | AML.T0110 | AI Agent Tool Poisoning |
| tool-mediated exfiltration | AML.T0086 | Exfiltration via AI Agent Tool Invocation |

Not every incident has an ATLAS mapping. An empty array is preferable to an invented identifier.

## NIST

The NIST crosswalk uses two complementary sources:

- SP 800-61 Rev. 3 frames cybersecurity incident response as a CSF 2.0 Community Profile across cybersecurity risk management; and
- AI RMF 1.0 organizes AI risk activity through GOVERN, MAP, MEASURE, and MANAGE.

MQ-AICIR governance/ownership maps informatively to GOVERN; system, boundary, asset, affected-party, and harm context to MAP; evidence, observability, time metrics, and controls to MEASURE; and containment, severity, remediation, and revalidation to MANAGE. Its timeline supports detection, response, containment, recovery, and learning records relevant to SP 800-61 Rev. 3.

The mapping does not claim that an incident record implements all NIST outcomes.

## OECD

The OECD terminology distinguishes actual-harm AI incidents from potential-harm AI hazards within its defined harm scope. MQ-AICIR retains the same essential distinction through separate realized and potential harm, while adding near-miss and boundary-violation event states for operational assurance.

- `E0` and some `E1/E2` records may relate to the OECD AI hazard concept.
- `E3/E4` records with realized harm may relate to the OECD AI incident concept.

The relationship remains conditional because MQ-AICIR covers operational, security, financial, privacy, legal, and third-party consequences that may not all fall within the OECD definition's specified harm scope.

## Maintenance

When updating a crosswalk:

1. use the current primary publisher source;
2. record exact content version/date and verification date;
3. verify every identifier against the versioned source;
4. describe relationship and limitations rather than writing “equivalent to”;
5. add regression tests; and
6. do not reinterpret historical incident crosswalks silently.

See [external-framework-versions.md](external-framework-versions.md) for the sources used by MQ-AICIR 1.0.

