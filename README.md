# WASTR Intelligence Loop

> **The closed-loop, self-learning operating system of WASTR.**
>
> A single source of truth where every customer signal, product bet, experiment, decision, bug, and outcome is captured as a structured GitHub issue — so the company gets measurably smarter with every cycle, and so AI agents can eventually reason over our full institutional memory.

---

## Why this repo exists

WASTR is being built as an **AI-native startup**. That is not a marketing phrase — it is an operating principle. For AI to take on real decisions (route suggestions, pricing, matching, customer comms), it needs three things we do not yet have at scale:

1. **A complete record of what happened** — every event, decision, and outcome.
2. **A structured format** — labels, fields, and links, not free-text in Slack or Notion.
3. **A feedback loop** — a way for outcomes to update the system's beliefs over time.

This repository is that record, that structure, and that loop. It is the **intelligence layer** of the company, separate from any individual service.

> If a future Denis or Siarhei is hit by a bus, the company's *thinking* survives in this repo. If a future AI agent is asked "why did we pivot away from per-pallet pricing in Q3?", the answer is here, linked to the signals that caused it.

---

## The loop, in one picture

```
        ┌────────────────────────────────────────────┐
        │  1. SIGNALS                                │
        │  Raw observations from the real world      │
        │  (interviews, pilots, support, analytics)  │
        └──────────────────┬─────────────────────────┘
                           │  cluster + interpret
                           ▼
        ┌────────────────────────────────────────────┐
        │  2. BETS                                   │
        │  Hypotheses with success + kill criteria   │
        └──────────────────┬─────────────────────────┘
                           │  design test
                           ▼
        ┌────────────────────────────────────────────┐
        │  3. EXPERIMENTS                            │
        │  Structured tests, measurable outcomes     │
        └──────────────────┬─────────────────────────┘
                           │  ship + measure
                           ▼
        ┌────────────────────────────────────────────┐
        │  4. OUTCOMES                               │
        │  Validated / invalidated / inconclusive    │
        └──────────────────┬─────────────────────────┘
                           │  weekly + monthly review
                           ▼
        ┌────────────────────────────────────────────┐
        │  5. SYNTHESIS                              │
        │  Confirmed learnings → /docs/knowledge     │
        │  Roadmap updated → /docs/strategy          │
        │  Decisions logged → /docs/architecture     │
        └──────────────────┬─────────────────────────┘
                           │
                           ▼
                     (next cycle)
```

**Issues** are raw events — high volume, structured, machine-readable.
**`/docs`** is synthesis — low volume, narrative, human-readable.

That separation is deliberate: issues are training data, docs are the model's "weights."

---

## How this is different from a Notion / Confluence / Jira combo

| Concern | Traditional setup | This repo |
|---|---|---|
| Source of truth | Scattered (Slack, Notion, Jira, Drive) | One repo, one project board |
| Structure | Free-text pages, ad-hoc tags | Typed issue templates, controlled label taxonomy |
| Searchability | Full-text, fragile | Label + field queries, GitHub API, future MCP |
| AI-readability | Poor (mixed formats) | High (issues = JSON-shaped events) |
| Change history | Notion page history | Git commit history on every doc |
| Linkage to code | Manual | Every PR in every Wastr repo references back here |
| Cost | $$ per seat per tool | Free (GitHub) |

---

## Repository layout

