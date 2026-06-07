"""Coverage benchmark for generated Unicode spoof corpora."""

from __future__ import annotations

from typing import Iterable

from detectors.unicode_risk_scorer import ProductionIngressGate


def benchmark_coverage(corpus: Iterable[str]) -> dict:
    """Measure how many corpus entries are rejected or flagged by display analysis."""
    gate = ProductionIngressGate()
    total = 0
    mixed_script = 0
    rejected = 0
    risk_flagged = 0
    for value in corpus:
        total += 1
        result = gate.analyze_display_name(value)
        if "mixed_script" in result["flags"]:
            mixed_script += 1
        if result["status"] == "REJECTED":
            rejected += 1
        if result["status"] == "RISK_FLAGGED":
            risk_flagged += 1
    detected = rejected + risk_flagged
    return {
        "total": total,
        "mixed_script": mixed_script,
        "rejected": rejected,
        "risk_flagged": risk_flagged,
        "detected": detected,
        "detection_rate": (detected / total) if total else 0.0,
        "residual_unflagged": total - detected,
    }
