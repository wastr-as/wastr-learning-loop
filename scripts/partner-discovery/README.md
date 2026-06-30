# Partner-discovery extractor — Brreg-first CDW shortlist for Iteo

> Operationalises issue **#70** (Phase 0) / BET **#56**. Owner: Siarhei. Hand-off to
> Iteo: Denis. Lane A / B2B — Innovasjon Norge-reportable. Output IP is WASTR's.

A re-runnable script that pulls real construction & demolition waste (CDW) actors
from the **Brønnøysund Register (Brreg / Enhetsregisteret)**, applies WASTR's
prioritisation, and writes a ranked **~200-row CSV** for hand-off to Iteo.

The value is the **filter**: we hand Iteo a curated shortlist, not a 10k dump, so
Iteo spends its paid hours qualifying — not sifting.

```
Funnel:  ~3,400 raw  ->  ~1,500 qualified  ->  200 prioritised (this CSV)
         Iteo qualifies ~30-40 via interviews  ->  1-5 pilot-ready (signed LOI/intent)
```

---

## Quick start

No dependencies — Python 3.10+ standard library only (`urllib`, `json`, `csv`).

```bash
python extract.py                       # Oslo + inner ring, ~200-row shortlist
python extract.py --oslo-only           # Oslo (0301) only
python extract.py --size 150            # cap shortlist size
python extract.py --no-cap              # write every qualified company (audit dump)
python extract.py --out path/to.csv     # custom output path
```

Output lands in `output/iteo-shortlist-YYYYMMDD.csv` (UTF-8 BOM, opens clean in
Excel). The `output/` folder is git-ignored — the CSV is a generated artefact.

---

## What it does

| Stage | Logic | Source file |
|---|---|---|
| **Fetch** | Brreg `enheter` API, one query per NACE code × all kommuner, paginated | `connectors/brreg.py` |
| **De-dup** | by `org.nr`, keeping the most contactable record | `extract.py` |
| **Quality filter** | active only · founded < 2025 · contact-or-MVA · size ≤ 20 (0/unregistered kept) · waste name-gate on broad codes | `scoring.py` |
| **Score** | 0–100 priority: NACE relevance + size + Oslo proximity + contact | `scoring.py` |
| **Select** | rank, enforce ~60/40 A/B mix, cut to ~200 | `scoring.py` |
| **Write** | CSV in the Iteo hand-off schema | `extract.py` |

### Segments (two SMB targets)

- **A — Haulers & waste collectors.** Core CDW codes: `38.11` Innsamling ikke-farlig
  avfall, `38.21` Behandling/disponering ikke-farlig avfall, `38.32` Sortering for
  materialgjenvinning. Plus adjacent transport: `49.41` Godstransport på vei, and —
  name-gated to waste only — `49.42` Flyttetransport and `77.39` utleie av
  skip/container/sekk (this is where skip-bag operators like Avfallssekk / Kvikk
  Bag / Containerservice register).
- **B — Small CDW-generating contractors**: `43.11` Riving, `43.12` Grunnarbeid,
  `43.99` Annen spesialisert bygg/anlegg, `41.20` Oppføring av bygninger.

> **Name-gated codes** (`77.39`, `49.42`) are broad/noisy, so a company qualifying
> *only* via one of them must also have a waste-related name keyword (avfall, sekk,
> container, renovasjon, gjenvinning, …). A company that also matches a clean code
> (e.g. `38.11`) is kept regardless.

### Geography (2024 Akershus codes, verified against Brreg)

Oslo `0301` first, then inner ring: Bærum `3201`, Asker `3203`, Lillestrøm `3205`,
Nordre Follo `3207`, Lørenskog `3222`.

### Priority score (0–100)

| Component | Weight | Full marks when… |
|---|---|---|
| NACE relevance / precision | 30 | a **core CDW** code (`38.11/38.21/38.32/43.11`) is primary |
| Size in band | 20 | 1–10 employees (the sweet spot) |
| Oslo proximity | 15 | kommune = Oslo `0301` |
| Contact completeness | 35 | website + phone + email present |

NACE relevance leads so actual waste operators rank above generic road-freight /
courier firms that merely share code `49.41`. Lean operators (0 registered
employees, no website, MVA-registered) are **not** buried: a registered `0` is
treated like "unregistered" and MVA registration earns real size + contact credit —
so flagship targets like **Hente AS** and **Kvikk Bag AS** rank inside the cut.

---

## Known limitation — contact data (read before hand-off)

**Brreg's open register exposes `hjemmeside` (website) only. It does NOT carry
phone or email.** Phase 0 is scoped Brreg-only (live enrichment is explicitly out
of scope in #70), so the `Phone` and `Email` columns ship empty.

What this means for the ≥80%-with-contact acceptance target:

| Reachability signal | Coverage in the 200-row cut |
|---|---|
| **Org.nr** (universal lookup key) | **100%** |
| MVA-registered (real operating business) | **100%** |
| Reachable (website **or** MVA) | **100%** |
| Direct website field | ~26% |

Every row carries an **org.nr**, which is the universal key for Norwegian contact
lookup (1881, Proff, Forvalt) and for the **first Phase 1 enrichment connector**.
So the list is 100% actionable today; phone/email pre-fill is the next increment,
not a Phase 0 blocker. This deviation is documented for Denis/Iteo in
[`icp-note.md`](icp-note.md).

> **Want every recognisable company, not just the top 200?** Run with `--no-cap`
> to emit the **full ranked qualified universe** (~1,500 rows) so any known
> operator can be found by org.nr. The 200-row cut is Iteo's focus list; the full
> file is the transparency backstop for "company X is missing" questions.

---

## Phase 1 — pluggable connectors (carries #56 forward)

New sources implement one interface — `connectors/base.py::Connector.fetch` —
yielding the source-agnostic `Company` model. Scoring, de-dup, and CSV output never
change. Candidate connectors: Mittanbud, Anbudstorget, FINN, Sortere.no, NOL,
Kompass, Sirk Norge, NCCE, NESO, EBA, MEF, a contact-**enrichment** connector
(keyed on org.nr), and a second-country slot (SE).

> **Legal gate:** any connector for a *non-open* source must respect robots.txt +
> ToS and trigger the **#56 legal/compliance kill-criterion review** before it
> ships. Brreg is open data under NLOD and carries no such risk.

---

## Files

```
partner-discovery/
├── config.py              # NACE, kommune codes, size band, weights, output schema
├── models.py              # Company — the source-agnostic record
├── connectors/
│   ├── base.py            # Connector ABC (Phase 1 extension point)
│   └── brreg.py           # Brreg / Enhetsregisteret connector (Phase 0)
├── scoring.py             # quality filter + priority score + 60/40 selection
├── extract.py             # CLI entrypoint, de-dup, CSV writer
├── icp-note.md            # one-page ICP + "what we want back" note for Iteo
├── requirements.txt       # (intentionally empty — stdlib only)
└── output/                # generated CSVs (git-ignored)
```
