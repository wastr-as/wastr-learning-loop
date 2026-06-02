# ADR-0012: NVDB as toll-data source for Norway

- **Status:** Accepted
- **Date:** 2026-06-03
- **Deciders:** Siarhei (CTO)

## Context

SPEC [#46](https://github.com/wastr-as/learning-loop/issues/46) Phase 0 requires choosing a toll-data source for the toll-aware routing capability. Three candidates were on the table:

| Source | Coverage | Cost | Quality | Risk |
|---|---|---|---|---|
| Fjellinjen / Skyttel commercial API | Full Oslo + national | License fee, procurement lead time | Authoritative, real-time | Vendor lock-in; slow to start |
| **Statens vegvesen NVDB** (open data) | National geometries + station metadata; partial tariffs | Free | Authoritative for geometry; tariffs lag and have coverage gaps | Manual tariff fallback needed; no per-pass invoicing |
| Public PDFs + manual zone polygons | What we curate | Engineering only | Brittle; stale fast | Acceptable only for one-off pilot validation |

## Decision

**Use NVDB API LES v3 (`https://nvdbapiles-v3.atlas.vegvesen.no`) as the primary toll-data source, with a small hand-curated tariff fallback table for stations where NVDB tariff attributes are missing or stale.**

- Read object type **45** (Bomstasjon), with `inkluder=alle&srid=4326`.
- Identify with `X-Client: wastr` header. No auth required; no licence fee.
- Geometry and station identity treated as authoritative.
- Tariffs (`Takst liten bil`, `Takst stor bil`, `Rushtidstillegg ...`, `Miljøtakst ...`) treated as best-effort; gaps filled by a CSV-based fallback table committed to `Wastr.Services.Fleet` and reviewed quarterly.
- Imported by a weekly TimerTrigger Azure Function inside FleetService; upserts by `ExternalId = "nvdb:45:{id}"`.

## Alternatives Considered

1. **Fjellinjen / Skyttel commercial API** — rejected for now. Costs procurement time we don't have in *Now*, and the marginal accuracy benefit (real-time tariff freshness, per-pass billing) is not needed for route *planning* — only for *invoice reconciliation*, which is out of scope. NVDB + fallback gets the planner to "within 5% on Oslo reference routes" which is the only target that matters at this stage. Commercial API remains an exit ramp once volume justifies the licence — the `TollZone`/`TollTariff` shape is identical, only the import job swaps.
2. **Public PDFs + manual zone polygons** — rejected. Doesn't scale beyond a single test fixture. Brittle. No value over NVDB.
3. **Use Azure Maps or Google Routes API toll-cost endpoints directly** — not investigated in depth; neither has authoritative NO bomstasjon data at vehicle-class granularity that we trust, and we'd still need the same geometry/tariff fallback shape.

## Consequences

**Positive**
- Zero cost, zero procurement.
- Geometry layer is high-quality and refreshed weekly.
- Same `TollZone`/`TollTariff` shape works with commercial source later — pure import-job swap.
- Open data sits well with WASTR's neutral-platform positioning.

**Negative**
- Tariff staleness: NVDB lags operator-announced tariff changes by weeks to months.
- Tariff coverage gaps: requires a hand-curated fallback table that must be maintained.
- Free-text time-of-day rules in NVDB are not always machine-readable; rush-hour windows encoded per-operator as constants in code.
- Public service, no SLA. Import job must be tolerant of NVDB outages (last-good cache retained).

## Mitigations

- `TollZone.last_verified_at` field; quarterly manual spot-check against operator websites.
- Alerting in App Insights when a delta import flips >2% of tariffs in one run (catches both real changes and accidental NVDB regressions).
- Fallback CSV in `Wastr.Services.Fleet` keyed by `ExternalId`, takes precedence over NVDB tariffs where present.
- Import job is idempotent and side-effect-free on NVDB outage (skip + log, do not delete existing rows).
- Buffer NVDB point geometries by ~30 m before polyline intersection (handles map-snapping mismatches between Azure Maps routes and NVDB station points).

## Revisit Trigger

- Toll-cost reporting (post-job actuals vs. plan) shows >5% systematic error on more than one operator → upgrade to commercial source.
- A second NO operator joins the market with significant cordon coverage and is not in NVDB → commercial.
- WASTR expands outside NO → re-evaluate per country (NVDB is Norway-only).
- Fallback CSV grows beyond ~50 entries → maintenance burden warrants commercial subscription.

## Linked

- [SPEC #46](https://github.com/wastr-as/wastr-learning-loop/issues/46) — Toll-aware routing (this ADR closes Phase 0)
- [SPEC #45](https://github.com/wastr-as/wastr-learning-loop/issues/45) — FleetService (Phase 4 owns the data plane; import job lives there)
- [Sketch: NvdbTollClient](sketches/nvdb-toll-client.md) — reference implementation for the import job
- [ADR-0011](0011-fleet-service.md) — FleetService home for toll reference data
