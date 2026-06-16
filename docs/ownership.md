# Ownership Map

> **Who maintains what. Two founders, two toolchains, one repo.**

The point of this map is not bureaucracy. It is to remove the daily question
*"who edits this — me or you?"* so that updates happen instead of waiting.

---

## Conventions

- **Owner** — the person who decides what the canonical version says and merges
  changes.
- **Contributor** — anyone may propose edits via PR or issue.
- **Both** — joint ownership; either may edit, but material changes require the
  other's review (a comment on the PR is enough; no formal approval needed).

---

## File and folder ownership

| Path | Owner | Notes |
|---|---|---|
| `README.md` | Both | Operating-model changes require both. |
| `docs/strategy/north-star.md` | Both | Highest-stakes file in the repo. |
| `docs/strategy/product-thesis.md` | CEO | CTO contributes the "what is shipped today" section. |
| `docs/strategy/roadmap-now-next-later.md` | Both | Updated at monthly review. |
| `docs/strategy/decision-log.md` | Both | Index file; auto-curated where possible. |
| `docs/customers/pilot-learnings.md` | CEO | Synthesis of customer signals, incl. recurring cross-segment patterns. |
| `docs/rituals/*.md` | Both | Process changes require both. |
| `docs/metrics/definitions.md` | CTO | Canonical metric definitions. CEO contributes business-side metrics. |
| `docs/knowledge/confirmed-learnings.md` | Both | Promotions decided at monthly review. |
| `docs/knowledge/revisit-queue.md` | Both | Auto-fed by `learning: revisit` label. |
| `docs/architecture/adr/` | CTO | ADRs are CTO's domain. |
| `docs/sync-contract.md` | Both | Cross-tool contract; either can propose edits. |
| `docs/tooling-protocol.md` | Both | Operating workflow; either can propose edits. |
| `docs/ownership.md` | Both | This file. |
| `.github/ISSUE_TEMPLATE/*.yml` | CTO | Schema-level changes; CEO consulted on field design. |
| `.github/pull_request_template.md` | CTO | Cross-repo template; CTO rolls out to all Wastr repos. |
| `.github/workflows/*.yml` *(future)* | CTO | Automation lives here once it exists. |

---

## Issue-type ownership

| Issue template | Primary filer | Reviewer |
|---|---|---|
| `[SIGNAL]` Customer Signal | CEO | CTO (for technical implications) |
| `[BET]` Product Bet | Either | The other co-founder |
| `[SPEC]` Feature Spec | CTO | CEO (for product fit) |
| `[BUG]` Bug or Friction | Either | CTO closes |
| `[EXP]` Experiment | Either | Both must agree on success / kill criteria |
| `[DECISION]` Decision Log | Either | The other co-founder comments before close |
| `[WEEKLY]` Weekly Review | CTO (ritual keeper) — pre-fills & files | CEO attends; comments within 24 h if absent |

---

## Ritual cadence ownership

The *templates* in `docs/rituals/*.md` are co-owned (see table above). **Running** the
cadence is owned by the **CTO as ritual keeper**: holding the fixed weekly + monthly
slots, pre-filling the review issue, and making sure the artifact gets filed every week.

**Default-alive rule:** either founder may run and file a review alone; the other
comments within 24 h. A review is "done" only when its issue / doc artifact exists —
a missing week is a visible gap, not a private lapse.

---

## Cross-repo responsibilities

| Concern | Owner |
|---|---|
| Rolling out the PR template to every Wastr service / app repo | CTO |
| Keeping the label taxonomy consistent across repos | CTO |
| Pilot customer relationships | CEO |
| Innovasjon Norge & Antler dialogue | CEO |
| Investor pipeline | CEO |
| Hiring | Both |
| Infrastructure & Azure costs | CTO |

---

## What happens if an owner is unavailable

- The other co-founder may merge edits to any file in this repo. Owner-of-record
  is preserved in the table above; temporary edits are reviewed by the owner on
  return.
- For decisions that cannot wait, file a `[DECISION]` issue with the rationale
  and a note that it is provisional pending the owner's review.

---

*See also: [sync-contract.md](sync-contract.md) and [tooling-protocol.md](tooling-protocol.md).*
