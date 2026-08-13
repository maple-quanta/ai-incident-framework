from pathlib import Path

from mqaicir.web import IncidentRepository, dashboard, detail, editor, incident_list


def test_local_pages_render_structured_review_views(tmp_path: Path, example_path: Path) -> None:
    target = tmp_path / example_path.name
    target.write_bytes(example_path.read_bytes())
    repository = IncidentRepository(tmp_path)
    incident = repository.all()[0][0]
    assert "Incidents by severity" in dashboard(repository)
    assert "Principal boundary" in incident_list(repository)
    assert "Severity rationale" in detail(incident)
    form = editor(incident)
    assert "Authorized" in form and "Boundaries crossed" in form and "Classification indicators" in form

