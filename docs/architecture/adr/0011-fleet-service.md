# ADR-0011: New FleetService with its own datastore

- **Status:** Accepted (supersedes ADR-0011 v1 draft from same date)
- **Date:** 2026-06-03
- **Deciders:** Siarhei (CTO)

> **Correction note:** An earlier draft of this ADR proposed putting the Fleet bounded context inside Collector Service. That was a factual error — Collector Service is a pure BFF with no datastore. The three real options were: (A) add a datastore to Collector Service, (B) co-locate fleet in User Service alongside Company, (C) create a dedicated FleetService. This document records the corrected decision: **C**.

## Context

The smart route planner bet ([#44](https://github.com/wastr-as/wastr-learning-loop/issues/44)) and SPEC [#45](https://github.com/wastr-as/wastr-learning-loop/issues/45) introduce a fleet model: vehicle types (catalog), vehicle instances (company-owned), and driver-vehicle assignments over time. These entities need persistent storage and CRUD APIs.

Wastr's existing services split cleanly into two shapes:

- **Domain services with their own datastore:** User (SQL/EF Core), Product (SQL/EF Core), Ordering (Cosmos DB), Matching, Geolocation.
- **BFFs with no datastore:** Collector, Driver.

Fleet is unambiguously a domain — it has its own entities, lifecycle, and invariants (e.g. "an active assignment cannot overlap another active assignment on the same vehicle"). It is not a view-shape over other services' data.

## Decision

**Create `Wastr.Services.Fleet` as a new domain service with its own SQL Server datastore (EF Core, same pattern as User and Product services).**

- Owns three entities: `VehicleType` (catalog), `Vehicle` (instance), `VehicleAssignment` (driver-vehicle binding with validity period).
- Cross-service references (`CompanyId`, `UserId` for driver) are stored as plain GUIDs — no DB-level FK across service boundaries; integrity enforced via service-call validation at write time.
- Collector BFF proxies VehicleType + Vehicle + VehicleAssignment writes/reads for the Collector app and Admin app.
- Driver BFF proxies a read-only "my current assignment" call for the Driver app.
- Same stack as User Service: .NET 9, ASP.NET Core, EF Core 9, SQL Server, port 8080, Docker multi-stage build, deployed via the existing ACR + Terraform pipeline.

## Alternatives Considered

1. **(A) Add a datastore to Collector Service** — rejected: breaks the BFF-only invariant of Collector Service, mixes aggregation logic with domain ownership, makes Collector Service's responsibilities unclear, and creates the worst of both worlds (a BFF that's also a system of record). If we accept a new DB anyway, the cost of a new service on top is small and the boundary is much cleaner.
2. **(B) Co-locate fleet in User Service** — rejected: User Service is identity + organisations. Fleet is operational asset management. The relational convenience (Company and User FKs are co-located) does not justify diluting the service's purpose; we'd be one feature away from also putting trucks-on-shift or driver-certifications there, and User Service becomes a junk drawer. Cross-service GUID references (option C) cost very little.
3. **(C) New FleetService with own datastore** — **chosen.** Honest boundary, clean ownership, room to grow (telemetry, leasing pools, vehicle-marketplace) without re-extraction. Pays the new-service tax now, in exchange for never paying the extraction tax later.
4. **Store in Ordering Service Cosmos** — rejected: wrong shape (no per-collector partition fit), wrong write profile, wrong lifecycle.

## Consequences

**Positive**
- Clean domain boundary; FleetService can evolve independently (telemetry, leasing, third-party integrations).
- Collector Service stays a pure BFF.
- Same well-trodden stack as User/Product Service — no new technology, no new team learning.
- Future Driver app, Customer app (vehicle-visibility-on-pickup), or external integrations consume one well-defined Fleet API instead of reaching into another service.
- The "vehicle as company asset" model maps naturally to a per-tenant Fleet store, simplifying multi-tenant scaling later.

**Negative**
- New service to deploy, monitor, secure, version, and migrate. Concrete ops cost: new ACR image, new App Service, new SQL DB, new Terraform module, new GitHub Actions pipeline, new MSAL app registration for service-to-service auth.
- Cross-service referential integrity (`CompanyId`, `UserId`) lives in code, not the database. Mitigation: validate against User Service on write, accept eventual cleanup if a User/Company is deleted.
- Slightly slower Collector + Driver app reads (one extra hop). Acceptable — already the BFF norm.

## Revisit Trigger

- If after 12 months the FleetService has fewer than 3 endpoints actively used in production, consider folding it back (probably into User Service).
- If vehicle telemetry / live GPS becomes the dominant write profile, evaluate splitting telemetry out as its own service (high-frequency time-series store) and leaving FleetService for slow-changing fleet metadata.

## Linked

- [SPEC #45](https://github.com/wastr-as/wastr-learning-loop/issues/45) — Fleet domain (VehicleType + Vehicle + VehicleAssignment)
- [BET #44](https://github.com/wastr-as/wastr-learning-loop/issues/44) — Smart route planner
- ADR-0006 — BFF pattern (Collector + Driver BFFs proxy FleetService)
- ADR-0009 — Route owns order sequence (unchanged)
