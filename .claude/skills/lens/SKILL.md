---
name: lens
description: Analyse a question from one stakeholder's perspective, using only that stakeholder's folder and the shared WASTR documents. Use inside a scoped session started by scripts/claude/lens.py.
disable-model-invocation: true
argument-hint: <question or claim to test>
allowed-tools: Read Grep Glob
---

# Perspective analysis

Question: `$ARGUMENTS`

## Check the scope first

1. Use Glob on `docs/stakeholders/*/*/` (excluding `lenses/`). If more than one stakeholder folder is
   present, stop and tell the user to start the session with `scripts/claude/lens.py <slug>`.
2. Identify the one stakeholder folder and its lens (`profile.md` front matter `lens:`, or the
   session prompt). Read `docs/stakeholders/lenses/<lens>.md`.

## Read

3. Read the stakeholder's `profile.md`, all `notes/`, `analysis/` and `materials/` files, and any
   `context/issue-*.md`. Read shared facts only as needed: `docs/strategy/`, `docs/knowledge/`,
   `docs/metrics/`, `docs/architecture/adr/`.

## Produce

4. Answer in four parts, each statement labelled `source:` (verbatim quote, with file) or
   `inference:`:
   1. What this stakeholder cares about, tied to their own words.
   2. How the claim or proposal lands with them, and which evidence they would ask for.
   3. Likely objections and what WASTR cannot yet answer.
   4. What must not be said to them (their confidentiality and customer-ownership limits).
5. Never invent their opinion. If the folder does not support a point, write
   `no basis in this folder` rather than filling the gap from the lens file.
6. Do not mention or hint at any other stakeholder. Write to `analysis/` in this stakeholder's
   folder only if the user asks; name the file `YYYY-MM-DD_lens-<lens>.md`.
