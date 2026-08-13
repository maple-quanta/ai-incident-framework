from mqaicir.classification.containment import calculate_containment, interpret_margin


def test_intervention_time_and_margin_are_calculated() -> None:
    metrics = calculate_containment(detection=10, decision=20, enforcement=30, damage=120)
    assert metrics.intervention_time_seconds == 60
    assert metrics.containment_margin == 2
    assert "faster" in interpret_margin(metrics)


def test_zero_component_values_are_valid() -> None:
    metrics = calculate_containment(detection=0, decision=0, enforcement=5, damage=10)
    assert metrics.intervention_time_seconds == 5
    assert metrics.containment_margin == 2


def test_zero_intervention_time_does_not_divide() -> None:
    metrics = calculate_containment(detection=0, decision=0, enforcement=0, damage=10)
    assert metrics.intervention_time_seconds == 0
    assert metrics.containment_margin is None
    assert "zero" in metrics.not_applicable_reason.lower()


def test_missing_component_makes_intervention_unavailable() -> None:
    metrics = calculate_containment(detection=10, decision=None, enforcement=5, damage=100)
    assert metrics.intervention_time_seconds is None
    assert metrics.containment_margin is None
    assert "component" in metrics.not_applicable_reason.lower()


def test_missing_damage_time_has_reason() -> None:
    metrics = calculate_containment(detection=10, decision=5, enforcement=5, damage=None)
    assert metrics.intervention_time_seconds == 20
    assert metrics.containment_margin is None
    assert metrics.not_applicable_reason == "Damage Time is unavailable."


def test_instantaneous_action_uses_prevention_not_ratio() -> None:
    metrics = calculate_containment(detection=0, decision=0, enforcement=0, damage=0, instantaneous_action=True)
    assert metrics.containment_margin is None
    assert "prevention" in metrics.not_applicable_reason.lower()


def test_explicit_misleading_metric_reason_is_preserved() -> None:
    metrics = calculate_containment(
        detection=10, decision=10, enforcement=10, damage=100,
        metric_misleading=True, not_applicable_reason="Damage pathway is non-temporal.",
    )
    assert metrics.containment_margin is None
    assert metrics.not_applicable_reason == "Damage pathway is non-temporal."

