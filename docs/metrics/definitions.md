# Metric Definitions

> **Canonical definitions.** If a metric is referenced anywhere (north-star, weekly review, dashboards, bets), it must be defined here first.

## Core Operational Metrics

### Empty-run %

⭑ **North Star metric** ([north-star.md](../strategy/north-star.md)). **Down is winning.**

- **Definition:** `unladenKm ÷ totalKm`, aggregated across all completed routes on the
  platform in the trailing 30 days. A leg is **laden** if, at the moment the vehicle departs
  a stop, it carries at least one order that has been picked up and not yet delivered.
  Everything else — depot-to-first-pickup, disposal-site-back-to-depot, and any repositioning
  between jobs — is **unladen**.
- **Unit of aggregation:** platform-wide for the North Star. Also computed **per vehicle per
  week** for operational review and **per transporter company** for customer-facing reports.
  Never compare across companies publicly — vendor neutrality
  ([product-thesis](../strategy/product-thesis.md)) forbids ranking transporters.

**Data source — phased, matching [ADR-0017](../architecture/adr/0017-route-execution-telemetry-and-anti-fraud-heuristics.md):**

| Phase | `totalKm` source | Laden/unladen split source | Confidence |
|---|---|---|---|
| **1 (now)** | `Route.ActualKm` = `EndOdometerKm − StartOdometerKm`, driver-typed | **Modelled**: leg-level laden flag derived from the `Route.OrderIds` sequence + each order's pickup/delivery stage; leg distances from the Geolocation Service matrix. Ratio applied to `ActualKm`. | Low — odometer is self-reported; split is planned-geometry, not observed. |
| **2 (SPEC #48 Ph.2)** | GPS polyline length | Same leg model, but leg distances are **observed** polyline segments between actual stop timestamps | Medium — real geometry, still a modelled laden flag. |
| **3 (SPEC #45 OBD)** | Vehicle odometer / fleet-card feed | As Phase 2, optionally corrected by load-cell or weigh-slip evidence | High — auditable, ESG-grade. |

- **Phase 1 formula (be explicit, it is an approximation):**
  `emptyRun% = (Σ plannedUnladenKm ÷ Σ plannedTotalKm) × 100`, reported alongside
  `actualKm ÷ plannedKm` as a **deviation factor**. We publish the ratio from planned geometry
  and the total from actuals; we do **not** pretend the split itself is measured.
- **Exclusions:** routes with any `TelemetryWarnings` (ADR-0017 heuristics) are excluded from
  the aggregate and reported separately as `excludedRoutePct`. If `excludedRoutePct > 15%`,
  the period's figure is **not publishable** — data quality, not performance, is the story.
- **Owner:** CTO (Siarhei) — instrumentation and definition. Collector managers own data
  quality per company (they review flagged routes).
- **Refresh cadence:** computed nightly; reviewed weekly (Friday `[WEEKLY]`); published
  monthly (30-day trailing) at the monthly product review.
- **Known bias:** Phase 1 over-trusts the driver on `totalKm` and over-trusts the planner on
  the laden split. Both biases are documented on every report. Do not use Phase 1 numbers in
  audited ESG or grant deliverables — see [ADR-0015](../architecture/adr/0015-sustainability-reporting-strategy.md).

#### Baseline-capture plan (empty-run %)

**The constraint: a baseline can only be captured *before* the Routing Service
([#47](https://github.com/wastr-as/wastr-learning-loop/issues/47)) starts influencing route
choice.** Once the optimiser is live, the pre-optimisation counterfactual is gone forever and
the −25% claim becomes permanently unfalsifiable. This is a one-way door and it is currently
open.

| Step | What | Gate / exit criterion |
|---|---|---|
| 1 | Ship SPEC #48 Phase 1 telemetry (odometer in/out, `ActualKm`, warnings) | Deployed to prod, drivers trained |
| 2 | Ship the leg-level laden/unladen computation + nightly aggregate | Metric visible on an internal dashboard |
| 3 | **Baseline window** — ≥4 consecutive weeks, ≥3 transporter companies, ≥100 completed routes, routes planned **manually** (collector drag-and-drop, no optimiser) | All four thresholds met; `excludedRoutePct ≤ 15%` |
| 4 | Freeze the baseline: record value + window + N + method in this file and in the [decision log](../strategy/decision-log.md) | A `[DECISION]` issue records the frozen number |
| 5 | **Only then** enable the Routing Service in shadow mode (plan but don't apply), then live | Post-baseline |

- **Baseline value:** _not yet captured._
- **Baseline window:** _pending._
- **If the baseline cannot be captured** (too few pilot transporters before #47 ships),
  the honest fallback is a **shadow-mode A/B**: run the optimiser in parallel without applying
  its plan, and compare planned-optimised km vs. actually-driven manual km on the same routes.
  Weaker evidence, but still falsifiable. Record which method was used.
- **Risk if skipped:** the 25% / 160 t CO₂ figures stay projections indefinitely, and any
  Innovasjon Norge or investor claim built on them is unsupportable under scrutiny.

### Active transporters

- **Definition:** unique transporter companies with ≥1 completed order in the trailing 7 days
- **Data source:** Ordering Service — distinct `Order.CompanyId` where `Status = Completed`
- **Owner:** CEO (Denis)
- **Refresh cadence:** weekly, at the Friday review

### Active projects

- **Definition:** unique builder projects with ≥1 order created in the trailing 7 days
- **Data source:** _pending_ — requires the Project entity from [ADR-0016](../architecture/adr/0016-project-ownership-and-builder-app.md); until then, proxy on distinct `Order.Address` per builder company
- **Owner:** CEO (Denis)
- **Refresh cadence:** weekly, at the Friday review

### Documented mass (tonnes)

- **Definition:** sum of weight (kg) on completed orders with full chain-of-custody evidence, in the trailing 30 days
- **Data source:** Ordering Service — `OrderEvidence.WeightKg` where the order has evidence at **both** `Pickup` and `Delivery` stages
- **Owner:** CTO (Siarhei)
- **Refresh cadence:** monthly, at the product review

## ESG Metrics

> Both ESG metrics are **derived** from empty-run % and inherit its phase confidence.
> They are not independently measured. Per [ADR-0014](../architecture/adr/0014-co2-accounting.md),
> routing uses **Tank-to-Wheel**; external ESG reporting requires **Well-to-Wheel** and must
> apply the fuel-production factor at read time — do not publish the routing number as an ESG number.

### CO₂ avoided (tonnes)

- **Definition:** `(baselineUnladenKm − actualUnladenKm) × co2GramsPerKm`, per month,
  summed per vehicle and converted to tonnes. Requires a frozen empty-run % baseline.
- **Data source:** FleetService `VehicleType.co2GramsPerKm` (with `Vehicle` override), seeded
  from HBEFA 4.x and carrying `co2SourceCitation`; km from the empty-run % pipeline above.
- **Sanity band:** literature puts a diesel refuse truck at ≈2.25 kg CO₂-eq/km. Any computed
  factor outside 1.5–3.0 kg/km for a diesel HGV is a seeding error, not a finding.
- **Owner:** CTO (Siarhei)
- **Refresh cadence:** monthly; **not publishable** until the empty-run % baseline is frozen.

### NOx avoided (kg)

- **Definition:** as CO₂ avoided, with the NOx emission factor.
- **Data source:** _pending_ — `noxGramsPerKm` does not yet exist on `VehicleType`
  (ADR-0014 covers CO₂ only). Requires a FleetService schema addition before this metric is computable.
- **Owner:** CTO (Siarhei)
- **Refresh cadence:** monthly, once instrumented.

## Product / Engagement Metrics

### Order completion rate

- **Definition:** orders completed ÷ orders created, trailing 7 days
- **Data source:** Ordering Service — `Order.Status` counts by `CreatedAt` window
- **Owner:** CTO (Siarhei)
- **Refresh cadence:** weekly

### Time-to-accept (median)

- **Definition:** minutes between order created and order accepted by a collector
- **Data source:** Ordering Service — first `OrderActivity` with `Status = Accepted` minus `Order.CreatedAt`
- **Owner:** CEO (Denis) — this is a marketplace liquidity signal, not an engineering one
- **Refresh cadence:** weekly

### Driver app DAU / WAU

- **Definition:** unique drivers opening the app per day / week
- **Data source:** frontend telemetry per [ADR-0020](../architecture/adr/0020-frontend-telemetry-build-time-injection.md)
- **Owner:** CTO (Siarhei)
- **Refresh cadence:** weekly
