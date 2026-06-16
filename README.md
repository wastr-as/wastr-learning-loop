# WASTR Intelligence Loop

> **The closed-loop, self-learning operating system of WASTR.**
>
> A single source of truth where every customer signal, product bet, experiment, decision, bug, and outcome is captured as a structured GitHub issue — so the company gets measurably smarter with every cycle, and so AI agents can eventually reason over our full institutional memory.

---

## Contents

| Section | What's in it | When to read |
|---|---|---|
| **[Why this repo exists](#why-this-repo-exists)** + **[How this differs from Notion / Jira / Linear](#how-this-is-different-from-notion--jira--linear)** | The case for the loop and what it replaces. | Once, to buy the premise. |
| **[The mental model](#the-mental-model)** | Vocabulary, loop diagram, worked example. | Once, end-to-end. After this you understand the system. |
| **[Reference — when filing or closing issues](#reference--when-filing-or-closing-issues)** | Issue templates, ADR vs `[DECISION]`, hypothesis rules, `[BET]` vs `[EXPERIMENT]`, the four `learning:` outcomes, contradicted learnings, repo layout. | Look up while filing or closing issues. |
| **[Operating the system](#operating-the-system)** | Rituals, project views, PR template, multi-tool integration. | Before your first weekly review and your first cross-repo PR. |
| **[How to start using it (today)](#how-to-start-using-it-today)** · **[Path to AI-native ops](#the-path-to-ai-native-operations)** · **[FAQ](#faq)** · **[Contact](#contact--owners)** | Onboarding checklist, roadmap, common objections. | Optional. |

---

## Why this repo exists

WASTR is being built as an **AI-native startup**. That is not a marketing phrase — it is an operating principle. For AI to take on real decisions (route suggestions, pricing, matching, customer comms), it needs three things we do not yet have at scale:

1. **A complete record of what happened** — every event, decision, and outcome.
2. **A structured format** — labels, fields, and links, not free-text in Slack or Notion.
3. **A feedback loop** — a way for outcomes to update the system's beliefs over time.

This repository is that record, that structure, and that loop. It is the **intelligence layer** of the company, separate from any individual service.

> If a future Denis or Siarhei is hit by a bus, the company's *thinking* survives in this repo. If a future AI agent is asked "why did we pivot away from per-pallet pricing in Q3?", the answer is here, linked to the signals that caused it.

---

## How this is different from Notion / Jira / Linear

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

## The mental model

> Read these three sub-sections together — they are the system. **Vocabulary** defines the labels, the **loop diagram** shows how those labels flow through an event's life cycle, and the **worked example** shows what it looks like end-to-end on a real feature. Everything else in this document is a reference manual or an operational note on top of this.

### Vocabulary — label taxonomy (25 labels, 5 groups)

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
| **segment:** | 🟦 teal | transporter · builder · homeowner · internal | *Whose problem is this?* |
| **lane:** | 🟣 violet / 🔴 red | b2b · b2c | *Which validation track — grant-facing or internal?* |

¹ `type: outcome` is only used by Weekly Review issues (template 07). Individual experiment/bet results live as close comments + `learning:` label swaps on the original issue — never as a new "outcome" issue. `learning: revisit` is applied to a **signal** that contradicts something previously confirmed (see [synthesis step 5](#the-loop-in-one-picture) and [contradicted learnings](#when-a-confirmed-learning-gets-contradicted)).

> **`lane:` enforces the Innovasjon Norge reporting boundary.** `lane: b2b` is the grant-facing track (Iteo A1–A3 SMB validation — transporters, contractors, property managers, collectors, documentation/routing) and is the **only** lane reported to Innovasjon Norge. `lane: b2c` is the internal-only homeowner revenue/signal track; its conversion data, consumer messaging tests, and revenue are **never** reported as an IN outcome. Both lanes share one operational backbone but stay separable for clean reporting.

Example queries this enables:

- *"Show me every invalidated bet in the routing domain in the last 90 days."*
  → `is:issue label:"type: decision" label:"learning: invalidated" label:"domain: routing"`
- *"What new insights did our builder pilot generate?"*
  → `label:"learning: new-insight" label:"segment: builder"`
- *"What high-impact bugs are still open?"*
  → `is:open label:"type: bug" label:"impact: high"`
- *"What can we report to Innovasjon Norge?"* (grant-facing B2B only)
  → `is:issue label:"lane: b2b"` — and never `label:"lane: b2c"` in an IN deliverable.

When AI agents are later wired in (via MCP), these are the queries they will reason over.

### The loop, in one picture

```
        ┌─────────────────────────────────────────────────┐
        │  1. SIGNALS                                     │
        │  Raw observations from the real world           │
        │  (interviews, pilots, support, analytics,       │
        │   AND production bugs — see step 4b)            │
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
                             │  design test + build
              ┌──────────────┼──────────────┐
              ▼                             ▼
   ┌──────────────────────┐    ┌──────────────────────────┐
   │  3a. SPECS           │    │  3b. EXPERIMENTS         │
   │  The thing we build  │    │  The measurement of      │
   │  to support the bet  │◄───┤  whether the spec works  │
   │  → [SPEC] issue,     │    │  → [EXP] issue,          │
   │    type:feature,     │    │    type:experiment,      │
   │    learning:         │    │    learning:hypothesis   │
   │    hypothesis        │    │                          │
   └──────────┬───────────┘    └────────────┬─────────────┘
              │  ship                       │  measure
              └──────────────┬──────────────┘
                             ▼
        ┌─────────────────────────────────────────────────┐
        │  4a. CLOSURE                                    │
        │  Close the [EXP] / [SPEC] / [BET] with a        │
        │  summary comment + swap learning:hypothesis for │
        │  learning:validated | invalidated | new-insight │
        │  No new "outcome" issue.                        │
        └────────────────────┬────────────────────────────┘
                             │  in production, reality bites
                             ▼
        ┌─────────────────────────────────────────────────┐
        │  4b. BUGS & FRICTION                            │
        │  Something broke or felt wrong post-ship        │
        │  → [BUG] issue, type:bug                        │
        │  Fixed in code; if it reveals a pattern, file   │
        │  a new [SIGNAL] back into step 1.               │
        └────────────────────┬────────────────────────────┘
                             │  monthly review
                             ▼
        ┌─────────────────────────────────────────────────┐
        │  5. SYNTHESIS                                   │
        │  Confirmed learning  → docs/knowledge/          │
        │  Roadmap delta       → docs/strategy/           │
        │  Architectural call  → docs/architecture/adr/   │
        │  Non-arch commitment → [DECISION] issue         │
        │  Contradicted later  → reopen issue (swap        │
        │                        confirmed→hypothesis) OR  │
        │                        row in revisit-queue.md   │
        │                        if learning lives in docs │
        └────────────────────┬────────────────────────────┘
                             │
                             ▼
                       (next cycle)

        ─── orthogonal cadence ───────────────────────────
        ┌─────────────────────────────────────────────────┐
        │  WEEKLY REVIEW (Fridays)                        │
        │  A snapshot that observes the loop, not a step  │
        │  in it. Aggregates what shipped, what closed,   │
        │  what was learned, what's next.                 │
        │  → [WEEKLY] issue, type:outcome                 │
        │  (the ONLY legitimate source of type:outcome)   │
        └─────────────────────────────────────────────────┘
```

Two governance rules embedded in the loop:

- **Workflow status (Ideas / Todo / In Progress / Test / Done)** lives in the GitHub Project `Status` field — never in a label. It auto-updates on issue close.
- **Each concept has one canonical home.** Outcomes are issue closures (not new issues). Decisions are ADRs *or* `[DECISION]` issues (never both). Contradicted learnings follow the **two-layer rule**: if the learning still lives on its `learning: confirmed` issue, reopen the issue and swap the label back to `learning: hypothesis`; if the learning has been promoted into [`docs/knowledge/confirmed-learnings.md`](docs/knowledge/confirmed-learnings.md) (entries L-001, L-002, …), add a row to [`docs/knowledge/revisit-queue.md`](docs/knowledge/revisit-queue.md) and tag the contradicting `[SIGNAL]` with `learning: revisit`. See [contradicted learnings](#when-a-confirmed-learning-gets-contradicted) for the full procedure.

**Issues** are raw events — high volume, structured, machine-readable.
**`/docs`** is synthesis — low volume, narrative, human-readable.

That separation is deliberate: issues are training data, docs are the model's "weights."

---

### A worked example, end-to-end

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

## Reference — when filing or closing issues

> Don't read this front-to-back. The table below is the cheat sheet — one row per issue type, every other rule in this section is a deeper cut of one of these columns. Jump to the linked subsection only when the table isn't enough.

### Cheat sheet — one row per issue type

| Issue type | Template | Opens with labels | On close — `learning:` action | Carries a hypothesis? | Canonical decision home | Deeper cut |
|---|---|---|---|---|---|---|
| **`[SIGNAL]`** | [01](#issue-templates) | `type: signal` (no `learning:`) | **Add** `learning: confirmed` / `invalidated` / `new-insight`. If it contradicts a doc-layer learning, also **add** `learning: revisit`. | No — raw observation | — | [Outcomes](#the-four-learning-outcome-labels) · [Contradicted](#when-a-confirmed-learning-gets-contradicted) |
| **`[BET]`** | [02](#issue-templates) | `type: decision`, `learning: hypothesis` | **Swap** `hypothesis` → `validated` / `invalidated` / `new-insight` | Yes — strategic claim, multi-week | The closed `[BET]` *is* the commitment record | [BET vs EXP](#bet-vs-experiment--which-do-i-file) · [Hypothesis](#what-is-a-hypothesis) |
| **`[SPEC]`** | [03](#issue-templates) | `type: feature`, `learning: hypothesis` | **Swap** `hypothesis` → `validated` / `invalidated` / `new-insight` | Yes — implicit *"shipping this produces the intended outcome"* | — | [Hypothesis](#what-is-a-hypothesis) |
| **`[BUG]`** | [04](#issue-templates) | `type: bug` | None — bugs are fixed or won't-fix. If a pattern emerges, file a new `[SIGNAL]`. | No — fact, not claim | — | — |
| **`[EXP]`** | [05](#issue-templates) | `type: experiment`, `learning: hypothesis` | **Swap** `hypothesis` → `validated` / `invalidated` / `new-insight` | Yes — one falsifiable, time-boxed claim | — | [BET vs EXP](#bet-vs-experiment--which-do-i-file) |
| **`[DECISION]`** | [06](#issue-templates) | `type: decision` (no `learning:`) | None — decisions are made, not validated | No — choice already made | **Architectural** → ADR canonical, issue optional pointer. **Product / commercial / ops** → `[DECISION]` issue canonical. Never both. | [ADR vs DECISION](#decision-records-adr-vs-decision-issue) |
| **`[WEEKLY]`** | [07](#issue-templates) | `type: outcome` (no `learning:`) | None — snapshot. **Only** issue type allowed to carry `type: outcome`. | No — observation of the loop | — | — |

**Quick-lookup recipes:**

- *"What labels go on a fresh X?"* → **Opens with** column.
- *"I'm closing X — what do I change?"* → **On close** column.
- *"Should this be a `[BET]` or `[EXPERIMENT]`?"* → [BET vs EXP](#bet-vs-experiment--which-do-i-file).
- *"Is this an ADR or a `[DECISION]` issue?"* → [Decision records](#decision-records-adr-vs-decision-issue).
- *"A confirmed learning is now in doubt — what do I do?"* → [When a confirmed learning gets contradicted](#when-a-confirmed-learning-gets-contradicted).
- *"What's the difference between `validated` and `confirmed`?"* → [The four `learning:` outcome labels](#the-four-learning-outcome-labels).

### Issue templates

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

### What is a hypothesis?

In this repo, a **hypothesis** is a *claim about the future that the world can prove wrong.* It has three required properties:

1. **Specific** — it names a concrete change, audience, and direction. Not *"users will like this"*, but *"return-load suggestions will increase Drammen transporter weekly revenue."*
2. **Falsifiable** — there is at least one observable outcome that would force you to abandon the claim. If you can't describe what would change your mind, it's a belief, not a hypothesis.
3. **Time-bounded** — it commits to a window in which the answer should arrive. *"Within 4 weeks"*, *"by end of Q3"*, *"after 100 orders processed."* Unbounded hypotheses become zombies.

A good hypothesis follows the shape:

> **We believe** *[change]* will produce *[outcome]* for *[audience]* within *[time window]*.
> **We'll know we're right when** *[observable metric or behaviour]*.
> **We'll kill it if** *[failure threshold]*.

The `learning: hypothesis` label marks any issue that *carries* an open hypothesis — i.e. the world hasn't yet told us if the claim holds. It's the **epistemic state** of "not settled." When evidence arrives, the label is swapped for one of the outcome labels (`validated` / `invalidated` / `new-insight`).

Hypotheses **live on**:

- `[BET]` issues — the bet's hypothesis is the strategic claim driving the commitment.
- `[EXPERIMENT]` issues — the experiment's hypothesis is the falsifiable, time-boxed claim being measured.
- `[SPEC]` issues — the spec's hypothesis is the implicit *"shipping this will produce the intended outcome"*; validated when the metric moves, invalidated when it doesn't.

Hypotheses do **not live on**:

- `[DECISION]` issues — a decision is a choice that has already been made.
- `[BUG]` issues — a bug is a fact, not a claim.
- `[SIGNAL]` issues — a signal is a raw observation from the world, not a claim about the future. Signals start with no `learning:` label and *receive* one on close (`confirmed` / `invalidated` / `new-insight`) to record how the team interpreted the evidence.
- `[WEEKLY]` issues — a weekly review is a snapshot, not a claim.

### `[BET]` vs `[EXPERIMENT]` — which do I file?

This is the most-confused pair, because both carry `learning: hypothesis` and both are open claims about the future. The difference is **scope and shape of the claim.**

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

### When a confirmed learning gets contradicted

Sometimes a new signal contradicts something we had already marked `learning: confirmed`. The procedure depends on **where the confirmed learning currently lives** — there are two layers, and they use different mechanisms.

**Two-layer rule:**

| Layer | Where the learning lives | Mechanism when contradicted |
|---|---|---|
| **Issue-layer** | Still a closed GitHub issue with `learning: confirmed`, not yet promoted to docs | **Reopen the issue**, swap `learning: confirmed` → `learning: hypothesis`, cross-link the contradicting signal in a comment. The reopened issue *is* the revisit surface. |
| **Doc-layer** | Promoted into [`docs/knowledge/confirmed-learnings.md`](docs/knowledge/confirmed-learnings.md) as L-NNN (the issue is closed and superseded by the doc) | Add a row to [`docs/knowledge/revisit-queue.md`](docs/knowledge/revisit-queue.md) pointing at the L-NNN entry, AND apply `learning: revisit` to the contradicting `[SIGNAL]` issue. |

**Why two mechanisms?** Once a learning has been promoted into `confirmed-learnings.md`, the canonical home is the doc entry (L-NNN), not the original closed issue. Reopening a long-closed issue would split the source of truth. The revisit-queue row is the doc-layer equivalent of "reopen the issue".

**The `learning: revisit` label** is applied to the **contradicting signal**, not to the original learning. Query: `is:issue label:"learning: revisit"` returns every signal currently calling a confirmed belief into question. The label is the entry point; the revisit-queue row is the tracking artefact.

**Resolution at the next monthly review:**

- **Issue-layer**: walk reopened `learning: hypothesis` issues that were previously confirmed. Either re-confirm (swap back to `learning: confirmed`) or close as `learning: invalidated`.
- **Doc-layer**: walk rows in `revisit-queue.md`. Pick one: (a) amend the L-NNN entry, (b) file an `[EXP]` to settle the point empirically (keep row open until it closes), (c) move L-NNN out of `confirmed-learnings.md` entirely, or (d) close as "still true, was a one-off". On resolution, delete the row, remove `learning: revisit` from the signal, and close the signal with its proper outcome label.

**Not to be confused with ADR `Revisit Trigger` sections** — those are tripwires defined *at the time a decision is made* ("reopen this ADR if X happens"). The revisit mechanism above is reactive (a contradicting signal arrived); ADR triggers are proactive (we anticipated when to re-look). Both can coexist on the same topic.

### Repository layout

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
│   │   └── pilot-learnings.md                  synthesis across signals (incl. cross-segment patterns)
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
│   │   └── revisit-queue.md                    promoted insights now in doubt
│   │
│   └── architecture/
│       └── adr/                                Architecture Decision Records
│
└── README.md                                   you are here
```

---

## Operating the system

> How the loop runs day-to-day: when we meet, what views to use, how code changes connect back to issues, and how our tool pipeline (Notion → Perplexity → GitHub, with Claude / Copilot on the code side) fits together.

### Rituals — weekly & monthly cadence

| Cadence | Ritual | Output | Guide |
|---|---|---|---|
| **Friday, 30 min** | Weekly review | one `[WEEKLY]` issue | [docs/rituals/weekly-review-template.md](docs/rituals/weekly-review-template.md) |
| **Last Friday of month, 90 min** | Monthly product review | updated `pilot-learnings.md`, updated `roadmap-now-next-later.md`, any new `[DECISION]` issues | [docs/rituals/monthly-product-review-template.md](docs/rituals/monthly-product-review-template.md) |
| **Continuous** | File signals as they happen | `[SIGNAL]` issues | template `01_customer_signal` |
| **As needed** | Decision log | `[DECISION]` issue + ADR file | template `06_decision_log` |

Rituals are short on purpose. The system only works if the team actually does them — so they are designed to be cheaper than skipping.

### Project board & recommended views

All issues are added to a single project board: [`WASTR Intelligence Loop`](https://github.com/orgs/wastr-as/projects/3).

Recommended views (to be configured):

| View | Filter | Purpose |
|---|---|---|
| **Signal stream** | `type: signal`, sorted by date | Raw firehose of customer reality |
| **Active bets** | `type: decision` + `learning: hypothesis` | What are we currently betting on? |
| **Running experiments** | `type: experiment` + Project `Status = In Progress` | What are we measuring? |
| **Recent learnings** | `learning: new-insight`, last 30 days | What did we just learn? |
| **Shipped this quarter** | Project `Status = Done`, closed this quarter | Public-facing progress |

> Contradicted learnings use a **two-layer mechanism** — issue-layer learnings reopen their original issue, doc-layer learnings get a row in [`docs/knowledge/revisit-queue.md`](docs/knowledge/revisit-queue.md). Neither is a daily project view; both are scheduled review surfaces. See [when a confirmed learning gets contradicted](#when-a-confirmed-learning-gets-contradicted).

### PR template — how code closes the loop

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

### Multi-tool integration (Notion → Perplexity → GitHub)

The loop runs on a **pipeline**, not a set of parallel tools. Each tool has a
distinct job, and content flows in one direction toward the canonical store.
Three short documents define the contract:

- [docs/sync-contract.md](docs/sync-contract.md) — what lives where, and how
  raw capture gets refined into a canonical result.
- [docs/tooling-protocol.md](docs/tooling-protocol.md) — concrete workflows
  (interviews, strategy analysis, code changes, weekly / monthly reviews).
- [docs/ownership.md](docs/ownership.md) — file-by-file owner map.

In one picture:

```
   Notion                  Perplexity                GitHub
   (raw capture)           (synthesis engine)        (canonical record)
   meeting notes,    ───►  clusters, summarises,  ───►  issues + /docs
   interview                turns raw notes into          in this repo
   transcripts,             a structured result
   customer logs            (hypothesis, signal
                            cluster, strategy memo)
                                                          │
                                                          │  referenced by
                                                          ▼
                                              Claude / Copilot
                                              (code generation, repo edits)
                                                          │
                                                          │  PR
                                                          ▼
                                              Wastr.Services.* / Wastr.Apps.*
                                              (production code, PR template
                                               links every change back to
                                               the loop)
```

**Notion is raw input, not a parallel source of truth.** It holds the messy
artefacts of real work — meeting notes, customer call transcripts, half-formed
thoughts. Nothing in Notion is canonical.

**Perplexity is the promotion engine.** It reads the raw Notion material, asks
clarifying questions, and produces a *result*: a structured hypothesis, a
signal cluster, a strategy memo — already in the shape of a GitHub issue or
`/docs` file. A human reviews that result and files it.

Once the result lands in this repo, the GitHub version is the version everyone
references. The Notion source becomes archival; if the two ever disagree,
GitHub wins.

---

## How to start using it (today)

If you have 30 minutes:

1. **Fill in** [docs/strategy/north-star.md](docs/strategy/north-star.md) — the one sentence that aligns every later decision.
2. **File 3 `[SIGNAL]` issues** from recent pilot conversations.
3. **File 1 `[BET]` issue** for the most important thing the team is currently building.
4. **Run this Friday's weekly review** using the template — even a 10-minute version.

That alone seeds the loop. Everything else compounds from there.

---

## The path to AI-native operations

This repo is intentionally designed so that, in 6–12 months, an AI agent can:

1. **Query the loop** — *"show me every invalidated bet about pricing in the last year and the signals that triggered them."* (already possible today via GitHub API.)
2. **Propose new bets** — given recent signals, the agent suggests hypotheses with kill criteria, written as draft `[BET]` issues. (next step: MCP server over this repo.)
3. **Detect contradictions** — when a new signal contradicts a previously confirmed learning, the agent applies the two-layer rule: if the learning still lives on an open `learning: confirmed` issue, it reopens that issue and swaps the label to `learning: hypothesis`; if the learning has been promoted into `docs/knowledge/confirmed-learnings.md`, it adds a row to `docs/knowledge/revisit-queue.md` and tags the new signal `learning: revisit`. In both cases it cross-links the contradicting signal.
4. **Pre-fill weekly reviews** — agent drafts the `[WEEKLY]` issue with metrics, shipped PRs, and clustered signals. Humans only approve and add interpretation.
5. **Run autopilot experiments** — for low-risk feature flags, the agent proposes A/B splits, monitors metrics, and files the `[EXP]` outcome.

We don't need any of this on day one. We need the **substrate** — structured, labelled, linked events — to make it possible. That substrate is what this repo is.

---

## FAQ

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
