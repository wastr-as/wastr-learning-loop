# Customers

One folder per customer or account. Cross-customer material lives in `_cross-customer/`; the monthly synthesis is [pilot-learnings.md](pilot-learnings.md).

## Layout

```
docs/customers/
  pilot-learnings.md              synthesis across customers (monthly)
  _cross-customer/                competitors, investor theses; not tied to one customer
  <customer-slug>/
    notes/                        meeting minutes (referat): curated, committed
    transcripts/                  raw transcripts: local only, git-ignored (see Confidentiality)
    analysis/                     synthesis, positioning, account assessments
```

## Customer slug

Lowercase ASCII, kebab-case. Transliterate Norwegian letters: `æ` to `ae`, `ø` to `o`, `å` to `a`.

- Named customer: `hente-no`, `easyavfall-no`.
- Customer not yet cleared to be named: `<segment>-discovery-<first-contact-date>`, e.g. `transporter-discovery-2026-10-26`. The mapping to the real name stays in the CEO's private Notion.

## File names

`YYYY-MM-DD_<type>-<topic>.md`

- Date is the meeting date (analysis: the date written). ISO format so the folder sorts chronologically.
- `<type>`: `intro`, `discovery`, `demo`, `followup`, `pilot`, `email`, `positioning`, `assessment`.
- `<topic>`: one to three words. Same-day second meeting: append `-2`.
- A transcript and its minutes share the same file name, in `transcripts/` and `notes/`.

Example: `hente-no/notes/2026-10-20_intro-call.md` and `hente-no/transcripts/2026-10-20_intro-call.md`.

## Front matter (notes and transcripts)

```yaml
---
customer: hente-no
date: 2026-10-20
type: intro
lane: b2b                # b2b | b2c
segment: transporter     # transporter | builder | homeowner
language: no             # no | en
participants: [Denis, "CEO of customer"]   # roles for unnamed customers
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
4. Account synthesis goes to `analysis/`; patterns across customers go to `pilot-learnings.md` at the monthly review.

## Confidentiality

This repository is public. Raw transcripts and customer-identifying detail must not be committed: `transcripts/` content is git-ignored (only `.gitkeep` is tracked), and `notes/` must be written so that it can be published, with unnamed customers pseudonymised. Truly confidential material stays in private Notion. See [tooling-protocol.md](../tooling-protocol.md#sensitive-content).
