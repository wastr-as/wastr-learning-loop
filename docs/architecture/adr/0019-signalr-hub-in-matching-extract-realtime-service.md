# ADR-0019: SignalR Hub Currently Lives in Matching — Plan to Extract a Dedicated RealTime Service

- **Status:** Accepted (recording state-of-the-world); Phase 6 refactor scheduled
- **Date:** 2026-06-05
- **Deciders:** Siarhei (CTO)
- **Supersedes (partially):** ADR-0002 hosting decision
- **Related:** SPEC #49 Phase 5f, ADR-0006 (BFF), ADR-0009 (route owns sequence)

## Context

ADR-0002 originally placed the SignalR hub "alongside the Collector BFF". In
practice, the hub (`OrderHub`) was implemented inside **Wastr.Services.Matching**
because the first three events to ship were all marketplace concerns:
`ReceiveOrder`, `OrderAssigned`, `OrderStatusChanged`. Matching already had the
Azure SignalR Service wiring, the Service Bus consumer, and the
`ICollectorNotifier` abstraction. Bolting more events on was the cheapest path.

SPEC #49 Phase 5f added three more events:

- `RouteLocationUpdated` — driver telemetry / live truck marker
- `RouteStatusChanged` — route lifecycle flip (Pending → InProgress → Completed / Cancelled)
- `RouteUpdated` — collector edited sequence / cancelled / deleted a route

After Phase 5f, **4 of 6 events have no functional relationship to the
matching/marketplace domain**. The interface is still called `ICollectorNotifier`
even though half its methods now fan out to drivers. Matching is silently
turning into a "real-time fan-out" god-service.

The exploration also surfaced two pre-existing scars:

1. **`OrderHub` has no `[Authorize]` attribute.** Anyone who knows the URL can
   connect and receive every broadcast.
2. **Every broadcast uses `Clients.All.SendAsync(...)`.** No groups, no
   `CompanyId`/`CollectorId`/`DriverId` filtering. Each client sees every other
   collector's order and route events.

Both contradict the original intent in ADR-0002 ("group membership is driven by
`CompanyId`, `CollectorId`, and `DriverId` claims").

## Decision

**Short-term (kept for SPEC #49 Phase 5f):**

- Phase 5f ships in Matching, extending the existing `ICollectorNotifier` and
  `MatchingController` notify-endpoint pattern. This is **knowingly the wrong
  bounded context** but the right pragmatic call to land live tracking and
  bidirectional route updates without a refactor blocking the feature.
- A clear comment header on each new endpoint marks it as a candidate for
  extraction.

**Phase 6 refactor (scheduled, separate spec):**

- Create a new ASP.NET host: **`Wastr.Services.RealTime`**.
  - The existing `Wastr.Services.Notification` repo is Azure Functions only —
    wrong runtime for an SignalR Hub.
  - The new service owns the Azure SignalR Service connection.
  - It hosts every hub: `OrderHub` for marketplace events, `RouteHub` for
    route + driver-location events, plus future hubs (live ETA, customer
    notifications, etc.).
- Move the six existing notify endpoints
  (`/api/matching/notify/*`) into `Wastr.Services.RealTime` at stable URLs
  (`/api/realtime/notify/*`). Update Driver BFF and Collector BFF
  `IMatchingServiceClient` to call the new service. Leave a temporary
  redirect or proxy in Matching for one release cycle.
- Fix the two hardening issues at the same time:
  1. Add `[Authorize]` to every hub.
  2. Replace `Clients.All` with group-based fan-out: drivers join
     `driver-{driverId}`, collectors join `collector-{collectorId}` (and/or
     `company-{companyId}`), route subscribers join `route-{routeId}` on
     demand. Both BFFs already know the identity needed to build these
     groups.

## Alternatives Considered

1. **Host hubs directly in each owning service** (e.g. `RouteHub` in Ordering,
   `OrderHub` in Matching) — rejected: Vue clients would have to connect to
   N hubs; auth and SignalR Service wiring multiplied N times; debugging
   ("where did the broadcast come from?") gets fragmented.
2. **Host the hub inside the Collector BFF and the Driver BFF** (each its own
   hub) — rejected: two hubs to maintain, two SignalR Service resources,
   plus a backplane needed for cross-BFF events (driver location ping needs
   to land in a collector dashboard).
3. **Keep everything in Matching, just rename** — rejected: papers over the
   bounded-context smell; doesn't fix auth or group filtering; gets worse
   with every new event.
4. **Pause Phase 5f and extract RealTime first** — rejected: blocks live
   tracking and bidirectional route push for the duration of the refactor;
   the gap analysis showed real operational pain today (collector polls,
   drivers manually refresh, no route-edit push).

## Consequences

### Positive
- Phase 5f ships now; collector dashboards get live truck markers and instant
  route status flips without waiting for an infrastructure refactor.
- The ADR captures the architectural drift so it doesn't quietly get worse.
- Phase 6 has a clear, scoped objective with three sub-goals (extract, auth,
  groups) that can be sequenced.

### Negative
- `Wastr.Services.Matching` carries `ICollectorNotifier` and six notify
  endpoints whose names lie about the bounded context. New contributors will
  need the comment headers to understand "yes, route-location push really
  does go through the matching service for now."
- The hub remains anonymous and broadcasts to all clients until Phase 6
  lands. This is acceptable inside a closed pilot (3–5 vetted Oslo
  transporters) but **must not ship to multi-tenant production** without
  the Phase 6 hardening.
- A second migration (move client `VITE_SIGNALR_URL` to the new service's
  endpoint) will be needed during Phase 6.

## Phase 6 Definition of Done

- [ ] `Wastr.Services.RealTime` exists, hosts Azure SignalR Service, runs in
      test and prod tenants.
- [ ] All six notify endpoints moved; BFFs point to RealTime instead of
      Matching.
- [ ] Hubs require `[Authorize]` with the same Bearer/AAD scheme as the
      BFFs.
- [ ] Per-route, per-driver, per-collector, per-company groups in use; no
      `Clients.All` remains.
- [ ] `Wastr.Services.Matching` retains only the marketplace algorithm and
      the original `IMatchingService`; its `ICollectorNotifier` and notify
      endpoints are removed.
- [ ] Vue apps point `VITE_SIGNALR_URL` at the new service.
- [ ] ADR-0002 updated to reflect the new hosting reality.
