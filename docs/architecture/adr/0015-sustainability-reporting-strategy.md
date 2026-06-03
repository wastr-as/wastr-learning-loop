# ADR-0015: Sustainability & reporting strategy — standards alignment, tiering, and what we will not claim

- **Status:** Accepted
- **Date:** 2026-06-03
- **Deciders:** Siarhei (CTO)

## Context

Once the routing stack ships ([BET #44](https://github.com/wastr-as/wastr-learning-loop/issues/44) consuming [#45](https://github.com/wastr-as/wastr-learning-loop/issues/45) / [#46](https://github.com/wastr-as/wastr-learning-loop/issues/46) / [#47](https://github.com/wastr-as/wastr-learning-loop/issues/47)), WASTR has the raw data needed to generate a wide range of reports — from per-route operational summaries up to per-company GHG inventories aligned with EU CSRD / ESRS E1. [ADR-0014](0014-co2-accounting.md) explicitly deferred ESG-grade emissions reporting to a future SPEC; this ADR locks in the **strategy** for that SPEC and the broader reporting roadmap, before any of it is built.

Three forces make this decision necessary now:

1. **The "25% empty-running reduction" headline is unauditable today.** Without a documented methodology and actuals capture, it's a marketing claim, not a measurable KPI. The data layer must be designed to make that claim defensible.
2. **Builders increasingly require Scope 3 transport emissions data from transporters** (CSRD push-down). The transporter who supplies credible numbers wins tenders. We control whether transporters can do this.
3. **Reporting standards are sharp-edged.** Claiming "NS 9431 compliant", "CSRD compliant", or "GHG Protocol certified" without going through actual conformance processes is reputational risk. The vocabulary has to be locked in before product copy is written.

A separate sustainability/methodology document (one PDF) is required regardless of which standards we align with — auditors and ESG officers ask "how did you compute this?" first. That document is a deliverable of [SPEC #51](https://github.com/wastr-as/wastr-learning-loop/issues/51) and a precondition for any tier-2+ report being released to customers.

## Decision

### 1. Report tiering — four tiers, three SPECs (filed this round) plus one future SPEC

| Tier | Scope | Filed as | Regulatory weight |
|---|---|---|---|
| **Tier 1 — Operational** | route summary, driver shift, empty-running KPI, fleet utilisation, toll breakdown | [SPEC #50](https://github.com/wastr-as/wastr-learning-loop/issues/50) | Low — internal/customer-facing operational reports, no standards-conformance claims |
| **Tier 2 — Builder/project-facing** | NS 9431 waste manifest, per-project CO₂ allocation, ESG fact sheet | [SPEC #51](https://github.com/wastr-as/wastr-learning-loop/issues/51) phases 2/3/5 | Medium — aligned with NS 9431 + ISO 14083; we supply data, builder owns their reporting |
| **Tier 3 — Transporter/company-facing** | annual GHG inventory (Scope 1), ISO 14083 per-shipment emissions, CSRD ESRS E1 data export | [SPEC #51](https://github.com/wastr-as/wastr-learning-loop/issues/51) phase 4 | High — defensible data; transporter owns their CSRD/GHG-Protocol filing |
| **Tier 4 — Public / marketing** | platform-wide impact dashboard, annual sustainability report, per-customer statement | **Deferred to future SPEC** | Variable — "avoided emissions" claims require a counterfactual methodology that does not yet exist; explicitly out of scope of [SPEC #51](https://github.com/wastr-as/wastr-learning-loop/issues/51) |

### 2. Standards alignment — three external standards adopted

- **NS 9431** (Norwegian Standard for construction waste classification and reporting) — adopted for waste manifest field structure and fraction codes. Per-project manifest will be a **"NS 9431-compatible export"**, not a "certified" report. Compliance certification is a separate, future business decision.
- **ISO 14083** (Greenhouse gas emissions of transport chain operations) — adopted for emissions allocation methodology (how route-level CO₂ splits across multiple orders/shipments). This is the *non-ambiguous* allocation rule; locking it in early prevents downstream rework when builders ask "how did you allocate this?".
- **HBEFA 4.x + EEA EMEP/EEA Guidebook + Miljødirektoratet** — already adopted per [ADR-0014](0014-co2-accounting.md). Sources of emission factors and conversion constants.

### 3. Allocation methodology — ISO 14083 (weight × distance basis) from day one

- All per-project / per-order emissions allocation follows ISO 14083 §6 rules: emissions for a multi-stop route are allocated to shipments in proportion to *weight × distance* (or stop-share when weight is unknown).
- Implemented as a pure function in [SPEC #51](https://github.com/wastr-as/wastr-learning-loop/issues/51) phase 3 with unit tests against worked examples from the standard.
- **Decision rationale:** ISO 14083 is the *only* widely-recognised standard that prescribes allocation unambiguously. Picking it now removes a recurring "how did you allocate" debate with every customer. Worse-but-simpler alternatives (per-stop equal share, per-order equal share) are *not* defensible in audit contexts.

### 4. Provenance and reproducibility — every report stamps its inputs

- Every report records: data source dates, emission-factor config version, methodology document version, computation date.
- Conversion factors and grid-intensity numbers live in versioned JSON config files (`conversion-factors-{year}.json`), not in a database; versioned in the same repo as the methodology PDF.
- Per-route enriched CO₂ snapshot persisted on `RouteExecution` completion (TTW + WTW + factor config version + computedAt) — reports recompute from the snapshot, not from drifting current values.

### 5. What we explicitly will NOT claim

- **"CSRD-compliant report"** — we supply data suitable for the customer's CSRD reporting; the customer's auditor signs off, not us.
- **"GHG Protocol Corporate Standard certified"** — same reasoning.
- **"NS 9431 certified"** — we export NS 9431-compatible data; conformance assessment is a separate process.
- **"Real-time emissions tracking"** — we report computed emissions per completed route; not telemetry-grade.
- **Avoided-emissions / counterfactual claims without a methodology** — the platform-wide "tonnes CO₂ saved" headline is real, but it depends on a baseline (what would have been emitted without optimisation). That baseline methodology is its own research project (overlap with R&D portfolio Projects #1, #5). Deferred until at least pilot data exists and a methodology PDF is drafted.

### 6. Sequencing — four SPECs in dependency order

The reports SPEC ([#51](https://github.com/wastr-as/wastr-learning-loop/issues/51)) depends on two foundational SPECs being shipped first:

```
[#48] Route execution telemetry (actuals)  ─┐
                                            ├──→  [#50] Operational reports  ──→  [#51] ESG reporting foundations
[#49] Project entity (grouping)            ─┘                                          (Tier 2 + Tier 3)
```

- **[SPEC #48](https://github.com/wastr-as/wastr-learning-loop/issues/48) — Route execution telemetry.** Captures actual km / duration / per-stop timestamps and (opt-in) GPS trail. Without it every report uses planner estimates, which is not defensible.
- **[SPEC #49](https://github.com/wastr-as/wastr-learning-loop/issues/49) — Project entity.** Introduces `Project` in Ordering Service with `Order.projectId` linkage. Without it, no per-project anything.
- **[SPEC #50](https://github.com/wastr-as/wastr-learning-loop/issues/50) — Tier 1 operational reports.** Aggregation + presentation only, no new domain modelling. Headline value for collector managers and finance.
- **[SPEC #51](https://github.com/wastr-as/wastr-learning-loop/issues/51) — ESG reporting foundations.** Tier 2 + Tier 3 reports with documented methodology, ISO 14083 allocation, NS 9431 manifest, per-company GHG inventory.

## Alternatives Considered

1. **Skip ISO 14083, pick a simpler allocation method (equal-per-stop, equal-per-order).** Rejected: cheap to implement but indefensible in any builder/auditor conversation. Switching later would require recomputing every historical report. Cost of adopting ISO 14083 from day one is modest (a pure function + unit tests).
2. **Claim CSRD / GHG Protocol / NS 9431 conformance now** to strengthen marketing. Rejected: certification is a real process with real cost; falsely claiming it is reputational risk that scales with company growth. "Compatible export" / "data suitable for" is honest and equally useful to customers.
3. **Build platform-wide "avoided emissions" headline number first (Tier 4) — it's the most marketing-effective.** Rejected: requires a counterfactual baseline methodology that does not exist, and a single audit query ("what would have happened without you?") collapses an undefended number into a credibility hit. Defer until methodology is researched.
4. **Build reporting in each consuming service (per-project export in Ordering, GHG inventory in Fleet, etc).** Rejected: report logic centralisation matters because all reports share the same methodology, factor config, citation handling, and PDF rendering. Co-locating in a Reporting module (Functions, initially co-located with Notification Service) keeps the methodology surface area in one place.
5. **Persist computed WTW values on every route at execution time.** Rejected for the live row, accepted as a snapshot: WTW factors change yearly; persisting the live value freezes year-2026 numbers into year-2030 reports. Per-route TTW snapshot + report-time WTW conversion is correct. (TTW is stable per vehicle; WTW is a yearly factor.)
6. **Defer reporting strategy until the first SPEC is being built.** Rejected: standards alignment (ISO 14083, NS 9431) and provenance design (snapshot on `RouteExecution`) materially shape Route Execution Telemetry ([#48](https://github.com/wastr-as/wastr-learning-loop/issues/48)) and Project entity ([#49](https://github.com/wastr-as/wastr-learning-loop/issues/49)) — both filed this round. Wrong storage choices now = migration later.

## Consequences

**Positive**
- Clear, ordered SPEC dependency chain — no ambiguity about what to build first.
- Standards alignment locked in before code, removing rework risk on allocation method.
- Marketing/sales vocabulary disciplined — no claims the product cannot back up.
- One methodology document lives in repo, versioned, referenced from every report — auditable surface area is one PDF.
- Reusable provenance pattern: snapshot at compute time, recompute from snapshot at report time, every report stamps its inputs.

**Negative**
- ISO 14083 + NS 9431 require careful reading and field-mapping work in [#51](https://github.com/wastr-as/wastr-learning-loop/issues/51). Cheap to defer the *reading* — expensive to skip it.
- "We do not claim CSRD compliance" may feel weaker in sales pitches than competitors who do claim it. Counter: when their compliance is challenged, ours is honest. Pick customers who care about defensibility (which is exactly the ESG-mature customers we want).
- Avoided-emissions Tier 4 reports — the marketing headline — are deferred. Marketing copy needs to use Tier 1 empty-running % until then.
- Methodology PDF requires external review (sustainability consultant or research partner — TØI, SINTEF) — small cost, real calendar time.

## Revisit Triggers

- First pilot customer asks for a specific report this ADR did not anticipate → write supplement, do not silently expand scope.
- Avoided-emissions methodology is researched and published (likely via R&D Projects #1 / #5) → file Tier 4 SPEC + ADR supplement.
- A standard we align with (NS 9431, ISO 14083) ships a major revision → revisit field mappings and allocation rules.
- Reception-site data integration materialises → recycling-rate column moves from "not available" to real on Tier 2/3 reports.
- Reporting module grows past ~3 distinct reports and a dashboard → promote from Functions-in-Notification to its own service (`Wastr.Services.Reporting`).

## Linked

- [ADR-0011](0011-fleet-service.md) — FleetService (vehicle data plane, source of `co2GramsPerKm` + `co2SourceCitation`)
- [ADR-0012](0012-toll-data-nvdb.md) — NVDB toll data (per-passage records consumed by [#50](https://github.com/wastr-as/wastr-learning-loop/issues/50) toll breakdown report)
- [ADR-0013](0013-route-engine-or-tools.md) — Route engine (produces `plannedCo2g` per route)
- [ADR-0014](0014-co2-accounting.md) — CO₂ accounting (this ADR implements its deferred "future ESG reporting SPEC")
- [BET #44](https://github.com/wastr-as/wastr-learning-loop/issues/44) — Smart route planner (produces planner output consumed by reports)
- [SPEC #45](https://github.com/wastr-as/wastr-learning-loop/issues/45) — FleetService (vehicle/CO₂/toll data)
- [SPEC #46](https://github.com/wastr-as/wastr-learning-loop/issues/46) — Toll-aware routing (toll passage data plane)
- [SPEC #47](https://github.com/wastr-as/wastr-learning-loop/issues/47) — Routing Service (planned KPIs)
- [SPEC #48](https://github.com/wastr-as/wastr-learning-loop/issues/48) — Route execution telemetry (actuals capture — foundation for credible reporting)
- [SPEC #49](https://github.com/wastr-as/wastr-learning-loop/issues/49) — Project entity (per-project grouping)
- [SPEC #50](https://github.com/wastr-as/wastr-learning-loop/issues/50) — Operational reports (Tier 1)
- [SPEC #51](https://github.com/wastr-as/wastr-learning-loop/issues/51) — ESG reporting foundations (Tier 2 + Tier 3)
- **External:** ISO 14083 (transport chain GHG accounting), NS 9431 (Norwegian construction waste classification/reporting), HBEFA 4.x, EEA EMEP/EEA Guidebook, Miljødirektoratet, EU CSRD / ESRS E1
