---
name: signal-from-notes
description: Draft a [SIGNAL] issue body from a stakeholder's meeting minutes. Use when the user wants a signal drafted from notes.
disable-model-invocation: true
argument-hint: <path to notes file>
allowed-tools: Read Grep Glob
---

# Signal draft from minutes

Argument: `$ARGUMENTS` = path to a file under `docs/stakeholders/**/notes/`.

1. Read the notes file and `.github/ISSUE_TEMPLATE/01_customer_signal.yml`.
2. If the notes contain several distinct observations, propose one signal per observation and ask
   which to draft; do not merge unrelated points into one issue.
3. For each, print a draft the author can paste into a new issue:
   - Title: `[SIGNAL] <short, factual>`
   - Labels to apply: `type: signal`, one `domain:`, one `segment:`, `lane:` (b2b or b2c) and
     `impact:`; add `learning: hypothesis` when the evidence is one source.
   - Body headings exactly as in the template: Customer Segment, Signal Source, What happened /
     what was said?, Context, Insight / So what?, Perceived Impact, Suggested Next Action.
   - Quotes verbatim from the notes; the notes file path in Context.
   - Anonymise per `AGENTS.md`: unnamed stakeholders stay unnamed.
4. State the evidence level plainly (one interview, recollection notes, desk research) and what the
   signal does not show. Check `docs/knowledge/confirmed-learnings.md`; if the signal contradicts an
   entry, say so and name the entry so the author can apply the two-layer rule.
5. Never file the issue yourself.
