"""Conservative secret redaction for reports and UI rendering."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

REDACTED = "[REDACTED]"
DEFAULT_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----.*?-----END (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----", re.DOTALL),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"\b(?:sk|pk)-(?:live|test|proj)?-?[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{20,}\b"),
    re.compile(
        r"(?i)\b(api[_-]?key|access[_-]?token|password|passwd|secret)\b(\s*[:=]\s*)(?!\[REDACTED\])([^\s,;\"']{6,}|\"[^\"]{6,}\"|'[^']{6,}')"
    ),
)


def compile_custom_patterns(patterns: Sequence[str] | None) -> tuple[re.Pattern[str], ...]:
    compiled: list[re.Pattern[str]] = []
    for pattern in patterns or ():
        if len(pattern) > 500:
            raise ValueError("custom redaction patterns must be 500 characters or fewer")
        compiled.append(re.compile(pattern))
    return tuple(compiled)


def redact_text(text: str, custom_patterns: Sequence[str] | None = None) -> str:
    result = text
    for pattern in DEFAULT_PATTERNS + compile_custom_patterns(custom_patterns):
        if pattern.groups >= 2 and "api[_-]?key" in pattern.pattern:
            result = pattern.sub(lambda match: f"{match.group(1)}{match.group(2)}{REDACTED}", result)
        else:
            result = pattern.sub(REDACTED, result)
    return result


def redact_value(value: Any, custom_patterns: Sequence[str] | None = None) -> Any:
    if isinstance(value, str):
        return redact_text(value, custom_patterns)
    if isinstance(value, Mapping):
        return {key: redact_value(item, custom_patterns) for key, item in value.items()}
    if isinstance(value, tuple):
        return tuple(redact_value(item, custom_patterns) for item in value)
    if isinstance(value, list):
        return [redact_value(item, custom_patterns) for item in value]
    return value

