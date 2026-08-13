"""Markdown incident report generation."""

from mqaicir.models.incident import Incident
from mqaicir.reporting.common import environment, report_context


def render_markdown(incident: Incident, custom_redaction_patterns: list[str] | None = None) -> str:
    template = environment(html=False).get_template("report.md.j2")
    return template.render(**report_context(incident, custom_redaction_patterns)).strip() + "\n"

