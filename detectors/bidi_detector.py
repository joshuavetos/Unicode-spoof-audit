"""Detection helpers for BiDi and invisible Unicode layout controls."""

from __future__ import annotations

BIDI_OR_INVISIBLE = frozenset(
    chr(codepoint)
    for start, end in ((0x200B, 0x200F), (0x202A, 0x202E), (0x2066, 0x2069), (0xFEFF, 0xFEFF))
    for codepoint in range(start, end + 1)
)


def contains_bidi_or_invisible(value: str) -> bool:
    """Return True when *value* contains a layout-control code point."""
    return any(character in BIDI_OR_INVISIBLE for character in value)
