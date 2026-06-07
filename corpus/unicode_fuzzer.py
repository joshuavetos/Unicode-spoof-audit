"""Generate Unicode parser-stability and layout-control fuzz cases."""

from __future__ import annotations

from itertools import combinations
from typing import Dict, Iterator, List
import unicodedata

FUZZ_CATEGORIES: Dict[str, List[str]] = {
    "zero_width": ["\u200b", "\u200c", "\u200d", "\ufeff"],
    "direction": ["\u202a", "\u202b", "\u202c", "\u202d", "\u202e"],
    "combining": ["\u0300", "\u0301", "\u0308", "\u0327"],
    "emoji_mod": ["\U0001f3fb", "\U0001f3fd", "\ufe0f"],
    "separators": ["\u2028", "\u2029"],
}


def generate_unicode_fuzz_cases(base_text: str = "Admin", max_width: int = 3) -> Iterator[dict]:
    """Yield fuzz cases made from combinations of risky Unicode categories."""
    all_chars = [character for values in FUZZ_CATEGORIES.values() for character in values]
    for width in range(1, max_width + 1):
        for combo in combinations(all_chars, width):
            fuzzed = base_text + "".join(combo)
            normalized = unicodedata.normalize("NFC", fuzzed)
            yield {
                "raw": fuzzed,
                "escaped": fuzzed.encode("unicode_escape").decode("ascii"),
                "utf8_hex": fuzzed.encode("utf-8", "surrogatepass").hex(),
                "nfc_length": len(normalized),
                "length_changed_by_nfc": len(fuzzed) != len(normalized),
                "categories": [unicodedata.category(character) for character in combo],
            }
