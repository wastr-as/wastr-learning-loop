---
name: weekly-prefill
description: Pre-fill the [WEEKLY] review issue from GitHub issues, merged PRs and git history. Use when the keeper prepares the weekly.
disable-model-invocation: true
argument-hint: [since YYYY-MM-DD]
allowed-tools: Read Grep Glob Bash(gh issue list *) Bash(gh issue view *) Bash(gh pr list *) Bash(git -C * log *)
---

# Weekly pre-fill

Argument: `$ARGUMENTS` = start date; default is the date of the last `[WEEKLY]` issue.

1. Read `.github/ISSUE_TEMPLATE/07_weekly_review.yml` and `docs/rituals/weekly-review-template.md`.
2. Find the last weekly: `gh issue list --repo wastr-as/wastr-learning-loop --state all --search "WEEKLY in:title"`.
3. Collect since the start date, read-only:
   - issues opened in the loop repo, grouped by type and lane;
   - commit subjects (`git -C ../<repo> log --since=<date> --no-merges --format=%ad%x20%h%x20%s --date=short`)
     for each sibling `Wastr.*`, `global-infra` and `wastr-learning-loop` checkout;
   - merged PRs where `gh` can reach the repo.
4. Draft the issue body with the template sections. For "What We Shipped", say that commits are not
   proof of release or deployment unless you checked tags or deploy runs.
5. Key Metrics: do not invent numbers. If you did not read the data, write "not read" and list what
   is needed (orders, routes, empty-run %, landing workbook tiles).
6. Keep both lanes visible; flag anything that would cross the `lane: b2b` / `lane: b2c` boundary.
7. Print the draft only. The keeper files it.
