from pathlib import Path

from mqaicir.classification.severity import classify_severity
from mqaicir.io import load_incident

ROOT = Path(__file__).resolve().parents[1]


def test_at_least_six_synthetic_examples_validate_and_classify() -> None:
    paths = sorted((ROOT / "examples" / "incidents").glob("*.json"))
    assert len(paths) >= 6
    for path in paths:
        incident = load_incident(path)
        result = classify_severity(incident)
        assert result.triggered_rules and result.rationale


def test_examples_do_not_contain_live_credential_shapes() -> None:
    forbidden = ("-----BEGIN PRIVATE KEY-----", "ghp_", "AKIA", "Bearer eyJ")
    for path in (ROOT / "examples" / "incidents").glob("*.json"):
        text = path.read_text(encoding="utf-8")
        assert not any(value in text for value in forbidden)

