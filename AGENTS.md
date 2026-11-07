# AGENTS.md

Shared instructions for any AI coding agent (Claude Code, Copilot) working in `wastr-learning-loop`.
Humans: see [README.md](README.md). Details: [docs/tooling-protocol.md](docs/tooling-protocol.md).

## What this repo is

The WASTR intelligence loop: signals, bets, experiments, decisions and what we learned, kept as
GitHub issues plus Markdown. It is the company's thinking layer, not code. The repository is
**public**.

## Layout

- `docs/strategy/`, `docs/knowledge/`, `docs/metrics/`, `docs/architecture/adr/`: shared WASTR facts.
- `docs/stakeholders/<group>/<slug>/`: one folder per outside organisation (`partners/`,
  `customers/`, `funding/`), each with `notes/`, `transcripts/`, `analysis/`, `materials/`.
  Conventions: [docs/stakeholders/README.md](docs/stakeholders/README.md).
- `docs/stakeholders/lenses/`: how a type of stakeholder judges WASTR.
- `docs/market/competitors/`: competitor desk research.
- `.claude/skills/`: repeatable jobs. `scripts/claude/`: scoped-session launcher and guard.

## Rules

1. **Agent drafts, human files.** Draft minutes, issues, docs and PRs. Do not file an issue, close
   or relabel one, merge, or push to `main` unless asked in that conversation.
2. **Quotes are verbatim** from the source file. Never paraphrase inside quotation marks. Keep
   Norwegian quotes in Norwegian.
3. **Separate fact from inference.** Anything the source did not say is labelled `inference:`.
4. **Never commit transcripts.** `docs/stakeholders/*/*/transcripts/` is git-ignored.
5. **Pseudonymise** stakeholders that have not approved being named: roles instead of names, no
   contact details, no financial figures. Use the slug convention from the stakeholders README.
6. **Do not promote a learning** to `confirmed`; that is decided at the monthly review.
7. **Claims discipline.** Say what WASTR cannot yet do. No unaudited numbers as KPIs. `lane: b2c`
   data is never an Innovasjon Norge outcome.

## Voice

English. No: disrupt, revolutionary, game-changer, transformative, cutting-edge, unprecedented,
seamless, synergy. Humble, factual, peer-to-peer. Sustainability claims need concrete numbers.
Always write *Innovasjon Norge* in full.

## Issues and labels

Titles start with `[SIGNAL]`, `[BET]`, `[SPEC]`, `[EXP]`, `[DECISION]`, `[BUG]` or `[WEEKLY]`.
Label taxonomy is in [README.md](README.md#vocabulary--label-taxonomy-25-labels-5-groups). Issue-shaped
export formats are in the tooling protocol. Write issue bodies to a file and pass `--body-file`.

## Lens sessions (scoped to one stakeholder)

A session started by `scripts/claude/lens.py` sees only the shared docs, one lens file and one
stakeholder folder. In such a session:

- Do not look for or reference any other stakeholder, even if a path suggests one.
- Never state one stakeholder's position to another; if asked, say the scope does not allow it.
- Writes go only to this stakeholder's folder.
- Label every statement `source:` (quote and file) or `inference:`; do not invent their opinion.
- If the working tree shows more than one stakeholder folder, stop: the session is not scoped.

## Skills

`/meeting-to-notes`, `/signal-from-notes`, `/weekly-prefill`, `/stakeholder-new`, `/lens`. Each
skill file states what it reads and writes.

## Git

Branch per task (`docs/<topic>`, `signal/<slug>`), PR to `main`, small commits. Review follows
[docs/ownership.md](docs/ownership.md).
