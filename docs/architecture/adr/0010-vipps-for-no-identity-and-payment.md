# ADR-0010: Vipps for NO identity + payment

- **Status:** Accepted
- **Date:** 2026-05-27
- **Deciders:** Denis (CEO), Siarhei (CTO)

## Context

Norwegian builders need to sign up and pay for a waste pickup with the smallest possible friction. The BR pilot (#34) confirmed Microsoft login was a conversion blocker; each market needs its own low-friction local answer. Vipps has ~95% adult coverage in Norway and combines identity *and* payment in a single redirect.

## Decision

For the **Norwegian market only**, identity + payment in the Customer App is handled by **Vipps Login + Vipps Checkout**, integrated via three new endpoints in the Ordering Service (`/Payment/vipps/checkout`, `/status`, `/token-exchange`).

Code is shipped in placeholder mode (scaffolded but not making live API calls). The cutover to live API calls is gated on merchant credential provisioning — see linked SPEC.

## Alternatives Considered

1. **Stripe / Adyen card form** — universal, but: no embedded identity, foreign brand, card-form completion friction. Rejected for primary NO flow; kept as fallback if Vipps bet fails.
2. **Klarna Checkout** — strong BNPL UX, weaker identity story, lower SMB construction brand affinity. Rejected.
3. **Manual invoice** — zero friction at order, but credit risk + 30+ day cash cycle. Rejected for SMB segment; may revisit for large-account builders.
4. **BankID identity + Stripe payment** — two redirects, two brands. Rejected.

## Consequences

**Positive**
- Single redirect for who-you-are *and* paid.
- Brand trust + ~95% NO adult coverage.
- Removes the signup tap entirely for most users.

**Negative**
- NO-only — does not solve BR or future EU markets.
- Vendor lock-in for the primary NO flow.
- Webhook reliability + reconciliation operational load (to be measured).
- Reversibility cost rises with active Vipps-bound user count.

## Revisit Trigger

- Vipps bet kill criteria hit (see linked `[BET]`): completion rate <60%, drop-off >25%, ≥3 friction signals, or >4 eng-hrs/week sustained ops cost.
- Vipps changes pricing or terms in a way that breaks SMB unit economics.
- We commit to a non-NO market large enough that single-rail strategy becomes a hard blocker.
- Cross-market payment strategy consolidates on a different primary rail.

## Linked

- `[DECISION]` #42 — Vipps over Stripe / Klarna / invoice for NO market
- `[BET]` #41 — Vipps-as-identity-and-payment converts NO builders
- `[SPEC]` #40 — Vipps payment + login scaffold (placeholder)
- `[SPEC]` #43 — Provision merchant credentials + cutover
