# Stakeholders

How the loop stores material about organisations outside WASTR that we talk to. One folder per stakeholder, grouped by current relationship. Cross-stakeholder synthesis is [pilot-learnings.md](pilot-learnings.md) (monthly). Competitors are not stakeholders; see [Competitors](#competitors).

## Groups

```
docs/stakeholders/
  pilot-learnings.md      synthesis across stakeholders
  lenses/                 how a type of stakeholder judges WASTR (partner, municipal, funder, customer)
  partners/               operators/transporters, municipal bodies, research institutions we pilot or fulfil with
  customers/              builders, contractors, homeowners (ordering side); create at the first meeting
  funding/                investors, accelerators, grants (e.g. innovasjon-norge)
```

File a stakeholder by its **current** relationship and move the folder when that changes. Operators are `partners/` until they pay us; today none has committed volume or a fee. The `segment:` label and the `segment` front-matter key (`transporter | builder | homeowner`) stay as they are, so a `segment: transporter` signal lives under `partners/`.

## Competitors

`docs/market/competitors/<competitor-slug>/analysis/`, plus the landscape document `investor-differentiation-theses.md`. Public-source desk research only: no meetings, no transcripts, no consent questions.

## Per-stakeholder layout

```
<group>/<stakeholder-slug>/
  profile.md                      facts only: who, role, status, boundaries, links (optional, recommended)
  notes/                          meeting minutes (referat): curated, committed
  transcripts/                    raw transcripts: local only, git-ignored (see Confidentiality)
  analysis/                       synthesis, positioning, account assessments, desk research
  materials/                      decks and pitches we send to the stakeholder (source + exports)
```

Create `notes/`, `transcripts/` and `materials/` only when first needed. Outbound material for a Norwegian audience is written in Norwegian.

## Stakeholder slug

Lowercase ASCII, kebab-case. Transliterate Norwegian letters: `æ` to `ae`, `ø` to `o`, `å` to `a`.

- Named stakeholder: `example-operator`, `example-municipality`, `example-funder`.
- Stakeholder not yet cleared to be named: `<segment>-discovery-<first-contact-date>`. The mapping to the real name stays in private Notion.

## File names

`YYYY-MM-DD_<type>-<topic>.md`

- Date is the meeting date (analysis: the date written). ISO format so the folder sorts chronologically.
- `<type>`: `intro`, `discovery`, `demo`, `followup`, `pilot`, `email`, `positioning`, `assessment`, `competitive-analysis`, `application`, `report`, `pitch`, `deck`.
- `<topic>`: one to three words. Same-day second meeting: append `-2`.
- A transcript and its minutes share the same file name, in `transcripts/` and `notes/`.

Example: `example-operator/notes/2026-10-20_intro-call.md` and `example-operator/transcripts/2026-10-20_intro-call.md`.

## Front matter (notes and transcripts)

```yaml
---
stakeholder: example-operator
stakeholder_type: partner       # partner | customer | funder
date: 2026-10-20
type: intro
lane: b2b                       # b2b | b2c
segment: transporter            # transporter | builder | homeowner | internal
language: no                    # no | en
participants: [Denis, "CEO of stakeholder"]   # roles for unnamed stakeholders
source: teams                   # teams | phone | in-person | email
consent_to_record: yes          # required for transcripts
transcript: ../transcripts/2026-10-20_intro-call.md
signals: [97]                   # [SIGNAL] issues filed from this meeting
---
```

## Workflow

1. Meeting held, recording consented, transcript saved to `transcripts/` (local).
2. Minutes written to `notes/` from the transcript: facts, quotes, open questions. No invented quotes; mark anything not said in the meeting as an interpretation.
3. `[SIGNAL]` issue(s) filed within 48 h per [tooling-protocol.md](../tooling-protocol.md), linking the notes file.
4. Stakeholder synthesis goes to `analysis/`; patterns across stakeholders go to `pilot-learnings.md` at the monthly review.

## Innovasjon Norge

Reporting boundary: only `lane: b2b` evidence is reported to Innovasjon Norge (see the lane rule in the [README](../../README.md)). Keep grant applications, milestone reports and meeting minutes in `funding/innovasjon-norge/`; link the underlying `[SIGNAL]` issues instead of copying customer evidence into it.

## Confidentiality

This repository is public. Raw transcripts and stakeholder-identifying detail must not be committed: `transcripts/` content is git-ignored (only `.gitkeep` is tracked), and `notes/` must be written so that it can be published, with unnamed stakeholders pseudonymised. Truly confidential material (financials, legal, personal data, investor terms) stays in private Notion. See [tooling-protocol.md](../tooling-protocol.md#sensitive-content).