```
wastr-learning-loop/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── 01_customer_signal.yml      raw field observations
│   │   ├── 02_product_bet.yml          hypothesis + kill criteria
│   │   ├── 03_feature_spec.yml         lightweight spec linked to a bet
│   │   ├── 04_bug_or_friction.yml      production issues + root cause
│   │   ├── 05_experiment.yml           structured tests with results
│   │   ├── 06_decision_log.yml         ADR-style, with revisit triggers
│   │   └── 07_weekly_review.yml        weekly outcome snapshot
│   └── pull_request_template.md        forces every PR to link back to the loop
│
├── docs/
│   ├── strategy/
│   │   ├── north-star.md                       the one sentence that aligns us
│   │   ├── product-thesis.md                   why this problem, why us, why now
│   │   ├── roadmap-now-next-later.md           rolling, opinion-driven roadmap
│   │   └── decision-log.md                     index of all [DECISION] issues
│   │
│   ├── customers/
│   │   ├── pilot-learnings.md                  synthesis across signals
│   │   └── objections-and-signals.md           recurring patterns
│   │
│   ├── rituals/
│   │   ├── weekly-review-template.md           how we run Friday reviews
│   │   └── monthly-product-review-template.md  how we run monthly reviews
│   │
│   ├── metrics/
│   │   └── definitions.md                      canonical metric definitions
│   │
│   ├── knowledge/
│   │   ├── confirmed-learnings.md              promoted insights (facts)
│   │   └── revisit-queue.md                    insights now in doubt
│   │
│   └── architecture/
│       └── adr/                                Architecture Decision Records
│
└── README.md                                   you are here
```

---

## The issue templates (the heart of the system)

Every event in the company has a home. No event is allowed to live only in Slack or someone's head.

| # | Template | When to use it | Default labels |
|---|---|---|---|
| 01 | **Customer Signal** | A user said / did / showed us something. Quote them directly. | `type: signal` |
| 02 | **Product Bet** | We're about to commit effort based on a hypothesis. | `type: decision`, `learning: hypothesis` |
| 03 | **Feature Spec** | We're building something concrete. | `type: feature`, `learning: hypothesis` |
| 04 | **Bug or Friction** | Something broke or felt wrong in production. | `type: bug` |
| 05 | **Experiment** | We're running a structured test of a bet. | `type: experiment`, `learning: hypothesis` |
| 06 | **Decision Log** | We made a non-trivial architectural / product / operational choice. | `type: decision` |
| 07 | **Weekly Review** | End of week — what shipped, what we learned, what's next. | `type: outcome` |

Each template forces the **important fields** to be filled in — e.g. a Product Bet must declare its **kill criteria** before it can be filed. This is how we prevent zombie projects.

---

## Label taxonomy (25 labels, 5 groups)

Labels are typed and disciplined. They let us slice the entire company history by question.

> **Workflow status lives in the GitHub Project, not in labels.**
> The Project `Status` field (`Ideas / Todo / In Progress / Test / Done`) is the
> single source of truth for *where in the pipeline* an item is, and it updates
> automatically when issues are closed. Labels carry the *epistemic* dimension
> only — what does the evidence say about the claim?

| Group | Color | Labels | What it answers |
|---|---|---|---|
| **type:** | 🔵 blue | signal · decision · experiment · outcome · bug · feature | *What kind of event is this?* |
| **domain:** | 🟣 purple | ordering · matching · routing · customer · driver · collector · infra | *Which part of the system?* |
| **impact:** | 🟠 orange | high · medium · low | *How much does this matter?* |
| **learning:** | 🟢 green | hypothesis · validated · invalidated · confirmed · new-insight · revisit | *What does the evidence say about this claim?* |
| **segment:** | 🟦 teal | transporter · builder · internal | *Whose problem is this?* |

Example queries this enables:

- *"Show me every invalidated bet in the routing domain in the last 90 days."*
  → `is:issue label:"type: decision" label:"learning: invalidated" label:"domain: routing"`
- *"What new insights did our builder pilot generate?"*
  → `label:"learning: new-insight" label:"segment: builder"`
- *"What high-impact bugs are still open?"*
  → `is:open label:"type: bug" label:"impact: high"`

When AI agents are later wired in (via MCP), these are the queries they will reason over.

---

## The closed loop — a worked example

Let's trace one realistic scenario from raw signal to shipped feature, end-to-end.

1. **Signal (`#42`)** — Pilot transporter Ola says in an interview:
   > "I drive empty back from Drammen twice a week and I never know if anyone needs a pickup on that route."

   → opens `[SIGNAL]` issue, labels `domain: routing`, `segment: transporter`, `impact: high`.

