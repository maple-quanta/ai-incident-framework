# Rule-based severity model

MQ-AICIR assigns `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL` using transparent, deterministic rules in `config/severity_rules.yaml`. The engine does not add, average, weight, train on, or generate a score from taxonomy numbers.

## Output contract

Every result includes:

```json
{
  "severity": "HIGH",
  "triggered_rules": ["SR-HIGH-001"],
  "rationale": ["Unauthorized action crossed an external or third-party boundary."],
  "ruleset_version": "1.0.0"
}
```

The highest matched severity wins. All matched rules at that decisive severity are returned in configuration order. Lower-severity matches are not listed as decisive reasons. A public `LOW` fallback rule guarantees that severity cannot be emitted without a rule and rationale.

## Public escalation rules

Critical rules cover:

- `SR-CRITICAL-001` — realized `H4` harm.
- `SR-CRITICAL-002` — analyst-confirmed destructive action, unauthorized consequential authority, privilege crossing, and critical-infrastructure impact.
- `SR-CRITICAL-003` — cross-tenant compromise with material or greater realized harm.
- `SR-CRITICAL-004` — major or greater, irreversible third-party harm.
- `SR-CRITICAL-005` — analyst-confirmed autonomous offensive cyber activity with unauthorized execution.
- `SR-CRITICAL-006` — credential propagation that produces broad privileged access.
- `SR-CRITICAL-007` — critical action, no preventive control, and a meaningful Containment Margin below one.

High rules cover:

- unauthorized external action;
- unauthorized consequential authority across a privilege boundary;
- persistent unauthorized access;
- confirmed sensitive-data exposure;
- material production impact;
- approval bypass of an executed, externalized, or authorized consequential action;
- major realized harm.

Medium rules cover:

- boundary violation;
- material realized harm;
- any unauthorized authority exercise;
- near miss with major or severe credible potential harm;
- weak or unobservable operation;
- a meaningful Containment Margin below one.

Low is the explicit fallback when no higher public rule matches.

## Configuration language

Rules contain an ID, severity, description, and an `all` list. The evaluator accepts only a fixed set of operators:

- `eq` — scalar equality;
- `contains` — membership in a collection;
- `intersects` — overlap between collections;
- `nonempty` — a value or collection exists;
- `lt` — numeric less-than, only when the value exists;
- `rank_gte` — ordinal comparison against a named, fixed taxonomy scale.

There is no expression evaluator, template execution, import, script hook, or arbitrary Python. Malformed rule IDs, severities, operators, or duplicate IDs fail closed when the ruleset loads.

## Analyst calibration

The public rules are a governance baseline, not universal legal or risk thresholds. Organizations should calibrate rules with security, safety, privacy, legal, operational, human-rights, and sector experts. A custom YAML path can be supplied to `mq-aicir classify --rules ...`.

Private rules should remain in the organization's controlled policy repository when they reveal client thresholds, proprietary assessor calibration, or confidential test logic. They should retain stable IDs, semantic ruleset versions, change approval, regression fixtures, and documented rationale.

## Change control

A severity result is reproducible only with the incident record and exact ruleset version. Changing a ruleset must not silently overwrite a prior decision. Case-management integrations should preserve the earlier result, actor, timestamp, ruleset digest, and reason for reclassification.

Severity is operational prioritization. It does not establish legal reportability, negligence, liability, or external-framework compliance.

