# Intervention and containment metrics

MQ-AICIR reuses the intervention concepts in Maple Quanta Agentic AI Containment Assurance.

## Intervention Time

`Ti = Tdetection + Tdecision + Tenforcement`

- Detection Time begins when unauthorized behaviour starts and ends when the organization or preventive system detects it.
- Decision Time covers triage and authorization of an effective response.
- Enforcement Time ends when the selected control actually constrains the agent or pathway.

All three components are required to calculate Intervention Time. Zero is a valid measured value; missing is `null`. MQ-AICIR never treats a missing value as zero and overwrites any supplied total with the calculated component sum.

## Damage Time

Damage Time (`TD`) is the shortest credible time between initiation of unauthorized behaviour and the first material or irreversible consequence for the defined scenario. It is scenario-specific. A later, more severe consequence does not replace the earliest material pathway without explanation.

## Containment Margin

Where timing is meaningful:

`CM = TD / Ti`

| Result | Interpretation |
|---|---|
| CM > 1 | Effective intervention occurred faster than the defined damage pathway. |
| CM = 1 | There is no operational timing margin. Measurement uncertainty can dominate. |
| CM < 1 | Damage can occur faster than effective intervention. |

CM is not a probability, safety score, control grade, or guarantee. It applies only to the recorded pathway and controls.

## Required non-applicability cases

MQ-AICIR does not calculate CM when:

- Damage Time is unavailable;
- any Intervention Time component is unavailable;
- Intervention Time is zero and a meaningful finite ratio cannot be produced;
- the analyst marks the comparison as misleading; or
- the action is effectively instantaneous and prevention is the relevant control.

The model returns `containment_margin: null` and a clear `not_applicable_reason`. For instantaneous disclosure, irreversible authorization, or a synchronous external commit, a kill switch that runs after the action is not containment of that consequence. Deterministic pre-authorization, least privilege, transaction design, and egress prevention are the relevant controls.

## Measurement guidance

- Use timestamps from independent enforcement and target systems where possible.
- Record clock source, synchronization quality, and uncertainty in evidence or extensions.
- Measure effective enforcement, not the time a stop request was issued.
- Preserve retry and autonomous continuation behaviour.
- Define the damage pathway before using CM in executive reporting.
- Re-measure after corrective controls; do not assume configuration change equals effective intervention.

The first example has an Intervention Time of 402 seconds and no Damage Time, so CM is `N/A`. The blocked near-miss example uses synchronous prevention and explicitly suppresses CM even though all component values are zero.

