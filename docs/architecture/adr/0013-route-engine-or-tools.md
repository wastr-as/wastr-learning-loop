# ADR-0013: Route engine — Azure Maps for routing primitive, OR-Tools for optimisation, separate Routing Service

- **Status:** Accepted
- **Date:** 2026-06-03
- **Deciders:** Siarhei (CTO)

## Context

The smart route planner bet ([#44](https://github.com/wastr-as/wastr-learning-loop/issues/44)) and R&D project #10 (integrated bidirectional optimisation) need a route engine that solves three distinct problems:

1. **Routing primitive** — point A → point B on the actual road network, truck-aware, with realistic duration estimates.
2. **Optimisation** — assign N orders across M vehicles, respecting capacity, time windows, pickup-before-delivery, two-way logistics; minimise a cost function (duration + toll + CO₂ + empty-km penalty).
3. **Cost overlays** — toll (already covered by [#46](https://github.com/wastr-as/wastr-learning-loop/issues/46) + ADR-0012), CO₂, time-of-day traffic.

Conflating layers 1 and 2 into a single tool is the most common mistake in this space. They have different cost/build/lock-in profiles and should be picked independently.

Today the platform has neither — Geolocation Service does pure Azure Maps distance/duration for ad-hoc lookups, but there is no matrix endpoint and no optimisation layer.

## Decision

### Layer 1 — Routing primitive: **Azure Maps Route + Matrix Routing API (`travelMode=truck`)**, owned by `Wastr.Services.Geolocation`.

- Already in the stack; Geolocation Service already authenticates against Azure Maps.
- Truck profile supports weight, height, axle count, hazmat — sufficient for CDW haulage in NO.
- Add `POST /api/geolocation/matrix` returning a duration + distance matrix for N waypoints.
- Cost is trivial at pilot volume (well under $50/mo for 5 transporters at <100 orders/day).

### Layer 2 — Optimisation: **Google OR-Tools (C# bindings, Apache 2.0)** inside a new service **`Wastr.Services.Routing`**.

- Stateless service: input/output only, no datastore.
- API: `POST /api/routing/optimise` takes `{ orders[], vehicles[], depots[], constraints, costWeights }` → `{ routes[], unassigned[], costBreakdown }`.
- Cost callback: `α·duration + β·tollNok + γ·co2 + δ·emptyKmPenalty`, weights configurable per request.
- Calls Geolocation Service for distance/duration matrices and toll cost; assembles cost matrix; runs OR-Tools VRP-with-PDP solver; returns sequences with explanation.

### Layer 3 — Cost overlays

- Toll: already designed in [#46](https://github.com/wastr-as/wastr-learning-loop/issues/46), consumed by Routing Service as a callback input.
- CO₂: simple `g_per_km × distance` per vehicle class, sourced from `VehicleType` metadata in FleetService.
- Future overlays (congestion, real-time traffic delta) plug into the same cost callback.

## Alternatives Considered

### Layer 1 alternatives

1. **OSRM (self-hosted, C++)** — fastest A→B in OSS, but no truck profile out of the box (community fork only). Memory-light. Rejected for now: setup + ops cost > Azure Maps savings at pilot scale.
2. **GraphHopper (self-hosted, Java)** — best OSS truck profile (weight, height, hazmat, time-aware). **The natural Phase 2 fallback if Azure Maps costs cross a threshold or NO-specific accuracy issues emerge.** Rejected now: adds JVM to ops for no immediate payoff.
3. **Valhalla (self-hosted, C++)** — best time-of-day costing and multi-modal. Most complex to operate. Rejected: overkill for CDW haulage.
4. **Itinero (.NET)** — native .NET fit, what one of our team has used before at Statens vegvesen. Sweet spot is custom-graph custom-rules (e.g. NVDB-derived edges with NO-specific restrictions). Rejected now: today's urban CDW use case doesn't need NVDB-level routing accuracy. Kept on the radar as a Phase 3 option if NO-specific routing edges become material to competitive differentiation.
5. **NVDB as routing graph** — would require building a routing engine on top (Itinero/custom). Months of work for marginal pilot benefit. Rejected. NVDB stays scoped to toll-data via ADR-0012.

### Layer 2 alternatives

1. **OptaPlanner (Java)** — equivalent capability to OR-Tools, adds JVM. Rejected: stack mismatch.
2. **Hand-rolled heuristic (greedy nearest-neighbour + 2-opt)** — workable for <20 stops/route, throws away decades of OR research, no growth runway. Rejected: false economy.
3. **Commercial VRP APIs (Routific, OptimoRoute, NextBillion, Onfleet)** — fastest pilot, zero IP, complete vendor lock-in. **Hands away the competitive moat (R&D project #10).** Hard reject for strategic reasons even if technically attractive.

### Service placement alternatives

1. **Put OR-Tools inside Ordering Service** — couples optimisation lifecycle to order lifecycle, mixes domains. Rejected.
2. **Put OR-Tools inside Geolocation Service** — Geolocation becomes a junk drawer (routing primitive + toll + optimisation). Rejected.
3. **Separate `Wastr.Services.Routing`** — chosen. Clean boundary, stateless, scales independently, owns the IP that justifies a separate service.

## Consequences

**Positive**
- Each layer picked on its own merits; can swap independently.
- IP (cost function, constraint modelling, bidirectional logic) lives in WASTR-owned code, not a black-box vendor.
- Same .NET 9 stack as other services — no new technology.
- OR-Tools at pilot scale solves in milliseconds; room to grow 100× before performance is a concern.
- Natural progression path to R&D project #10 (replace standard solver with custom bidirectional + dynamic-pricing + ML-demand-forecasting algorithm) — same service, swap the strategy.

**Negative**
- Two-layer call shape: Routing Service → Geolocation Service (matrix + toll) → Azure Maps. Adds latency on cold paths. Mitigated by caching distance matrices for short windows.
- Another new microservice (after FleetService) — same ops cost shape: ACR image, App Service, Terraform module, GHA pipeline, MSAL registration. No DB needed (stateless), which keeps the cost lower than FleetService.
- OR-Tools cost callbacks must be integer-typed; we scale and round. Standard practice but a footgun if forgotten.
- Azure Maps lock-in for Layer 1 — explicit, time-boxed, with a named exit ramp (GraphHopper).

## Revisit Triggers

**Layer 1 (swap Azure Maps → self-hosted GraphHopper):**
- Azure Maps spend exceeds $500/mo on routing calls.
- Measured route-duration error vs. operator-reported actuals exceeds 10% systematically (something Azure Maps doesn't know that we do).
- A specific NO routing nuance (seasonal weight restrictions, low-bridge edges from NVDB) starts costing real money in misrouted jobs.

**Layer 2 (replace OR-Tools standard solver with custom from R&D project #10):**
- R&D partnership with NTNU/SINTEF delivers a validated bidirectional algorithm.
- OR-Tools solve time exceeds 5s for typical daily problems (>500 stops).
- Standard VRP cost function stops capturing real economics (e.g. dynamic pricing needs joint optimisation that OR-Tools' callback shape struggles with).

**Service placement (fold Routing into another service):**
- After 12 months, Routing Service has <3 production endpoints actively used.

## Linked

- [BET #44](https://github.com/wastr-as/wastr-learning-loop/issues/44) — Smart route planner (consumer of this engine)
- SPEC for `Wastr.Services.Routing` (filed alongside this ADR)
- [SPEC #45](https://github.com/wastr-as/wastr-learning-loop/issues/45) — FleetService (provides `VehicleType.tollVehicleClass` + CO₂ metadata)
- [SPEC #46](https://github.com/wastr-as/wastr-learning-loop/issues/46) — Toll-aware routing (cost-callback input)
- [ADR-0012](0012-nvdb-toll-data-source.md) — NVDB for toll data
- R&D project #5 (Two-Way Routing Engine PoC) and #10 (Integrated Optimisation) — the natural evolution targets for Layer 2
