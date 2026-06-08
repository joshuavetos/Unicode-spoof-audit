# Methodology

The corpus combines deterministic homoglyph substitutions for the protected identifier `Admin` with parser-stability fuzz cases involving zero-width controls, bidirectional embedding, override, isolate, and mark controls, combining marks, emoji modifiers, variation selectors, and Unicode separators.

Policies are evaluated through two explicit boundaries: a strict ASCII-only authority gate for identifiers and an advisory Unicode risk scorer for display names.
