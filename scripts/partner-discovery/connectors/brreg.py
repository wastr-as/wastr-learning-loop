"""Brreg / Enhetsregisteret connector (Phase 0 primary source).

Source: https://data.brreg.no/enhetsregisteret/api/enheter — open data under NLOD,
free to use, redistribute, and hand to Iteo. No login, no ToS risk.

The open register exposes org.nr, name, NACE (up to 3 codes), address/kommune,
employee count, registration date, MVA status, and ``hjemmeside`` (website). It does
NOT expose phone or email — those stay empty in Phase 0 and are candidates for a
Phase 1 enrichment connector.

Uses only the Python standard library so the hand-off script runs with no
``pip install`` step.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterator

from connectors.base import Connector
from models import Company

API_URL = "https://data.brreg.no/enhetsregisteret/api/enheter"
PAGE_SIZE = 500           # Brreg caps page*size at 10000; per nace+kommune we stay well under
REQUEST_TIMEOUT = 30      # seconds
POLITE_DELAY = 0.2        # seconds between requests — open API, but be courteous
MAX_RETRIES = 3
USER_AGENT = "wastr-partner-discovery/1.0 (+https://github.com/wastr-as)"


class BrregConnector(Connector):
    name = "brreg"
    is_open_data = True

    def fetch(
        self,
        nace_codes: list[str],
        kommuner: list[str],
    ) -> Iterator[Company]:
        """Stream Company records for every (nace, kommune) the spec targets.

        One query per NACE code, with all kommuner passed at once (Brreg accepts a
        repeated ``kommunenummer`` param). De-duplication across NACE codes is the
        pipeline's job, not the connector's.
        """
        for nace in nace_codes:
            yield from self._fetch_nace(nace, kommuner)

    # ------------------------------------------------------------------ #
    # Internals
    # ------------------------------------------------------------------ #
    def _fetch_nace(self, nace: str, kommuner: list[str]) -> Iterator[Company]:
        page = 0
        while True:
            payload = self._get(
                [
                    ("naeringskode", nace),
                    *[("kommunenummer", k) for k in kommuner],
                    ("konkurs", "false"),
                    ("size", str(PAGE_SIZE)),
                    ("page", str(page)),
                ]
            )

            enheter = payload.get("_embedded", {}).get("enheter", [])
            for raw in enheter:
                yield self._to_company(raw)

            page_info = payload.get("page", {})
            total_pages = page_info.get("totalPages", 0)
            page += 1
            if page >= total_pages:
                break
            time.sleep(POLITE_DELAY)

    @staticmethod
    def _get(params: list[tuple[str, str]]) -> dict:
        url = f"{API_URL}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(
            url, headers={"Accept": "application/json", "User-Agent": USER_AGENT}
        )
        last_err: Exception | None = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except (urllib.error.URLError, TimeoutError) as exc:  # pragma: no cover
                last_err = exc
                time.sleep(POLITE_DELAY * attempt * 2)
        raise RuntimeError(f"Brreg request failed after {MAX_RETRIES} retries: {last_err}")

    @staticmethod
    def _to_company(raw: dict) -> Company:
        nace_codes: list[str] = []
        nace_primary: str | None = None
        nace_description: str | None = None
        for i, key in enumerate(("naeringskode1", "naeringskode2", "naeringskode3")):
            node = raw.get(key)
            if node and node.get("kode"):
                nace_codes.append(node["kode"])
                if i == 0:
                    nace_primary = node["kode"]
                    nace_description = node.get("beskrivelse")

        # Prefer the business address, fall back to the postal address.
        addr = raw.get("forretningsadresse") or raw.get("postadresse") or {}
        kommune_nr = addr.get("kommunenummer")
        kommune_name = addr.get("kommune")

        founded_year = None
        reg_date = raw.get("registreringsdatoEnhetsregisteret")
        if reg_date and len(reg_date) >= 4:
            founded_year = int(reg_date[:4])

        employees = None
        if raw.get("harRegistrertAntallAnsatte"):
            employees = raw.get("antallAnsatte")

        return Company(
            org_nr=raw.get("organisasjonsnummer", ""),
            name=raw.get("navn", ""),
            nace_primary=nace_primary,
            nace_codes=nace_codes,
            nace_description=nace_description,
            kommune_nr=kommune_nr,
            kommune_name=kommune_name,
            employees=employees,
            founded_year=founded_year,
            phone=None,                                  # not in open register
            email=None,                                  # not in open register
            website=raw.get("hjemmeside") or None,
            mva_registered=bool(raw.get("registrertIMvaregisteret")),
            bankrupt=bool(raw.get("konkurs")),
            under_liquidation=bool(raw.get("underAvvikling")),
            under_forced_liquidation=bool(
                raw.get("underTvangsavviklingEllerTvangsopplosning")
            ),
            org_form=(raw.get("organisasjonsform") or {}).get("kode"),
            source="brreg",
        )
