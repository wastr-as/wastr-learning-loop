# ADR-0011: Vehicle + Fleet domain in Collector Service (no separate FleetService yet)

- **Status:** Accepted
- **Date:** 2026-06-03
- **Deciders:** Siarhei (CTO)

## Context

The smart route planner bet ([#44](https://github.com/wastr-as/wastr-learning-loop/issues/44)) requires a fleet model: vehicles, vehicle types (catalog), and driver-to-vehicle assignments over time. See [SPEC #45](https://github.com/wastr-as/wastr-learning-loop/issues/45) for the entity model.

Two reasonable homes exist:
1. **New FleetService** — clean domain boundary, future-proof for telemetry / leasing pools / multi-collector sharing.
2. **Fleet bounded context inside Collector Service** — co-located with the operational layer that already owns routes, marketplace, and company drivers list.

## Decision

**Build the Fleet bounded context inside Collector Service.** Do not create FleetService at this time.

Entities (`VehicleType`, `Vehicle`, `VehicleAssignment`) live in Collector Service's datastore. Admin app talks to Collector Service for VehicleType CRUD; Collector app does so for Vehicle + Assignment. Driver app reads via Driver BFF, which proxies Collector Service.

The internal package / namespace structure should treat Fleet as a distinct bounded context (separate folder, separate repository interfaces, separate DTOs) so that an extraction into FleetService later is mechanical rather than a rewrite.

## Alternatives Considered

1. **New FleetService now** — rejected for now: zero vehicles exist, the bet that justifies fleet ops is in *Later*, and a new service adds CI / deploy / monitoring / network overhead with no consumer beyond the same Collector app. Premature service extraction is one of the most expensive recoverable mistakes in microservices.
2. **Fleet inside User Service** — rejected: vehicles are operational fleet ops, not identity. User Service should stay narrow.
3. **Fleet inside Ordering Service** — rejected: vehicles are not order-shaped (no per-collector partition fit), and Ordering should stay focused on the order lifecycle.
4. **Inline vehicle fields on User entity** — rejected: collapses the catalog/instance/assignment distinction needed for fleets >5 vehicles and forces schema churn the moment a driver swaps vehicles.

## Consequences

**Positive**
- Zero new infrastructure (service, pipeline, monitoring, networking).
- Operational data lives next to the operational app that owns it.
- Mirrors the established Collector BFF pattern.
- Bounded-context separation inside Collector Service keeps the future extraction door open.

**Negative**
- Collector Service grows. If left unchecked it could become a "junk drawer" service.
- Cross-collector fleet sharing (leasing pool, marketplace-of-vehicles) would force extraction; until then it's free.
- VehicleType is platform-wide metadata living inside what is otherwise a per-collector service — slightly awkward conceptually. Mitigation: clear namespace + a single source-of-truth API the Admin app calls.

## Revisit Trigger

Extract to **FleetService** when any of these hit:

- ≥2 services beyond Collector need to read vehicle data and the BFF proxy pattern becomes painful (current count: 1, the Driver BFF).
- Multi-collector vehicle sharing (leasing pool, vehicle marketplace) is on the active roadmap, not in Later.
- Vehicle telemetry (live GPS, fuel, load sensors) is added and the write volume / lifecycle differs materially from the rest of Collector Service.
- Collector Service grows past ~3 bounded contexts and clarity suffers.
- A second product line (e.g. construction-material delivery) needs the same vehicle model — at that point, Fleet becomes a shared service.

## Linked

- [SPEC #45](https://github.com/wastr-as/wastr-learning-loop/issues/45) — Driver vehicle + fleet model
- [BET #44](https://github.com/wastr-as/wastr-learning-loop/issues/44) — Smart route planner
- ADR-0006 — BFF pattern for Collector and Driver apps (Driver BFF will proxy fleet reads)
- ADR-0009 — Route owns order sequence (unchanged)
