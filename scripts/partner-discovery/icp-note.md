# ICP note — WASTR partner shortlist for Iteo (Phase 0)

> Accompanies `iteo-shortlist-YYYYMMDD.csv`. One page. Read this first.
> Issue #70 · BET #56 · Lane A / B2B · Hand-off coordinated by Denis.

## What this list is

A **prioritised ~200-company shortlist** of real construction & demolition waste
(CDW) actors in Oslo + inner ring, pulled from the open Brønnøysund Register and
ranked by WASTR's fit logic. **We filtered; you qualify.** This is curated volume,
not our analysis of who to sign — the actor prioritisation, interview guide, and
ICP authoring are Iteo's paid deliverable.

## The funnel target

```
200 companies (this sheet)
  → Iteo qualifies ~30-40 via interviews
    → 1-5 pilot-ready companies (signed LOI / pilot intent)
```

## Who is on the list (ICP definition)

Two SMB segments, mixed ~**60% A / 40% B**:

- **A — Independent haulers, 1–5 trucks.** NACE `49.41` (godstransport på vei),
  `38.11` (innsamling ikke-farlig avfall). The empty-running pain is sharpest here.
- **B — Small CDW-generating contractors.** NACE `43.11` (riving), `43.12`
  (grunnarbeid), `43.99` (annen spesialisert bygg/anlegg), `41.20` (oppføring).
  These generate the waste and feel the coordination/admin burden.

**Filters applied:** active companies only (no konkurs / avvikling); founded before
2025 (operating, not brand-new); 1–20 employees (haulers skew 1–10); Oslo first,
inner ring (Bærum, Asker, Lillestrøm, Nordre Follo, Lørenskog) next. De-duplicated
by org.nr. Each row's **"Why prioritised"** column shows what earned its score.

## What we want back per conversation

For every company Iteo talks to, three signals:

1. **Pain confirmed?** Do they actually lose time/money to empty-running (A) or
   waste coordination + documentation (B)? Y / N + one quote.
2. **Willingness to pay?** Would they pay a monthly licence (A: per vehicle) or
   per-project licence (B)? Rough price reaction.
3. **Pilot interest?** Y / N — and if Y, would they sign an LOI / pilot intent?

## Honest caveat — contact data

Brreg's open data gives us **org.nr, name, NACE, kommune, employees, founding year,
and website** — but **not phone or email** (the open register simply doesn't carry
them). So on this sheet:

- **Org.nr is present for 100% of rows** — the universal key. Phone numbers are a
  one-step public lookup from org.nr (1881.no, Proff, gulesider).
- ~44% have a website; ~91% are MVA-registered (i.e. real, operating businesses).
- **100% are reachable** via org.nr + standard lookups.

Pre-filled phone/email is the **next increment** (a Phase 1 enrichment connector,
keyed on the org.nr we already provide) — not a blocker for starting outreach now.

## Sheet columns

`Company | Org.nr | Segment (A/B) | NACE | Kommune | Employees | Founded | Phone |
Email | Website | Priority score | Why prioritised`

## Re-running

The list is produced by a re-runnable script (`extract.py`) — re-run any time to
refresh as the register updates, widen geography, or change the size band. No login,
no manual pull.
