# Decision Log Index

> Index of all `[DECISION]` issues + lightweight ADR summaries.
> Full context lives in the linked issue. This file is the searchable map.

| # | Date | Decision | Domain | Status | Revisit trigger |
|---|---|---|---|---|---|
| [#9](https://github.com/wastr-as/wastr-learning-loop/issues/9) | 2025-09-12 | Store all service secrets in Azure Key Vault, referenced via UAMI | infra | Validated · [ADR-0003](../architecture/adr/0003-secrets-in-keyvault.md) | Multi-tenant secret isolation per customer |
| [#10](https://github.com/wastr-as/wastr-learning-loop/issues/10) | 2025-11-10 | Maintain a separate Test (sandbox) environment, promote to Prod after validation | infra | Validated · [ADR-0004](../architecture/adr/0004-test-and-prod-environments.md) | Release cadence high enough to warrant ephemeral PR envs |

## How to add an entry

1. Open a `[DECISION]` issue using the `06_decision_log` template.
2. After the decision is final, add a row here linking to the issue.
3. If a decision is later reversed, do not delete — add a new row referencing the prior.
