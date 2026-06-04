# ADR-0018: Route plan is immutable post-save — driver executes, doesn't re-optimise

- **Status:** Accepted
- **Date:** 2026-06-04
- **Deciders:** Siarhei (CTO)

## Context

[ADR-0009](0009-route-owns-order-sequence.md) puts the visit sequence on the
Route entity (`Route.OrderIds[]`).
[ADR-0013](0013-route-engine-or-tools.md) introduces `Wastr.Services.Routing`
(OR-Tools-based) and [SPEC #47](https://github.com/wastr-as/wastr-learning-loop/issues/47)
adds an "Auto-arrange" entry point in the Collector route builder.

Open question that ADR-0013 deliberately punted:

> Once the sequence is saved, **who is allowed to change it, when, and where
> does optimisation happen at runtime — if at all?**

Three plausible execution-time models:

A. **Driver app re-optimises locally** — solver runs on the phone each time
   the driver opens the route.
B. **Driver app re-optimises by calling Routing Service** — server solves on
   each route open / status change.
C. **Plan is immutable from the moment of save** — driver executes the saved
   `OrderIds[]` order verbatim, no re-optimisation runs at execution time.

This needs an explicit decision because the answer drives a lot of other
design: caching, audit, customer ETA stability, driver-side complexity,
Routing Service load profile, and what "plan vs. actual" means.

## Decision

**Adopt Model C: the saved route is the plan of record. The driver app
executes the saved sequence verbatim. No re-optimisation runs at execution
time as part of the normal flow.**

Concretely:

- `Wastr.Services.Routing` is **only invoked at plan time**, from the
  Collector's `RoutePlannerModal`.
- After the collector saves, `Route.OrderIds[]` is the contract.
- Driver app: `GET /api/driver/{driverId}/routes` returns orders sorted by
  the saved array sequence. The driver app calls Geolocation to render the
  path through those stops in that order; **it does not re-sequence, and it
  does not call Routing Service.**
- Editing a route post-save is governed by the existing Pending-only rule
  (collector edit/delete gated on `route.status === 'Pending'`).
- Any future driver-initiated re-optimisation is an **explicit, user-driven
  action** with audit (see "Phase 2 escape hatch" below). It is not an
  automatic background behaviour.

## Why

| Reason | Detail |
|---|---|
| **Single source of truth** | Collector, driver, customer notifications, and downstream telemetry all reference one sequence. Silent driver-side re-ordering would mean dispatch, customer ETA, and audit logs disagree on what was supposed to happen. |
| **Auditability** | "Plan vs. actual" is a stated R&D direction. [SPEC #48](https://github.com/wastr-as/wastr-learning-loop/issues/48) already captures actuals (start/end odometer, opt-in GPS trail, completion times). Comparison needs an immutable plan to compare against. |
| **Accountability** | Deviations should be visible. If the driver wants to deviate, that intent must be logged — not absorbed silently by a local re-solve. |
| **Performance** | OR-Tools on a phone is the wrong place for a CPU-bound solver. Solver lives server-side, called once per plan. |
| **Determinism** | When the collector clicks Save, they saw "stop 3 will be visited 4th". The driver app must honour that promise. |
| **Cost** | Each Routing Service call cascades into Azure Maps Matrix calls (paid). Solving on every driver route-open multiplies cost with no proportional product value. |
| **Failure mode containment** | A bug in the solver shouldn't be able to reorder a route a driver has already partially executed. |

## Alternatives Considered

### Model A — Driver app re-optimises locally
- Pros: zero server cost; offline-friendly.
- Cons: stack divergence (we'd run OR-Tools or a heuristic in the browser /
  PWA), audit invisibility, ETA drift, battery and CPU cost on field
  devices. **Hard reject.**

### Model B — Driver app re-optimises by calling Routing Service on each open
- Pros: server still owns the solver; driver always sees "the current best
  plan".
- Cons: hides reorderings from the collector and customer; multiplies
  Azure Maps cost with no user-facing trigger; makes "plan vs. actual"
  meaningless because the plan keeps moving. **Rejected** as default
  behaviour; allowed only as the **explicit** Phase 2 escape hatch
  (below).

### Model C — Plan immutable post-save (this ADR)
- Pros: see "Why" table above.
- Cons: doesn't react to events that happen between plan-time and
  execution-time (a cancelled stop, a late accept, traffic disruption).
  Mitigated by the Phase 2 escape hatch.

## Phase 2 escape hatch — explicit, audited, opt-in

Specifically **out of scope** for the [SPEC #47](https://github.com/wastr-as/wastr-learning-loop/issues/47)
Phase 1 PoC, but designed in advance so we don't paint ourselves into a
corner:

- Driver app exposes a **"Re-optimise remaining stops"** button. Available
  only when `route.status === 'InProgress'` and at least 2 unvisited stops
  remain.
- On press: driver app sends `{ remainingOrderIds, currentGpsLocation }` to
  Routing Service. Current GPS becomes the synthetic "depot".
- Routing Service returns a proposed new ordering of the trailing portion.
- Driver app shows a **diff preview**: *"Reorder remaining 4 stops to save
  ~12 min? [Apply] [Keep current]"*.
- On **Apply**: `updateRoute` is called with the new `OrderIds` and an
  audit record is written (driver id, timestamp, old vs. new sequence,
  predicted savings). The `updateRoute` endpoint is extended to permit
  editing the **trailing (unvisited) portion** of an `InProgress` route —
  visited stops stay frozen.
- The customer notification system fires updated ETAs for the moved stops
  only.
- Feature is behind a flag, opt-in per collector, and only available to
  Phase-2 pilot collectors initially.

The non-negotiable property of the escape hatch: **the reordering is a
recorded event, not a silent recomputation.** If we ever break that
property we've abandoned the principle of this ADR.

## Consequences

**Positive**
- Routing Service is a planning-time concern; runtime is unaffected.
- Driver app code requires zero changes for the Routing Service PoC
  ([SPEC #47](https://github.com/wastr-as/wastr-learning-loop/issues/47)
  Phases 0–3).
- Customer ETAs (when we add them) can be computed once at plan time and
  trusted until execution.
- Plan vs. actual analysis is meaningful from day one of telemetry capture
  ([SPEC #48](https://github.com/wastr-as/wastr-learning-loop/issues/48)).
- No solver code, dependency, or runtime cost on driver devices.

**Negative**
- A plan can become stale between save and execution start (e.g. a stop is
  cancelled, traffic changes materially). Phase 1 acceptance is that the
  driver / collector reacts manually (cancel route, rebuild). The Phase 2
  escape hatch addresses this without compromising the audit story.
- The collector is responsible for re-planning if marketplace state
  changes after save. This is fine at pilot scale; if it becomes painful
  we revisit (see revisit triggers).

## Revisit Triggers

1. Pilot collectors regularly cancel-and-rebuild routes more than once per
   route on average → bring the Phase 2 escape hatch forward.
2. We add real-time traffic or disruption events from a data source other
   than the driver's own GPS → consider an automated "suggest re-plan"
   nudge (still surfaced to the driver as an explicit choice, never
   silent).
3. Customer ETA accuracy in production diverges from solver estimates by
   more than 15% systematically → the issue is solver realism, not the
   immutability principle; do not relax this ADR, fix the solver inputs.
4. We move to multi-day / multi-shift planning → the unit of immutability
   may need to shift from "route" to "shift segment". Reopen this ADR
   then.

## Linked

- [ADR-0009](0009-route-owns-order-sequence.md) — Route owns the ordered `OrderIds` (where the plan lives)
- [ADR-0013](0013-route-engine-or-tools.md) — How the plan is computed (Azure Maps + OR-Tools)
- [ADR-0017](0017-route-execution-telemetry-and-anti-fraud-heuristics.md) — Capture of actuals (the other half of plan-vs-actual)
- [SPEC #47](https://github.com/wastr-as/wastr-learning-loop/issues/47) — Routing Service; Phase 2 escape hatch lives here as a future phase
- [SPEC #48](https://github.com/wastr-as/wastr-learning-loop/issues/48) — Route execution telemetry (actuals)
- [BET #44](https://github.com/wastr-as/wastr-learning-loop/issues/44) — Smart route planner (the consumer of immutable plans)
- [EXP #54](https://github.com/wastr-as/wastr-learning-loop/issues/54) — Auto-arrange A/B (tests the planning surface; orthogonal to but consistent with this ADR)
