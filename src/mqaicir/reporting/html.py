"""Escaped, standalone HTML incident report generation."""

from mqaicir.models.incident import Incident
from mqaicir.reporting.common import environment, report_context


def render_html(incident: Incident, custom_redaction_patterns: list[str] | None = None) -> str:
    template = environment(html=True).get_template("report.html.j2")
    return template.render(**report_context(incident, custom_redaction_patterns)).strip() + "\n"

