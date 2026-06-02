# ADR-0007: Multi-Tenancy via `CompanyId` and Azure AD Group Claims

- **Status:** Accepted
- **Date:** 2026-01-22
- **Deciders:** Siarhei (CTO)

## Context

Wastr is a two-sided marketplace. Many transporter companies share the platform;
each company's data (orders, routes, drivers) must be fully isolated from the
others, while admins see across all and the marketplace remains neutral.

We had to choose how tenancy is represented and enforced.

## Decision

- Every tenant-scoped entity (`Order`, `Route`, `User`) carries a nullable
  `CompanyId`.
- Tenant identity is sourced from **Azure AD group claims**. Each Wastr Company
  is mapped to an AAD group; the `JitProvisioningFilter` reads the group claim
  on every BFF request and resolves it to a Wastr `CompanyId`.
- Authorization is layered:
  - `My`-scoped endpoints (`/api/collector/{collectorId}/orders`) — caller must
    BE that collector.
  - `Company`-scoped endpoints (`/api/collector/company/orders`) — caller must
    belong to that company.
  - Admin endpoints — `UserManager`/`ProductManager` roles bypass scope.

## Alternatives Considered

1. **Separate database per tenant** — rejected: operational explosion, kills
   the neutral-marketplace story.
2. **Row-level security (RLS) in SQL** — partially applicable but Cosmos has
   no equivalent; needed an application-layer approach anyway.
3. **Tenant ID derived from subdomain** — rejected: same user can act across
   tenants in marketplace flows; subdomain lock-in is wrong shape.

## Consequences

**Positive**
- Tenancy is a simple filter at every query: `WHERE companyId = @companyId`.
- AAD is the source of truth for membership — no parallel user/group store to
  drift.
- New companies onboard by creating an AAD group; no schema changes.

**Negative**
- Every query that returns tenant data MUST include the `companyId` predicate.
  Forgetting it is a data-leak bug — enforced by code review + integration
  tests.
- JIT provisioning runs on every request → User Service is on the hot path
  for every BFF call (mitigated by short-lived in-memory cache).

## Revisit Trigger

- We onboard a tenant that requires data residency in a separate region
  (e.g., regulated DACH market) — at that point, consider per-region Cosmos
  accounts with `CompanyId` → region routing in the BFF.
- AAD group claim size approaches token limits at scale.
