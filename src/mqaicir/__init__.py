"""Maple Quanta AI Incident Classification & Reporting Framework."""

from mqaicir._version import INCIDENT_SCHEMA_VERSION, SOFTWARE_VERSION
from mqaicir.models.incident import Incident

__all__ = ["Incident"]
__version__ = SOFTWARE_VERSION

FRAMEWORK_NAME = "Maple Quanta AI Incident Classification & Reporting Framework"
# Kept as a compatibility alias for consumers of the 1.0 record format.
FRAMEWORK_VERSION = INCIDENT_SCHEMA_VERSION
FRAMEWORK_ID = "MQ-AICIR"
