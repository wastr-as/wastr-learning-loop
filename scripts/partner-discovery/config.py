"""Configuration for the partner-discovery extractor (issue #70, operationalises #56).

All tunable knobs — target segments (NACE), geography (kommune), size band,
quality filters, and scoring weights — live here so the extraction is a
re-runnable, auditable script rather than a one-off manual pull.

NACE codes use Brreg's dotted format (e.g. ``49.410``). The trailing digit is
significant: Brreg stores 5-digit næringskoder, so ``49.41`` from the spec maps
to ``49.410`` in the register.

Kommune codes verified against the live Brreg kommune registry on 2026-06-29
(2024 Akershus reform applied — Viken codes are retired).
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Segments — the two SMB targets (issue #70 "Prioritisation logic")
# --------------------------------------------------------------------------- #
SEGMENT_A = "A"  # Independent haulers, 1-5 trucks
SEGMENT_B = "B"  # Small CDW-generating contractors

# Brreg 5-digit næringskoder per segment. Keyed by the dotted Brreg code.
SEGMENT_NACE: dict[str, dict[str, str]] = {
    SEGMENT_A: {
        "49.410": "Godstransport på vei",
        "38.110": "Innsamling av ikke-farlig avfall",
    },
    SEGMENT_B: {
        "43.110": "Riving av bygninger og andre konstruksjoner",
        "43.120": "Grunnarbeid",
        "43.990": "Annen spesialisert bygge- og anleggsvirksomhet",
        "41.200": "Oppføring av bygninger",
    },
}

# Flat lookup: dotted NACE code -> segment letter.
NACE_TO_SEGMENT: dict[str, str] = {
    code: segment
    for segment, codes in SEGMENT_NACE.items()
    for code in codes
}

# --------------------------------------------------------------------------- #
# Geography — Oslo first, optional inner ring (2024 Akershus codes)
# --------------------------------------------------------------------------- #
OSLO = "0301"

# Inner ring around Oslo. Codes verified against the Brreg kommune registry.
RING_KOMMUNER: dict[str, str] = {
    "3201": "Bærum",
    "3203": "Asker",
    "3205": "Lillestrøm",
    "3207": "Nordre Follo",
    "3222": "Lørenskog",
}

KOMMUNE_NAMES: dict[str, str] = {OSLO: "Oslo", **RING_KOMMUNER}

# Default geography for a Phase 0 run: Oslo + inner ring.
DEFAULT_KOMMUNER: list[str] = [OSLO, *RING_KOMMUNER.keys()]

# --------------------------------------------------------------------------- #
# Size band — the SMB cut
# --------------------------------------------------------------------------- #
MIN_EMPLOYEES = 1   # exclude 0-employee shells
MAX_EMPLOYEES = 20  # exclude 50+ (too big for the wedge); 20 is the hard cut
SWEET_SPOT_MAX = 10  # haulers skew 1-10 -> full size points in this band

# Keep companies that have NOT registered an employee count? Many sole-proprietor
# (ENK) haulers never register one, so excluding them would gut Segment A. We keep
# them but score them lower (see scoring.py).
KEEP_UNREGISTERED_EMPLOYEE_COUNT = True

# --------------------------------------------------------------------------- #
# Quality filters
# --------------------------------------------------------------------------- #
# Founded strictly before this year (operating, not brand-new).
FOUNDED_BEFORE_YEAR = 2025

# --------------------------------------------------------------------------- #
# Scoring weights (sum = 100). See scoring.py for how each is computed.
#
# Contact is weighted heaviest on purpose: a reachable company is worth far more
# to Iteo than an unreachable one, and contact reach is the scarcest signal in the
# open register (Brreg exposes only ``hjemmeside`` — no phone/email). Weighting it
# high pushes contactable companies to the top of the ~200-row cut.
# --------------------------------------------------------------------------- #
WEIGHT_NACE_PRECISION = 25   # segment fit + how precise the NACE match is
WEIGHT_SIZE_IN_BAND = 20
WEIGHT_OSLO_PROXIMITY = 15
WEIGHT_CONTACT_COMPLETENESS = 40

# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
SHORTLIST_SIZE = 200          # ~200-row Iteo handoff sheet
TARGET_SEGMENT_A_RATIO = 0.60  # ~60% haulers (A) / 40% contractors (B)

CSV_COLUMNS = [
    "Company",
    "Org.nr",
    "Segment",
    "NACE",
    "Kommune",
    "Employees",
    "Founded",
    "Phone",
    "Email",
    "Website",
    "Priority score",
    "Why prioritised",
]
