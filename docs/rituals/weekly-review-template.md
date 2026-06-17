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
- **Landing analytics:** open the *WASTR Landing — Analytics* workbook and read the 5 tiles (see [Landing workbook check](#landing-workbook-check-how--where) below). Paste the funnel numbers + bounce % into the issue.

The live 30 min is for **reactions + decisions**, not a status read-out.

## Agenda (30 min)

| Time | Topic | Notes |
|---|---|---|
| 0–5 | What we shipped | scan merged PRs |
| 5–10 | Signals collected | scan `type: signal` issues opened this week |
| 10–15 | Key metrics | empty-run %, orders, errors, **landing funnel + bounce** |
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

## Landing workbook check (how & where)

The public site **wastras.com** sends client-side telemetry to a dedicated
Application Insights resource. The weekly read is a 2-minute glance at one workbook.
See [ADR-0020](../architecture/adr/0020-frontend-telemetry-build-time-injection.md)
for the why.

### Where to find it

1. [Azure Portal](https://portal.azure.com) → resource group **`wastr-shared-services-rg`**.
2. Open the App Insights resource **`appi-wastr-landing`** (Log Analytics workspace: `law-wastr-landing`).
3. Left nav → **Monitoring → Workbooks** → open **WASTR Landing — Analytics**.
   - It's provisioned as code (`global-infra/shared-resources/landing-workbook.json`), so it's
     always there — don't recreate it. To change a query, edit the JSON + `terraform apply`,
     not the portal (portal edits get overwritten on next apply).

### What each tile means & what to flag

| Tile | Reads | Flag when |
|---|---|---|
| **Traffic & top pages (7d)** | views + unique visitors per page | Traffic drops to ~0 (deploy broke telemetry) or a page you expected is missing. |
| **Conversion funnel (7d)** | sessions surviving each step: `visit → hero_calculator_clicked → calc_started → calc_completed → save_cta_clicked` | A big step-to-step drop = friction. Note the worst drop as the funnel's weakest link. |
| **Bounce rate (7d)** | % of single-pageview sessions | Sustained rise vs prior weeks = landing message/landing-page mismatch. |
| **Exceptions (24h)** | client-side JS errors by message | Any non-zero you don't recognise → open a `type: signal` / bug issue. |
| **Load performance (7d, ms)** | p50 / p95 page load per page | p95 creeping up (slow page = lost visitors). |

### What to capture in the weekly issue

- Funnel: the 5 step counts (or just the conversion % visit→`save_cta_clicked`) and the **single worst drop-off**.
- Bounce %: this week vs last.
- Any exception cluster or p95 regression → spawn a follow-up issue and link it back.

### Alerts (don't wait for the weekly)

Two Azure alerts email **skar@wastras.com** between reviews — you don't need to poll for these:

- **No telemetry in 2h** → the site is up but tracking is dead (usually a broken deploy /
  missing `VITE_APP_INSIGHTS_CONNECTION` secret). Treat as a deploy regression.
- **Exception spike (>10 / 15 min)** → a client-side error is hitting real visitors. Triage same-day.

If an alert fired during the week, note it in **Blockers & risks** even if already resolved —
it's a signal about deploy/quality health.

> **Note:** several SDK helpers (`trackCTA`, `trackScrollDepth`, `trackOutboundLink`, etc.)
> are defined but **not yet wired**, so those dimensions are empty. Only the 5 funnel events
> above emit data today. Don't read absence there as a drop.
