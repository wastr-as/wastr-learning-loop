# ADR-0003: All service secrets in Azure Key Vault, referenced via UAMI

- **Status:** Accepted
- **Date:** 2025-09-12
- **Deciders:** Siarhei (CTO)
- **Issue:** [#9](https://github.com/wastr-as/wastr-learning-loop/issues/9)

## Context

Wastr microservices need to consume secret values (Cosmos connection strings,
Service Bus connection strings, Redis keys, third-party API keys, Azure AD
client secrets) without:

- shipping them in app settings, source control, or container images,
- losing them when a resource group is rebuilt by Terraform,
- requiring per-service secret rotation tooling.

Each App Service also needs an identity to read those secrets without storing
a vault-access secret of its own — a classic chicken-and-egg.

## Decision

- A single **Azure Key Vault per environment** holds all service secrets.
- A shared **User-Assigned Managed Identity (UAMI)** is granted `get`, `list`
  on the vault and attached to every App Service.
- App settings reference secrets via `@Microsoft.KeyVault(SecretUri=...)`;
  values are resolved by the platform at startup using the UAMI.
- Terraform provisions the vault, the secrets, the UAMI, and the access
  policy from `global-infra`. Secret values arrive as `sensitive = true`
  variables from the CI secret store; the Terraform state is in encrypted
  Azure Storage.

## Alternatives Considered

1. **Per-app system-assigned managed identity** — rejected: identity is lost
   on app re-creation, breaking the "destroy and recreate without losing
   access" goal. UAMI is decoupled from app lifecycle.
2. **Secrets as Terraform-rendered app settings** — rejected: values land in
   the state file, in app settings telemetry, and in plain text on the App
   Service Configuration blade.
3. **HashiCorp Vault / external KMS** — rejected at this scale: Azure Key
   Vault gives us native UAMI integration and Key Vault references for free.
4. **Environment variables baked into container images** — rejected: rotation
   would require image rebuild; secrets would land in the registry.

## Consequences

**Positive**

- Resource group can be destroyed and recreated; the vault lives outside that
  RG (soft-delete + purge-protection on), so secrets survive.
- Per-secret rotation in the vault is picked up by apps on next read with no
  redeploy.
- Least-privilege: UAMI gets only `get`, `list`; apps cannot enumerate users
  or write secrets.
- One audit trail (vault diagnostic logs) for every secret read.

**Negative**

- Two-step bootstrap: vault + UAMI must exist before apps deploy.
- Adding a new secret requires a Terraform change + plan/apply; cannot be
  done from the portal without drifting from IaC.
- Local development still needs a fallback (developer Azure AD identity with
  scoped vault access; never shared secrets in `appsettings.json`).

## Revisit Trigger

- When/if we adopt **per-customer secret isolation** (multi-tenant
  vault-per-tenant or vault namespacing).
- If Key Vault access latency becomes a hot-path cost (mitigation: secret
  caching with short TTL is already in the App Service runtime).
