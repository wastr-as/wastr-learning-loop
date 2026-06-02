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
        ┌─────────────────────────────────────────────────┐
        │  1. SIGNALS                                     │
        │  Raw observations from the real world           │
        │  (interviews, pilots, support, analytics)       │
        │  → [SIGNAL] issue, type:signal                  │
        └────────────────────┬────────────────────────────┘
                             │  cluster + interpret (weekly)
                             ▼
        ┌─────────────────────────────────────────────────┐
        │  2. BETS                                        │
        │  Hypotheses with success + kill criteria        │
        │  → [BET] issue, type:decision,                  │
        │    learning:hypothesis                          │
        └────────────────────┬────────────────────────────┘
                             │  design test
                             ▼
        ┌─────────────────────────────────────────────────┐
        │  3. EXPERIMENTS                                 │
        │  Structured tests with a measurable metric      │
        │  → [EXP] issue, type:experiment,                │
        │    learning:hypothesis                          │
        └────────────────────┬────────────────────────────┘
                             │  ship + measure
                             ▼
        ┌─────────────────────────────────────────────────┐
        │  4. CLOSURE                                     │
        │  Close the [EXP] / [BET] with a summary         │
        │  comment + swap learning:hypothesis for         │
        │  learning:confirmed | validated | invalidated   │
        │  | new-insight. No new "outcome" issue.         │
        └────────────────────┬────────────────────────────┘
                             │  monthly review
                             ▼
        ┌─────────────────────────────────────────────────┐
        │  5. SYNTHESIS                                   │
        │  Confirmed learning  → docs/knowledge/          │
        │  Roadmap delta       → docs/strategy/           │
        │  Architectural call  → docs/architecture/adr/   │
        │  Non-arch commitment → [DECISION] issue         │
        │  Re-look obligation  → docs/revisit-queue.md    │
        └────────────────────┬────────────────────────────┘
                             │
                             ▼
                       (next cycle)
```

Two governance rules embedded in the loop:

- **Workflow status (Ideas / Todo / In Progress / Test / Done)** lives in the GitHub Project `Status` field — never in a label. It auto-updates on issue close.
- **Each concept has one canonical home.** Outcomes are issue closures (not new issues). Decisions are ADRs *or* `[DECISION]` issues (never both). Revisit work is the doc (not a Project view).

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

> **Outcomes are not their own issue type.** When an experiment or bet concludes, close the existing issue with a summary comment and swap `learning: hypothesis` for `learning: confirmed` / `validated` / `invalidated` / `new-insight`. The close comment *is* the outcome record. The `type: outcome` label is reserved exclusively for **Weekly Review** snapshots (template 07).

### Decision records: ADR vs `[DECISION]` issue

Each decision has exactly **one** canonical home. Never both.

| Decision type | Canonical home | Why |
|---|---|---|
| **Architectural / technical** — changes how code is structured, what services exist, what protocols we speak | **ADR** under `docs/architecture/adr/` | Engineers need to find it in 2 years while reading code. Numbered, stable URL, browsable as a sequence. |
| **Product / commercial / operational** — no code structure impact (pricing, vendor choice, hiring model, partner strategy) | **`[DECISION]` issue** (template 06) | Lives where the bets and signals that produced it live. Closeable, commentable, linkable from non-engineering work. |
| **Architectural AND broad org impact** | **ADR is canonical, `[DECISION]` issue is a pointer** (optional) | The ADR has the substance; the issue exists only if non-engineers also need to find the decision. The issue body says "See ADR-NNNN" and nothing else. |

Default is **one or the other, not both.** "Both" is a rare special case.

When to skip both entirely: a closed `[BET]` with a clear outcome comment *is* the decision to keep going — don't double-record.

### HOWTO: `[BET]` vs `[EXPERIMENT]` — both carry `learning: hypothesis`, so which do I file?

This is the most-confused pair, because both are open claims about the future. The difference is **scope and shape of the claim.**

| Aspect | `[BET]` (`type: decision` + `learning: hypothesis`) | `[EXPERIMENT]` (`type: experiment` + `learning: hypothesis`) |
|---|---|---|
| **What it is** | A *strategic commitment* — "we are going to invest effort in X because we believe Y." | A *tactical, structured test* of one falsifiable claim. |
| **Granularity** | Broad. *"Return-load suggestions will reduce empty-running."* | Narrow. *"4-week Drammen pilot with 3 transporters: empty-run % per driver per week drops ≥15%."* |
| **Time scale** | Weeks–quarters. Outlives any single experiment. | Days–weeks. Has a hard end date. |
| **Metric** | Optional headline metric, often qualitative ("transporters adopt this"). | **Required.** One number, one threshold, defined up front. |
| **Spawns** | Typically 1–N experiments + maybe specs and decisions. | Usually nothing — it produces evidence that updates its parent bet. |
| **Closure** | Closes when the underlying belief is resolved (via the experiments it spawned). | Closes on the planned end date, with the metric result. |
| **Killable mid-flight?** | Yes — if early experiments invalidate, kill the bet before more is spent. | Almost never — you let it run to its planned end so the data is comparable. |

**Use `[BET]` when** you're making a multi-week direction call — you want to *commit and signal* that the team is going this way, even before you know exactly which experiments will prove it. A bet is the *parent* container for a thesis.

**Use `[EXPERIMENT]` when** you have a single, sharp, falsifiable claim with a metric and a time-box. An experiment is *the act of measuring*.

**The parent/child relationship:**

```
[BET]  Return-load suggestions reduce empty-running     (strategic claim, 1 quarter)
  ├── [EXPERIMENT]  Drammen 4-week pilot, 3 transporters  (one measurement)
  ├── [EXPERIMENT]  Oslo 8-week pilot, 8 transporters     (replication at scale)
  └── [SPEC]        Driver-app UI for return-load card    (the build to support both)
