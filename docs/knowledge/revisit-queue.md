# Revisit Queue

> **Doc-layer revisit surface.** When a `[SIGNAL]` contradicts an entry in
> [`confirmed-learnings.md`](confirmed-learnings.md), add a row here and tag
> the signal `learning: revisit`. The full two-layer model is in the README:
> [When a confirmed learning gets contradicted](../../README.md#when-a-confirmed-learning-gets-contradicted).
>
> **Scope:** *reactive* re-looks only — a contradicting signal has actually
> arrived. *Proactive* tripwires ("re-look if metric X breaches Y") belong on
> the L-NNN entry itself as a `Revisit trigger` bullet, or in an ADR's
> `Revisit Trigger` section.

| # | Contradicted learning (L-NNN) | Contradicting signal | Owner |
|---|---|---|---|
| *(empty)* | | | |

## Procedure

**Filing a row** (when a signal contradicts a doc-layer learning):

1. File the `[SIGNAL]` as usual; apply `learning: revisit` in addition to the
   normal labels.
2. Add a row above pointing at the L-NNN entry and linking the signal issue.
3. Cross-link from the signal back to the L-NNN entry in its body.

**Resolving at the next monthly review**, pick one:

- **(a)** Amend the L-NNN entry in `confirmed-learnings.md` (wording change,
  added caveat, narrowed scope).
- **(b)** File an `[EXP]` to settle the disputed point empirically; keep the
  row open until the experiment closes.
- **(c)** Move the L-NNN entry out of `confirmed-learnings.md` entirely
  (the belief no longer holds).
- **(d)** Close as "still true, was a one-off" — no change to L-NNN.

**Cleanup on resolution** (mandatory for all of (a)/(c)/(d), and for (b)
once the experiment closes):

- Delete the row from the table above.
- Remove `learning: revisit` from the contradicting `[SIGNAL]` issue.
- Close the signal with its appropriate `learning:` outcome label
  (`confirmed` / `invalidated` / `new-insight`).
