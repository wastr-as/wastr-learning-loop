# Tooling Protocol

> **Concrete workflows for the three-tool setup: GitHub, Notion, Claude.**
>
> The [sync contract](sync-contract.md) defines *what* lives where. This document
> defines *how* the team actually operates day to day, including how we work with
> Claude against this repo.

---

## Daily / weekly workflows

### Stakeholder meeting (CEO)

1. **Record** with consent (see [stakeholders/README.md](stakeholders/README.md#confidentiality));
   live notes in Notion if useful.
2. **Transcribe locally** with `scripts/meeting-transcripts`; the transcript goes to
   `docs/stakeholders/<group>/<slug>/transcripts/` (git-ignored, stays on the machine).
3. **Minutes:** Claude drafts them into `notes/` from the transcript (skill `meeting-to-notes`);
   the CEO reads and corrects before committing.
4. **Within 48 h:** `[SIGNAL]` issue(s) for each distinct observation (skill
   `signal-from-notes` drafts them; a human files them). Quote the stakeholder directly and
   verbatim. Apply labels per the taxonomy. Link the notes file in the issue footer.
5. **If the signal contradicts a confirmed learning,** apply the two-layer rule:
   - **Issue-layer** (learning still lives on a `learning: confirmed` issue):
     reopen that issue, swap its label to `learning: hypothesis`, cross-link
     the two issues.
   - **Doc-layer** (learning has been promoted into
     `docs/knowledge/confirmed-learnings.md` as L-NNN): apply
     `learning: revisit` to the new signal AND add a row to
     `docs/knowledge/revisit-queue.md` pointing at the L-NNN entry. The weekly review
     will pick it up via the open-hypothesis filter.

### Strategy analysis (CEO or CTO + Claude)

1. Open Claude Code in this repo, or in a scoped session for one stakeholder
   (see [Perspective analysis](#perspective-analysis-and-data-isolation)).
2. Claude reads the repo itself. There is no separate memory file to maintain: what the
   loop knows is what is committed.
3. **If the session produced a decision or canonical fact:** open a `[DECISION]` issue or
   propose an edit to the relevant `docs/strategy/*.md` file. Link the notes or issues the
   analysis relied on in the footer.
4. A conclusion that stays only in a chat has not happened.

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

### Weekly review (CEO + CTO, Friday 30 min — CTO is ritual keeper)

**Keeper:** the CTO owns *that this happens* — holds the fixed recurring slot,
pre-fills the issue, ensures it's filed. **Default-alive:** if one founder can't
attend, the other runs it and files; the absent founder comments within 24 h. The
week is "done" only when the `[WEEKLY]` issue exists.

1. **Before the call (keeper, ~10 min solo):** pre-fill the `[WEEKLY]` issue from the
   loop (skill `weekly-prefill`: merged PRs and commits across the Wastr repos, new
   `type: signal` issues, running `[EXP]`s, kill-criteria checks, metrics). Status is read
   async; the call is for decisions.
2. **Live (30 min):** scan both lanes (Lane A grant-facing, Lane B internal — keep the
   boundary), then converge on **at most 3 joint decisions** (bet to open, kill-criteria
   hit, lane-priority conflict). Don't manufacture three; one real decision is a good week.
3. Any signal that contradicts a confirmed learning → apply the two-layer rule (reopen the `learning: confirmed` issue OR add a row to `docs/knowledge/revisit-queue.md` if the learning has been promoted to a doc entry).
4. Any bet hitting kill criteria → close as `invalidated`.

### Monthly review (CEO + CTO, last Friday, 90 min — CTO is ritual keeper)

> Same keeper + default-alive rule as the weekly. Output artifacts are the updated docs
> below, not a `[WEEKLY]` issue.

1. Promote eligible insights into `docs/knowledge/confirmed-learnings.md`.
2. Re-rank `docs/strategy/roadmap-now-next-later.md`.
3. Walk both revisit surfaces — reopened `learning: hypothesis` issues (previously confirmed, now in doubt) AND rows in `docs/knowledge/revisit-queue.md` — and either re-confirm each item or close as `learning: invalidated` (issues) / update `confirmed-learnings.md` (doc entries).
4. Scan `[SIGNAL]` issues across segments — if the same pattern appears in ≥3 signals, open an `[L-NNN]` promotion candidate or add a cross-segment note to `docs/stakeholders/pilot-learnings.md`.
5. Update `docs/stakeholders/pilot-learnings.md` with the month's synthesis (per-segment notes + any cross-segment patterns identified in step 4).

---

## Working with Claude

> **Status: proposal (weekly W2026-W45, decision D2).** The files named below exist in the same PR
> but have not been run with Claude Code yet; the guard and launcher are tested only in isolation
> (see "Validated so far" at the end of this section).

### Principles

1. **The repo is the memory.** Claude learns the company from committed files. Nothing
   canonical lives in a chat, and there is no side-channel knowledge file to re-upload.
2. **Agent drafts, human files.** Claude may draft minutes, issues, docs and PRs. A human
   reads the draft before it is filed or merged.
3. **Instructions guide, settings enforce.** `CLAUDE.md`, rules and skills shape what Claude
   tries; they are context, not a boundary. Anything that must hold (what a session may read,
   what it may run) is a permission rule or a hook, which Claude Code enforces regardless of
   what the model decides.
4. **Facts and inference stay visibly separate.** A quote is verbatim from the source file.
   Everything else is labelled as interpretation.

### Instruction layers

| Layer | Location | Holds | Loaded |
|---|---|---|---|
| Shared rules | `AGENTS.md`, imported by `CLAUDE.md` (`@AGENTS.md`) | repo layout, issue templates and labels, tone filter, language, sensitive-content rules; under 200 lines | every session |
| Path rules | `.claude/rules/*.md` with `paths:` | e.g. `docs/stakeholders/**`: verbatim quotes only, pseudonymise, never name unapproved stakeholders | when Claude touches matching files |
| Skills | `.claude/skills/<name>/SKILL.md` | the repeatable jobs below | when invoked |
| Lens definitions | `docs/stakeholders/lenses/<type>.md` | how a type of stakeholder judges WASTR | by the `lens` skill |
| Enforcement | `.claude/settings.json`, `scripts/claude/*` | permission rules, hooks, launcher | always (client-enforced) |
| Personal | `CLAUDE.local.md` (git-ignored) | individual preferences | every session |

`AGENTS.md` is the single tool-neutral file, so Copilot and Claude read the same rules.
`CLAUDE.md` imports it with `@AGENTS.md` (an import, not a symlink, so it also works for a
Windows clone). Keep both short; move procedures into skills.

### Skills

| Skill | Does | Reads | Writes |
|---|---|---|---|
| `meeting-to-notes <stakeholder> <date>` | minutes from a transcript | that stakeholder's folder | `notes/<file>.md` |
| `signal-from-notes <notes file>` | `[SIGNAL]` draft in the issue-shaped YAML | the notes file, labels taxonomy | a draft for a human to file |
| `weekly-prefill` | `[WEEKLY]` draft | issues, merged PRs, git history | a draft for the keeper |
| `lens <stakeholder> <question>` | perspective analysis | scoped files only (below) | stdout, or `analysis/` on request |
| `stakeholder-new <group> <name>` | scaffold folder and profile | templates | the new folder |

Skills with side effects set `disable-model-invocation: true`, so only a human starts them.

### Perspective analysis and data isolation

**Goal:** run analysis from one stakeholder's point of view (an operator such as
Medarbeiderne, a municipal body such as REG, a funder such as Innovasjon Norge) without
another stakeholder's material bleeding into it.

**Two different risks.** This repository is public, so committed notes are publishable by
design and cross-reading them is not a confidentiality breach. The real risks are:

- **Perspective contamination:** a REG analysis that quietly uses what Medarbeiderne said, or
  an output that states one stakeholder's position to another. A discipline problem.
- **Confidential material** (raw transcripts, job-scoped data, terms): must never be in this
  repository at all. A storage problem.

**Isolation levels, from cheapest to strongest:**

| Level | Mechanism | Stops | Does not stop |
|---|---|---|---|
| 0. Prompt | "use only X's files" | nothing enforceable | the model drifting or being injected |
| 1. Scoped session | the launcher creates a sparse git worktree holding the shared docs plus one stakeholder's folder; the session starts there with `blockReadsOutsideWorkingDirectories` on and Bash denied | accidental reads of other stakeholders; local transcripts are not in the worktree | a user or tool deliberately pointing outside the worktree |
| 2. Enforced scope | level 1 plus a `PreToolUse` hook that exits 2 for any path outside the allow-list | prompt injection and mistakes that use the file tools | anything that never goes through a Claude Code tool |
| 3. Physical separation | the sensitive stakeholder's data lives in a separate private repository or directory that is not on the same machine or session as the others, optionally with its own `CLAUDE_CONFIG_DIR` | the data being reachable at all | nothing, at the price of overhead |

**Recommendation.** Use level 2 as the default for every perspective run: one launcher,
`scripts/claude/lens.py <slug> [--lens partner|municipal|funder|customer]`, with no
per-stakeholder duplication because the path is derived from the slug. Use level 3 only for
stakeholders whose shared material is genuinely confidential (job-scoped operator data, a
municipal body's internal documents); this needs the private-repo option in D1.

**What a scoped session can see:**

- `docs/stakeholders/<group>/<slug>/**`, the matching lens file, and the shared WASTR facts:
  `docs/strategy/`, `docs/knowledge/`, `docs/metrics/`, `docs/architecture/adr/`.
- Only the GitHub issues listed in that stakeholder's `signals:` front matter, pre-fetched by
  the launcher. No free-form `gh` search and no Bash in a lens session.
- Not visible: other stakeholders' folders, `docs/market/`, and any `transcripts/` that belong
  to someone else.

**What a lens run must produce:**

1. What this stakeholder cares about, each point tied to a file and quote.
2. How a given WASTR claim lands with them, and which evidence they would ask for.
3. Likely objections and what we cannot yet answer.
4. What we must not say to them (their confidentiality limits).

Every statement is labelled `source:` (a verbatim quote from their folder) or `inference:`.
The lens file supplies the type-level frame (goals, decision criteria, trusted evidence,
vocabulary); the stakeholder folder supplies the facts. A lens never invents a stakeholder's
opinion, and an output meant for one stakeholder must not carry another's information.

**Questions that span stakeholders** ("what do all operators say about invoicing?") are run
by a human owner in an unscoped session, and the result is pseudonymised before it is
committed. One stakeholder's notes are never fed into another's perspective run.

**In-session shortcut.** A `lens-<slug>` subagent can answer a quick "how would REG read
this?" inside a normal session. It has a fresh context and a read-only tool list, but it
shares the machine with everything else, so treat it as level 0 to 1, not as isolation.

*To validate in the scaffolding PR:* sparse-checkout behaviour in linked worktrees, which
Claude Code settings keys the launcher can pass with `--settings`, and whether the hook sees
paths in the form the allow-list expects on both Windows and macOS.

### How Denis and Siarhei work in the same repo

- **Branch and PR:** each task on its own branch (`docs/<topic>`, `signal/<slug>`), merged by PR.
  Agent sessions never push to `main`.
- **Review follows the [ownership map](ownership.md):** the owner merges; the other founder
  comments within 24 h on strategy, ADR and template changes.
- **Provenance:** an AI-drafted issue or PR keeps a footer naming the tool and is read by its
  author before filing. Anything not stated in the source is marked as interpretation.
- **Sync:** pull before a session, keep PRs small, and put personal preferences in
  `CLAUDE.local.md` rather than in shared files.
- **Hygiene:** run `/doctor prompt-audit` after changing instruction files, to catch conflicting
  or outdated rules.

---

## Export formats — the shared schema

To keep Claude's outputs interoperable with GitHub, it must export
**issue-shaped** outputs when proposing new signals, bets, or decisions.

### Minimum signal export

```yaml
type: signal
domain: routing | matching | ordering | customer | driver | collector | infra
segment: transporter | builder | homeowner | internal
lane: b2b | b2c
impact: high | medium | low
source: "notes file path, e.g. docs/stakeholders/partners/hente-no/notes/2026-10-20_intro-call.md"
quote: "Direct customer quote, verbatim."
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
source: "<notes file, issue or document reference>"
```

Both formats map 1:1 onto the corresponding `.github/ISSUE_TEMPLATE/*.yml`.
A human pastes the YAML into a new issue and fills in any missing fields.

---

## The forbidden-words and tone filter

Outputs from Claude that land in this repo must pass this filter:

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
- Norwegian: inside direct quotes from Innovasjon Norge, customers, or industry
  sources, and in outbound material written for a Norwegian audience (see
  [stakeholders/README.md](stakeholders/README.md#per-stakeholder-layout)).
- Always write *Innovasjon Norge* in full in English contexts. *IN* is fine
  only inside Norwegian-language threads.

---

## Sensitive content

Anonymise customer names in `[SIGNAL]` issues unless the customer has
explicitly approved being named. Truly confidential material (financials,
legal, personal data) does not belong in this repo at all — it lives in
the CEO's private Notion or a separate IR channel.

Raw transcripts stay on the machine that made them (`transcripts/` is git-ignored). A
perspective session never reads another stakeholder's transcript, and the launcher does not
place transcripts in a worktree it did not create for that stakeholder.

---

## Open questions

- First automation target — GitHub Actions, n8n, or a small custom service?
  *(decision pending; track as a `[DECISION]` issue once first automation is
  needed)*
- Do we want a Slack / email digest of new `[SIGNAL]` issues for the founder
  who didn't file them? *(low priority while the team is two people)*
- Confidentiality of raw stakeholder material: local-only transcripts, or a private
  repository (weekly D1)? Level 3 isolation depends on the answer.

---

*See also: [sync-contract.md](sync-contract.md) and [ownership.md](ownership.md).*
