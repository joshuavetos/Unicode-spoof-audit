"""Curated confusable characters used by the audit corpus."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import unicodedata


@dataclass(frozen=True)
class Confusable:
    """A single code point that can visually resemble an ASCII target."""

    target: str
    character: str
    codepoint: str
    name: str


_RAW_CONFUSABLES: Dict[str, List[str]] = {
    "A": ["Α", "А", "Ꭺ", "Ａ"],
    "a": ["а", "α", "ａ"],
    "d": ["ԁ", "ⅾ", "ｄ"],
    "m": ["м", "ⅿ", "ｍ"],
    "i": ["і", "ι", "Ꭵ", "ｉ"],
    "n": ["ո", "п", "ｎ"],
}


def build_confusable_map() -> Dict[str, List[Confusable]]:
    """Return confusable metadata keyed by ASCII target character."""
    result: Dict[str, List[Confusable]] = {}
    for target, characters in _RAW_CONFUSABLES.items():
        result[target] = [
            Confusable(
                target=target,
                character=character,
                codepoint=f"U+{ord(character):04X}",
                name=unicodedata.name(character),
            )
            for character in characters
        ]
    return result


CONFUSABLE_MAP = build_confusable_map()
