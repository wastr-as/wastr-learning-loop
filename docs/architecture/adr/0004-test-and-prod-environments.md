# ADR-0004: Two-tenant topology — Test (sandbox) environment separate from Prod

- **Status:** Accepted
- **Date:** 2025-11-10
- **Deciders:** Siarhei (CTO)
- **Issue:** [#10](https://github.com/wastr-as/wastr-learning-loop/issues/10)

## Context

Several classes of change cannot be validated safely in production:

- Cosmos DB container or partition-key changes,
- EF Core migrations on the User Service,
- Azure AD app registration changes (redirect URIs, scopes, group claims),
- Service Bus / Event Grid topology changes,
- Breaking API contract changes between services.

A pilot customer cannot be the test bed for any of these. At the same time,
the team is small enough that running per-engineer ephemeral environments
is overkill.

## Decision

Two long-lived Azure tenants, both Terraform-managed from the same modules
in `global-infra` (secrets stored as per [ADR-0003](0003-secrets-in-keyvault.md)):

- **Test (sandbox)** — `*.tfvars` = `test.tfvars`. Receives every merge to
  `main`. Used for integration validation, manual pilot rehearsal, and
  destructive testing.
- **Prod** — `*.tfvars` = `prod.tfvars`. Deploys are gated by manual
  approval in the GitHub Actions pipeline.

Both environments are identical in shape (same services, same infra
modules) but differ in:

- Azure AD app registrations (environment-specific redirect URIs and client
  IDs),
- Cosmos and SQL throughput tiers,
- Key Vault contents (see [ADR-0003](0003-secrets-in-keyvault.md)),
- Resource naming suffix (`-test` vs `-prod`).

The two-account `gh auth` setup (`siarhei-karabitski` for repo work,
`wastras` for org-owner operations) mirrors this separation on the
governance side.

## Alternatives Considered

1. **Single environment with feature flags** — rejected: schema and infra
   changes cannot hide behind flags.
2. **Per-PR ephemeral environments** — rejected at current team size:
   spin-up time and Azure cost outweigh the safety benefit for a 2-person
   engineering team. Revisit when merge rate goes up.
3. **Production with blue/green slot swaps only** — rejected: addresses
   app-tier swaps but not stateful changes (Cosmos containers, migrations,
   Service Bus topics).

## Consequences

**Positive**

- Pilot customers in Prod are insulated from in-progress changes.
- Same Terraform modules deploy to both — environment drift is visible in
  PR diffs, not discovered at 2 AM.
- Manual approval on Prod creates a natural pause for release notes and
  smoke-test checklist.
- CI cost predictable: one Test deploy per merge, Prod deploy on demand.

**Negative**

- Two of every Azure resource doubles the baseline cost — acceptable while
  small, must be revisited at scale.
- AAD app registrations must be created and maintained per environment
  (one-time per service).
- Test data drift: Test is destructively reset more often than Prod, so it
  cannot be used as a backup or for production-data analysis.

## Revisit Trigger

- Merge cadence climbs to the point where Test becomes the bottleneck
  (multiple in-flight features colliding).
- Engineering team grows past ~5 people and per-PR ephemeral environments
  become cost-justified.
- A regulated customer requires a dedicated isolated environment (would
  become Prod-EU, Prod-NO, etc., rather than collapsing Test/Prod).
