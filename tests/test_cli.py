from pathlib import Path

from typer.testing import CliRunner

from mqaicir.cli import app

runner = CliRunner()


def test_version_reports_software_release() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "mq-aicir 1.0.1"


def test_validate_command(example_path: Path) -> None:
    result = runner.invoke(app, ["validate", str(example_path)])
    assert result.exit_code == 0
    assert "VALID" in result.stdout


def test_classify_shows_rationale(example_path: Path) -> None:
    result = runner.invoke(app, ["classify", str(example_path)])
    assert result.exit_code == 0
    assert '"triggered_rules"' in result.stdout
    assert '"rationale"' in result.stdout


def test_summary_keeps_vector_dimensions_visible(example_path: Path) -> None:
    result = runner.invoke(app, ["summary", str(example_path)])
    assert result.exit_code == 0
    for value in ("Event State", "Authority Exercised", "Boundaries Crossed", "Harm", "Reversibility", "Observability", "Triggered Severity Rules"):
        assert value in result.stdout


def test_new_and_report_commands(tmp_path: Path) -> None:
    incident = tmp_path / "incident.json"
    created = runner.invoke(app, ["new", str(incident), "--id", "MQ-2026-9200"])
    assert created.exit_code == 0
    report = tmp_path / "report.html"
    generated = runner.invoke(app, ["report", str(incident), "--format", "html", "--output", str(report)])
    assert generated.exit_code == 0
    assert report.read_text().startswith("<!doctype html>")
