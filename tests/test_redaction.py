from mqaicir.redaction import redact_text


def test_redacts_bearer_password_api_key_and_private_key() -> None:
    value = """Bearer abcdefghijklmnopqrstuvwxyz
password=correct-horse-battery
api_key: abcdefghijklmnop
-----BEGIN PRIVATE KEY-----
not-real-key-material
-----END PRIVATE KEY-----"""
    redacted = redact_text(value)
    for secret in ("abcdefghijklmnopqrstuvwxyz", "correct-horse", "abcdefghijklmnop", "not-real-key"):
        assert secret not in redacted
    assert redacted.count("[REDACTED]") >= 4


def test_custom_redaction_pattern() -> None:
    assert redact_text("CLIENT-SECRET-123", [r"CLIENT-SECRET-\d+"]) == "[REDACTED]"

