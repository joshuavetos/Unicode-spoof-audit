from detectors.unicode_risk_scorer import ProductionIngressGate
from corpus.homoglyph_generator import generate_homoglyph_variants, options_for_character
from corpus.unicode_fuzzer import generate_unicode_fuzz_cases


def test_representative_policy_results():
    gate = ProductionIngressGate()
    assert gate.enforce_strict_identifier_policy("Admin")["status"] == "REJECTED"
    assert gate.enforce_strict_identifier_policy("Josh_90")["status"] == "SECURE"
    assert gate.enforce_strict_identifier_policy("admіn")["reason"] == "Violates strict ASCII allowlist"
    assert gate.analyze_display_name("admіn")["status"] == "REJECTED"
    assert gate.analyze_display_name("共有")["status"] == "APPROVED"
    assert gate.analyze_display_name("Jose\u0301")["status"] == "RISK_FLAGGED"
    assert gate.analyze_display_name("abc\u202Etxt")["status"] == "REJECTED"


def test_generators_emit_expected_cases():
    variants = list(generate_homoglyph_variants("Admin", limit=5))
    fuzz_cases = list(generate_unicode_fuzz_cases("Admin", max_width=1))
    assert variants[0] == "Admin"
    assert len(variants) == 5
    assert any(case["raw"].startswith("Admin") for case in fuzz_cases)


def test_display_name_rejects_blank_and_nfkc_reserved_collision():
    gate = ProductionIngressGate()
    assert gate.analyze_display_name("   ")["status"] == "REJECTED"
    fullwidth_admin = "Ａｄｍｉｎ"
    result = gate.analyze_display_name(fullwidth_admin)
    assert result["canonical_form"] == "admin"
    assert result["status"] == "REJECTED"
    assert result["reason"] == "Reserved identity collision"
    assert "compatibility_normalized" in result["flags"]


def test_empty_reserved_names_and_empty_confusable_map_are_respected():
    gate = ProductionIngressGate(reserved_names=[])
    assert gate.enforce_strict_identifier_policy("Admin")["status"] == "SECURE"
    assert options_for_character("A", confusable_map={}) == ["A"]
    assert list(generate_homoglyph_variants("Admin", limit=0)) == []


def test_display_name_rejects_additional_layout_controls():
    gate = ProductionIngressGate()
    for control in ("\u061c", "\u2060", "\u2066", "\u2069"):
        result = gate.analyze_display_name(f"safe{control}name")
        assert result["status"] == "REJECTED"
        assert result["reason"] == "BiDi/Invisible detected"
        assert "layout_control" in result["flags"]


def test_unicode_fuzzer_includes_expanded_layout_controls():
    fuzz_cases = list(generate_unicode_fuzz_cases("Admin", max_width=1))
    raw_values = {case["raw"] for case in fuzz_cases}
    assert "Admin\u061c" in raw_values
    assert "Admin\u2060" in raw_values
    assert "Admin\u2066" in raw_values
    assert "Admin\u2069" in raw_values
