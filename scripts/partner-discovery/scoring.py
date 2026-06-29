"""Quality filtering, prioritisation scoring, and selection.

This module is the "we filter" value of the deliverable (#70): it turns the raw
Brreg universe into a curated, ranked ~200-row shortlist so Iteo spends its paid
hours qualifying, not sifting.

Pipeline:
    1. quality_filter   — active / age / contact-or-MVA / size band
    2. score            — priority_score + why_prioritised on each Company
    3. select_shortlist — rank, apply ~60/40 A/B mix, cut to ~200
"""

from __future__ import annotations

import config
from models import Company


# --------------------------------------------------------------------------- #
# 1. Quality filters
# --------------------------------------------------------------------------- #
def passes_quality(company: Company) -> bool:
    """True if a company survives the hard quality cuts (issue #70)."""
    # Active only.
    if not company.is_active:
        return False

    # Founded before the cutoff (operating, not brand-new).
    if company.founded_year is None or company.founded_year >= config.FOUNDED_BEFORE_YEAR:
        return False

    # Has at least one contact field OR is MVA-registered.
    if not (company.has_contact or company.mva_registered):
        return False

    # Size band (the SMB cut). Companies with no registered count are kept only if
    # configured to (they score lower); a registered count must sit in 1-20.
    if company.employees is None:
        return config.KEEP_UNREGISTERED_EMPLOYEE_COUNT
    return config.MIN_EMPLOYEES <= company.employees <= config.MAX_EMPLOYEES


# --------------------------------------------------------------------------- #
# 2. Scoring
# --------------------------------------------------------------------------- #
def _nace_precision_points(company: Company) -> tuple[float, str]:
    """Segment fit + NACE precision. Full marks when a target NACE is primary."""
    target = {c for codes in config.SEGMENT_NACE.values() for c in codes}
    primary_hit = company.nace_primary in target
    secondary_hit = any(c in target for c in company.nace_codes)

    if primary_hit:
        return config.WEIGHT_NACE_PRECISION, "primary NACE on-target"
    if secondary_hit:
        return config.WEIGHT_NACE_PRECISION * 0.5, "secondary NACE on-target"
    return 0.0, ""


def _size_points(company: Company) -> tuple[float, str]:
    """Size-in-band. Sweet spot (1-10) full; 11-20 partial; unknown lowest."""
    w = config.WEIGHT_SIZE_IN_BAND
    if company.employees is None:
        return w * 0.4, "employee count not registered"
    if company.employees <= config.SWEET_SPOT_MAX:
        return w, f"{company.employees} employees (sweet spot)"
    return w * 0.7, f"{company.employees} employees"


def _proximity_points(company: Company) -> tuple[float, str]:
    """Oslo proximity. Oslo full; inner ring partial."""
    w = config.WEIGHT_OSLO_PROXIMITY
    if company.kommune_nr == config.OSLO:
        return w, "Oslo"
    if company.kommune_nr in config.RING_KOMMUNER:
        return w * 0.6, config.RING_KOMMUNER[company.kommune_nr]
    return 0.0, ""


def _contact_points(company: Company) -> tuple[float, str]:
    """Contact completeness — the heaviest signal.

    A reachable company is worth far more to Iteo than an unreachable one. Brreg's
    open register exposes only ``hjemmeside`` (website), so website presence carries
    most of the weight; phone/email top it up when a Phase 1 enrichment connector
    fills them. MVA registration is a weak fallback proxy when no direct channel
    exists at all.
    """
    w = config.WEIGHT_CONTACT_COMPLETENESS
    if company.website or company.phone or company.email:
        pts = 0.0
        present: list[str] = []
        if company.website:
            pts += w * 0.6
            present.append("website")
        if company.phone:
            pts += w * 0.2
            present.append("phone")
        if company.email:
            pts += w * 0.2
            present.append("email")
        return min(pts, w), "contact: " + "+".join(present)
    if company.mva_registered:
        return w * 0.25, "MVA-registered (no direct contact)"
    return 0.0, ""


def score(company: Company) -> Company:
    """Set ``segment``, ``priority_score`` (0-100) and ``why_prioritised``."""
    company.segment = config.NACE_TO_SEGMENT.get(company.nace_primary or "")
    if company.segment is None:
        # Primary NACE off-target but a secondary code matched -> attribute by the
        # first matching secondary code.
        for c in company.nace_codes:
            if c in config.NACE_TO_SEGMENT:
                company.segment = config.NACE_TO_SEGMENT[c]
                break

    reasons: list[str] = []
    total = 0.0
    for points, reason in (
        _nace_precision_points(company),
        _size_points(company),
        _proximity_points(company),
        _contact_points(company),
    ):
        total += points
        if reason:
            reasons.append(reason)

    company.priority_score = round(total)
    company.why_prioritised = "; ".join(reasons)
    return company


# --------------------------------------------------------------------------- #
# 3. Selection — rank + ~60/40 A/B mix, cut to ~200
# --------------------------------------------------------------------------- #
def select_shortlist(
    companies: list[Company],
    size: int = config.SHORTLIST_SIZE,
    segment_a_ratio: float = config.TARGET_SEGMENT_A_RATIO,
) -> list[Company]:
    """Return the top ~``size`` companies, honouring the target A/B mix.

    Each segment is filled from its own score-ranked queue up to its quota; any
    shortfall in one segment is back-filled from the other so we always hit ``size``
    when enough candidates exist.
    """
    ranked = sorted(companies, key=lambda c: c.priority_score, reverse=True)
    queue_a = [c for c in ranked if c.segment == config.SEGMENT_A]
    queue_b = [c for c in ranked if c.segment == config.SEGMENT_B]

    quota_a = round(size * segment_a_ratio)
    quota_b = size - quota_a

    picked_a = queue_a[:quota_a]
    picked_b = queue_b[:quota_b]

    # Back-fill any shortfall from the other segment's remainder.
    shortfall = size - len(picked_a) - len(picked_b)
    if shortfall > 0:
        leftovers = sorted(
            queue_a[len(picked_a):] + queue_b[len(picked_b):],
            key=lambda c: c.priority_score,
            reverse=True,
        )
        picked_a_b = picked_a + picked_b + leftovers[:shortfall]
    else:
        picked_a_b = picked_a + picked_b

    return sorted(picked_a_b, key=lambda c: c.priority_score, reverse=True)
