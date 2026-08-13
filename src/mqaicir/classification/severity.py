"""Configurable, deterministic, non-averaging severity classification."""

from __future__ import annotations

from collections.abc import Iterable
from enum import Enum
from importlib.resources import files
from pathlib import Path
from typing import Any

import yaml

from mqaicir.models.incident import Incident, SeverityAssessment
from mqaicir.models.taxonomy import Severity

SEVERITY_ORDER = {Severity.LOW: 0, Severity.MEDIUM: 1, Severity.HIGH: 2, Severity.CRITICAL: 3}
RANKS = {
    "harm": {f"H{i}": i for i in range(5)},
    "observability": {f"O{i}": i for i in range(5)},  # larger means worse
    "reversibility": {f"R{i}": i for i in range(5)},
    "blast_radius": {f"BR{i}": i for i in range(6)},
    "mcai": {f"A{i}": i for i in range(5)},
}
SUPPORTED_OPS = {"eq", "contains", "intersects", "nonempty", "lt", "rank_gte"}


def default_rules_path() -> Path:
    source_path = Path(__file__).resolve().parents[3] / "config" / "severity_rules.yaml"
    if source_path.is_file():
        return source_path
    return Path(str(files("mqaicir").joinpath("data/severity_rules.yaml")))


def _plain(value: Any) -> Any:
    return value.value if isinstance(value, Enum) else value


def _resolve(value: Any, path: str) -> Any:
    """Resolve dotted paths, flattening attributes across lists."""

    current: list[Any] = [value]
    for part in path.split("."):
        following: list[Any] = []
        for item in current:
            if isinstance(item, list):
                for child in item:
                    following.append(child.get(part) if isinstance(child, dict) else getattr(child, part, None))
            else:
                following.append(item.get(part) if isinstance(item, dict) else getattr(item, part, None))
        current = following
    result = [_plain(item) for item in current if item is not None]
    return result[0] if len(result) == 1 else result


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_plain(item) for item in value]
    if isinstance(value, (set, tuple)):
        return [_plain(item) for item in value]
    return [_plain(value)]


def _condition_matches(incident: Incident, condition: dict[str, Any]) -> bool:
    path = condition.get("path")
    op = condition.get("op")
    if not isinstance(path, str) or op not in SUPPORTED_OPS:
        raise ValueError(f"unsupported severity condition: {condition!r}")
    actual = _resolve(incident, path)
    expected = condition.get("value")
    if op == "eq":
        return _plain(actual) == expected
    if op == "contains":
        return expected in _as_list(actual)
    if op == "intersects":
        return bool(set(_as_list(actual)).intersection(_as_list(expected)))
    if op == "nonempty":
        return bool(actual)
    if op == "lt":
        return actual is not None and not isinstance(actual, list) and actual < expected
    if op == "rank_gte":
        scale = condition.get("scale")
        if scale not in RANKS:
            raise ValueError(f"unknown rank scale: {scale!r}")
        return RANKS[scale][_plain(actual)] >= RANKS[scale][expected]
    raise AssertionError("unreachable")


def load_rules(path: Path | None = None) -> dict[str, Any]:
    rules_path = (path or default_rules_path()).resolve()
    if not rules_path.is_file() or rules_path.suffix.lower() not in {".yaml", ".yml"}:
        raise ValueError(f"invalid severity rules path: {rules_path}")
    document = yaml.safe_load(rules_path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("rules"), list):
        raise ValueError("severity configuration must contain a rules list")
    ids: set[str] = set()
    for rule in document["rules"]:
        if not isinstance(rule, dict) or not {"id", "severity", "description", "all"}.issubset(rule):
            raise ValueError(f"malformed severity rule: {rule!r}")
        if rule["id"] in ids:
            raise ValueError(f"duplicate severity rule id: {rule['id']}")
        ids.add(rule["id"])
        Severity(rule["severity"])
        if not isinstance(rule["all"], list) or not rule["all"]:
            raise ValueError(f"rule {rule['id']} must contain conditions")
        for condition in rule["all"]:
            if condition.get("op") not in SUPPORTED_OPS:
                raise ValueError(f"rule {rule['id']} uses an unsupported operator")
    return document


def classify_severity(incident: Incident, rules_path: Path | None = None) -> SeverityAssessment:
    """Evaluate explicit escalation rules; no dimension values are averaged."""

    document = load_rules(rules_path)
    matched = [
        rule
        for rule in document["rules"]
        if all(_condition_matches(incident, condition) for condition in rule["all"])
    ]
    if not matched:
        raise RuntimeError("severity rules produced no result; configure a deterministic fallback")
    highest = max((Severity(rule["severity"]) for rule in matched), key=SEVERITY_ORDER.__getitem__)
    decisive = [rule for rule in matched if Severity(rule["severity"]) == highest]
    return SeverityAssessment(
        severity=highest,
        triggered_rules=[rule["id"] for rule in decisive],
        rationale=[rule["description"] for rule in decisive],
        ruleset_version=str(document.get("ruleset", {}).get("version", "unknown")),
    )
