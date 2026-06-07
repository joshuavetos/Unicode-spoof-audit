from detectors.unicode_risk_scorer import ProductionIngressGate
from corpus.homoglyph_generator import generate_homoglyph_variants
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
