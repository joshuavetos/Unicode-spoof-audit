"""Run a representative Unicode spoof policy audit."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from detectors.unicode_risk_scorer import ProductionIngressGate

TEST_INPUTS = ["Admin", "admіn", "Josh_90", "共有", "Jose\u0301", "abc\u202Etxt"]


def main() -> None:
    gate = ProductionIngressGate()
    print(f"{'Raw Input':<15} | {'Policy':<12} | {'Status':<12} | Reason")
    print("-" * 90)
    for value in TEST_INPUTS:
        escaped = value.encode("unicode_escape").decode("ascii")
        identifier = gate.enforce_strict_identifier_policy(value)
        display = gate.analyze_display_name(value)
        print(f"{escaped:<15} | Identifier   | {identifier['status']:<12} | {identifier['reason']}")
        print(f"{escaped:<15} | Display Name | {display['status']:<12} | {display['reason']}")
        print("-" * 90)


if __name__ == "__main__":
    main()
