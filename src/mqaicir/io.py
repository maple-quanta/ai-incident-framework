"""Bounded, deterministic JSON file I/O."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from mqaicir.models.incident import Incident

MAX_INCIDENT_BYTES = 10 * 1024 * 1024


def validated_input_path(path: Path) -> Path:
    resolved = path.expanduser().resolve(strict=True)
    if resolved.suffix.lower() != ".json" or not resolved.is_file():
        raise ValueError("incident input must be a regular .json file")
    if resolved.stat().st_size > MAX_INCIDENT_BYTES:
        raise ValueError(f"incident file exceeds {MAX_INCIDENT_BYTES} bytes")
    return resolved


def validated_output_path(path: Path, allowed_suffixes: set[str]) -> Path:
    expanded = path.expanduser()
    if expanded.suffix.lower() not in allowed_suffixes:
        raise ValueError(f"output suffix must be one of: {', '.join(sorted(allowed_suffixes))}")
    parent = expanded.parent.resolve(strict=True)
    resolved = parent / expanded.name
    if resolved.exists() and resolved.is_symlink():
        raise ValueError("refusing to overwrite a symbolic link")
    return resolved


def load_json(path: Path) -> dict[str, Any]:
    resolved = validated_input_path(path)
    try:
        value = json.loads(resolved.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("incident JSON must be an object")
    return value


def load_incident(path: Path) -> Incident:
    return Incident.model_validate(load_json(path))


def atomic_write(path: Path, content: str) -> None:
    """Write next to the target and atomically replace it; reject symlink targets."""

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.is_symlink():
        raise ValueError("refusing to overwrite a symbolic link")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def save_incident(incident: Incident, path: Path) -> None:
    target = validated_output_path(path, {".json"})
    content = json.dumps(incident.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n"
    atomic_write(target, content)

