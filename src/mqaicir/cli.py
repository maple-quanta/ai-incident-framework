"""MQ-AICIR command-line interface."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from mqaicir._version import SOFTWARE_VERSION
from mqaicir.classification.lifecycle import transition_incident
from mqaicir.classification.severity import classify_severity
from mqaicir.io import atomic_write, load_incident, save_incident, validated_output_path
from mqaicir.models.incident import Incident, LifecycleOverride
from mqaicir.models.taxonomy import (
    BOUNDARY_CODES,
    LifecycleState,
    coded_boundary,
    label_for,
)
from mqaicir.reporting import render_html, render_markdown
from mqaicir.scaffold import new_incident

app = typer.Typer(
    name="mq-aicir",
    help=f"Maple Quanta AI Incident Classification & Reporting Framework (MQ-AICIR) {SOFTWARE_VERSION}",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"mq-aicir {SOFTWARE_VERSION}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Show the software version and exit.",
        ),
    ] = False,
) -> None:
    """Maple Quanta AI Incident Classification & Reporting Framework."""


def _fail(message: str, code: int = 1) -> None:
    typer.secho(message, fg=typer.colors.RED, err=True)
    raise typer.Exit(code)


@app.command("new")
def create_new(
    output: Annotated[Path, typer.Argument(help="New incident .json file")],
    incident_id: Annotated[str, typer.Option("--id", help="MQ-YYYY-... identifier")] = "MQ-2026-0001",
    title: Annotated[str, typer.Option(help="Incident title")] = "New AI incident",
    system: Annotated[str, typer.Option(help="AI system name")] = "Unspecified AI system",
) -> None:
    """Create a valid DRAFT incident record."""

    try:
        target = validated_output_path(output, {".json"})
        if target.exists():
            _fail(f"refusing to overwrite existing file: {target}")
        save_incident(new_incident(incident_id, title, system), target)
    except (ValueError, ValidationError) as exc:
        _fail(str(exc))
    typer.echo(f"Created {target}")


@app.command()
def validate(incident_file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)]) -> None:
    """Validate JSON syntax, the Pydantic model, and semantic constraints."""

    try:
        incident = load_incident(incident_file)
    except (ValueError, ValidationError) as exc:
        _fail(f"INVALID\n{exc}", 2)
    typer.echo(f"VALID — {incident.incident_id} (MQ-AICIR {incident.framework.version})")


@app.command()
def classify(
    incident_file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    rules: Annotated[Path | None, typer.Option(help="Custom YAML ruleset")] = None,
    write: Annotated[bool, typer.Option("--write", help="Persist severity_result in the record")] = False,
) -> None:
    """Run deterministic rules and always show the decisive rationale."""

    try:
        incident = load_incident(incident_file)
        result = classify_severity(incident, rules)
        if write:
            incident.severity_result = result
            save_incident(incident, incident_file)
    except (ValueError, ValidationError, OSError) as exc:
        _fail(str(exc))
    typer.echo(json.dumps(result.model_dump(mode="json"), indent=2))


@app.command()
def report(
    incident_file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    format: Annotated[str, typer.Option("--format", help="markdown or html")] = "markdown",
    output: Annotated[Path | None, typer.Option("--output", "-o")] = None,
    redact_pattern: Annotated[list[str] | None, typer.Option(help="Additional regular expression to redact")] = None,
) -> None:
    """Generate a redacted Markdown or escaped standalone HTML report."""

    try:
        incident = load_incident(incident_file)
        if format not in {"markdown", "html"}:
            raise ValueError("format must be 'markdown' or 'html'")
        content = (
            render_markdown(incident, redact_pattern)
            if format == "markdown"
            else render_html(incident, redact_pattern)
        )
        if output is None:
            typer.echo(content, nl=False)
        else:
            suffix = ".md" if format == "markdown" else ".html"
            target = validated_output_path(output, {suffix})
            atomic_write(target, content)
            typer.echo(f"Wrote {target}")
    except (ValueError, ValidationError, OSError) as exc:
        _fail(str(exc))


@app.command()
def summary(incident_file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)]) -> None:
    """Print the visible multidimensional incident vector and rationale."""

    try:
        incident = load_incident(incident_file)
        result = incident.severity_result or classify_severity(incident)
    except (ValueError, ValidationError) as exc:
        _fail(str(exc))
    boundaries = "\n".join(
        f"  {coded_boundary(item)} {label_for(item)}" for item in incident.boundaries_crossed
    )
    authorities = "\n".join(f"  {item.value}" for item in incident.authority.actually_exercised) or "  None"
    cm = "N/A" if incident.containment.containment_margin is None else f"{incident.containment.containment_margin:.2f}"
    typer.echo(
        f"Incident: {incident.incident_id}\n\n"
        f"Event State:\n{incident.event_state.value} — {label_for(incident.event_state)}\n\n"
        f"Severity:\n{result.severity.value}\n\n"
        f"Authority Exercised:\n{authorities}\n\n"
        f"Boundaries Crossed:\n{boundaries}\n\n"
        f"Harm:\n{incident.harm.realized_level.value} — {label_for(incident.harm.realized_level)}\n"
        f"Potential: {incident.harm.potential_level.value} — {label_for(incident.harm.potential_level)}\n\n"
        f"Reversibility:\n{incident.reversibility.value} — {label_for(incident.reversibility)}\n\n"
        f"Observability:\n{incident.observability.level.value} — {label_for(incident.observability.level)}\n\n"
        f"Blast Radius:\n{incident.blast_radius.value} — {label_for(incident.blast_radius)}\n\n"
        f"MCAI:\n{incident.mcai.post_incident_reassessed.value if incident.mcai.post_incident_reassessed else 'N/A'}\n\n"
        f"Intervention Time:\n{incident.containment.intervention_time_seconds if incident.containment.intervention_time_seconds is not None else 'N/A'} seconds\n\n"
        f"Containment Margin:\n{cm}\n\n"
        f"Triggered Severity Rules:\n" + "\n".join(f"  {rule}" for rule in result.triggered_rules)
    )


@app.command()
def transition(
    incident_file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    target: Annotated[LifecycleState, typer.Argument()],
    responsible_person: Annotated[str | None, typer.Option(help="Person authorizing an exception override")] = None,
    rationale: Annotated[str | None, typer.Option(help="Exception override rationale")] = None,
) -> None:
    """Move through an allowed lifecycle transition and enforce closure gates."""

    try:
        incident = load_incident(incident_file)
        override = None
        if responsible_person or rationale:
            if not responsible_person or not rationale:
                raise ValueError("override requires both --responsible-person and --rationale")
            override = LifecycleOverride(
                responsible_person=responsible_person,
                timestamp=datetime.now(timezone.utc),
                rationale=rationale,
            )
        updated = transition_incident(incident, target, override=override)
        save_incident(updated, incident_file)
    except (ValueError, ValidationError) as exc:
        _fail(str(exc))
    typer.echo(f"{updated.incident_id}: {incident.lifecycle_status.value} -> {updated.lifecycle_status.value}")


@app.command()
def serve(
    directory: Annotated[Path, typer.Option("--directory", "-d", help="Directory containing incident JSON files")] = Path("examples/incidents"),
    port: Annotated[int, typer.Option(min=1024, max=65535)] = 8765,
) -> None:
    """Run the local-only incident editor and dashboard."""

    from mqaicir.web import serve as serve_web

    serve_web(directory, port=port)


if __name__ == "__main__":
    app()
