"""Runtime benchmark for detector policies."""

from __future__ import annotations

from time import perf_counter
from typing import Callable, Iterable

from detectors.unicode_risk_scorer import ProductionIngressGate


def time_detector(values: Iterable[str], detector: Callable[[str], dict]) -> dict:
    """Return elapsed seconds and item count for a detector callable."""
    items = list(values)
    started = perf_counter()
    for value in items:
        detector(value)
    elapsed = perf_counter() - started
    return {"count": len(items), "elapsed_seconds": elapsed, "items_per_second": (len(items) / elapsed) if elapsed else 0.0}


def benchmark_policies(values: Iterable[str]) -> dict:
    """Benchmark strict-identifier and display-name policy paths."""
    items = list(values)
    gate = ProductionIngressGate()
    return {
        "identifier_policy": time_detector(items, gate.enforce_strict_identifier_policy),
        "display_name_policy": time_detector(items, gate.analyze_display_name),
    }
