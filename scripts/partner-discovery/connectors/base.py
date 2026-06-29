"""Pluggable connector interface (Phase 1 extension point, carries #56 forward).

Every source — Brreg today, Mittanbud / FINN / Sortere.no / a second country
tomorrow — implements ``Connector.fetch`` and yields normalised ``Company``
records. The rest of the pipeline (dedup, scoring, CSV) never needs to know which
source a record came from.

Legal note: a connector for any *non-open* source MUST respect robots.txt + ToS
and trigger the #56 legal/compliance kill-criterion review before it ships.
Brreg (Enhetsregisteret) is open data under NLOD, so it carries no such risk.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

from models import Company


class Connector(ABC):
    """Base class for all partner-discovery data sources."""

    #: Short identifier stamped onto every Company this connector yields.
    name: str = "base"

    #: True only for open-data sources (NLOD/CC). Non-open connectors are gated
    #: behind the #56 legal review before they may run.
    is_open_data: bool = False

    @abstractmethod
    def fetch(
        self,
        nace_codes: list[str],
        kommuner: list[str],
    ) -> Iterator[Company]:
        """Yield normalised Company records matching the given NACE + kommune sets.

        Implementations should stream results (yield) rather than building a giant
        list, and apply only *source-side* filtering. Cross-cutting quality filters
        and scoring are applied centrally so behaviour is identical across sources.
        """
        raise NotImplementedError
