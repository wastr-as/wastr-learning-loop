"""Connector package.

A *connector* fetches raw company records from one source and yields normalised
``Company`` objects. Phase 0 ships only the Brreg connector; Phase 1 adds more
(Mittanbud, FINN, Sortere.no, a SE slot, ...) by implementing the same
``Connector`` interface — no change to scoring, dedup, or output (#56 / #70).
"""

from .base import Connector
from .brreg import BrregConnector

__all__ = ["Connector", "BrregConnector"]