```

The bet doesn't have a metric of its own — its outcome is the *sum* of its experiments. If Drammen validates AND Oslo validates → bet `learning: validated`. If Drammen invalidates → kill the bet without running Oslo, mark `learning: invalidated`.

**Anti-patterns:**

- **Filing a bet as an experiment** — *"Pilot Customer App in Brazil"* as a single `[EXPERIMENT]`. It's actually a bet ("we believe the core flow generalises across markets") that should spawn experiments (Brazil pilot, then market #2). Look at #30 — backfilled as an experiment, but the *real* hypothesis ("the product is geography-agnostic") is a bet that lasts beyond one pilot.
- **Filing an experiment as a bet** — *"Run a 4-week A/B test on button copy"* as a `[BET]`. It's not a strategic commitment, it's a measurement. Use `[EXPERIMENT]`.
- **Filing a hypothesis without either** — typing "we should try this" into a `[DECISION]` issue. If it's not settled, it's a bet or an experiment, not a decision.

**Quick rule of thumb:**

> If the claim takes longer than a single test to resolve → `[BET]`.
> If the claim is *"one test will tell us"* → `[EXPERIMENT]`.
> A bet without at least one experiment to back it up is an opinion. Add the experiment or downgrade the bet.

### The four `learning:` outcome labels

When you close an experiment, bet, or signal, you apply one of four `learning:` outcome labels. The mechanism differs slightly by issue type:

- **`[BET]` / `[SPEC]` / `[EXP]`** — start their life with `learning: hypothesis`. On close, **swap** `learning: hypothesis` for one of the outcome labels below.
- **`[SIGNAL]`** — starts with no `learning:` label (just `type: signal`). On close, **add** one of the outcome labels below.
- **`[BUG]` / `[DECISION]` / `[WEEKLY]`** — don't use `learning:` labels at all. Bugs are fixed or won't-fix; decisions are made; weekly reviews are snapshots.

The four labels are **not synonyms** — pick the one that matches what actually happened.

| Label | Means | Use when |
|---|---|---|
| **`learning: validated`** | The bet's success criterion was met. | A `[BET]` / `[EXP]` / `[SPEC]` finished with the metric hitting target. Mechanical: "we predicted ≥15% reduction, we got 22%." Never used on signals. |
| **`learning: invalidated`** | The bet's kill criterion was hit, OR a signal turned out to be noise. | A `[BET]` / `[EXP]` missed target by enough that we agreed up-front we'd stop. Or a `[SIGNAL]` we couldn't reproduce / wasn't real. |
| **`learning: confirmed`** | A belief we already held was reinforced by new evidence. | A `[SIGNAL]` that confirms the existing thesis without changing it ("yes, 3 more transporters said the same thing"). Never used on bets. |
| **`learning: new-insight`** | We learned something we didn't predict. | A `[BET]` / `[EXP]` where the *interesting* finding wasn't the headline metric, OR a `[SIGNAL]` that tells us something new about the world. |

**Decision tree:**

```
What type of issue is closing?
├── [BET] / [SPEC] / [EXP]  (started with learning: hypothesis)
│   │  swap learning: hypothesis for:
│   ├── Metric ≥ success threshold  →  learning: validated
│   ├── Metric ≤ kill threshold     →  learning: invalidated
│   ├── Unexpected dominant finding →  learning: new-insight
│   └── In between (inconclusive)   →  keep learning: hypothesis,
│                                       run longer or kill as invalidated
│
└── [SIGNAL]  (started with no learning: label)
    │  add one of:
    ├── Reinforces existing thesis        →  learning: confirmed
    ├── Tells us something new            →  learning: new-insight
    └── Noise / couldn't reproduce        →  learning: invalidated
