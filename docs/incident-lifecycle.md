# Incident lifecycle

## States

| State | Purpose |
|---|---|
| DRAFT | Initial record; facts may be incomplete. |
| TRIAGE | Validate the signal, establish handling, assign ownership, and make immediate escalation decisions. |
| ACTIVE | Response activity is ongoing and the event may still be developing. |
| CONTAINED | Effective containment has stopped the active pathway; investigation may continue. |
| INVESTIGATION | Reconstruct events, preserve evidence, assess impact, and establish causes. |
| REMEDIATION | Implement corrective controls and recovery actions. |
| REVALIDATION | Test that corrective controls operate under credible recurrence scenarios. |
| CLOSED | Closure gates are satisfied or an accountable exception is recorded. |

## Default transitions

```text
DRAFT -> TRIAGE
TRIAGE -> ACTIVE | CONTAINED
ACTIVE -> CONTAINED | INVESTIGATION
CONTAINED -> INVESTIGATION | REMEDIATION
INVESTIGATION -> REMEDIATION | ACTIVE
REMEDIATION -> REVALIDATION | ACTIVE
REVALIDATION -> CLOSED | REMEDIATION
```

Returning to `ACTIVE` represents recurrence or discovery that containment was ineffective. Returning from `REVALIDATION` to `REMEDIATION` represents a failed test. Closed records do not transition in the 1.0 core; reopening should create an auditable case-management event and a new active revision under organization policy.

## Closure gates

Without an exception override, `CLOSED` requires:

- a structured primary root cause, including explicit `unknown` where the investigation could not determine one;
- non-empty containment documentation;
- corrective actions where `corrective_actions_required` is true;
- an owner for every corrective action; and
- a closure rationale.

Completion of every corrective action is not universally required for administrative incident closure because long-term remediation may continue in a governed risk process. The closure rationale must explain any remaining open or accepted-risk action, and organization policy can impose stricter gates.

## Exception override

An override records a responsible person, timezone-aware timestamp, and rationale. It can authorize an otherwise invalid transition or bypass closure gates. The override is intentionally conspicuous in reports. It is an accountability mechanism, not a way to erase incomplete facts.

Use the CLI:

```bash
mq-aicir transition incident.json TRIAGE
mq-aicir transition incident.json CLOSED \
  --responsible-person "Accountable Executive" \
  --rationale "Emergency administrative closure; retrospective documentation due under case 1234."
```

The CLI writes the validated record atomically. In a multi-user system, add optimistic locking, record revision, actor identity, and an append-only audit log around this core function.

