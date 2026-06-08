"""Detection helpers for BiDi and invisible Unicode layout controls."""

from __future__ import annotations

BIDI_OR_INVISIBLE_RANGES = (
    (0x061C, 0x061C),  # ARABIC LETTER MARK, Unicode Bidi_Control
    (0x200B, 0x200F),  # zero-width controls plus LRM/RLM
    (0x202A, 0x202E),  # embedding/override controls
    (0x2060, 0x2064),  # word joiner and invisible math operators
    (0x2066, 0x2069),  # isolate controls
    (0xFEFF, 0xFEFF),  # zero-width no-break space / BOM
)

BIDI_OR_INVISIBLE = frozenset(
    chr(codepoint)
    for start, end in BIDI_OR_INVISIBLE_RANGES
    for codepoint in range(start, end + 1)
)


def contains_bidi_or_invisible(value: str) -> bool:
    """Return True when *value* contains a layout-control code point."""
    return any(character in BIDI_OR_INVISIBLE for character in value)
