"""ASCII-only authority gate for security-sensitive identifiers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List, Literal, Optional, Set
import re

Status = Literal["SECURE", "APPROVED", "RISK_FLAGGED", "REJECTED"]


@dataclass(frozen=True)
class GateResult:
    raw_input: str
    canonical_form: str
    status: Status
    reason: str
    scripts: List[str]
    flags: List[str]


class StrictIdentifierPolicy:
    """Reject Unicode participation in authoritative identifiers."""

    STRICT_IDENTIFIER_RE = re.compile(r"\A[A-Za-z0-9_-]+\Z")

    def __init__(self, reserved_names: Optional[List[str]] = None):
        base_reserved = reserved_names or ["admin", "root", "system", "support"]
        self.reserved_set: Set[str] = {name.casefold().strip() for name in base_reserved if name}

    @staticmethod
    def result(raw: str, canonical: str, status: Status, reason: str, scripts: set[str] | None = None, flags: list[str] | None = None) -> dict:
        return asdict(GateResult(raw, canonical, status, reason, sorted(scripts or set()), flags or []))

    def evaluate(self, input_str: str) -> dict:
        """Evaluate an identifier and return a serializable policy result."""
        if not isinstance(input_str, str):
            return self.result("", "", "REJECTED", "Not a string")
        if not input_str:
            return self.result("", "", "REJECTED", "Empty identifier")
        if not self.STRICT_IDENTIFIER_RE.fullmatch(input_str):
            return self.result(input_str, "", "REJECTED", "Violates strict ASCII allowlist")
        canonical = input_str.casefold().strip()
        if canonical in self.reserved_set:
            return self.result(input_str, canonical, "REJECTED", "Reserved identity collision")
        return self.result(input_str, canonical, "SECURE", "Passed strict ASCII isolation")
