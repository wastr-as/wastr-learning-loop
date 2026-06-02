# ADR-0014: CO₂ accounting — TTW for routing, HBEFA-derived seed, WTW reserved for ESG reporting

- **Status:** Accepted
- **Date:** 2026-06-03
- **Deciders:** Siarhei (CTO)

## Context

SPEC [#47](https://github.com/wastr-as/wastr-learning-loop/issues/47) Phase 3 introduces CO₂ as a cost overlay in the OR-Tools routing engine (`α·duration + β·tollNok + γ·co2 + δ·emptyKmPenalty`). To compute it, the platform needs a per-arc CO₂ number, which requires deciding:

1. **What scope of emissions to count** — Tank-to-Wheel (combustion only), Well-to-Wheel (incl. fuel production), or full Life-Cycle (incl. vehicle manufacturing).
2. **Where the per-vehicle emission factor lives.**
3. **What precision is required** — load-weighted? speed/gradient-aware? real-world calibrated?
4. **Whether the same number serves ESG reporting** (NS 9431, CSRD) or whether reporting needs its own model.

These are not the same question. Routing only cares about relative comparison (route A vs route B); reporting cares about absolute auditability against an external standard.

## Decision

### 1. Scope: **Tank-to-Wheel (TTW) for routing**

- The routing cost callback consumes TTW g CO₂/km — combustion emissions only.
- Rationale: TTW is the number that varies meaningfully between *route choices for a given vehicle*. WTW adds a fuel-production constant that doesn't change route ranking.
- Electric vehicles report TTW = 0 in routing. The optimiser will favour them; this is intentional and aligned with WASTR's environmental positioning.

### 2. Storage: **`co2GramsPerKm` on `VehicleType` (mandatory) + `Vehicle` (nullable override)**

- Defined in FleetService (SPEC [#45](https://github.com/wastr-as/wastr-learning-loop/issues/45) Phase 1/2), same fallback pattern as `tollVehicleClass`.
- Each `VehicleType` row carries a `co2SourceCitation` string identifying the source (e.g. `"HBEFA 4.2, urban delivery, diesel HGV >12t"`) so values are auditable and updatable.

### 3. Precision: **single g/km per vehicle type, no load/speed/gradient weighting in Phase 1**

- Load weighting (full vs empty), speed-band tables, and gradient correction are **deferred**. They add significant implementation cost for second-order effects that don't change route ranking at pilot scale.
- Real-world vs HBEFA published values: real-world is typically 15–30% higher. This systematic offset doesn't affect *relative* comparison — skipped for routing. Revisit when ESG reporting matures.

### 4. Source: **HBEFA 4.x summary tables + Miljødirektoratet for NO electricity mix**

- HBEFA (Handbook Emission Factors for Road Transport) is the European gold standard — used by EEA, Statens vegvesen, EU regulators. Full dataset is paid-licensed; summary tables are freely and widely cited and sufficient for our seed values.
- Miljødirektoratet publishes the current Norwegian electricity grid carbon intensity (~11 g CO₂/kWh; ~95% hydro). Used only when computing WTW for EVs in future reporting.
- Cross-reference against EEA EMEP/EEA Guidebook (open) and DEFRA UK conversion factors (open, annual) at seed time.

### 5. ESG reporting: **separate concern, future SPEC**

- NS 9431, CSRD, and builder-facing emissions reports need WTW, source provenance, and audit trail.
- They will consume the same per-arc data captured on completed routes, but transform it (TTW → WTW, add fuel-production factor per fuel type, attach citation).
- Out of scope for this ADR and for [#47](https://github.com/wastr-as/wastr-learning-loop/issues/47).

## Alternatives Considered

1. **WTW for routing** — rejected: adds a fuel-production constant that doesn't change route ranking. Cleaner to keep routing on TTW and apply WTW conversion at reporting time when the user-visible question is "what was emitted" not "which route emits less".
2. **Load-weighted emissions** (`g/km` interpolated between empty and full mass) — rejected for Phase 1: implementation cost is real (requires per-arc load tracking, interpolation in cost callback, more validation), benefit on route ranking is small at pilot scale, complexity bleeds into testing. Revisit when ESG reporting demands per-job accuracy.
3. **Speed-band HBEFA tables** — rejected: HBEFA varies g/km by speed band (urban / rural / motorway). Real benefit, real cost. Defer until measurement shows routing decisions are being made wrong because of this gap.
4. **Live emissions sensors / telemetry** — rejected: no fleet data, no sensors, no integration. Aligned with FleetService telemetry being explicitly deferred per [ADR-0011](0011-fleet-service.md) revisit triggers.
5. **Per-fuel-type table separate from vehicle type** — rejected: simpler to bake fuel type into the VehicleType row (one diesel hooklift, one biogas hooklift, etc.) since vehicles in our fleet model don't switch fuel mid-life.

## Consequences

**Positive**
- Cheap to implement: one integer field per `VehicleType`, optional override per `Vehicle`, one multiplication in the cost callback.
- Auditable from day one via `co2SourceCitation`.
- Honest about precision: documented as "good enough for relative route ranking" not "ESG-grade".
- Path to ESG reporting is clear — reuse the same captured data, transform at read time.

**Negative**
- Will look naive to anyone comparing against a sophisticated emissions model (academic, ESG consultancy). Document the choice and the upgrade path so it's clear this is a *deliberate* simplification.
- Electric vehicles get a 0 in routing optimisation, which is the right answer for *combustion* but can mislead naive consumers into thinking electric = no environmental cost. Mitigation: surface explanation in cost breakdown (Phase 3 of [#47](https://github.com/wastr-as/wastr-learning-loop/issues/47)).
- Seed values must be verified against HBEFA at FleetService seed time; if seeders don't, garbage-in/garbage-out.

## Revisit Triggers

- Builder-facing ESG reporting is filed as a SPEC → load-weighting, speed-bands, WTW conversion become real requirements; write ADR-0014-supplement at that point.
- A measurable case where routing chose a worse route because the CO₂ model was too coarse (e.g. ignoring that route A is mostly motorway and route B is urban stop-go, which HBEFA speed bands would have caught).
- Telemetry data becomes available (per [ADR-0011](0011-fleet-service.md) telemetry trigger) → upgrade to measured fuel consumption per arc.

## Linked

- [SPEC #45](https://github.com/wastr-as/wastr-learning-loop/issues/45) — FleetService (owns `co2GramsPerKm` on `VehicleType` + override on `Vehicle` + `co2SourceCitation`)
- [SPEC #47](https://github.com/wastr-as/wastr-learning-loop/issues/47) — Routing Service (consumer in Phase 3 cost callback)
- [ADR-0011](0011-fleet-service.md) — FleetService home
- [ADR-0013](0013-route-engine-or-tools.md) — Route engine architecture (cost callback structure)
- HBEFA 4.x — Handbook Emission Factors for Road Transport (European reference dataset)
- Miljødirektoratet — Norwegian electricity-mix carbon intensity (for future WTW conversion)
