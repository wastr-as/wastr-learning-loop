# Roadmap — Now / Next / Later

> **A rolling, opinion-driven roadmap. No dates, only sequencing.**
> Covers the whole company across four lanes: Product, Commercial, Funding & partnerships, Team & ops.
> Update at every monthly review. Move items only when learnings justify it.

_Last updated: 2026-06-02_

## Now (this quarter — currently in flight)

### Product
- [ ] Vipps login + checkout cutover from placeholder to live (NO market) — [#43](https://github.com/wastr-as/wastr-learning-loop/issues/43) (blocks bet [#41](https://github.com/wastr-as/wastr-learning-loop/issues/41), depends on merchant credentials)

### Commercial
- [ ] Provision Vipps merchant account (Test + Prod) — commercial half of [#43](https://github.com/wastr-as/wastr-learning-loop/issues/43)

### Funding & partnerships
- [ ] …

### Team & ops
- [ ] …

## Next (next quarter — on deck, specs being shaped)

### Product
- [ ] Cross-market payment strategy (BR + future EU) — Vipps is NO-only per [ADR-0010](../architecture/adr/0010-vipps-for-no-identity-and-payment.md)

### Commercial
- [ ] …

### Funding & partnerships
- [ ] …

### Team & ops
- [ ] …

## Later (parked — keep visible, don't commit)

### Product
- [ ] Smart route planner — auto-assign orders to most suitable driver, pre-accept simulation at marketplace, pluggable strategy (time / distance / cost / CO₂), toll-aware (bomstasjon), two-way logistics integration — [#44](https://github.com/wastr-as/wastr-learning-loop/issues/44) (directional bet, anchors near-term decisions; not yet a spec)

### Commercial
- [ ] …

### Funding & partnerships
- [ ] …

### Team & ops
- [ ] …

## Recently Shipped

| Date | Lane | Item | Outcome link |
|---|---|---|---|
| 2025-09-05 | Product | Waste-bag photo evidence persisted in Azure Blob via Ordering Service | [#11](https://github.com/wastr-as/wastr-learning-loop/issues/11) |
| 2025-09-12 | Product | All service secrets in Azure Key Vault (UAMI-backed) | [#9](https://github.com/wastr-as/wastr-learning-loop/issues/9) · [ADR-0003](../architecture/adr/0003-secrets-in-keyvault.md) |
| 2025-09-12 | Product | Collector map preserves zoom/center after closing order detail | [#35](https://github.com/wastr-as/wastr-learning-loop/issues/35) |
| 2025-10-01 | Product | Notification Service for order-status events (email/SMS/WhatsApp/push) | [#12](https://github.com/wastr-as/wastr-learning-loop/issues/12) |
| 2025-10-01 | Product | Combined QR + photo capture in a single Customer App step | [#17](https://github.com/wastr-as/wastr-learning-loop/issues/17) |
| 2025-11-10 | Product | Test (sandbox) environment separate from Prod | [#10](https://github.com/wastr-as/wastr-learning-loop/issues/10) · [ADR-0004](../architecture/adr/0004-test-and-prod-environments.md) |
| 2025–2026 | Product | User Service (identity, roles, prefs) + User Management App | [#13](https://github.com/wastr-as/wastr-learning-loop/issues/13) · [#14](https://github.com/wastr-as/wastr-learning-loop/issues/14) |
| 2025–2026 | Product | Product Service + Price management in Admin dashboard | [#15](https://github.com/wastr-as/wastr-learning-loop/issues/15) · [#16](https://github.com/wastr-as/wastr-learning-loop/issues/16) |
| 2025-11 → 2026-05 | Product | Customer App MVP UX hardening (10 friction fixes) | [#19](https://github.com/wastr-as/wastr-learning-loop/issues/19) (epic) |
| 2025-11 → 2026-02 | Product | Brazil pilot — Customer App variant for cooking-oil waste (PT-BR) | [#30](https://github.com/wastr-as/wastr-learning-loop/issues/30) (experiment) |
| 2026-05 | Product | WASTR logo + brand identity across all apps | [#18](https://github.com/wastr-as/wastr-learning-loop/issues/18) |

## Recently Killed

| Date | Lane | Item | Why killed |
|---|---|---|---|
| – | – | – | – |
