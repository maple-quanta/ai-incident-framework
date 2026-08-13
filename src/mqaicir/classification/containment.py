"""Containment metric helpers."""

from mqaicir.models.incident import ContainmentMetrics


def calculate_containment(
    *,
    detection: float | None,
    decision: float | None,
    enforcement: float | None,
    damage: float | None,
    metric_misleading: bool = False,
    instantaneous_action: bool = False,
    not_applicable_reason: str | None = None,
) -> ContainmentMetrics:
    """Build validated metrics and deterministically calculate Ti and CM."""

    return ContainmentMetrics(
        detection_time_seconds=detection,
        decision_time_seconds=decision,
        enforcement_time_seconds=enforcement,
        damage_time_seconds=damage,
        metric_misleading=metric_misleading,
        instantaneous_action=instantaneous_action,
        not_applicable_reason=not_applicable_reason,
    )


def interpret_margin(metrics: ContainmentMetrics) -> str:
    if metrics.containment_margin is None:
        return f"N/A — {metrics.not_applicable_reason or 'not calculated'}"
    if metrics.containment_margin > 1:
        return "Containment occurred faster than the defined damage pathway."
    if metrics.containment_margin == 1:
        return "Containment and damage times are equal; there is no operational margin."
    return "Damage can occur faster than effective intervention."

