# ADR-0005: Cosmos DB for Ordering, SQL Server for User

- **Status:** Accepted
- **Date:** 2025-11-15
- **Deciders:** Siarhei (CTO)

## Context

Two services had very different access patterns:

- **Ordering** — append-heavy, document-shaped (orders embed items, evidence, addresses,
  geolocation), highly partitionable by `CollectorId`, frequent partial reads ("all
  orders for collector X"), unbounded growth, JSON-native at the domain layer.
- **User** — small bounded dataset, strong relational integrity (User ↔ Company ↔ Role),
  frequent joins, identity-critical (auth profiles, JIT provisioning), low write volume.

Picking one engine for both would mean either denormalizing identity (risky for audit)
or paying RU costs for joins we don't need.

## Decision

- **Ordering Service** → Azure Cosmos DB (NoSQL API), partition key `/collectorId`
  on the `orders` container, `/collectorId` on the `routes` container.
- **User Service** → Azure SQL via EF Core 9 with migrations.

## Alternatives Considered

1. **All Cosmos** — rejected: identity joins and uniqueness constraints (email,
   AzureAdObjectId) are awkward without server-side enforcement.
2. **All SQL Server** — rejected: orders embed variable-shape evidence and items;
   schema churn would dominate engineering time.
3. **PostgreSQL + JSONB everywhere** — rejected: would work, but loses Cosmos's
   partition-key elasticity and global distribution story for the EU expansion.

## Consequences

**Positive**
- Cheap horizontal scale for orders (per-collector partitioning).
- Identity remains query-rich and consistent.
- Each service owns its own datastore — no shared schema coupling.

**Negative**
- Two operational profiles to monitor (RU/s vs DTU).
- BFFs must enrich Cosmos documents with SQL-resolved names (see ADR-0008).
- Cross-store transactions impossible — handled by event-driven compensation.

## Revisit Trigger

- Orders container exceeds 50 GB per logical partition.
- We need cross-collector analytical queries beyond what Synapse Link handles.
