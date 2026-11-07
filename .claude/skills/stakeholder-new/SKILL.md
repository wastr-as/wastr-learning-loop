---
name: stakeholder-new
description: Scaffold a stakeholder folder (notes, transcripts, analysis, profile). Use when the user adds a new customer, partner or funder.
disable-model-invocation: true
argument-hint: <partners|customers|funding> <slug>
allowed-tools: Read Write Glob
---

# New stakeholder folder

Arguments: `$0` = group, `$1` = slug.

1. Validate: group is `partners`, `customers` or `funding`; slug is lowercase ASCII kebab-case
   (`æ` to `ae`, `ø` to `o`, `å` to `a`). For a stakeholder not cleared to be named, use
   `<segment>-discovery-<first-contact-date>`.
2. If `docs/stakeholders/$0/$1/` already exists, stop. Never overwrite.
3. Create `notes/.gitkeep`, `transcripts/.gitkeep` and `profile.md` from `profile-template.md` in
   this skill's folder. Create `analysis/` and `materials/` only when there is something to put in them.
4. Fill what the user told you; leave the rest as `unknown`. Do not research or guess facts.
5. Tell the user which lens fits (`partner`, `municipal`, `funder` or `customer`) and that raw
   transcripts for this stakeholder stay local.
