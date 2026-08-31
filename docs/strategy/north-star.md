# North Star

> **The single sentence that aligns every decision.**

_Status: **Provisional** — drafted 2026-08-31 by CTO, pending CEO sign-off at the
next monthly review. Adopt or amend; do not leave provisional past one cycle._

## Our North Star

> **Every kilogram of construction & demolition waste in Norway is logged,
> routed, and recycled — with zero empty-running.**

Three claims are load-bearing, and each maps to a differentiator:

- **"logged"** — QR + photo + geo capture at source, so data exists where none did before.
- **"routed"** — two-way logistics optimisation, the core technical IP.
- **"zero empty-running"** — the measurable, falsifiable end-state we are paid to move toward.

## North Star Metric

- **Metric:** **Empty-run %** — km driven without a revenue-generating load ÷ total km driven,
  aggregated across all vehicles on the platform, trailing 30 days.
  Canonical definition: [`docs/metrics/definitions.md`](../metrics/definitions.md#empty-run-).
- **Why this metric:** it is the only number that moves **only** if we are genuinely winning
  on all three fronts at once. It requires transporters to actually use the platform (adoption),
  it requires the routing engine to make better decisions than a dispatcher with a phone
  (product), and it converts directly into the CO₂/NOx figures that builders, Innovasjon Norge
  and future EU customers pay attention to (ESG). A vanity metric like "orders created" can rise
  while we destroy value; empty-run % cannot.
- **Direction:** **down is winning.** (The only supporting metric with inverted polarity —
  stated explicitly so dashboards and reviews don't mis-render it.)
- **Current baseline:** **not yet measured.** Baseline capture is gated on
  [SPEC #48](https://github.com/wastr-as/wastr-learning-loop/issues/48) Phase 1 telemetry
  ([ADR-0017](../architecture/adr/0017-route-execution-telemetry-and-anti-fraud-heuristics.md))
  and must be captured **before** the Routing Service
  ([#47](https://github.com/wastr-as/wastr-learning-loop/issues/47)) starts influencing
  route choice — see [baseline-capture plan](../metrics/definitions.md#baseline-capture-plan-empty-run-).
- **12-month target:** **−25% relative reduction** vs. the captured pilot baseline.
  This is the figure already used in grant and investor material; adopting it here makes it
  falsifiable rather than promotional.

> **Honesty note.** The headline claims in circulation (25% empty-running reduction,
> ~180,000 km/yr, ~160 t CO₂/yr in Oslo) are **modelled projections, not measured results**
> ([ADR-0015](../architecture/adr/0015-sustainability-reporting-strategy.md)). Until a
> baseline exists, external copy should cite Tier 1 empty-run % as *the metric we track*,
> never as an achieved outcome.

> **Candidate (under validation — not adopted):** "Can WASTR become the place
> homeowners go *first* when they have renovation waste?" — a demand-side
> first-touch / repeat-intent metric proposed by the cold-start reframing in
> bet [#59](https://github.com/wastr-as/wastr-learning-loop/issues/59). Listed
> here only as a candidate; do not adopt until the homeowner-segment validation
> round returns signal. Note this is a `lane: b2c` metric and can never replace
> the North Star metric in Innovasjon Norge reporting ([#62](https://github.com/wastr-as/wastr-learning-loop/issues/62)).

## Supporting Metrics

Each supporting metric answers "is the North Star moving for a *real* reason?".
Empty-run % can be gamed by driving fewer, longer routes — the supporting metrics are the guardrails.

| Metric | Definition | Guards against | Current | Target |
|---|---|---|---|---|
| **Empty-run %** ⭑ | km without load ÷ total km (trailing 30d) | — (this is the North Star) | – | −25% vs. baseline |
| Active transporters | unique companies with ≥1 completed order in trailing 7d | improving the metric by shedding users | – | – |
| Active projects | unique builder projects with ≥1 order in trailing 7d | supply-side growth with no demand | – | – |
| Documented mass | tonnes with full chain-of-custody evidence (trailing 30d) | routing well but documenting nothing | – | – |

⭑ = North Star metric. `–` = not yet instrumented; every blank is a known gap, not an oversight.

## What we are NOT

## What we are NOT

<!-- Explicit non-goals to prevent drift. -->

- Not a waste broker (we don't take title of waste)
- Not a hardware company (no IoT sensors)
- Not vendor-locked (neutral marketplace)
