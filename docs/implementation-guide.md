# Implementation guide

## Architecture

MQ-AICIR is an isolated Python 3.12 package because the parent repository is a static Cloudflare website with no application or Python architecture to extend. The package does not modify or depend on the website build.

```text
JSON / CLI / local UI
        ↓
Pydantic Incident model ←→ Draft 2020-12 JSON Schema
        ↓
Severity rules · containment metrics · lifecycle gates
        ↓
Redacted Markdown / escaped HTML · crosswalk suggestions
```

Dependencies are limited to Pydantic v2, Typer, Jinja2, and PyYAML. The web interface uses Python's standard-library HTTP server to avoid adding a web framework. `pytest`, `jsonschema`, and coverage support are development-only.

## Install

```bash
cd ai_incident
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
```

## CLI

```bash
mq-aicir new incident.json --id MQ-2026-0042 --title "Credential boundary event" --system "Research Agent"
mq-aicir validate incident.json
mq-aicir classify incident.json
mq-aicir classify incident.json --write
mq-aicir summary incident.json
mq-aicir report incident.json --format markdown --output incident.md
mq-aicir report incident.json --format html --output incident.html
mq-aicir transition incident.json TRIAGE
mq-aicir serve --directory ./incidents --port 8765
```

Input JSON is bounded to 10 MiB and must be a regular `.json` file. Output suffixes are command-specific, existing symlink targets are rejected, and incident JSON writes are atomic. The CLI does not evaluate user expressions or execute incident content.

## Python API

```python
from pathlib import Path

from mqaicir.classification.severity import classify_severity
from mqaicir.io import load_incident
from mqaicir.reporting import render_markdown

incident = load_incident(Path("incident.json"))
result = classify_severity(incident)
report = render_markdown(incident)
```

Use `model_dump(mode="json")` for interoperable records. Construct or update through `Incident.model_validate(...)` so semantic checks, timeline sorting, calculated containment fields, reference integrity, and closure gates run.

## Schema generation

The Pydantic model is canonical for runtime validation. Generate the committed interoperability artifact with:

```bash
.venv/bin/python scripts/generate_schema.py
```

The script adds the Draft 2020-12 URI, stable `$id`, semantic version, taxonomy descriptions, and a valid example. CI/tests check the schema itself and every synthetic record with `jsonschema.Draft202012Validator`.

The `$id` is an identifier. It does not claim that `maplequanta.ca` currently hosts the schema. Deploying the file at that URL is a separate publishing decision.

## Local interface

The interface lists incidents, supplies structured taxonomy selectors, shows vector, timeline, authority, boundary, severity rationale, containment, controls, and corrective actions, and aggregates the requested dashboard measures.

Security properties:

- binds only to `127.0.0.1`;
- accepts only loopback `Host` values to reduce DNS-rebinding exposure;
- has a 1 MiB form limit and bounded field count;
- uses validated incident IDs as filenames and verifies the resolved parent;
- applies HTML escaping and report redaction;
- emits a restrictive Content Security Policy and no-store response headers; and
- suppresses request logging because paths and incident IDs can be sensitive.

It has no authentication, concurrency control, audit identity, TLS, or multi-user authorization. Do not publish or reverse-proxy it. Integrate the typed core into an existing authenticated case-management system for shared production use.

## Custom severity policy

Copy `config/severity_rules.yaml` to a controlled policy repository, retain the small supported condition language, use stable rule IDs, and run regression fixtures. Pass it with `--rules`. Do not place private assessor calibration in the public package.

## Extensions

The `extensions` object accepts organization-specific, namespaced JSON-compatible values. Recommended keys resemble `ca.example.incident_policy` rather than generic names. The public core stores but does not interpret extensions.

Avoid putting executable templates, code, query expressions, secrets, or raw forensic payloads in extensions. A consuming application must validate its own extension schema separately.

## Version compatibility and migration

Every record declares exact framework name and version. Version 1.0 code rejects a record that claims another version. `mqaicir.migrations.REGISTRY` is intentionally empty in the initial release. A future migration should:

1. preserve the original record and digest;
2. validate the source version with its own model/schema;
3. transform explicitly and deterministically;
4. record actor, timestamp, source/target versions, migration code version, and material interpretation changes;
5. validate against the target schema; and
6. never overwrite historical classification without an audit trail.

## Testing and release checks

```bash
.venv/bin/pytest
.venv/bin/python scripts/generate_schema.py
.venv/bin/mq-aicir validate examples/incidents/01-indirect-prompt-injection.json
.venv/bin/mq-aicir report examples/incidents/01-indirect-prompt-injection.json --format html --output /tmp/mq-aicir-example.html
```

Before a release, also review external framework versions, public/private content boundaries, redaction patterns, dependency vulnerabilities, organization-specific rule calibration, legal language, and the schema diff.

## Integration limits

MQ-AICIR does not provide a database, evidence vault, identity provider, notification service, legal decision engine, or multi-tenant authorization system. These belong in the deployment environment. The framework provides deterministic records and services that such systems can call.

