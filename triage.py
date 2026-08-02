"""
PitchTrap Triage Engine – Master Playbook implementation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from config import UGLY_KEYWORDS, UGLY_DOMAINS, BAD_KEYWORDS, GOOD_SIGNALS

Category = Literal["Ugly", "Bad", "Good"]


@dataclass
class TriageResult:
    category: Category
    confidence: float
    reasons: list[str]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def classify_offer(text: str) -> TriageResult:
    if not text or not text.strip():
        return TriageResult("Ugly", 0.9, ["Empty content"])

    normalized = _normalize(text)
    reasons: list[str] = []

    # Ugly
    ugly_hits = [kw for kw in UGLY_KEYWORDS if kw in normalized]
    if ugly_hits:
        reasons.append(f"Pressure language: {', '.join(ugly_hits[:3])}")

    email_match = re.search(r"[\w\.-]+@([\w\.-]+)", text)
    if email_match and email_match.group(1).lower() in UGLY_DOMAINS:
        reasons.append(f"Unprofessional domain: {email_match.group(1)}")
        ugly_hits.append("domain")

    if re.search(r"\b(ssn|social security|bank account|routing number)\b", normalized):
        reasons.append("Requests sensitive info upfront")
        ugly_hits.append("sensitive")

    if ugly_hits:
        return TriageResult("Ugly", min(0.95, 0.7 + 0.08 * len(ugly_hits)), reasons)

    # Bad
    bad_hits = [kw for kw in BAD_KEYWORDS if kw in normalized]
    if re.search(r"\b(daily|weekly)\s+(payment|remittance|debit)\b", normalized):
        reasons.append("Daily/weekly payment structure")
        bad_hits.append("frequency")

    if bad_hits:
        reasons.insert(0, f"High-cost signals: {', '.join(bad_hits[:3])}")
        return TriageResult("Bad", min(0.92, 0.65 + 0.08 * len(bad_hits)), reasons)

    # Good
    good_hits = [s for s in GOOD_SIGNALS if s in normalized]
    has_numbers = bool(re.search(r"\$[\d,]+|\d+\.\d+%|\d+\s*(months|years)", normalized))
    if good_hits and has_numbers:
        reasons.append(f"Transparent terms: {', '.join(good_hits[:3])}")
        return TriageResult("Good", 0.78, reasons)

    reasons.append("No strong signals – defaulting to Bad for engagement")
    return TriageResult("Bad", 0.55, reasons)
