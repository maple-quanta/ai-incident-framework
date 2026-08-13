from __future__ import annotations

from pathlib import Path

import pytest

from mqaicir.io import load_incident
from mqaicir.models.incident import Incident

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "incidents"


@pytest.fixture()
def example_path() -> Path:
    return EXAMPLES / "01-indirect-prompt-injection.json"


@pytest.fixture()
def example(example_path: Path) -> Incident:
    return load_incident(example_path)

