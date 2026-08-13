"""NIST SP 800-61 Rev. 3 and AI RMF 1.0 crosswalk."""

from mqaicir.crosswalks.common import references
from mqaicir.models.incident import CrosswalkReference, Incident


def suggest(incident: Incident) -> list[CrosswalkReference]:
    # All four AI RMF functions are contextual, not sequential, and incident response spans CSF 2.0.
    return references("nist", {"govern", "map", "measure", "manage", "incident_response"})

