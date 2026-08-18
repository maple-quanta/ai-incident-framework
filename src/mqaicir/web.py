"""Dependency-free, loopback-only review UI for local incident files."""

from __future__ import annotations

import html
import statistics
from collections import Counter
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

from pydantic import ValidationError

from mqaicir._version import SOFTWARE_VERSION
from mqaicir.classification.severity import classify_severity
from mqaicir.io import MAX_INCIDENT_BYTES, load_incident, save_incident
from mqaicir.models.incident import Incident
from mqaicir.models.taxonomy import (
    AuthorityClass,
    BlastRadius,
    BoundaryType,
    ClassificationIndicator,
    EventState,
    HarmLevel,
    LifecycleState,
    MCAILevel,
    ObservabilityLevel,
    ReversibilityLevel,
    RootCauseCategory,
    coded_boundary,
    label_for,
)
from mqaicir.redaction import redact_text
from mqaicir.reporting import render_html
from mqaicir.scaffold import new_incident

MAX_FORM_BYTES = 1024 * 1024
ALLOWED_HOSTS = {"127.0.0.1", "localhost", "[::1]"}

CSS = """
:root{--ink:#14242b;--muted:#607078;--brand:#174f45;--brand2:#286f62;--paper:#fff;--wash:#f1f6f4;--line:#ccd9d5;--danger:#952f2f}*{box-sizing:border-box}body{margin:0;background:#e9f0ed;color:var(--ink);font:15px/1.45 system-ui,sans-serif}header{background:#103f37;color:#fff;padding:18px 28px}header a{color:#fff;text-decoration:none}nav{margin-top:8px}nav a{margin-right:18px}.page{max-width:1200px;margin:22px auto;padding:0 20px}.panel{background:#fff;border:1px solid var(--line);padding:22px;margin-bottom:18px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}.metric{background:var(--wash);border-left:4px solid var(--brand);padding:14px}.metric strong{font-size:1.45rem;display:block}.vector{font:14px/1.5 ui-monospace,monospace;background:#102e29;color:#e8fff8;padding:14px;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;display:block;overflow-x:auto}th,td{padding:9px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}th{background:var(--wash)}a{color:var(--brand2)}label{font-weight:650;display:block;margin-top:10px}input[type=text],input[type=datetime-local],select,textarea{width:100%;padding:9px;border:1px solid #9eafa9;background:#fff}textarea{min-height:100px}.checks{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:4px 12px}.checks label{font-weight:400;margin:0}.checks input{margin-right:6px}button,.button{display:inline-block;background:var(--brand);color:#fff;border:0;padding:10px 16px;text-decoration:none;cursor:pointer;margin-top:14px}.barrow{display:grid;grid-template-columns:180px 1fr 40px;gap:8px;align-items:center;margin:6px 0}.bar{height:18px;background:var(--brand2)}.error{border-left:5px solid var(--danger);background:#fff0f0;padding:12px;white-space:pre-wrap}.badge{font-weight:700}.muted{color:var(--muted)}details{margin:14px 0}h1,h2{line-height:1.2}h2{margin-top:1.8rem}@media(max-width:650px){.barrow{grid-template-columns:110px 1fr 30px}}
"""


def e(value: object) -> str:
    return html.escape(redact_text(str(value)), quote=True)


def layout(title: str, body: str) -> str:
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{e(title)} · MQ-AICIR</title><style>{CSS}</style></head><body>"
        "<header><strong>Maple Quanta AI Incident Classification &amp; Reporting Framework</strong>"
        "<nav><a href='/'>Dashboard</a><a href='/incidents'>Incidents</a><a href='/new'>New incident</a></nav></header>"
        f"<main class='page'>{body}</main></body></html>"
    )


def _option(value: str, label: str, current: str | None) -> str:
    selected = " selected" if value == current else ""
    return f"<option value='{e(value)}'{selected}>{e(label)}</option>"


def _select(name: str, values: list[tuple[str, str]], current: str | None) -> str:
    return f"<select name='{e(name)}'>" + "".join(_option(value, label, current) for value, label in values) + "</select>"


def _checks(name: str, values: list[tuple[str, str]], selected: set[str]) -> str:
    return "<div class='checks'>" + "".join(
        f"<label><input type='checkbox' name='{e(name)}' value='{e(value)}'{' checked' if value in selected else ''}>{e(label)}</label>"
        for value, label in values
    ) + "</div>"


