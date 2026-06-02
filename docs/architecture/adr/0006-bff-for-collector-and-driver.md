# ADR-0006: BFF Pattern for Collector and Driver Apps

- **Status:** Accepted
- **Date:** 2025-12-02
- **Deciders:** Siarhei (CTO)

## Context

The Collector and Driver web apps need:
1. **Aggregated data** — an order list with collector names, company names, driver
   names, product details (spread across User, Ordering, Product services).
2. **Identity context** — every request must resolve "who is calling, what company,
   what role" from Azure AD claims before touching domain services.
3. **Per-role surface area** — drivers see a tiny slice; collector managers see
   company-wide data; admins see everything.

Letting each frontend orchestrate 3–4 backend calls per screen would:
- leak the microservice topology to the browser,
- multiply round-trips on mobile networks,
- spread auth logic across JavaScript.

## Decision

Introduce **two thin BFF services**: `Wastr.Services.Collector` and
`Wastr.Services.Driver`. Each:
- Exposes a frontend-shaped API (`/api/collector/...`, `/api/driver/...`).
- Acquires Azure AD client-credential tokens to call Ordering, User, Product.
- Runs a `JitProvisioningFilter` on every request to map Azure AD identity →
  Wastr user (creating one on first sight).
- Performs **batch enrichment** — collect user IDs from a list of orders, call
  `POST /api/user/batch/names` once, then stamp transient `*Name` properties.

## Alternatives Considered

1. **API Gateway with response composition** — rejected: composition logic is
   non-trivial (JIT, batching, role-specific shapes); easier as a service.
2. **GraphQL gateway** — rejected: adds a query language we don't need yet;
   revisit if frontend teams diverge.
3. **Frontend orchestration** — rejected: see Context.

## Consequences

**Positive**
- Frontends stay dumb and fast.
- Single place to enforce per-role authorization.
- Domain services stay pure (no identity enrichment in Ordering).

**Negative**
- Two more services to deploy and monitor.
- BFF is a tempting place to leak business logic into — must be policed in review.

## Revisit Trigger

- A third frontend (e.g., Customer mobile native) needs a different aggregation
  shape — consider whether to fold into existing BFFs or add a third.
- BFF endpoints start containing domain rules instead of orchestration.
