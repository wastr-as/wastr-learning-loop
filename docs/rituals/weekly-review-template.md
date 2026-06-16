# Weekly Review — Ritual Guide

> **Cadence:** every Friday, fixed recurring 30-min slot (set once, never move it).
> **Keeper:** CTO — holds the slot, pre-fills the issue, ensures it's filed.
> **Output:** one `[WEEKLY]` issue using the `07_weekly_review` template.
> **Default-alive:** if one founder can't attend, the other runs it and files; the
> absent founder comments within 24 h. The week is "done" only when the issue exists.

## Before the call — keeper pre-fills (~10 min solo)

Status is read **async**, not narrated live. The keeper fills the issue from the loop first:

- Shipped: merged PRs across the Wastr repos this week.
- Signals: new `type: signal` issues opened this week (scan both lanes).
- Experiments: running `[EXP]`s + any kill-criteria checks due.
- Metrics: orders, empty-run %, errors.

The live 30 min is for **reactions + decisions**, not a status read-out.

## Agenda (30 min)

| Time | Topic | Notes |
|---|---|---|
| 0–5 | What we shipped | scan merged PRs |
| 5–10 | Signals collected | scan `type: signal` issues opened this week |
| 10–15 | Key metrics | empty-run %, orders, errors |
| 15–20 | Top 3 learnings | from experiments, bugs, signals |
| 20–25 | Blockers & risks | what could derail next week |
| 25–30 | Next week focus | top 3 priorities |

## Rules

1. **No solutioning during review.** Capture, don't fix.
2. **Every learning that surprised us** gets a `learning: new-insight` label on a follow-up issue.
3. **Every blocker** gets an owner before the meeting ends.
4. **At most 3 decisions.** "Top 3 learnings" / "Next week focus = top 3" are a *ceiling to
   protect the 30-min box, not a quota.* Don't manufacture three — one real joint decision
   is a good week. Don't let it sprawl past three; overflow goes to the loop as issues.
5. **Scan both lanes, keep the boundary.** Cover Lane A (grant-facing) and Lane B (internal);
   only Lane A feeds the Innovasjon Norge narrative at the monthly.
6. **Thematic weeks are allowed.** A single deep topic (e.g. the B2C readiness audit, #64)
   is a legitimate weekly on its own — the broad 6-section format is the default, not a law.

## How to file the review

1. Open new issue from `07 · Weekly Review` template.
2. Title: `[WEEKLY] W{YYYY-Www}` (e.g. `[WEEKLY] W2026-W22`).
3. Add to "WASTR Intelligence Loop" project.
4. After publishing, link any spawned issues back to it.