2. **Bet (`#51`, links `#42`)** — Team forms a hypothesis:
   > *"We believe that surfacing potential return-load orders to transporters mid-route will reduce empty-running by ≥15% for pilot transporters within 30 days."*

   Kill criterion: if <5% reduction after 30 days, we kill the feature.

3. **Spec (`#58`, links `#51`)** — Lightweight feature spec for the "return load suggestion" UI in the Driver app.

4. **Experiment (`#63`, links `#51`)** — Pilot with 3 transporters for 4 weeks. Metric: empty-run % per driver per week.

5. **Implementation PRs** in `Wastr.Apps.Web.Driver` and `Wastr.Services.Matching` — each PR's body links back to `#58` and `#63` via the PR template.

6. **Outcome (`#71`)** — Result: 22% reduction in empty-running. Bet validated.

7. **Synthesis** — At the monthly review, this learning is promoted to `docs/knowledge/confirmed-learnings.md`. Roadmap in `docs/strategy/roadmap-now-next-later.md` moves the feature from "Next" to "Now" for full rollout.

8. **Decision (`#74`)** — `[DECISION]` issue: *"Return-load suggestion becomes a core capability of the matching service."* ADR added under `docs/architecture/adr/`.

Every step is captured, linked, labelled, and searchable. A new team member — or a future AI agent — can read this chain end-to-end in minutes.

---

## How Claude, Perplexity, Notion, and GitHub interact

WASTR runs on four tools, not one. The risk in a multi-tool setup is the same
idea drifting across systems with no agreed canonical version. Three short
documents define how the tools fit together:

- [docs/sync-contract.md](docs/sync-contract.md) — what lives where, and how a
  draft gets promoted to canonical.
- [docs/tooling-protocol.md](docs/tooling-protocol.md) — concrete workflows
  (interviews, strategy analysis, code changes, weekly / monthly reviews).
- [docs/ownership.md](docs/ownership.md) — file-by-file owner map.

In one picture:

```
   Notion                Perplexity              Claude / Copilot
   (drafts,              (strategy &             (code generation,
    meeting notes,        research               repo edits)
    customer logs)        scratchpad)
       │                     │                          │
       │  draft              │  Learning Log            │  PR
       ▼                     ▼                          ▼
   ┌─────────────────────────────────────────────────────────┐
   │                       GitHub                            │
   │  wastr-learning-loop  ──  issues + /docs (canonical)    │
   │  Wastr.Services.*     ──  production code               │
   │  Wastr.Apps.*         ──  production code               │
   │   PR template links every code change back to the loop  │
   └─────────────────────────────────────────────────────────┘
```

Notion and Perplexity are **upstream** of GitHub, never parallel to it. Once
something is promoted into this repo, the GitHub version is the version
everyone references.

---

## How PRs in *other* Wastr repos close the loop

The mechanism that keeps the loop genuinely closed (not just decorative) is the **pull request template**, which we will roll out across every Wastr repo:

- `Wastr.Services.Ordering`
- `Wastr.Services.Matching`
- `Wastr.Services.Driver`
- `Wastr.Services.Collector`
- `Wastr.Services.User`
- `Wastr.Services.Product`
- `Wastr.Services.Geolocation`
- `Wastr.Services.Notification`
- `Wastr.Apps.Web.Customer`
- `Wastr.Apps.Web.Driver`
- `Wastr.Apps.Web.Collector`
- `Wastr.Apps.Web.Admin`
- `global-infra`

Every PR is required to:

1. **Link back** to at least one issue in `wastr-learning-loop` (signal, bet, spec, experiment, decision).
2. **Declare what was learned** in the build process.
3. **Confirm** that the linked issue has been updated with the outcome.

This makes the codebase a *citation* of the intelligence layer, not an independent artifact.

---

## Rituals — how the loop turns

