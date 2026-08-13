"""Crosswalk file loading and typed reference conversion."""

from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path
from typing import Any

from mqaicir.models.incident import CrosswalkReference


def crosswalk_path(name: str) -> Path:
    if name not in {"safe", "mitre_atlas", "nist", "oecd"}:
        raise ValueError("unknown crosswalk")
    source_path = Path(__file__).resolve().parents[3] / "config" / "crosswalks" / f"{name}.json"
    if source_path.is_file():
        return source_path
    return Path(str(files("mqaicir").joinpath("data/crosswalks", f"{name}.json")))


def load(name: str) -> dict[str, Any]:
    data = json.loads(crosswalk_path(name).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise ValueError(f"malformed {name} crosswalk")
    return data


def references(name: str, keys: set[str]) -> list[CrosswalkReference]:
    data = load(name)
    return [
        CrosswalkReference(
            identifier=entry.get("identifier"),
            title=entry["title"],
            relationship=entry["relationship"],
            source_version=data["source_version"],
            verified_at=data.get("verified_at"),
        )
        for entry in data["entries"]
        if entry["key"] in keys
    ]

