from mqaicir.crosswalks import suggest_atlas, suggest_nist, suggest_oecd, suggest_safe


def test_crosswalks_are_typed_and_versioned(example) -> None:
    for suggestion in (suggest_safe(example), suggest_atlas(example), suggest_nist(example), suggest_oecd(example)):
        assert suggestion
        assert all(item.source_version and item.relationship for item in suggestion)


def test_indirect_injection_maps_to_verified_atlas_identifier(example) -> None:
    identifiers = {item.identifier for item in suggest_atlas(example)}
    assert "AML.T0051.001" in identifiers
    assert "AML.T0053" in identifiers

