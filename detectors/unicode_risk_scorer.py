"""Advisory Unicode risk scoring for non-authoritative display names."""

from __future__ import annotations

from typing import List, Optional, Set
import unicodedata

from detectors.bidi_detector import contains_bidi_or_invisible
from detectors.mixed_script_detector import classify_script, significant_scripts
from detectors.strict_identifier_policy import StrictIdentifierPolicy

ILLEGAL_CATEGORIES = {"Cc", "Cf", "Cs", "Co", "Cn", "Zl", "Zp"}


class UnicodeRiskScorer:
    """Analyze display names without granting authorization semantics."""

    def __init__(self, reserved_names: Optional[List[str]] = None):
        self.identifier_policy = StrictIdentifierPolicy(reserved_names)
        self.reserved_set: Set[str] = self.identifier_policy.reserved_set

    def analyze(self, input_str: str) -> dict:
        """Return advisory risk results for a display-name string."""
        if not isinstance(input_str, str):
            return StrictIdentifierPolicy.result("", "", "REJECTED", "Not a string")
        canonical = unicodedata.normalize("NFC", input_str).casefold().strip()
        if not input_str:
            return StrictIdentifierPolicy.result("", "", "REJECTED", "Empty display name")
        if contains_bidi_or_invisible(input_str):
            return StrictIdentifierPolicy.result(input_str, canonical, "REJECTED", "BiDi/Invisible detected", flags=["layout_control"])

        flags: list[str] = []
        for character in input_str:
            category = unicodedata.category(character)
            if category in ILLEGAL_CATEGORIES:
                return StrictIdentifierPolicy.result(input_str, canonical, "REJECTED", f"Disallowed category: {category}")
            if category.startswith("M"):
                flags.append("combining_mark")
            if classify_script(character) == "Inherited":
                flags.append("inherited_script")

        scripts = significant_scripts(input_str)
        if len(scripts) > 1:
            return StrictIdentifierPolicy.result(input_str, canonical, "REJECTED", f"Mixed-script: {sorted(scripts)}", scripts, flags + ["mixed_script"])
        if canonical in self.reserved_set:
            return StrictIdentifierPolicy.result(input_str, canonical, "REJECTED", "Reserved identity collision", scripts, flags)
        if "combining_mark" in flags:
            return StrictIdentifierPolicy.result(input_str, canonical, "RISK_FLAGGED", "Contains combining marks; safe only as non-authoritative metadata", scripts, flags)
        return StrictIdentifierPolicy.result(input_str, canonical, "APPROVED", "Passed advisory checks", scripts, flags)


class ProductionIngressGate:
    """Combined interface for strict identifiers and display names."""

    def __init__(self, reserved_names: Optional[List[str]] = None):
        self.identifier_policy = StrictIdentifierPolicy(reserved_names)
        self.display_name_scorer = UnicodeRiskScorer(reserved_names)

    def enforce_strict_identifier_policy(self, input_str: str) -> dict:
        return self.identifier_policy.evaluate(input_str)

    def analyze_display_name(self, input_str: str) -> dict:
        return self.display_name_scorer.analyze(input_str)