def _bar_chart(title: str, counter: Counter[str]) -> str:
    maximum = max(counter.values(), default=1)
    rows = "".join(
        f"<div class='barrow'><span>{e(label)}</span><span class='bar' style='width:{count / maximum * 100:.1f}%'></span><strong>{count}</strong></div>"
        for label, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ) or "<p class='muted'>No data.</p>"
    return f"<section class='panel'><h2>{e(title)}</h2>{rows}</section>"


class IncidentRepository:
    def __init__(self, directory: Path):
        self.directory = directory.expanduser().resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        if not self.directory.is_dir():
            raise ValueError("incident repository must be a directory")

    def all(self) -> tuple[list[Incident], list[str]]:
        incidents: list[Incident] = []
        errors: list[str] = []
        for path in sorted(self.directory.glob("*.json")):
            try:
                incidents.append(load_incident(path))
            except (ValueError, ValidationError) as exc:
                errors.append(f"{path.name}: {exc}")
        return incidents, errors

    def find(self, incident_id: str) -> Incident | None:
        for incident in self.all()[0]:
            if incident.incident_id == incident_id:
                return incident
        return None

    def save(self, incident: Incident) -> None:
        safe_name = incident.incident_id + ".json"  # constrained by the model regex
        target = (self.directory / safe_name).resolve()
        if target.parent != self.directory:
            raise ValueError("invalid incident output path")
        save_incident(incident, target)


def dashboard(repository: IncidentRepository) -> str:
    incidents, errors = repository.all()
    severity = Counter((item.severity_result or classify_severity(item)).severity.value for item in incidents)
    boundaries = Counter(label_for(boundary) for item in incidents for boundary in item.boundaries_crossed if boundary != BoundaryType.NONE)
    authorities = Counter(authority.value for item in incidents for authority in item.authority.actually_exercised)
    roots = Counter(item.root_cause.primary_root_cause.value if item.root_cause else "not_recorded" for item in incidents)
    near_vs_incidents = Counter(
        "Near misses" if item.event_state == EventState.NEAR_MISS else "Incidents (E3/E4)" if item.event_state in {EventState.INCIDENT, EventState.SERIOUS_SYSTEMIC_INCIDENT} else "Other states"
        for item in incidents
    )
    intervention = [item.containment.intervention_time_seconds for item in incidents if item.containment.intervention_time_seconds is not None]
    credentials = sum(BoundaryType.CREDENTIAL in item.boundaries_crossed for item in incidents)
    external = sum(
        BoundaryType.THIRD_PARTY in item.boundaries_crossed or AuthorityClass.EXTERNALIZE in item.authority.actually_exercised
        for item in incidents
    )
    metrics = (
        "<section class='grid'>"
        f"<div class='metric'><strong>{len(incidents)}</strong>Total records</div>"
        f"<div class='metric'><strong>{credentials}</strong>Credential boundary</div>"
        f"<div class='metric'><strong>{external}</strong>External actions</div>"
        f"<div class='metric'><strong>{statistics.mean(intervention):.1f} s</strong>Average Intervention Time</div>" if intervention else
        "<section class='grid'>"
        f"<div class='metric'><strong>{len(incidents)}</strong>Total records</div>"
        f"<div class='metric'><strong>{credentials}</strong>Credential boundary</div>"
        f"<div class='metric'><strong>{external}</strong>External actions</div>"
        "<div class='metric'><strong>N/A</strong>Average Intervention Time</div>"
    )
    metrics += f"<div class='metric'><strong>{statistics.median(intervention):.1f} s</strong>Median Intervention Time</div></section>" if intervention else "<div class='metric'><strong>N/A</strong>Median Intervention Time</div></section>"
    error_html = f"<div class='error'>{e(chr(10).join(errors))}</div>" if errors else ""
    return layout(
        "Dashboard",
        f"<section class='panel'><h1>Incident dashboard</h1><p class='muted'>Local records in {e(repository.directory)}</p>{error_html}</section>"
        + metrics
        + _bar_chart("Incidents by severity", severity)
        + _bar_chart("Incidents by boundary", boundaries)
        + _bar_chart("Incidents by authority type", authorities)
        + _bar_chart("Near misses vs incidents", near_vs_incidents)
        + _bar_chart("Incidents by root cause", roots),
    )


