# ADR-0002: SignalR for Client Realtime, One Hub for Collector and Driver

- **Status:** Accepted
- **Date:** 2026-02-25
- **Deciders:** Siarhei (CTO)

## Context

Both the Collector dispatcher view and the Driver executor view need to react
to the same domain events without polling:

- New order in marketplace → both potential bidders and assigned drivers care.
- Route reordered / order reassigned → the affected driver needs to know now;
  the dispatcher needs to see the change reflected in the live board.
- Evidence captured / order completed → dispatcher view updates without manual
  refresh.

Polling these endpoints from two apps at sensible intervals (5–10s) was burning
RU/s on Cosmos for queries that returned identical data 90% of the time.

## Decision

- Use **ASP.NET Core SignalR** (WebSockets with long-polling fallback) as the
  single client-push transport.
- **One hub** serves both Collector and Driver apps. Connection identity is
  the authenticated user; group membership is driven by `CompanyId`,
  `CollectorId`, and `DriverId` claims.
- Push payloads are **thin**: the *fact* of change plus the entity id
  (`{ type: "OrderUpdated", orderId: "..." }`). Clients re-fetch through the
  BFF to get the full, authorized shape.
- Hub is hosted alongside the Collector BFF (closest to the domain it serves);
  the Driver app connects to the same hub via the BFF's exposed endpoint.

## Alternatives Considered

1. **Per-app push channels** (separate hub per frontend) — rejected: the
   underlying events are identical; duplicating infrastructure for the same
   payloads is wasted.
2. **Server-Sent Events (SSE)** — viable for our one-way push need; rejected
   because SignalR brings reconnection, group management, and ASP.NET-native
   auth integration for free.
3. **Re-using Event Grid for client push** — rejected: Event Grid is
   server-side fan-out; pushing to browsers requires per-client auth + group
   semantics that SignalR already provides.
4. **Polling with ETags** — rejected: still pays per-request RU cost; UX
   latency unacceptable for the marketplace flow.

## Consequences

**Positive**
- One realtime infrastructure for the whole platform — adding the customer
  "your driver is en route" view or an admin live board joins the same hub.
- Thin payloads keep authorization in one place (the BFF), not duplicated in
  push messages.
- Reconnection, group join/leave, and backpressure are framework concerns.

**Negative**
- Sticky scale-out — when we horizontally scale the Collector BFF, SignalR
  needs a backplane (Redis or Azure SignalR Service). Not yet required at
  pilot scale.
- Every push triggers a follow-up REST call from the client → 2× traffic on
  highly-changing entities. Acceptable: REST responses are cacheable and
  short-lived; total RU spend dropped significantly vs. polling.

## Revisit Trigger

- Single-instance BFF can no longer hold all connections → migrate to Azure
  SignalR Service (managed backplane).
- Push payload thinness becomes a UX problem (perceived double-latency on
  visible state) → consider payload-rich pushes for specific hot paths.
- A third party needs to consume these events → expose Event Grid (ADR-0001)
  instead of SignalR; SignalR remains client-only.
