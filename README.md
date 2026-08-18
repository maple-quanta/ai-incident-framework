# Maple Quanta AI Incident Classification & Reporting Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21988462.svg)](https://doi.org/10.5281/zenodo.21988462)

MQ-AICIR software release 1.0.1 is a typed, auditable framework for recording hazards, near misses, boundary violations, and incidents involving agentic AI systems. It complements Maple Quanta's Agentic AI Containment Assurance methodology.

Developed and maintained by [Maple Quanta Inc.](https://maplequanta.ca/), an independent Canadian AI, data science, and quantum technology advisory firm.

> An AI incident is not defined only by whether information was stolen. It must be understood through the authority exercised, the boundary crossed, the asset affected, the harm produced, the reversibility of the consequence, and the organization's ability to observe and contain it.

MQ-AICIR is a Maple Quanta technical assurance and governance framework. It is not an international standard, a regulatory certification, legal advice, or an automated compliance determination.

## ⚡ AI incidents unfold at machine speed. Is your incident response ready?

Before a conventional incident-response process even begins, an autonomous AI agent can cross boundaries, invoke tools, use credentials, create persistent resources, or affect third parties. To keep pace, AI incident records must be both human-readable and machine-readable.

- **For people:** Security teams, executives, auditors, and affected parties need immediate clarity about what happened, what was affected, and why the event matters.
- **For systems:** Software needs structured data to validate, classify, compare, route, and analyze incidents without relying on fragile heuristics or guesses derived from unstructured text.

A shared, interoperable framework bridges this gap. It supports rapid response, evidence preservation, cross-incident analysis, control improvement, and continuous organizational learning.

Traditional incident labels often hide the facts that matter for agentic systems: which delegated capability became action, whether an evaluation reached the real world, whether identity or privilege boundaries failed, whether damage was reversible, and whether intervention could beat the damage pathway. MQ-AICIR preserves those dimensions so incidents are comparable, explainable, and useful for control improvement.

## 🚀 Introducing MQ-AICIR 1.0

MQ-AICIR is the **Maple Quanta AI Incident Classification & Reporting Framework**, developed by Maple Quanta Inc. The current software release is 1.0.1 and implements the unchanged MQ-AICIR 1.0 incident-record format.

MQ-AICIR characterizes AI events across eight core dimensions:

- **Event State:** Was this a hazard, near miss, boundary violation, incident, or serious/systemic incident?
- **🔑 Authority Exercised:** What privileges or delegated capabilities did the agent use?
- **🚧 Boundary Crossed:** What authorization, technical, security, organizational, or external perimeter was crossed?
- **🎯 Asset Affected:** What systems, data, identities, code, infrastructure, people, or third parties were affected?
- **💥 Realized and Potential Harm:** What damage occurred, and what credible harm almost occurred?
- **🔄 Reversibility:** Can the consequence be undone automatically, manually, partially, or not at all?
- **👁️ Observability:** How clearly can the organization reconstruct and explain the behaviour?
- **🛑 Containment Ability:** How effectively can the organization detect, decide, enforce, and isolate before damage occurs?

### Deterministic, transparent, and interoperable

The complete incident profile remains visible across structured JSON, CLI output, local review views, and human-readable reports. Severity is determined through explicit rules rather than opaque AI-generated scores or arbitrary weighted averages. Every classification identifies the decisive rules and their rationale.

### Included in the open-source release

- 🏷️ Formal taxonomy and Draft 2020-12 JSON Schema
- 🐍 Strict, typed Python models
- ⚖️ Deterministic classification and containment metrics
- 📊 Reporting engine and command-line interface
- 💻 Loopback-only local review interface
- 🧪 Synthetic examples and automated tests
- 🌐 Apache-2.0-licensed public core designed for interoperability

Repository: [github.com/maple-quanta/ai-incident-framework](https://github.com/maple-quanta/ai-incident-framework)

## What is an AI incident?

MQ-AICIR uses five event states:

- `E0` Hazard — a credible failure pathway exists, but no event occurred.
- `E1` Near Miss — a failure condition occurred or nearly occurred, but controls prevented consequential impact.
- `E2` Boundary Violation — a defined authorization, technical, security, organizational, or environmental boundary was crossed, with or without harm.
- `E3` Incident — AI activity caused an adverse consequence.
- `E4` Serious/Systemic Incident — consequences are severe, widespread, physical, rights-affecting, critical-infrastructure-related, or potentially systemic.

`E4` is not automatically equivalent to any jurisdiction's legal definition of a serious incident. The separate `regulatory_serious_incident` assessment records that question without automating it.

## What is the incident vector?

Every record preserves:

`I = (E, A, B, X, H, R, O, C)`

- `E` — Event State
- `A` — Authority Exercised
- `B` — Boundary Crossed
- `X` — Asset Affected
- `H` — realized and potential Harm
- `R` — Reversibility
- `O` — Observability
- `C` — Containment

Reports render a profile such as:

`[E2 | EXECUTE, EXTERNALIZE | B4,B6,B9 | IDENTITY,CODE | H0/H3 | R2 | O1 | CM=N/A]`

The code is always accompanied by human-readable labels. For Observability, `O0` is best and `O4` is worst; a larger number means poorer observability.

## Why not use one risk score?

Averages erase dangerous shapes. High privilege plus weak observability is not made safe by a low value elsewhere. MQ-AICIR never averages taxonomy values and never produces an opaque AI-generated score. The full vector remains visible in JSON, CLI output, reports, exports, and the local UI.

## How is severity determined?

`LOW`, `MEDIUM`, `HIGH`, and `CRITICAL` are assigned by deterministic rules in `config/severity_rules.yaml`. The engine supports a small, non-executable condition language. It reports every decisive rule ID and rationale. Organization-specific thresholds can be supplied as a separate rules file without embedding private assessor calibration in the public core.

## Quick start

Python 3.12 or newer is required.

```bash
cd ai_incident
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/mq-aicir validate examples/incidents/01-indirect-prompt-injection.json
.venv/bin/mq-aicir classify examples/incidents/01-indirect-prompt-injection.json
.venv/bin/mq-aicir summary examples/incidents/01-indirect-prompt-injection.json
.venv/bin/mq-aicir report examples/incidents/01-indirect-prompt-injection.json --format markdown --output incident-report.md
```

Create a record:

```bash
.venv/bin/mq-aicir new incident.json --id MQ-2026-0042 --title "Boundary review" --system "Research Agent"
```

Run the loopback-only interface (no cloud service is required):

```bash
.venv/bin/mq-aicir serve --directory examples/incidents --port 8765
```

Open `http://127.0.0.1:8765`. The interface provides an incident table, structured taxonomy editor, detail views, full reports, and aggregate charts. It binds only to loopback, validates the `Host` header, emits restrictive browser headers, and does not log request values.

## How do I create a report?

Use the `report` command with `--format markdown` or `--format html`. Common API keys, bearer tokens, password assignments, and private-key blocks are redacted. HTML is autoescaped. Add conservative organization-specific patterns with repeated `--redact-pattern` options. Evidence objects should contain references to controlled evidence, never actual secrets.

## How does this relate to Agentic AI Containment Assurance?

MQ-AICIR reuses Authority, MCAI, Intervention Time, Damage Time, Containment Margin, and Observability. It turns operational evidence into the feedback loop:

```text
Containment Assurance -> Deploy -> Observe -> Incident / Near Miss
-> Classification -> Root Cause Analysis -> Corrective Controls
-> Revalidation -> Re-Assurance
```

Containment Margin is `Damage Time / Intervention Time` only where the ratio is meaningful. For effectively instantaneous actions, prevention is the relevant control and the record states why CM is not applicable.

## Public methodology vs organization-specific policy

The taxonomy, JSON Schema, public severity rules, report format, examples, crosswalk architecture, and methodology are suitable for a public core. Private attack playbooks, client thresholds, assessor calibration, engagement scoring, and confidential control tests belong in namespaced `extensions` or separate rules/configuration repositories. The core never evaluates extension data.

## Repository map

- `schemas/ai-incident-1.0.schema.json` — JSON Schema Draft 2020-12
- `src/mqaicir/models/` — Pydantic v2 record and taxonomy models
- `src/mqaicir/classification/` — severity, lifecycle, and containment logic
- `src/mqaicir/reporting/` — redacted Markdown and escaped HTML reports
- `src/mqaicir/crosswalks/` and `config/crosswalks/` — informative external mappings
- `src/mqaicir/web.py` — local structured editor and dashboard
- `examples/incidents/` — six synthetic records
- `tests/` — schema, model, classification, lifecycle, report, example, redaction, CLI, and web tests
- `docs/` — methodology and implementation guidance

## Data handling

Incident records may contain highly sensitive security, personal, contractual, and third-party information. Use the `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, or `RESTRICTED` handling marking; minimize collection; store evidence separately; apply access control and retention policy; and review reports before distribution. See `docs/evidence-guide.md` and `SECURITY.md`.

## Compatibility and versioning

The software release version and incident-record compatibility version are separate. Software release 1.0.1 continues to read and write MQ-AICIR 1.0 records whose `framework.version` is `1.0.0`, using the unchanged `schemas/ai-incident-1.0.schema.json`. MQ-AICIR 1.0 rejects records claiming another framework version instead of silently reinterpreting them. Future migrations belong in `mqaicir.migrations` and must produce a new validated record with an auditable migration note. See `docs/implementation-guide.md`.

## Citation

Citation metadata for this release is available in [`CITATION.cff`](CITATION.cff). It records the author, affiliation, ORCID, licence, repository, release version, and release date in Citation File Format 1.2.

## License

Licensed under the [Apache License 2.0](LICENSE). The license does not grant permission to use Maple Quanta Inc. trade names, trademarks, service marks, or product names except as allowed by the license.
