# Sync Contract

> **Where each kind of artifact lives, who edits it, and how it gets promoted.**
>
> This contract exists to prevent the single biggest failure mode of a multi-tool
> setup: the same idea drifting across Notion, Perplexity, and GitHub with no
> agreed canonical version.

---

## The four tools, in one line each

| Tool | Role | Owner | Canonical for… |
|---|---|---|---|
| **GitHub** (this repo + code repos) | Source of truth, versioned, AI-readable | CTO (steward) | Approved strategy, decisions, ADRs, issues, code |
| **Notion** | Drafts, meeting notes, customer notes-in-progress | CEO (steward) | Live working drafts, agendas, CRM-style customer logs |
| **Perplexity** | Strategy analysis & research scratchpad | CEO | Nothing canonical — outputs flow into GitHub or Notion |
| **Claude / Copilot** | Code generation & repo edits | CTO | Nothing canonical — outputs flow into GitHub via PRs |

**One rule above all:** if an artifact has a canonical home in GitHub, that is
the version everyone references. Notion and Perplexity are upstream of GitHub,
never parallel to it.

---

## Canonical location per artifact type

| Artifact | Drafted in | Promoted to (canonical) | Trigger for promotion |
|---|---|---|---|
| Customer interview raw notes | Notion | `[SIGNAL]` issue (GitHub) | Within 48 h of interview |
| Recurring customer pattern | Notion | `docs/customers/objections-and-signals.md` | Monthly review |
| Pilot synthesis | Notion | `docs/customers/pilot-learnings.md` | Monthly review |
| Product hypothesis | Anywhere | `[BET]` issue (GitHub) | Before any build effort |
| Feature spec | Anywhere | `[SPEC]` issue (GitHub) | Before code is written |
| Experiment design | Anywhere | `[EXP]` issue (GitHub) | Before experiment starts |
| Strategy analysis (Perplexity) | Perplexity | `docs/strategy/*.md` *or* `[DECISION]` issue | When CEO + CTO agree it's a decision, not a draft |
| Architectural decision | Anywhere | ADR in `docs/architecture/adr/` + `[DECISION]` issue | At the moment of commitment |
| Roadmap | Anywhere | `docs/strategy/roadmap-now-next-later.md` | Updated at monthly review |
| Confirmed learning | `[EXP]` outcome | `docs/knowledge/confirmed-learnings.md` | Monthly review (promotion vote) |
| Weekly review | GitHub directly | `[WEEKLY]` issue | Every Friday |
| Investor update | Notion | Not in this repo — separate IR channel | Monthly |
| Application text (Innovasjon Norge, Antler) | Dedicated Perplexity space | Not in this repo — owned by CEO | n/a |

---

## Promotion rules

1. **Drafts stay in Notion or Perplexity until they earn their place in GitHub.**
   Earning means: at least one of CEO or CTO has read it and agrees it represents
   a decision, a hypothesis, or a confirmed fact — not a half-formed thought.

2. **When promoting, link back.** A `[DECISION]` issue or a `docs/` file that
   originated in Notion or Perplexity should reference the source (Notion page
   URL or Perplexity thread title) in its footer. This preserves the
   "why did we think this?" trail.

3. **Once promoted, the GitHub version wins.** The Notion or Perplexity draft
   becomes historical context. If new edits are needed, they are made in GitHub
   and (optionally) reflected back into Notion for visibility — never the
   reverse.

4. **Re-promotion is allowed.** If GitHub canonical conflicts with a newer
   draft, open a `[DECISION]` issue to reconcile. Do not silently overwrite.

---

## Anti-duplication rules

- **Strategy documents live in exactly one place: `docs/strategy/`.** Notion may
  hold draft versions in flight; once merged, the Notion page is archived or
  reduced to a pointer.
- **Customer signals are filed as GitHub issues, not Notion pages.** Interview
  notes can start in Notion, but the *signal* (quote + interpretation + labels)
  belongs in a `[SIGNAL]` issue within 48 hours.
- **Decisions are never made in Perplexity threads.** Perplexity can help
  analyze; the decision itself is a `[DECISION]` issue with a written rationale.
- **AI outputs are not canonical until a human commits them.** A Claude
  suggestion or a Perplexity analysis becomes truth only when committed by an
  owner into the appropriate GitHub artifact.

---

## What this contract is not

- It is not a tool ban. Notion and Perplexity remain in active daily use —
  they are where messy thinking happens. The contract only governs the moment
  thinking crystallises into a fact, a decision, or a plan.
- It is not a process for code. Code lives in the Wastr service / app repos
  and cross-links back here via the PR template. This repo holds the *thinking*
  layer, not the build artifacts.
- It is not a substitute for the weekly and monthly rituals. The rituals are
  when promotions happen in bulk; the contract just defines the destination.

---

## Open questions

- Should we add a `notion-archive/` folder for snapshots of promoted Notion
  pages, or trust Notion's own page history? *(default: trust Notion until
  proven otherwise)*
- Do we need a lightweight Notion → GitHub issue bridge (manual copy works at
  current volume; tooling worth revisiting at ~50 signals / month)?

---

*See also: [tooling-protocol.md](tooling-protocol.md) for the concrete
"who-does-what-in-which-tool" workflows, and [ownership.md](ownership.md) for
the file-level owner map.*
