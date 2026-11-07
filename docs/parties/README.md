# External Parties

How the loop stores material about people and organisations outside WASTR. One folder per party, grouped by relationship. Cross-party synthesis sits at the root of each group.

## Groups

```
docs/parties/
  customers/                      transporters, builders, homeowners, public-sector pilots
    pilot-learnings.md            synthesis across customers (monthly)
  competitors/                    companies we are compared with
    investor-differentiation-theses.md   landscape across competitors, used in investor talks
  investors/                      investors, accelerators, incubators
  funders/                        grants and public funding (e.g. innovasjon-norge)
```

A party belongs to the group of its main relationship. If it plays two roles (a customer that is also a competitor), keep one folder and link from the other group. Add a group (`partners/` for research institutions and municipalities) when the first party needs it.

## Per-party layout

```
<group>/<party-slug>/
  notes/                          meeting minutes (referat): curated, committed
  transcripts/                    raw transcripts: local only, git-ignored (see Confidentiality)
  analysis/                       synthesis, positioning, account assessments, desk research
  materials/                      decks and pitches we send to the party (source + exports)
```

Create `notes/`, `transcripts/` and `materials/` only when first needed; competitors often have `analysis/` only. Outbound material for a Norwegian audience is written in Norwegian.

## Party slug

Lowercase ASCII, kebab-case. Transliterate Norwegian letters: `æ` to `ae`, `ø` to `o`, `å` to `a`.

- Named party: `hente-no`, `medarbeiderne`, `checksammy`, `innovasjon-norge`.
- Party not yet cleared to be named: `<segment>-discovery-<first-contact-date>`. The mapping to the real name stays in private Notion.

## File names

`YYYY-MM-DD_<type>-<topic>.md`

- Date is the meeting date (analysis: the date written). ISO format so the folder sorts chronologically.
- `<type>`: `intro`, `discovery`, `demo`, `followup`, `pilot`, `email`, `positioning`, `assessment`, `competitive-analysis`, `application`, `report`, `pitch`, `deck`.
- `<topic>`: one to three words. Same-day second meeting: append `-2`.
- A transcript and its minutes share the same file name, in `transcripts/` and `notes/`.

Example: `hente-no/notes/2026-10-20_intro-call.md` and `hente-no/transcripts/2026-10-20_intro-call.md`.

## Front matter (notes and transcripts)

```yaml
---
party: hente-no
party_type: customer     # customer | competitor | investor | funder
date: 2026-10-20
type: intro
lane: b2b                # b2b | b2c
segment: transporter     # customers only: transporter | builder | homeowner
language: no             # no | en
participants: [Denis, "CEO of party"]   # roles for unnamed parties
source: teams            # teams | phone | in-person | email
consent_to_record: yes   # required for transcripts
transcript: ../transcripts/2026-10-20_intro-call.md
signals: [97]            # [SIGNAL] issues filed from this meeting
---
```

## Workflow

1. Meeting held, recording consented, transcript saved to `transcripts/` (local).
2. Minutes written to `notes/` from the transcript: facts, quotes, open questions. No invented quotes; mark anything not said in the meeting as an interpretation.
3. `[SIGNAL]` issue(s) filed within 48 h per [tooling-protocol.md](../tooling-protocol.md), linking the notes file.
4. Party synthesis goes to `analysis/`; patterns across parties go to the group's root document at the monthly review.

## Innovasjon Norge

Reporting boundary: only `lane: b2b` evidence is reported to Innovasjon Norge (see the lane rule in the [README](../../README.md)). Keep grant applications, milestone reports and meeting minutes in `funders/innovasjon-norge/`; link the underlying `[SIGNAL]` issues instead of copying customer evidence into it.

## Confidentiality

This repository is public. Raw transcripts and party-identifying detail must not be committed: `transcripts/` content is git-ignored (only `.gitkeep` is tracked), and `notes/` must be written so that it can be published, with unnamed parties pseudonymised. Truly confidential material (financials, legal, personal data, investor terms) stays in private Notion. See [tooling-protocol.md](../tooling-protocol.md#sensitive-content).
