"""Pluggable enricher interface.

An enricher augments companies that are already in the shortlist with fields the
primary connector (Brreg open register) does not expose — revenue, direct contact
details, etc. It mutates the ``Company`` objects in place; it must never add or
drop records.

Legal note (carries #56 forward): an enricher backed by any *non-open* source
MUST respect robots.txt + ToS, require explicit credentials, and pass the #56
legal/compliance review before it is allowed to run. Open-data enrichers
(``is_open_data = True``) carry no such gate.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from models import Company


class Enricher(ABC):
    """Base class for all shortlist enrichers."""

    #: Short identifier for logging.
    name: str = "base"

    #: True only for open-data sources (NLOD/CC). Non-open enrichers are gated
    #: behind credentials + the #56 legal review before they may run.
    is_open_data: bool = False

    def available(self) -> bool:
        """Return True if the enricher is configured and allowed to run.

        Open-data enrichers are always available. Commercial ones override this to
        check for credentials and the legal-review opt-in.
        """
        return self.is_open_data

    @abstractmethod
    def enrich(self, companies: list[Company]) -> None:
        """Populate additional fields on each company in place.

        Implementations should degrade gracefully: a per-company lookup failure
        must leave that company untouched rather than aborting the whole run.
        """
        raise NotImplementedError
