"""1881 contact enricher — phone/email fallback (commercial, gated).

Source: the 1881 API (https://www.api1881.no) — the same "best-in-test" contact
database Denis falls back to on 1881.no when proff.no is thin. It is a *commercial*
service: access needs a paid subscription and an API key, and there is NO open
endpoint. This enricher therefore:

  * never scrapes the 1881.no website (that would breach their ToS);
  * only calls the official API, using credentials supplied via env vars;
  * stays disabled until BOTH the credentials AND the #56 legal/ToS review
    opt-in are present, so it can be committed safely without running.

Configuration (all via environment variables):

    API1881_URL          Base lookup URL from your 1881 API contract, with an
                         ``{org_nr}`` placeholder, e.g.
                         "https://api.api1881.no/lookup/company/{org_nr}".
    API1881_KEY          API key / bearer token from your subscription.
    WASTR_1881_LEGAL_OK  Set to "1" to confirm the #56 legal/ToS review passed.

Because the exact response schema depends on the subscribed product, the JSON
field mapping is applied defensively (several likely key names) and should be
confirmed against the provisioned contract before first production use.

Standard library only.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

from enrichers.base import Enricher
from models import Company

REQUEST_TIMEOUT = 30
POLITE_DELAY = 0.3
MAX_RETRIES = 3
USER_AGENT = "wastr-partner-discovery/1.0 (+https://github.com/wastr-as)"

# Response keys we will accept for each field, in priority order. The 1881 product
# schema is confirmed per subscription; this covers the common shapes.
_PHONE_KEYS = ("phone", "telefon", "mobil", "phoneNumber", "telephone")
_EMAIL_KEYS = ("email", "epost", "e_post", "emailAddress")


class Api1881Enricher(Enricher):
    name = "api1881"
    is_open_data = False  # commercial — gated behind creds + #56 review

    def __init__(self) -> None:
        self.base_url = os.environ.get("API1881_URL", "")
        self.api_key = os.environ.get("API1881_KEY", "")
        self.legal_ok = os.environ.get("WASTR_1881_LEGAL_OK") == "1"

    def available(self) -> bool:
        """Only runnable with an endpoint, a key, and the #56 legal opt-in."""
        return bool(self.base_url and self.api_key and self.legal_ok)

    def enrich(self, companies: list[Company]) -> None:
        if not self.available():
            print(
                "    1881 enricher skipped — set API1881_URL, API1881_KEY and "
                "WASTR_1881_LEGAL_OK=1 (paid subscription + #56 review) to enable."
            )
            return

        # Only look up companies still missing a direct channel — saves paid calls.
        targets = [c for c in companies if not (c.phone or c.email)]
        total = len(targets)
        for i, company in enumerate(targets, start=1):
            if not company.org_nr:
                continue
            phone, email = self._lookup(company.org_nr)
            if phone and not company.phone:
                company.phone = phone
            if email and not company.email:
                company.email = email
            if i % 25 == 0 or i == total:
                print(f"    contact enriched {i}/{total}")
            time.sleep(POLITE_DELAY)

    # ------------------------------------------------------------------ #
    # Internals
    # ------------------------------------------------------------------ #
    def _lookup(self, org_nr: str) -> tuple[str | None, str | None]:
        payload = self._get(org_nr)
        if not payload:
            return None, None
        return self._first(payload, _PHONE_KEYS), self._first(payload, _EMAIL_KEYS)

    @staticmethod
    def _first(payload: dict, keys: tuple[str, ...]) -> str | None:
        for key in keys:
            value = payload.get(key)
            if value:
                return str(value)
        return None

    def _get(self, org_nr: str) -> dict:
        url = self.base_url.format(org_nr=org_nr)
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": USER_AGENT,
            },
        )
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    return data if isinstance(data, dict) else {}
            except urllib.error.HTTPError as exc:
                if exc.code == 404:      # no listing for this org.nr
                    return {}
                time.sleep(POLITE_DELAY * attempt * 2)
            except (urllib.error.URLError, TimeoutError):
                time.sleep(POLITE_DELAY * attempt * 2)
        return {}
