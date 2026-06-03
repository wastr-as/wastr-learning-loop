# ADR-0017: Route execution telemetry — driver-reported odometer with non-blocking anti-fraud heuristics

- **Status:** Accepted
- **Date:** 2026-06-03
- **Deciders:** Siarhei (CTO)
- **Related:** [SPEC #48](https://github.com/wastr-as/wastr-learning-loop/issues/48), [SPEC #47 (route engine)](https://github.com/wastr-as/wastr-learning-loop/issues/47), [SPEC #45 (Fleet)](https://github.com/wastr-as/wastr-learning-loop/issues/45), [ADR-0008 (immutable audit)](0008-immutable-audit-trail-user-ids.md)

## Context

SPEC #48 Phase 1 needed a way to capture **actual distance driven** per
route so the platform can:

- Compare planned (from SPEC #47 OR-Tools engine) vs actual km and produce
  the deviation% needed for ESG reporting and pricing reconciliation.
- Feed real-world ground-truth back into the routing engine.
- Quantify the empty-running reduction claim (25%, ~180 t CO₂/yr in Oslo).

We picked the cheapest possible Phase 1 source: **the driver types the
odometer reading into the app when starting and completing a route**, with
an optional GPS coordinate captured silently in the background. The result
is stored on the `Route` entity (`StartOdometerKm`, `EndOdometerKm`,
`StartLocation`, `EndLocation`) and derived `ActualKm` /
`ActualDurationMin` are exposed read-only.

The objection is obvious: **a driver can type any number**. Over-reporting
distance inflates invoiced kilometres and pollutes the routing engine's
training data; under-reporting hides empty-running that should reduce the
driver's score. We need a defence proportional to the Phase 1 scope —
neither blocking the route nor pretending the field is trustworthy.

## Decision

1. **Treat driver-typed odometer as a Phase-1 placeholder, not ground truth.**
   It is one signal among several that will arrive in later phases (GPS
   trail in Phase 2, vehicle telematics via SPEC #45 OBD integration). The
   data model is already shaped so we can swap the source without breaking
   consumers (`ActualKm` is a derived property; the source field can change
   from `EndOdometerKm − StartOdometerKm` to a GPS-polyline computation).

2. **Run a set of cheap server-side sanity heuristics on every route
   completion** and surface the results as a `TelemetryWarnings: string[]`
   field on the Route. The heuristics are deliberately conservative — they
   only flag readings that are *physically* implausible, not merely
   suspicious-looking:

   | Code | Trigger |
   |---|---|
   | `ODOMETER_IMPLAUSIBLE_HIGH` | `actualKm > 2000` |
   | `ODOMETER_NO_MOVEMENT` | `actualKm == 0` and the route has stops |
   | `ODOMETER_BELOW_STRAIGHT_LINE` | `actualKm + 0.5 < haversine(start, end) * 0.9` |
   | `AVG_SPEED_IMPLAUSIBLE` | `actualKm / hours > 130` |

3. **Warnings are non-blocking.** The route completes regardless. The
   Collector web app renders flagged routes in an amber banner so a human
   collector manager can review them. We do not want to lock a driver out
   of completing their work over a heuristic.

4. **Hard validation stays minimal.** Only physically impossible inputs
   are rejected outright (negative odometer; end < start; invalid lat/lon).
   Everything else is a warning.

5. **The defence stack escalates phase by phase**, and this ADR commits to
   the trajectory:
   - **Phase 1 (now):** typed odometer + heuristic warnings.
   - **Phase 2 (#48 Phase 2):** Driver app streams GPS points during the
     route. `ActualKm` is recomputed from the polyline; odometer becomes a
     *cross-check* (deviation between polyline-km and odometer-km is the
     new fraud signal). The typed odometer remains useful as a fallback
     when GPS is denied or unavailable (tunnels, basement loading).
   - **Phase 3 (SPEC #45 follow-up):** when a `Vehicle` is linked to a
     `Route` and has an OBD / fleet-card feed, the platform pulls odometer
     from the truck and stores `OdometerSource = Vehicle | Driver | Gps`.
     The typed value is then audit-only.
   - **Always-on organisational layer:** every warning is pinned to the
     driver (via `CreatedBy` per [ADR-0008](0008-immutable-audit-trail-user-ids.md))
     so collector managers can spot patterns across many routes. A driver
     whose routes are flagged twice a week is a management conversation,
     not a code problem.

## Alternatives Considered

1. **Reject on heuristic failure.**
   Rejected: a single false positive blocks a real driver from closing a
   real route on a real customer site. Operational pain >> fraud pain at
   this scale. Heuristic = human review, not gatekeeping.

2. **Skip heuristics; trust the driver and audit later.**
   Rejected: gives the routing engine no defence against bad training data
   and gives the collector manager no signal to act on. The heuristics are
   ~50 lines and cost nothing per route.

3. **Make typed odometer mandatory.**
   Rejected: the modal is already blocking enough; a driver in a no-signal
   tunnel or with a broken odometer needs an escape hatch. Field is
   optional; warnings naturally fire when it is absent and we still have
   timestamps.

4. **Build a separate `RouteExecution` entity / Cosmos container.**
   Rejected for Phase 1: telemetry is 1:1 with `Route` and only a handful
   of fields. We can refactor to a separate document later if Phase 2 GPS
   trail (potentially thousands of points per route) makes the route doc
   too fat — and a separate container is the *right* place for that
   high-cardinality data when it arrives.

5. **Use a third-party telematics vendor end-to-end (Fleetio, Verizon
   Connect, Wialon).**
   Rejected for now: locks pilot transporters into hardware they don't
   have, contradicts the "no IoT required" platform differentiator, and
   adds per-vehicle SaaS cost during validation. Revisit as an
   *optional* integration once SPEC #45 OBD support lands.

## Consequences

**Positive**

- Phase 1 ships with an honest threat model: nobody on the team or in the
  pilot can mistake the driver-typed odometer for ground truth.
- Collector managers get an immediate signal channel for review — pinned
  to the responsible driver via the existing audit trail.
- The data shape (`Route` entity gains a `TelemetryWarnings` array) is
  identical whether the warning is computed in Phase 1, Phase 2, or
  Phase 3 — consumers don't change.
- Routing engine (SPEC #47) can filter training data by
  `TelemetryWarnings.length == 0` once it goes live.

**Negative / trade-offs**

- Heuristics will produce false positives (e.g. ferry crossings show
  `ODOMETER_BELOW_STRAIGHT_LINE` because the truck moves without the
  odometer turning). We accept this in Phase 1; the planned reaction is
  "the manager looks at it", not "the system reacts automatically".
- Determined fraud (a driver who types a number consistent with all four
  heuristics) is *not* caught at this layer. The Phase 2 GPS trail is the
  real answer; until then the deterrent is the audit trail + manager
  visibility, not the code.
- The `TelemetryWarnings` field will accumulate code strings the consumer
  has to know about. We keep the list small (4 codes) and translate them
  in the frontend via i18n keys (`routes.telemetryWarnings.<CODE>`).

**Out of scope**

- Vehicle-side OBD integration (SPEC #45 follow-up).
- GPS trail streaming, GDPR consent flow for live tracking, Leaflet
  replay (SPEC #48 Phase 2).
- Empty-running / deadhead classification (SPEC #48 Phase 3, depends on
  Phase 2 trail).
- Automatic invoice adjustment based on actuals — pricing reconciliation
  will be its own SPEC once #47 lands and we have planned-vs-actual.