def incident_list(repository: IncidentRepository) -> str:
    incidents, errors = repository.all()
    rows = "".join(
        "<tr>"
        f"<td><a href='/incident/{quote(item.incident_id)}'>{e(item.incident_id)}</a></td>"
        f"<td>{e(item.occurred_at.date())}</td><td>{e(item.event_state.value)} — {e(label_for(item.event_state))}</td>"
        f"<td class='badge'>{e((item.severity_result or classify_severity(item)).severity.value)}</td>"
        f"<td>{e(item.system.name)}{(' / ' + e(item.system.model)) if item.system.model else ''}</td>"
        f"<td>{e(coded_boundary(item.boundaries_crossed[0]))} — {e(label_for(item.boundaries_crossed[0]))}</td>"
        f"<td>{e(item.harm.realized_level.value)} / {e(item.harm.potential_level.value)}</td><td>{e(item.lifecycle_status.value)}</td></tr>"
        for item in incidents
    ) or "<tr><td colspan='8'>No incidents found.</td></tr>"
    error_html = f"<div class='error'>{e(chr(10).join(errors))}</div>" if errors else ""
    return layout("Incidents", f"<section class='panel'><h1>Incidents</h1>{error_html}<table><thead><tr><th>ID</th><th>Date</th><th>Event state</th><th>Severity</th><th>Model/system</th><th>Principal boundary</th><th>Harm</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></section>")


def editor(incident: Incident | None = None, error: str | None = None) -> str:
    item = incident or new_incident("MQ-2026-0001")
    actual = {value.value for value in item.authority.actually_exercised}
    authorized = {value.value for value in item.authority.authorized}
    unauthorized = {value.value for value in item.authority.unauthorized_exercised}
    boundaries = {value.value for value in item.boundaries_crossed}
    indicators = {value.value for value in item.classification_indicators}
    authority_values = [(value.value, f"{value.value} — {label_for(value)}") for value in AuthorityClass]
    boundary_values = [(value.value, f"{coded_boundary(value)} — {label_for(value)}") for value in BoundaryType]
    indicator_values = [(value.value, label_for(value)) for value in ClassificationIndicator]
    occurred = item.occurred_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M") if item.occurred_at.tzinfo else item.occurred_at.strftime("%Y-%m-%dT%H:%M")
    error_html = f"<div class='error'>{e(error)}</div>" if error else ""
    body = f"""
<section class='panel'><h1>{'Edit ' + e(item.incident_id) if incident else 'Create incident'}</h1>{error_html}
<form method='post' action='/save'>
<div class='grid'><div><label>Incident ID</label><input name='incident_id' required pattern='MQ-[0-9]{{4}}-[A-Z0-9-]+' value='{e(item.incident_id)}'></div>
<div><label>Occurred at (UTC)</label><input type='datetime-local' name='occurred_at' required value='{e(occurred)}'></div></div>
<label>Title</label><input name='title' required value='{e(item.title)}'><label>Description</label><textarea name='description'>{e(item.description)}</textarea>
<div class='grid'><div><label>System name</label><input name='system_name' required value='{e(item.system.name)}'></div><div><label>Model</label><input name='model' value='{e(item.system.model or '')}'></div>
<div><label>Lifecycle</label>{_select('lifecycle_status', [(v.value, v.value) for v in LifecycleState], item.lifecycle_status.value)}</div>
<div><label>Event state</label>{_select('event_state', [(v.value, f'{v.value} — {label_for(v)}') for v in EventState], item.event_state.value)}</div>
<div><label>Realized harm</label>{_select('realized_harm', [(v.value, f'{v.value} — {label_for(v)}') for v in HarmLevel], item.harm.realized_level.value)}</div>
<div><label>Potential harm</label>{_select('potential_harm', [(v.value, f'{v.value} — {label_for(v)}') for v in HarmLevel], item.harm.potential_level.value)}</div>
<div><label>Reversibility</label>{_select('reversibility', [(v.value, f'{v.value} — {label_for(v)}') for v in ReversibilityLevel], item.reversibility.value)}</div>
<div><label>Observability (larger is worse)</label>{_select('observability', [(v.value, f'{v.value} — {label_for(v)}') for v in ObservabilityLevel], item.observability.level.value)}</div>
<div><label>Blast radius</label>{_select('blast_radius', [(v.value, f'{v.value} — {label_for(v)}') for v in BlastRadius], item.blast_radius.value)}</div>
<div><label>Post-incident MCAI</label>{_select('mcai', [('', 'Not assessed')] + [(v.value, f'{v.value} — {label_for(v)}') for v in MCAILevel], item.mcai.post_incident_reassessed.value if item.mcai.post_incident_reassessed else '')}</div></div>
<details open><summary><strong>Authority</strong></summary><label>Authorized</label>{_checks('authorized', authority_values, authorized)}<label>Actually exercised</label>{_checks('actual', authority_values, actual)}<label>Unauthorized exercised</label>{_checks('unauthorized', authority_values, unauthorized)}</details>
<details open><summary><strong>Boundaries crossed</strong></summary><p class='muted'>B0/none must be selected alone.</p>{_checks('boundaries', boundary_values, boundaries)}</details>
<details><summary><strong>Classification indicators</strong></summary><p class='muted'>Select only analyst-confirmed facts. These are inputs to transparent rules.</p>{_checks('indicators', indicator_values, indicators)}</details>
<div class='grid'><div><label>Primary root cause</label>{_select('root_cause', [('', 'Not recorded')] + [(v.value, label_for(v)) for v in RootCauseCategory], item.root_cause.primary_root_cause.value if item.root_cause else '')}</div>
<div><label>Containment documentation</label><textarea name='containment_documentation'>{e(item.containment.documentation)}</textarea></div></div>
<button type='submit'>Validate and save</button></form></section>"""
    return layout("Incident editor", body)


