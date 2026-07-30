"""Enricher package.

Where a *connector* discovers companies (yields new ``Company`` records), an
*enricher* takes companies already in the shortlist and fills in fields the
primary source (Brreg's open register) cannot provide:

* ``RegnskapEnricher``  — operating revenue (omsetning) from Brreg's open
  Regnskapsregister. This automates the manual proff.no revenue check.
* ``Api1881Enricher``   — phone/email from the commercial 1881 API. Non-open,
  credential-gated, and subject to the #56 legal/ToS review before it runs.

Enrichers mutate the passed-in ``Company`` objects in place and never drop or add
records, so they are safe to chain in any order after selection.
"""

from .base import Enricher
from .regnskap import RegnskapEnricher
from .api1881 import Api1881Enricher

__all__ = ["Enricher", "RegnskapEnricher", "Api1881Enricher"]
