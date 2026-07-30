# Meeting-transcript extractor

> Local, free, Norwegian-first meeting transcription for the WASTR intelligence loop.
> Issue [#72](https://github.com/wastr-as/wastr-learning-loop/issues/72) — July priority #1.

Turns a meeting recording into clean text so it can flow through the pipeline:
**Notion (raw capture) → Perplexity (synthesis) → GitHub (canonical).**

## Why faster-whisper

Chosen over hosted transcription tools (see the tooling discussion on #72), price first:

| | faster-whisper (this) | Whisper API | Otter/Fireflies |
|---|---|---|---|
| Cost | **Free** (local) | ~NOK 3–4/hr | Subscription |
| Norwegian | Excellent (`large-v3`) | Excellent | Weak/English-first |
| Privacy | Audio never leaves the machine | Uploaded | Uploaded |

## Recording a meeting

This tool needs one audio/video file as input. How to produce it:

### Teams / Google Meet (built-in)

- **Teams:** `···` (More actions) → **Record and transcribe** → **Start recording**. The `.mp4` lands in the organiser's **OneDrive → Recordings** (channel meetings: the channel's SharePoint). Needs a plan/policy that allows recording.
- **Google Meet:** **Activities** → **Recording** → **Start recording**. The `.mp4` lands in the organiser's **Google Drive → Meet Recordings**. Needs an eligible Google Workspace plan (not free Gmail).

Both already produce their own transcript — use faster-whisper when you want **better Norwegian**, **local/private** processing, or a **non-Teams/Meet** recording.

### Any platform, or no recording feature

- **OBS Studio** (free) — records screen + system audio + mic to `.mp4`; captures both sides on any platform.
- **Windows Game Bar** (`Win+G` → record) — quick built-in screen+audio capture, no install.
- **In-person meetings** — your phone's voice-memo app → transfer the `.m4a`.

### Consent (customer/partner meetings)

Third parties are recorded, so **start recording visibly and get a verbal "ok to record?"** at the top of the call. The `--context customer` / `--context partner` runs print a GDPR consent reminder for this reason.

## Setup

```powershell
# 1. Python 3.10+
# 2. Install the Python dependency
cd scripts/meeting-transcripts
pip install -r requirements.txt
```

`faster-whisper` bundles **PyAV** (the `av` package), which ships the ffmpeg
libraries — so audio/video decoding works out of the box and a **separate ffmpeg
install is not required**. Install the ffmpeg CLI only if you want it for your own
pre-processing (`winget install Gyan.FFmpeg`).

The Whisper model (~3 GB for `large-v3`) downloads and caches on first run.

## Meeting contexts

We record two kinds of meetings, and they feed the loop differently — pick one with `--context`:

| `--context` | Use for | External? | Loop routing |
|---|---|---|---|
| `founders` (default) | Internal founder ops/strategy talks | No | `segment: internal` — ops/strategy signals |
| `customer` | Calls with builders/contractors | Yes | `segment: customer` — pains, JTBD, pricing signals |
| `partner` | Calls with transporters/partners | Yes | `segment: partner` — fit, integration, neutrality signals |

The context is stamped into the transcript header (a routing hint for the Perplexity synthesis step) and output is filed under `output/<context>/`. Because everything runs **locally**, third-party audio never leaves the machine — but `customer`/`partner` meetings also print a **GDPR consent reminder**: confirm all participants consented to recording before you transcribe.

## Where to put recordings

Drop the file into the matching context folder, then run the tool by name:

```
input/
  founders/   <- internal founder meetings
  customer/   <- builder/contractor calls
  partner/    <- transporter/partner calls
```

A bare filename is resolved against `input/<context>/` first, then `input/`. You can still pass a full path to a file anywhere. Recordings are git-ignored — only the folder structure is tracked.

## Usage

```powershell
# drop file in input/<context>/ and run by name
python transcribe.py standup.m4a                     # input/founders/standup.m4a
python transcribe.py acme-call.m4a --context customer  # input/customer/acme-call.m4a
python transcribe.py hauler-call.m4a --context partner # input/partner/hauler-call.m4a

# or pass any full path
python transcribe.py C:\rec\meeting.mp4 --language en   # force English
python transcribe.py standup.m4a --model medium         # smaller/faster on a weak laptop
python transcribe.py standup.m4a --format md            # timestamped markdown
python transcribe.py standup.m4a --device cuda          # use an NVIDIA GPU
python transcribe.py standup.m4a --out notes/2026-07-team.txt
```

| Flag | Default | Notes |
|---|---|---|
| `--context` | `founders` | `founders`/`customer`/`partner` — routing hint + output subfolder |
| `--model` | `large-v3` | `tiny`/`base`/`small`/`medium`/`large-v3` — quality vs speed |
| `--language` | `no` | ISO code, or `auto` to detect |
| `--device` | `auto` | `cuda` if a GPU is found, else `cpu` |
| `--format` | `txt` | `txt` (pipeline-ready) or `md` (timestamped) |
| `--out` | `output/<context>/<name>.<ext>` | custom output path |

## Output

- `txt` — a short context/routing header followed by a single clean paragraph-joined transcript; paste straight into Notion → Perplexity.
- `md` — context + metadata header, then timestamped segments for skimming a long meeting before synthesis.

Recordings and transcripts are git-ignored (captured in Notion, not committed here).
