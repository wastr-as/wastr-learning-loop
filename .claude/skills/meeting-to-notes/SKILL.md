---
name: meeting-to-notes
description: Draft meeting minutes (referat) for a stakeholder from a local transcript. Use when the user asks for minutes from a transcript.
disable-model-invocation: true
argument-hint: <group/slug> <YYYY-MM-DD_type-topic>
allowed-tools: Read Grep Glob Write
---

# Minutes from a transcript

Arguments: `$0` = `<group>/<slug>` (for example `partners/hente-no`), `$1` = file base name
(for example `2026-10-20_intro-call`).

1. Read `docs/stakeholders/$0/transcripts/$1.md`. If it is missing, stop and say so; do not look
   for transcripts elsewhere.
2. Read `docs/stakeholders/$0/profile.md` and `docs/stakeholders/README.md` (front matter keys) if present.
3. Write `docs/stakeholders/$0/notes/$1.md` with the front matter from the stakeholders README and
   these sections:
   - **Facts and decisions**: what was stated or agreed, one bullet each.
   - **Quotes**: verbatim, in the original language, each with a timestamp if the transcript has one.
   - **Open questions**: what was left unclear or promised.
   - **Interpretation**: your reading, every line starting `inference:`.
   - **Follow-ups**: owner and date only if stated in the meeting.
4. Rules: no invented quotes; mark inaudible or unclear passages `[unclear]`; refer to individuals by
   role, not name; leave out contact details and financial figures; if the stakeholder is not cleared
   to be named, use the pseudonymous slug throughout.
5. Report what you wrote and list anything you were unsure about. Do not create `[SIGNAL]` issues;
   that is `/signal-from-notes`, after a human has read the minutes.
