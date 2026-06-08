"""Generate homoglyph substitutions for protected identifiers."""

from __future__ import annotations

from dataclasses import asdict
from itertools import product
from typing import Dict, Iterator, List

from corpus.confusable_maps import CONFUSABLE_MAP, Confusable


def options_for_character(character: str, confusable_map: Dict[str, List[Confusable]] | None = None) -> List[str]:
    """Return the original character plus known visual substitutes."""
    mapping = CONFUSABLE_MAP if confusable_map is None else confusable_map
    return [character] + [entry.character for entry in mapping.get(character, [])]


def generate_homoglyph_variants(target: str = "Admin", limit: int | None = None) -> Iterator[str]:
    """Yield unique homoglyph permutations for *target* in deterministic order."""
    if limit is not None and limit <= 0:
        return

    seen: set[str] = set()
    emitted = 0
    option_sets = [options_for_character(character) for character in target]
    for parts in product(*option_sets):
        value = "".join(parts)
        if value in seen:
            continue
        seen.add(value)
        yield value
        emitted += 1
        if limit is not None and emitted >= limit:
            return


def describe_confusables() -> List[dict]:
    """Return serializable confusable-map rows for reporting."""
    rows: List[dict] = []
    for entries in CONFUSABLE_MAP.values():
        rows.extend(asdict(entry) for entry in entries)
    return rows
