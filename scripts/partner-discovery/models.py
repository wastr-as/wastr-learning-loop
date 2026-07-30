"""Domain models for the partner-discovery extractor.

``Company`` is the source-agnostic record every connector must yield. Keeping it
independent of any one source (Brreg today; Mittanbud/FINN/SE in Phase 1) is what
lets new connectors plug in without a core rewrite (acceptance criterion, #70).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Company:
    """A normalised company record produced by a connector."""

    org_nr: str
    name: str

    # Primary NACE (dotted Brreg code) + all NACE codes the company is registered under.
    nace_primary: str | None = None
    nace_codes: list[str] = field(default_factory=list)
    nace_description: str | None = None

    kommune_nr: str | None = None
    kommune_name: str | None = None

    employees: int | None = None        # None = not registered in source
    founded_year: int | None = None

    phone: str | None = None
    email: str | None = None
    website: str | None = None

    mva_registered: bool = False

    # Latest annual operating revenue (omsetning / sumDriftsinntekter) and the year
    # it is for. Populated by the Brreg Regnskapsregister enricher (open data), which
    # automates the manual proff.no omsetning check. None = accounts not fetched or
    # not filed.
    revenue_nok: int | None = None
    revenue_year: int | None = None

    # Status flags used by the active-only quality filter.
    bankrupt: bool = False
    under_liquidation: bool = False
    under_forced_liquidation: bool = False

    org_form: str | None = None          # ENK, AS, ...
    source: str = "unknown"              # which connector produced this record

    # Populated by scoring.py.
    segment: str | None = None
    priority_score: int = 0
    why_prioritised: str = ""

    # Talk-urgency tier (1 = talk now ... 4 = future / below revenue gate). Assigned
    # by scoring.assign_tier after revenue enrichment; mirrors Denis's manual pass.
    tier: int | None = None

    @property
    def is_active(self) -> bool:
        """True if the company is not bankrupt or being wound down."""
        return not (
            self.bankrupt or self.under_liquidation or self.under_forced_liquidation
        )

    @property
    def has_contact(self) -> bool:
        """True if at least one direct contact field is present."""
        return bool(self.phone or self.email or self.website)
