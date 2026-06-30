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

    # Size band (the SMB cut). A registered count must sit at/under the cap; 0 and
    # an unregistered count are treated alike (kept; many real AS register 0). The
    # contact-or-MVA gate above already removes genuine dormant shells.
    if company.employees is not None and company.employees > 0:
        if not (config.MIN_EMPLOYEES <= company.employees <= config.MAX_EMPLOYEES):
            return False
    elif not config.KEEP_ZERO_OR_UNREGISTERED_EMPLOYEES:
        return False

    # Name gate for broad/noisy NACE codes: a company qualifying ONLY via a gated
    # code (e.g. equipment leasing 77.390) must look waste-related by name.
    if not _passes_name_gate(company):
        return False

    return True


def _passes_name_gate(company: Company) -> bool:
    """Require a waste keyword when a company only matches a name-gated NACE code."""
    target_hits = [
        c for c in ([company.nace_primary] + company.nace_codes)
        if c in config.NACE_TO_SEGMENT
    ]
    if not target_hits:
        return True  # no on-target code at all; segment attribution handles it
    clean_hits = [c for c in target_hits if c not in config.NACE_NAME_GATED]
    if clean_hits:
        return True  # qualifies on a non-gated code -> no keyword required
    name = company.name.lower()
    return any(kw in name for kw in config.WASTE_NAME_KEYWORDS)


# --------------------------------------------------------------------------- #
# 2. Scoring
# --------------------------------------------------------------------------- #
def _nace_precision_points(company: Company) -> tuple[float, str]:
    """CDW relevance + NACE precision.

    Core CDW codes (collection/treatment/sorting/demolition) score full; adjacent
    on-target codes (generic freight, groundwork, building) score lower; a match on
    a secondary code only scores lower still.
    """
    w = config.WEIGHT_NACE_PRECISION
    target = set(config.NACE_TO_SEGMENT)

    if company.nace_primary in target:
        if company.nace_primary in config.NACE_TIER1:
            return w, "core CDW NACE (primary)"
        return w * 0.85, "primary NACE on-target"

    secondary = [c for c in company.nace_codes if c in target]
    if secondary:
        if any(c in config.NACE_TIER1 for c in secondary):
            return w * 0.6, "core CDW NACE (secondary)"
        return w * 0.45, "secondary NACE on-target"
    return 0.0, ""


def _size_points(company: Company) -> tuple[float, str]:
    """Size-in-band. Sweet spot (1-10) full; 11-20 partial; 0/unknown lower.

    A registered 0 or an unregistered count is common for lean, real operators —
    if MVA-registered (i.e. a genuine operating business) it gets meaningful credit
    rather than being treated as a dead shell.
    """
    w = config.WEIGHT_SIZE_IN_BAND
    if not company.employees:  # None or 0 -> count not meaningfully registered
        if company.mva_registered:
            return w * 0.6, "lean/0 employees, MVA-registered"
        return w * 0.35, "employee count not registered"
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
        return w * 0.5, "MVA-registered (no direct contact)"
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
