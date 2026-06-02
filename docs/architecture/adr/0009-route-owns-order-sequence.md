# ADR-0009: Route Owns Order Sequence via Ordered `OrderIds` Array

- **Status:** Accepted
- **Date:** 2026-01-08
- **Deciders:** Siarhei (CTO)

## Context

A driver's route visits multiple pickup orders in a specific sequence. Two
modelling options:

A. **Sequence on the order** — `Order.SequenceInRoute: int`. Drag-and-drop
   reorder updates N orders.

B. **Sequence on the route** — `Route.OrderIds: Guid[]`, with array position
   = visit position. Drag-and-drop reorder updates 1 route document.

The Collector UI features a drag-and-drop route builder (`vue-draggable-next`);
sequencing happens often and on small N (typically 3–15 orders per route).

## Decision

Sequence lives on the **Route** entity as an ordered `OrderIds` array.
The Order has a back-pointer `RouteId` for the inverse lookup but no
sequence field.

## Alternatives Considered

1. **`SequenceInRoute` on Order** — rejected: reorder = N writes + risk of
   gaps/duplicates if a write fails midway.
2. **Linked list (each Order has `NextOrderId`)** — rejected: traversal cost
   and broken-link recovery aren't worth it for N≤20.
3. **Separate `RouteStop` join table** — rejected: over-modeled for the
   document database; Route is already a small, naturally-grouped aggregate.

## Consequences

**Positive**
- Reorder = 1 Cosmos `ReplaceItem` on the route document.
- Sequence integrity is intrinsic (array order can't have gaps).
- Driver app reads route, then fetches orders sorted by the array index.

**Negative**
- Adding an order to a route requires touching both Route (append ID) and
  Order (set `RouteId`) — handled in a single Ordering Service transaction.
- Driver-side sorting must respect the array order, not a DB-level `ORDER BY`.

## Revisit Trigger

- Routes routinely exceed 50 stops, making the array cumbersome to ship in
  responses → reconsider join model.
- We need per-stop metadata (planned arrival, dwell time, etc.) → upgrade
  array of IDs to array of stop objects.
