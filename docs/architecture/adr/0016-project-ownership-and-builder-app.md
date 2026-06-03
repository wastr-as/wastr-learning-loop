# ADR-0016: Project ownership belongs to Company, not User; introduces a Builder app

- **Status:** Proposed
- **Date:** 2026-06-03
- **Deciders:** Siarhei (CTO), Denis (CEO) — TBD
- **Related:** [SPEC #49](https://github.com/wastr-as/wastr-learning-loop/issues/49), [ADR-0007 (multi-tenancy)](0007-multitenancy-via-company-id-and-aad-groups.md), [Sketch: Builder app](../sketches/builder-app.md)

## Context

SPEC #49 Phase 1 shipped a `Project` entity inside the Ordering Service
partitioned by `CustomerId` (the user who created it). Two issues surfaced
in review on the same day:

1. **Ownership is wrong.** Construction-and-demolition projects in Norway
   are run by **companies** (Veidekke, Skanska, "Byggmester X AS"), not
   individuals. Multiple employees of the same builder must share the same
   project list, and the project must survive personnel changes.
   `CustomerId` as the partition key forces a single-owner model that does
   not match the domain.
2. **Wrong UX home.** The Customer app (`Wastr.Apps.Web.Customer`) is
   intentionally stateless: QR → photo → order, no login, no profile, no
   project list. Adding project management screens to it would break the
   zero-friction principle that makes the Customer app work. Builders are
   a fundamentally different persona and need their own front-end.

The Phase 1 implementation has not yet been used in production — no
Cosmos data exists in the `projects` container — so we can pivot cleanly.

## Decision

1. **Repartition `Project` by `CompanyId`.** Make `CompanyId` a required,
   immutable property and the Cosmos partition key. `CreatedBy` keeps the
   user id strictly for audit per [ADR-0008](0008-immutable-audit-trail-user-ids.md).
2. **Order auto-links to the project's company.** When an order is created
   with a `ProjectId`, the Ordering Service copies `Project.CompanyId` to
   `Order.CompanyId`. This holds even when the placing customer is a guest
   scanning a project-scoped QR — the **project owns the company link**, not
   the orderer.
3. **Validation rule changes:** `IProjectService.EnsureBelongsToCompanyAsync(projectId, companyId)`
   replaces the `EnsureBelongsToCustomerAsync` shipped in Phase 1. Orders
   without a CompanyId (pure ad-hoc guest orders) cannot carry a `ProjectId`.
4. **Introduce a fourth front-end, `Wastr.Apps.Web.Builder`**, dedicated to
   the construction-company persona. Customer app stays stateless and gains
   only a `?project={id}` URL parameter handler. Sketch lives in
   [docs/architecture/sketches/builder-app.md](../sketches/builder-app.md).
5. **Builder backend access pattern** to be decided in a follow-up ADR —
   either a new `Wastr.Services.Builder` BFF (matches Collector/Driver
   symmetry) or `/api/builder/*` endpoints inside Ordering. This ADR does
   not commit either way.

## Alternatives Considered

1. **Keep `CustomerId` ownership, add a `CompanyId` filter on queries.**
   Rejected: still leaves the model lying about who owns the project,
   forces every list query to remember the dual filter, and makes
   employee handover (the leaving-employee problem) require data migration.
2. **Owner = `OwnerId` (= `CompanyId ?? UserId`), polymorphic.**
   Rejected: smuggles two domain concepts into one column, makes Cosmos
   queries branch on shape, and pushes the resolution logic into every
   consumer. Cleaner to say "Projects require a Company; ad-hoc orders
   need no project."
3. **Add project management screens to the Customer app behind a login.**
   Rejected: kills the QR-first zero-friction UX that the Customer app
   was built for, mixes two incompatible session models, and forces every
   homeowner through a login wall they don't need.
4. **Defer building a Builder app; expose Projects only via Collector app.**
   Rejected: Collector app is the transporter UI; builders and transporters
   have opposed economic interests and must not share a workspace.
   Vendor-neutrality (a core platform principle) requires separation.

## Consequences

**Positive**

- Projects align with how the CDW domain actually works in Norway.
- Same-company employees collaborate naturally; no per-user re-creation.
- ESG / NS 9431 reports are per company, which is what regulators and
  builders expect.
- Customer app stays the lightweight tool that pilot customers responded
  to; the Builder app can grow without contaminating it.
- The QR-poster flow (Builder generates poster → on-site worker scans →
  Customer app pre-fills `ProjectId`) becomes the killer onboarding
  story for the builder segment.

**Negative**

- Adds a new front-end repo to maintain (CI/CD, Dockerfile, nginx, MSAL).
- Requires Company creation for builders before they can use Projects —
  needs onboarding flow (likely Vipps for Business; see ADR-0010).
- The Phase 1 SPEC #49 code shipped today (1ced65d in Ordering,
  328309d in global-infra) needs immediate refactor:
  `Project.CustomerId` → `CompanyId`, Cosmos container partition key
  redefined (`/CustomerId` → `/CompanyId`).
- Cross-aggregate validator name change ripples into `OrderService`.

**Migration / cleanup steps if accepted**

1. Refactor `Project` domain: drop `CustomerId`, require `CompanyId`,
   update `ProjectRepository`, `ProjectService`, `ProjectController`.
2. Update `OrderService.CreateOrderAsync`: validate `ProjectId` against
   the project's `CompanyId`, then copy it to the new order.
3. Update Terraform: `azurerm_cosmosdb_sql_container.projects.partition_key_paths`
   from `["/CustomerId"]` to `["/CompanyId"]`. Cosmos containers cannot
   change partition keys in place → `terraform destroy` + `terraform apply`
   on this single resource (safe: container is empty in both test and prod).
4. Bump SPEC #49 acceptance criteria in the issue.

## Revisit Trigger

- A pilot tells us individual professionals (sole-proprietor handymen
  without an AS) need project grouping → reconsider a "personal project"
  shape backed by user-as-company.
- We expand outside Norway and find a market where projects are owned by
  the worksite (not the contractor) — re-evaluate ownership semantics.
- Builder app proves to be the wrong tool (e.g., pilots actually want
  projects inside the Customer app via a saved-profile mode) — supersede.

## Open follow-up decisions

- **ADR-00xx (TBD):** Builder backend topology — separate BFF vs. Ordering
  extension.
- **ADR-00xx (TBD):** Builder identity provider — Vipps for Business vs.
  Azure AD vs. both.
- **SPEC #49 Phase 2:** Builder app MVP scope (Projects CRUD + per-project
  order list).
