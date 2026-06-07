"""Build the JSON spoof corpus used by examples and benchmarks."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json

from corpus.homoglyph_generator import describe_confusables, generate_homoglyph_variants
from corpus.unicode_fuzzer import generate_unicode_fuzz_cases

OUTPUT_PATH = Path("corpus/generated/admin_spoof_corpus.json")


def build_corpus(target: str = "Admin") -> dict:
    homoglyphs = list(generate_homoglyph_variants(target))
    fuzz_cases = list(generate_unicode_fuzz_cases(target, max_width=2))
    return {
        "target": target,
        "confusables": describe_confusables(),
        "homoglyph_variants": homoglyphs,
        "unicode_fuzz_cases": fuzz_cases,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    corpus = build_corpus()
    OUTPUT_PATH.write_text(json.dumps(corpus, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(corpus['homoglyph_variants'])} homoglyph variants and {len(corpus['unicode_fuzz_cases'])} fuzz cases to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
