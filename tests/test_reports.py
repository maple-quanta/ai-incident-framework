from mqaicir.models.incident import Incident
from mqaicir.reporting import render_html, render_markdown


def test_markdown_contains_all_required_sections_and_vector(example: Incident) -> None:
    report = render_markdown(example)
    for section in (
        "Executive Summary", "Incident Classification", "AI System Information", "Event Timeline",
        "Authority Exercised", "Boundary Analysis", "Assets Affected", "Harm Assessment",
        "Reversibility", "Observability", "Intervention & Containment", "Root Cause",
        "Control Performance", "Evidence", "Notifications", "Corrective Actions", "Revalidation", "Closure",
    ):
        assert f"## {section}" in report
    assert "Incident Profile:" in report
    assert "E2 — Boundary Violation" in report
    assert "SR-HIGH-001" in report


def test_html_is_standalone_and_escaped(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["executive_summary"] = "<script>alert('x')</script>"
    rendered = render_html(Incident.model_validate(data))
    assert rendered.startswith("<!doctype html>")
    assert "<script>alert" not in rendered
    assert "&lt;script&gt;" in rendered
    assert "HANDLING: CONFIDENTIAL" in rendered


def test_reports_handle_missing_optional_fields() -> None:
    from mqaicir.scaffold import new_incident

    item = new_incident("MQ-2026-9100")
    assert "No timeline events recorded" in render_markdown(item)
    assert "Root cause has not yet" in render_html(item)


def test_reports_redact_common_secrets(example: Incident) -> None:
    data = example.model_dump(mode="python")
    data["executive_summary"] = "Authorization: Bearer abcdefghijklmnopqrstuvwxyz password=hunter-two"
    rendered = render_markdown(Incident.model_validate(data))
    assert "abcdefghijklmnopqrstuvwxyz" not in rendered
    assert "hunter-two" not in rendered
    assert "[REDACTED]" in rendered

