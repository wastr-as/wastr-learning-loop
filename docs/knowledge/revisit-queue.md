# Revisit Queue

> **Items tagged `learning: revisit`.**
> Things we believed, then a contradicting signal appeared. We owe ourselves a re-look.

| # | Original learning | Contradicting signal | Status | Owner |
|---|---|---|---|---|
| 1 | **L-010** — Resolve address at the picker, not at confirmation | [#36](https://github.com/wastr-as/wastr-learning-loop/issues/36) — geo-resolved address sometimes wrong, no manual override. Shipping fallback in [#37](https://github.com/wastr-as/wastr-learning-loop/issues/37). **Trigger to revisit L-010 itself:** `addressSource = "manual"` rate exceeds 20% over a rolling 30-day window. | open | @siarhei-karabitski |

## Rules

1. When a `[SIGNAL]` contradicts an entry in `confirmed-learnings.md`, add a row here.
2. Discuss at the next monthly product review.
3. Resolve by either: (a) updating `confirmed-learnings.md`, (b) running an `[EXP]`, or (c) closing as "still true, was a one-off."
