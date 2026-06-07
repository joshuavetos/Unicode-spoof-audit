"""Run corpus generation plus coverage and runtime benchmarks."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from benchmarks.coverage_benchmark import benchmark_coverage
from benchmarks.performance_benchmark import benchmark_policies
from corpus.homoglyph_generator import generate_homoglyph_variants
from corpus.unicode_fuzzer import generate_unicode_fuzz_cases


def main() -> None:
    homoglyphs = list(generate_homoglyph_variants("Admin"))
    fuzz_values = [case["raw"] for case in generate_unicode_fuzz_cases("Admin", max_width=2)]
    corpus = homoglyphs + fuzz_values
    coverage = benchmark_coverage(corpus)
    performance = benchmark_policies(corpus)
    print("Coverage:")
    for key, value in coverage.items():
        print(f"  {key}: {value}")
    print("Performance:")
    for policy, result in performance.items():
        print(f"  {policy}: {result}")


if __name__ == "__main__":
    main()
