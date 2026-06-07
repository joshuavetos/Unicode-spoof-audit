"""Script-family analysis for Unicode labels."""

from __future__ import annotations

from typing import Set
import unicodedata

CJK_FAMILY = {"Han", "Hiragana", "Katakana", "Hangul"}


def classify_script(character: str) -> str:
    """Classify a single character into a supported script family."""
    category = unicodedata.category(character)
    if category.startswith("M"):
        return "Inherited"
    name = unicodedata.name(character, "")
    if not name:
        return "Unknown"
    if "LATIN" in name:
        return "Latin"
    if "CYRILLIC" in name:
        return "Cyrillic"
    if "GREEK" in name:
        return "Greek"
    if "CJK UNIFIED IDEOGRAPH" in name or "CJK COMPATIBILITY IDEOGRAPH" in name:
        return "Han"
    if "HIRAGANA" in name:
        return "Hiragana"
    if "KATAKANA" in name:
        return "Katakana"
    if "HANGUL" in name:
        return "Hangul"
    if category[0] in {"P", "S", "N", "Z"}:
        return "Common"
    return "Unknown"


def significant_scripts(value: str) -> Set[str]:
    """Return non-common scripts, collapsing common CJK scripts into one family."""
    scripts: Set[str] = set()
    for character in value:
        script = classify_script(character)
        if script in {"Common", "Inherited"}:
            continue
        scripts.add("CJK_FAMILY" if script in CJK_FAMILY else script)
    return scripts


def is_mixed_script(value: str) -> bool:
    """Return True when *value* contains more than one significant script family."""
    return len(significant_scripts(value)) > 1