```

**Two distinctions that matter:**

- **`validated` vs `confirmed`** — `validated` is for *bets/experiments* (a prediction was tested and was right). `confirmed` is for *signals/beliefs* (no formal prediction, just more evidence stacking up). A `[BET]` should never end as `confirmed` — if you wrote a bet, you committed to a measurable claim.
- **`validated` vs `new-insight`** — these can co-exist on the same issue. If the experiment hit its target AND surfaced something surprising, use `validated` (primary outcome) and write the surprise in the close comment. Only use `new-insight` *instead* of `validated` if the surprise is more important than the headline metric.

**No `inconclusive` label exists by design.** If a bet is inconclusive after its planned duration, either extend it (keep `learning: hypothesis`, update end date) or close it as `learning: invalidated` with a comment ("ran for X weeks, signal too weak to justify continued investment"). Inconclusive results that go nowhere *are* invalidations of the bet, even if not of the underlying belief.

**Anti-patterns:**

- Closing every shipped feature as `validated`. Shipping ≠ validating. Validation requires the metric to move.
- Using `confirmed` on bets. If it was a bet, it's `validated` or `invalidated`.
- Stacking multiple outcome labels "just in case." Pick the dominant one; the close comment carries nuance.
- Avoiding `invalidated` because it feels like failure. It's the most valuable outcome — it stops you wasting more effort.

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
| **type:** | 🔵 blue | signal · decision · experiment · outcome¹ · bug · feature | *What kind of event is this?* |
| **domain:** | 🟣 purple | ordering · matching · routing · customer · driver · collector · infra | *Which part of the system?* |
| **impact:** | 🟠 orange | high · medium · low | *How much does this matter?* |
| **learning:** | 🟢 green | hypothesis · validated · invalidated · confirmed · new-insight · revisit | *What does the evidence say about this claim?* |
| **segment:** | 🟦 teal | transporter · builder · internal | *Whose problem is this?* |

¹ `type: outcome` is only used by Weekly Review issues (template 07). Individual experiment/bet results live as close comments + `learning:` label swaps on the original issue — never as a new "outcome" issue.

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

6. **Experiment closure** — `[EXP] #63` is closed with a comment summarising the result: *"22% reduction in empty-running over 4 weeks across 3 transporters. Bet validated."* The `learning: hypothesis` label is swapped for `learning: confirmed`. **No new issue is created for the outcome** — the close comment on the experiment is the outcome.

7. **Synthesis** — At the monthly review, this learning is promoted to `docs/knowledge/confirmed-learnings.md`. Roadmap in `docs/strategy/roadmap-now-next-later.md` moves the feature from "Next" to "Now" for full rollout.

8. **Architectural commitment** — Because this changes what the matching service does, an ADR is written: `ADR-NNNN: Return-load suggestion as a core capability of the matching service`. The ADR links back to `[BET] #51` and `[EXP] #63` as evidence. **No separate `[DECISION]` issue** — the ADR is the decision record.

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
| **Shipped this quarter** | Project `Status = Done`, closed this quarter | Public-facing progress |

> Revisit work is tracked in [`docs/revisit-queue.md`](docs/revisit-queue.md) — a scheduled review surface, not a daily project view. One source per concept.

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
