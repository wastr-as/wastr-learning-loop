"""Brreg Regnskapsregister enricher — operating revenue (omsetning).

Source: https://data.brreg.no/regnskapsregisteret/regnskap/{orgnr}
Open data under NLOD — free, no login, safe to hand to Iteo. This is the API that
makes the manual proff.no step unnecessary: proff.no has no open API and scraping
it breaches their ToS, but the *same* omsetning figure is filed here for every
company that submits annual accounts (AS, etc.).

The endpoint returns a JSON list of annual accounts (newest years included). We
take the most recent period and read operating revenue from:

    resultatregnskapResultat.driftsresultat.driftsinntekter.sumDriftsinntekter

Companies that have not filed accounts (many brand-new or very small ENK) simply
return no data and are left with ``revenue_nok = None``.

Standard library only — no ``pip install`` needed.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from collections.abc import Iterable

from enrichers.base import Enricher
from models import Company

API_URL = "https://data.brreg.no/regnskapsregisteret/regnskap/{org_nr}"
REQUEST_TIMEOUT = 30
POLITE_DELAY = 0.2        # open API, but be courteous — one call per company
MAX_RETRIES = 3
USER_AGENT = "wastr-partner-discovery/1.0 (+https://github.com/wastr-as)"


class RegnskapEnricher(Enricher):
    name = "regnskap"
    is_open_data = True

    def enrich(self, companies: list[Company]) -> None:
        total = len(companies)
        for i, company in enumerate(companies, start=1):
            if not company.org_nr:
                continue
            revenue, year = self._fetch_latest_revenue(company.org_nr)
            if revenue is not None:
                company.revenue_nok = revenue
                company.revenue_year = year
            if i % 25 == 0 or i == total:
                print(f"    revenue enriched {i}/{total}")
            time.sleep(POLITE_DELAY)

    # ------------------------------------------------------------------ #
    # Internals
    # ------------------------------------------------------------------ #
    def _fetch_latest_revenue(self, org_nr: str) -> tuple[int | None, int | None]:
        """Return (revenue_nok, year) for the most recent filed accounts, or (None, None)."""
        accounts = self._get(org_nr)
        if not accounts:
            return None, None

        latest = self._latest_period(accounts)
        if latest is None:
            return None, None

        revenue = (
            latest.get("resultatregnskapResultat", {})
            .get("driftsresultat", {})
            .get("driftsinntekter", {})
            .get("sumDriftsinntekter")
        )
        if revenue is None:
            return None, None

        til_dato = latest.get("regnskapsperiode", {}).get("tilDato", "")
        year = int(til_dato[:4]) if til_dato[:4].isdigit() else None
        return int(round(revenue)), year

    @staticmethod
    def _latest_period(accounts: Iterable[dict]) -> dict | None:
        """Pick the accounts entry with the newest ``regnskapsperiode.tilDato``."""
        best: dict | None = None
        best_key = ""
        for entry in accounts:
            til = entry.get("regnskapsperiode", {}).get("tilDato", "")
            if til > best_key:
                best_key = til
                best = entry
        return best

    @staticmethod
    def _get(org_nr: str) -> list[dict]:
        url = API_URL.format(org_nr=org_nr)
        req = urllib.request.Request(
            url, headers={"Accept": "application/json", "User-Agent": USER_AGENT}
        )
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    return data if isinstance(data, list) else []
            except urllib.error.HTTPError as exc:
                # 404 = no accounts filed for this org.nr; treat as "no data".
                if exc.code == 404:
                    return []
                time.sleep(POLITE_DELAY * attempt * 2)
            except (urllib.error.URLError, TimeoutError):
                time.sleep(POLITE_DELAY * attempt * 2)
        # Give up on this company rather than aborting the whole run.
        return []