def detail(item: Incident) -> str:
    severity = item.severity_result or classify_severity(item)
    cm = "N/A" if item.containment.containment_margin is None else f"{item.containment.containment_margin:.2f}"
    vector = (
        f"[{item.event_state.value} | {', '.join(v.value for v in item.authority.actually_exercised) or 'NONE'} | "
        f"{','.join(coded_boundary(v) for v in item.boundaries_crossed)} | "
        f"{','.join(v.type.value for v in item.assets_affected) or 'NONE'} | {item.harm.realized_level.value}/{item.harm.potential_level.value} | "
        f"{item.reversibility.value} | {item.observability.level.value} | CM={cm}]"
    )
    timeline = "".join(f"<tr><td>{e(v.timestamp)}</td><td>{e(v.event_type.value)}</td><td>{e(v.actor)}</td><td>{e(v.description)}</td></tr>" for v in item.timeline) or "<tr><td colspan='4'>No events</td></tr>"
    controls = "".join(f"<li><strong>{e(v.control_id)} — {e(v.control_name)}</strong>: {e(v.status.value)}<br>Expected: {e(v.expected_behavior)}<br>Observed: {e(v.observed_behavior)}</li>" for v in item.control_performance) or "<li>None recorded</li>"
    actions = "".join(f"<li><strong>{e(v.action_id)}</strong> [{e(v.priority.value)} / {e(v.status.value)}] {e(v.recommended_action)} · owner {e(v.owner or 'unassigned')}</li>" for v in item.corrective_actions) or "<li>None recorded</li>"
    return layout(
        item.incident_id,
        f"<section class='panel'><p><strong>HANDLING: {e(item.handling.classification.value)}</strong></p><h1>{e(item.incident_id)} — {e(item.title)}</h1>"
        f"<p><a class='button' href='/edit/{quote(item.incident_id)}'>Edit classification</a> <a class='button' href='/report/{quote(item.incident_id)}'>Full report</a></p>"
        f"<p class='vector'>{e(vector)}</p><div class='grid'><div class='metric'><strong>{e(severity.severity.value)}</strong>Severity</div><div class='metric'><strong>{e(item.event_state.value)}</strong>{e(label_for(item.event_state))}</div><div class='metric'><strong>{e(item.lifecycle_status.value)}</strong>Lifecycle</div></div>"
        f"<h2>Severity rationale</h2><p>Rules: {e(', '.join(severity.triggered_rules))}</p><ul>{''.join(f'<li>{e(r)}</li>' for r in severity.rationale)}</ul>"
        f"<h2>Authority</h2><p>Authorized: {e(', '.join(v.value for v in item.authority.authorized) or 'None')}<br>Actually exercised: {e(', '.join(v.value for v in item.authority.actually_exercised) or 'None')}<br><strong>Unauthorized: {e(', '.join(v.value for v in item.authority.unauthorized_exercised) or 'None')}</strong></p>"
        f"<h2>Boundaries</h2><ul>{''.join(f'<li>{e(coded_boundary(v))} — {e(label_for(v))}</li>' for v in item.boundaries_crossed)}</ul>"
        f"<h2>Containment</h2><p>Intervention Time: {e(item.containment.intervention_time_seconds if item.containment.intervention_time_seconds is not None else 'N/A')} seconds · Damage Time: {e(item.containment.damage_time_seconds if item.containment.damage_time_seconds is not None else 'N/A')} seconds · CM: {e(cm)}</p><p>{e(item.containment.documentation or 'No containment documentation.')}</p>"
        f"<h2>Timeline</h2><table><tr><th>Time</th><th>Type</th><th>Actor</th><th>Description</th></tr>{timeline}</table>"
        f"<h2>Control performance</h2><ul>{controls}</ul><h2>Corrective actions</h2><ul>{actions}</ul></section>",
    )


