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
#
# Segment A is the haul/collect side. Beyond the two codes in the original #70
# spec, real CDW-collection peers (skip-bag / container / removal operators such as
# Hente, Kvikk Bag, Avfallssekk, Containerservice) register under waste-treatment
# and equipment-rental codes too — so those are included here. The broad, noisy
# codes (equipment leasing 77.390, removal transport 49.420) are name-gated below
# so only waste-relevant companies survive.
SEGMENT_NACE: dict[str, dict[str, str]] = {
    SEGMENT_A: {
        "49.410": "Godstransport på vei",
        "38.110": "Innsamling av ikke-farlig avfall",
        "38.210": "Behandling og disponering av ikke-farlig avfall",
        "38.320": "Sortering og bearbeiding av avfall for materialgjenvinning",
        "49.420": "Flyttetransport",
        "77.390": "Utleie/leasing av andre maskiner og utstyr (skip/container/sekk)",
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

# Broad NACE codes that also contain a lot of non-waste noise. A company qualifying
# ONLY via one of these codes must additionally have a waste-related name keyword
# (see WASTE_NAME_KEYWORDS) to survive the quality filter. A company that also
# matches a clean target code (e.g. 38.110) is kept regardless.
NACE_NAME_GATED: set[str] = {"77.390", "49.420"}

# CDW-relevance tiers used by scoring. Tier 1 = core construction & demolition waste
# collection / treatment / sorting / demolition — the codes that most precisely
# identify a WASTR-relevant actor. Everything else on-target is adjacent (generic
# road freight, groundwork, building) — it catches real firms but also noise, so it
# scores lower. This is what floats actual waste operators above generic freight.
NACE_TIER1: set[str] = {"38.110", "38.210", "38.320", "43.110"}

WASTE_NAME_KEYWORDS: tuple[str, ...] = (
    "avfall", "sekk", "container", "renovasjon", "gjenvinning", "miljø", "miljo",
    "resirk", "skrot", "deponi", "søppel", "soppel", "rydd", "kast", "skvett",
    "bag", "henger", "lift", "massetransport", "masse",
)

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
MIN_EMPLOYEES = 1   # lower bound of the registered-count band
MAX_EMPLOYEES = 20  # exclude 50+ (too big for the wedge); 20 is the hard cut
SWEET_SPOT_MAX = 10  # haulers skew 1-10 -> full size points in this band

# Many real, operating AS companies register ``antallAnsatte = 0`` (owner-operated,
# or staff hired via sub-contract) — e.g. Hente AS. Treating a registered 0 as a
# hard "shell" exclusion drops flagship targets, so 0 is handled like "not
# registered": kept (it still must pass the contact-or-MVA gate) and scored low.
# Genuine dormant shells are removed by the contact-or-MVA quality filter instead.
KEEP_ZERO_OR_UNREGISTERED_EMPLOYEES = True

# --------------------------------------------------------------------------- #
# Quality filters
# --------------------------------------------------------------------------- #
# Founded strictly before this year (operating, not brand-new).
FOUNDED_BEFORE_YEAR = 2025

# --------------------------------------------------------------------------- #
# Scoring weights (sum = 100). See scoring.py for how each is computed.
#
# Balanced so CDW relevance (NACE) leads, with contact still a strong signal but
# not so dominant that it buries lean, recognisable waste operators (often 0
# registered employees, no website, MVA-registered only) beneath generic freight
# firms that merely happen to have a website.
# --------------------------------------------------------------------------- #
WEIGHT_NACE_PRECISION = 30   # CDW relevance + how precise the NACE match is
WEIGHT_SIZE_IN_BAND = 20
WEIGHT_OSLO_PROXIMITY = 15
WEIGHT_CONTACT_COMPLETENESS = 35

# --------------------------------------------------------------------------- #
# Revenue gate + talk-urgency tiers (Denis's manual pass, automated)
#
# Denis tiers the shortlist by omsetning (from proff.no) + talk-urgency:
#   * omsetning < 3 MNOK        -> Tier 4 immediately
#   * otherwise Tier 1 (talk now) / 2 (contact soon) / 3 (future) by strength.
# The omsetning figure is fetched for free from Brreg's Regnskapsregister (the
# RegnskapEnricher), so this reproduces the objective part of his rule. The
# subjective signals ("ønsket pilot", "brukt selv") stay a manual override in the
# "Why prioritised" column.
# --------------------------------------------------------------------------- #
REVENUE_GATE_NOK = 3_000_000   # < this -> Tier 4 (Denis's ">3 MNOK" relevance gate)

# Priority-score thresholds for tiering companies that clear the revenue gate (or
# whose revenue is unknown). Scores typically land ~72-86 for flagship targets.
TIER1_MIN_SCORE = 75   # talk right now
TIER2_MIN_SCORE = 60   # can wait, but must contact
# Below TIER2_MIN_SCORE -> Tier 3 (future pipeline).

# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
SHORTLIST_SIZE = 200          # ~200-row Iteo handoff sheet
TARGET_SEGMENT_A_RATIO = 0.60  # ~60% haulers (A) / 40% contractors (B)

CSV_COLUMNS = [
    "Company",
    "Org.nr",
    "Segment",
    "Tier",
    "NACE",
    "Kommune",
    "Employees",
    "Revenue (NOK)",
    "Revenue year",
    "Founded",
    "Phone",
    "Email",
    "Website",
    "Priority score",
    "Why prioritised",
]
