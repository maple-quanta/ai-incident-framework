"""Explicit framework-version migration registry.

No migrations exist for 1.0.0 because it is the initial release. A future
migration must accept a source-version document, preserve the original, add an
auditable migration note, and return a record validated under the target model.
"""

from collections.abc import Callable
from typing import Any

Migration = Callable[[dict[str, Any]], dict[str, Any]]
REGISTRY: dict[tuple[str, str], Migration] = {}


def migrate(document: dict[str, Any], source: str, target: str) -> dict[str, Any]:
    if source == target:
        return document.copy()
    try:
        operation = REGISTRY[(source, target)]
    except KeyError as exc:
        raise ValueError(f"no explicit MQ-AICIR migration registered from {source} to {target}") from exc
    return operation(document)