def apply_form(repository: IncidentRepository, form: dict[str, list[str]]) -> Incident:
    def one(name: str, default: str = "") -> str:
        return form.get(name, [default])[0].strip()

    incident_id = one("incident_id")
    existing = repository.find(incident_id)
    item = existing or new_incident(incident_id, one("title"), one("system_name"))
    data = item.model_dump(mode="python")
    occurred = datetime.fromisoformat(one("occurred_at"))
    if occurred.tzinfo is None:
        occurred = occurred.replace(tzinfo=timezone.utc)
    data.update(
        title=one("title"),
        description=one("description"),
        occurred_at=occurred,
        lifecycle_status=one("lifecycle_status"),
        event_state=one("event_state"),
        reversibility=one("reversibility"),
        blast_radius=one("blast_radius"),
        classification_indicators=form.get("indicators", []),
    )
    data["system"]["name"] = one("system_name")
    data["system"]["model"] = one("model") or None
    data["harm"]["realized_level"] = one("realized_harm")
    data["harm"]["potential_level"] = one("potential_harm")
    data["observability"]["level"] = one("observability")
    data["mcai"]["post_incident_reassessed"] = one("mcai") or None
    data["authority"] = {
        "authorized": form.get("authorized", []),
        "actually_exercised": form.get("actual", []),
        "unauthorized_exercised": form.get("unauthorized", []),
    }
    data["boundaries_crossed"] = form.get("boundaries", ["none"])
    root = one("root_cause")
    data["root_cause"] = {"primary_root_cause": root, "contributing_factors": [], "analysis": ""} if root else None
    data["containment"]["documentation"] = one("containment_documentation")
    data["severity_result"] = None  # stale classifications are never retained after an edit
    validated = Incident.model_validate(data)
    validated.severity_result = classify_severity(validated)
    repository.save(validated)
    return validated


def handler_factory(repository: IncidentRepository) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = f"MQ-AICIR/{SOFTWARE_VERSION}"

        def log_message(self, fmt: str, *args: object) -> None:
            # Avoid logging request paths or values: incident identifiers can be sensitive.
            return

        def _host_allowed(self) -> bool:
            host = self.headers.get("Host", "").rsplit(":", 1)[0]
            return host in ALLOWED_HOSTS

        def _send(self, content: str, status: HTTPStatus = HTTPStatus.OK, content_type: str = "text/html; charset=utf-8") -> None:
            payload = content.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:  # noqa: N802
            if not self._host_allowed():
                self._send("Host not allowed", HTTPStatus.FORBIDDEN, "text/plain; charset=utf-8")
                return
            path = urlparse(self.path).path
            if path == "/":
                self._send(dashboard(repository))
            elif path == "/incidents":
                self._send(incident_list(repository))
            elif path == "/new":
                self._send(editor())
            elif path.startswith("/incident/") or path.startswith("/edit/") or path.startswith("/report/"):
                incident_id = unquote(path.split("/", 2)[2])
                item = repository.find(incident_id)
                if item is None:
                    self._send(layout("Not found", "<section class='panel'><h1>Incident not found</h1></section>"), HTTPStatus.NOT_FOUND)
                elif path.startswith("/edit/"):
                    self._send(editor(item))
                elif path.startswith("/report/"):
                    self._send(render_html(item))
                else:
                    self._send(detail(item))
            else:
                self._send(layout("Not found", "<section class='panel'><h1>Not found</h1></section>"), HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:  # noqa: N802
            if not self._host_allowed() or urlparse(self.path).path != "/save":
                self._send("Forbidden", HTTPStatus.FORBIDDEN, "text/plain; charset=utf-8")
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > MAX_FORM_BYTES:
                    raise ValueError("invalid form size")
                raw = self.rfile.read(length).decode("utf-8")
                form = parse_qs(raw, keep_blank_values=True, max_num_fields=200)
                saved = apply_form(repository, form)
            except (ValueError, UnicodeDecodeError, ValidationError) as exc:
                self._send(editor(error=str(exc)), HTTPStatus.UNPROCESSABLE_ENTITY)
                return
            self.send_response(HTTPStatus.SEE_OTHER)
            self.send_header("Location", f"/incident/{quote(saved.incident_id)}")
            self.send_header("Content-Length", "0")
            self.end_headers()

    return Handler


def serve(directory: Path, *, port: int = 8765) -> None:
    repository = IncidentRepository(directory)
    server = ThreadingHTTPServer(("127.0.0.1", port), handler_factory(repository))
    print(f"MQ-AICIR local interface: http://127.0.0.1:{port}")
    print(f"Incident directory: {repository.directory}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
