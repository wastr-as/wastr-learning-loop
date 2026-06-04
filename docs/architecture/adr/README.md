# Architecture Decision Records (ADRs)

> **One file per significant architectural decision.**
> Each ADR is also mirrored as a `[DECISION]` issue for discussion + searchability.

## Format

Filename: `NNNN-short-slug.md` (e.g. `0001-cosmos-db-for-ordering.md`)

Each ADR contains:
1. **Status** — Proposed / Accepted / Superseded by ADR-NNNN
2. **Context** — what forced the decision
3. **Decision** — what we chose
4. **Alternatives** — what we considered and rejected
5. **Consequences** — positive and negative
6. **Revisit trigger** — when to reopen

## Index

> Ordered chronologically by decision date (earliest first).

| ADR | Title | Status | Issue |
|---|---|---|---|
| [0001](0001-service-bus-and-event-grid.md) | Service Bus for work, Event Grid for fan-out | Accepted | – |
| [0002](0002-signalr-for-client-realtime.md) | SignalR for client realtime, one hub for Collector and Driver | Accepted | – |
| [0003](0003-secrets-in-keyvault.md) | All service secrets in Azure Key Vault, referenced via UAMI | Accepted | [#9](https://github.com/wastr-as/wastr-learning-loop/issues/9) |
| [0004](0004-test-and-prod-environments.md) | Two-tenant topology — Test (sandbox) separate from Prod | Accepted | [#10](https://github.com/wastr-as/wastr-learning-loop/issues/10) |
| [0005](0005-cosmos-db-for-ordering-sql-for-user.md) | Cosmos DB for Ordering, SQL for User | Accepted | – |
| [0006](0006-bff-for-collector-and-driver.md) | BFF pattern for Collector and Driver apps | Accepted | – |
| [0007](0007-multitenancy-via-company-id-and-aad-groups.md) | Multi-tenancy via `CompanyId` + AAD group claims | Accepted | – |
| [0008](0008-immutable-audit-trail-user-ids.md) | Immutable audit trail — store IDs, resolve names at read time | Accepted | – |
| [0009](0009-route-owns-order-sequence.md) | Route owns order sequence via ordered `OrderIds` array | Accepted | – |
| [0010](0010-vipps-for-no-identity-and-payment.md) | Vipps for NO identity + payment (Customer App) | Accepted | [#42](https://github.com/wastr-as/wastr-learning-loop/issues/42) |
| [0011](0011-fleet-service.md) | New FleetService with its own datastore | Accepted | [#45](https://github.com/wastr-as/wastr-learning-loop/issues/45) |
| [0012](0012-nvdb-toll-data-source.md) | NVDB as toll-data source for Norway | Accepted | [#46](https://github.com/wastr-as/wastr-learning-loop/issues/46) |
| [0013](0013-route-engine-or-tools.md) | Route engine: Azure Maps (Layer 1) + OR-Tools (Layer 2) in new Routing Service | Accepted | [#44](https://github.com/wastr-as/wastr-learning-loop/issues/44) |
| [0014](0014-co2-accounting.md) | CO₂ accounting: TTW for routing, HBEFA seed, WTW reserved for ESG | Accepted | [#45](https://github.com/wastr-as/wastr-learning-loop/issues/45) · [#47](https://github.com/wastr-as/wastr-learning-loop/issues/47) |
| [0015](0015-sustainability-reporting-strategy.md) | Sustainability & reporting strategy: tiering, standards alignment (ISO 14083, NS 9431), what we will not claim | Accepted | [#48](https://github.com/wastr-as/wastr-learning-loop/issues/48) · [#49](https://github.com/wastr-as/wastr-learning-loop/issues/49) · [#50](https://github.com/wastr-as/wastr-learning-loop/issues/50) · [#51](https://github.com/wastr-as/wastr-learning-loop/issues/51) |
| [0016](0016-project-ownership-and-builder-app.md) | Project ownership belongs to Company, not User; introduces a Builder app | Proposed | [#49](https://github.com/wastr-as/wastr-learning-loop/issues/49) |
| [0017](0017-route-execution-telemetry-and-anti-fraud-heuristics.md) | Route execution telemetry: driver-reported odometer with non-blocking anti-fraud heuristics (phased toward GPS trail + OBD) | Accepted | [#48](https://github.com/wastr-as/wastr-learning-loop/issues/48) |
| [0018](0018-route-plan-immutability-driver-executes.md) | Route plan is immutable post-save — driver executes saved sequence, does not re-optimise (Phase 2 escape hatch designed but deferred) | Accepted | [#47](https://github.com/wastr-as/wastr-learning-loop/issues/47) · [#54](https://github.com/wastr-as/wastr-learning-loop/issues/54) |
