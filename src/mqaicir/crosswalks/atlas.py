"""MITRE ATLAS mechanism crosswalk."""

from mqaicir.crosswalks.common import references
from mqaicir.models.incident import CrosswalkReference, Incident
from mqaicir.models.taxonomy import AuthorityClass, HarmCategory, RootCauseCategory


def suggest(incident: Incident) -> list[CrosswalkReference]:
    keys: set[str] = set()
    causes = {incident.root_cause.primary_root_cause, *incident.root_cause.contributing_factors} if incident.root_cause else set()
    if RootCauseCategory.PROMPT_INJECTION in causes:
        keys.add("prompt_injection")
    if RootCauseCategory.INDIRECT_PROMPT_INJECTION in causes:
        keys.add("indirect_prompt_injection")
    if RootCauseCategory.TOOL_INJECTION in causes:
        keys.add("tool_injection")
    if AuthorityClass.EXECUTE in incident.authority.actually_exercised:
        keys.add("tool_invocation")
    if HarmCategory.CONFIDENTIALITY in incident.harm.categories and AuthorityClass.EXTERNALIZE in incident.authority.actually_exercised:
        keys.add("exfiltration")
    return references("mitre_atlas", keys)