| Cadence | Ritual | Output | Guide |
|---|---|---|---|
| **Friday, 30 min** | Weekly review | one `[WEEKLY]` issue | [docs/rituals/weekly-review-template.md](docs/rituals/weekly-review-template.md) |
| **Last Friday of month, 90 min** | Monthly product review | updated `pilot-learnings.md`, updated `roadmap-now-next-later.md`, any new `[DECISION]` issues | [docs/rituals/monthly-product-review-template.md](docs/rituals/monthly-product-review-template.md) |
| **Continuous** | File signals as they happen | `[SIGNAL]` issues | template `01_customer_signal` |
| **As needed** | Decision log | `[DECISION]` issue + ADR file | template `06_decision_log` |

Rituals are short on purpose. The system only works if the team actually does them — so they are designed to be cheaper than skipping.

---

## The GitHub Project — "WASTR Intelligence Loop"

All issues are added to a single project board: [`WASTR Intelligence Loop`](https://github.com/orgs/wastr-as/projects/3).

Recommended views (to be configured):

| View | Filter | Purpose |
|---|---|---|
| **Signal stream** | `type: signal`, sorted by date | Raw firehose of customer reality |
| **Active bets** | `type: decision` + `learning: hypothesis` | What are we currently betting on? |
| **Running experiments** | `type: experiment` + Project `Status = In Progress` | What are we measuring? |
| **Recent learnings** | `learning: new-insight`, last 30 days | What did we just learn? |
| **Revisit queue** | `learning: revisit` | What do we owe ourselves a re-look on? |
| **Shipped this quarter** | Project `Status = Done`, closed this quarter | Public-facing progress |

---

## The path to AI-native operations

This repo is intentionally designed so that, in 6–12 months, an AI agent can:

1. **Query the loop** — *"show me every invalidated bet about pricing in the last year and the signals that triggered them."* (already possible today via GitHub API.)
2. **Propose new bets** — given recent signals, the agent suggests hypotheses with kill criteria, written as draft `[BET]` issues. (next step: MCP server over this repo.)
3. **Detect contradictions** — when a new signal contradicts a `confirmed-learning`, the agent files it automatically into the `revisit-queue`.
4. **Pre-fill weekly reviews** — agent drafts the `[WEEKLY]` issue with metrics, shipped PRs, and clustered signals. Humans only approve and add interpretation.
5. **Run autopilot experiments** — for low-risk feature flags, the agent proposes A/B splits, monitors metrics, and files the `[EXP]` outcome.

We don't need any of this on day one. We need the **substrate** — structured, labelled, linked events — to make it possible. That substrate is what this repo is.

---

## How to start using it (today)

If you have 30 minutes:

1. **Fill in** [docs/strategy/north-star.md](docs/strategy/north-star.md) — the one sentence that aligns every later decision.
2. **File 3 `[SIGNAL]` issues** from recent pilot conversations.
3. **File 1 `[BET]` issue** for the most important thing the team is currently building.
4. **Run this Friday's weekly review** using the template — even a 10-minute version.

That alone seeds the loop. Everything else compounds from there.

---

## Frequently asked questions

**Q: Isn't this overhead?**
For a 2–3 person team, yes — for two weeks. After that, the time spent on issues is recovered 5× by not re-explaining context, not re-litigating decisions, and not re-discovering invalidated bets. And the asset compounds — by month 6 it is a hiring tool, a fundraising tool, and an AI training set.

**Q: Why not just use Notion / Linear / Jira?**
Three reasons: (1) GitHub is where the code already lives, so PR-to-issue linkage is native; (2) GitHub's API is the best-supported source for AI agents and MCP servers; (3) free.

**Q: What if we change tools later?**
Issues and markdown are portable. The label taxonomy and ritual structure work in any tool. The substrate survives a tool migration.

**Q: Is this public?**
The repo is public so the team, advisors, and (selectively) investors can read along. Sensitive customer names should be anonymised at the time of filing. Anything truly confidential (legal, financial, personal data) does not belong in issues.

---

## Contact / owners

- **CEO / product:** Denis Pozhinsky
- **CTO / architecture:** Siarhei Karabitski
- **This repo's steward:** rotates with whoever runs the weekly review

---

*This is a living system. If the loop is not working, file a `[SIGNAL]` about the loop itself, and we'll iterate.*
