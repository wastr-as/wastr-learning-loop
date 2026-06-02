# Pilot Learnings

> **Synthesis across many `[SIGNAL]` issues.**
> Re-read and update after every monthly product review.

_Last synthesis: 2026-06-02 — covering backfilled issues #19–#35 (Customer App MVP hardening + Brazil pilot)_

## Headline Learnings

1. **The core order flow generalises across markets and waste fractions.** The QR + geo + photo + product-select pattern shipped in Oslo (construction & demolition waste) transferred cleanly to a Brazilian pilot for cooking-oil collection with **no changes to the core flow** — only localisation. This validates the platform thesis that WASTR is a logistics product, not a Norwegian-CDW product. ([#30](https://github.com/wastr-as/wastr-learning-loop/issues/30))
2. **Localisation pain concentrates in identity and address, not the order flow.** Every BR pilot friction issue clustered in two areas: identity fields (CPF instead of MS login) and address structure (CEP, apartment, responsible person ≠ generator). The order steps themselves needed only translation. ([#29](https://github.com/wastr-as/wastr-learning-loop/issues/29), [#31](https://github.com/wastr-as/wastr-learning-loop/issues/31), [#34](https://github.com/wastr-as/wastr-learning-loop/issues/34))
3. **Every removed tap in the Customer App is measurable.** Ten small UX fixes (combined QR+photo, drop-down for bag count, NEXT button above the fold, smaller fonts to avoid scrolling) compounded into a one-screen order flow. Each individually felt cosmetic; cumulatively they are what makes the QR-to-order conversion work. ([#19](https://github.com/wastr-as/wastr-learning-loop/issues/19) epic)

## By Segment

### Transporters (SMB)

- **Jobs-to-be-done observed:** _Not yet covered by backfill — synthesis to follow once first Oslo transporter pilot signals land._
- **Top friction points:**
- **Surprises:**
- **Willingness to pay signals:**

### Builders / Contractors

- **Jobs-to-be-done observed:** Drop a waste pickup order from a job site without installing anything, with photo evidence captured at source for site documentation.
- **Top friction points:** Anything that breaks the "one screen, one tap" feel — overflowing buttons, freeform quantity inputs, two-step QR-then-photo capture, locale-wrong notifications.
- **Surprises:** Customers want to attach **several** photos per order, not one (driver-side evidence needs already pointed this way — customer-side demand confirmed it). Builders in BR pilot expected a comment field on the photo step for special instructions.
- **Willingness to pay signals:** _Pricing model deferred during BR pilot; first paid orders pending._

## What Changed in the Product Because of This

| Learning | Change made | Issue link |
|---|---|---|
| Two camera steps (QR then photo) is one friction too many | Combined QR + photo capture into a single step | [#17](https://github.com/wastr-as/wastr-learning-loop/issues/17) |
| Customers want to attach multiple photos per order | Evidence model & UI extended to N photos per order | [#36](https://github.com/wastr-as/wastr-learning-loop/issues/28) |
| Notification language was wrong without explicit user signal | Language selector in Customer App, persisted on user | [#22](https://github.com/wastr-as/wastr-learning-loop/issues/22) |
| BR pilot proved core flow is market-agnostic | Architecture principle codified: no hardcoded Norwegian assumptions | [#30](https://github.com/wastr-as/wastr-learning-loop/issues/30) |
| Pricing/currency abstraction insufficient for non-NOK markets | Logged for revisit — see [revisit-queue](../knowledge/revisit-queue.md) |  |

## What We Still Don't Know

- Transporter (SMB) JTBD — backfill covers Customer + infra; transporter-side pilot signals are still to come.
- Quantitative impact of UX hardening on QR-to-order conversion rate (no baseline captured pre-fixes).
- Whether the BR pilot finding generalises to a **third** market (would confirm the platform thesis at a higher confidence level).
