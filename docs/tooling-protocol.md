# Tooling Protocol

> **Concrete workflows for the four-tool setup: GitHub, Notion, Perplexity, Claude.**
>
> The [sync contract](sync-contract.md) defines *what* lives where. This document
> defines *how* the team actually operates day to day.

---

## Daily / weekly workflows

### Customer interview (CEO)

1. **Live notes** in Notion during the call (free-form, raw quotes).
2. **Within 48 h:** open `[SIGNAL]` issue(s) in this repo for each distinct
   observation. Quote the customer directly. Apply labels per the taxonomy.
3. **Link** the Notion page URL in the issue footer.
4. **If the signal contradicts a confirmed learning,** apply the two-layer rule:
   - **Issue-layer** (learning still lives on a `learning: confirmed` issue):
     reopen that issue, swap its label to `learning: hypothesis`, cross-link
     the two issues.
   - **Doc-layer** (learning has been promoted into
     `docs/knowledge/confirmed-learnings.md` as L-NNN): apply
     `learning: revisit` to the new signal AND add a row to
     `docs/knowledge/revisit-queue.md` pointing at the L-NNN entry. The weekly review
   will pick it up via the open-hypothesis filter.

### Strategy analysis (CEO + Perplexity)

1. Run analysis in the relevant Perplexity space (Innovasjon Norge / investor /
   Brazil / public sector / strategy).
2. Perplexity ends every substantive session with a **Learning Log block**.
3. CEO copies the Learning Log into `WASTR_LearningLog.md` (Notion or local)
   and re-uploads to Perplexity to keep its memory current.
4. **If the session produced a decision or canonical fact:** CEO opens a
   `[DECISION]` issue here, or proposes an edit to the relevant `docs/strategy/*.md`
   file. The Perplexity thread title goes in the issue footer.

### Code change (CTO + Claude / Copilot)

1. Claude / Copilot drafts code locally in VS Code.
2. CTO reviews, commits, opens a PR in the relevant Wastr service / app repo.
3. PR template forces a link back to a `[SIGNAL]` / `[BET]` / `[SPEC]` /
   `[EXP]` / `[DECISION]` issue in this repo.
4. Merging the PR is the trigger to update the linked issue's status
   (`in-progress` → `shipped`).

### Architectural decision (CTO)

1. Draft the ADR locally (markdown).
2. Open a `[DECISION]` issue summarising the choice + alternatives + rationale.
3. Commit the ADR under `docs/architecture/adr/NNNN-title.md`.
4. Reference the ADR file from the issue and vice versa.

### Weekly review (CEO + CTO, Friday 30 min)

1. Open one `[WEEKLY]` issue from the template.
2. Review: shipped PRs, new signals, running experiments, kill-criteria checks.
3. Any signal that contradicts a confirmed learning → apply the two-layer rule (reopen the `learning: confirmed` issue OR add a row to `docs/knowledge/revisit-queue.md` if the learning has been promoted to a doc entry).
4. Any bet hitting kill criteria → close as `invalidated`.

### Monthly review (CEO + CTO, last Friday, 90 min)

1. Promote eligible insights into `docs/knowledge/confirmed-learnings.md`.
2. Re-rank `docs/strategy/roadmap-now-next-later.md`.
3. Walk both revisit surfaces — reopened `learning: hypothesis` issues (previously confirmed, now in doubt) AND rows in `docs/knowledge/revisit-queue.md` — and either re-confirm each item or close as `learning: invalidated` (issues) / update `confirmed-learnings.md` (doc entries).
4. Scan `[SIGNAL]` issues across segments — if the same pattern appears in ≥3 signals, open an `[L-NNN]` promotion candidate or add a cross-segment note to `docs/customers/pilot-learnings.md`.
5. Update `docs/customers/pilot-learnings.md` with the month's synthesis (per-segment notes + any cross-segment patterns identified in step 4).

---

## Export formats — the shared schema

To keep Claude and Perplexity interoperable with GitHub, both must export
**issue-shaped** outputs when proposing new signals, bets, or decisions.

### Minimum signal export

```yaml
type: signal
domain: routing | matching | ordering | customer | driver | collector | infra
segment: transporter | builder | homeowner | internal
impact: high | medium | low
source: "Notion page title" or "Perplexity thread title"
quote: "Direct customer quote."
interpretation: "One-line interpretation."
```

### Minimum decision export

```yaml
type: decision
domain: <as above>
learning: hypothesis | validated | invalidated
title: "Short imperative title"
context: "What forced this decision now?"
choice: "What we are going to do."
alternatives_rejected:
  - "Option A — why not"
  - "Option B — why not"
kill_or_revisit_trigger: "What would change our mind?"
source: "<Notion / Perplexity reference>"
```

Both formats map 1:1 onto the corresponding `.github/ISSUE_TEMPLATE/*.yml`.
A human pastes the YAML into a new issue and fills in any missing fields.

---

## The forbidden-words and tone filter

Outputs from Perplexity and Claude that land in this repo must pass the same
filter Perplexity already applies to strategy work:

- **No:** disrupt, revolutionary, game-changer, transformative, cutting-edge,
  unprecedented, seamless, synergy.
- **Tone:** humble, factual, peer-to-peer. Honest about what WASTR cannot yet
  do.
- **Sustainability claims:** concrete numbers (CO₂ per trip, % recycled,
  km saved). No generic eco-language.

If an AI-generated draft contains forbidden words, the human committing it is
responsible for rewriting before merge.

---

## Language

- Default: English for all repo content.
- Norwegian: only inside direct quotes from Innovasjon Norge, customers, or
  industry sources.
- Always write *Innovasjon Norge* in full in English contexts. *IN* is fine
  only inside Norwegian-language threads.

---

## Sensitive content

Anonymise customer names in `[SIGNAL]` issues unless the customer has
explicitly approved being named. Truly confidential material (financials,
legal, personal data) does not belong in this repo at all — it lives in
the CEO's private Notion or a separate IR channel.

---

## Open questions

- First automation target — GitHub Actions, n8n, or a small custom service?
  *(decision pending; track as a `[DECISION]` issue once first automation is
  needed)*
- Do we want a Slack / email digest of new `[SIGNAL]` issues for the founder
  who didn't file them? *(low priority while the team is two people)*

---

*See also: [sync-contract.md](sync-contract.md) and [ownership.md](ownership.md).*
