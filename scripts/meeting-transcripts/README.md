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

## Setup

```powershell
# 1. Python 3.10+ and ffmpeg on PATH
winget install Gyan.FFmpeg

# 2. Install the Python dependency
cd scripts/meeting-transcripts
pip install -r requirements.txt
```

The Whisper model (~3 GB for `large-v3`) downloads and caches on first run.

## Meeting contexts

We record two kinds of meetings, and they feed the loop differently — pick one with `--context`:

| `--context` | Use for | External? | Loop routing |
|---|---|---|---|
| `founders` (default) | Internal founder ops/strategy talks | No | `segment: internal` — ops/strategy signals |
| `customer` | Calls with builders/contractors | Yes | `segment: customer` — pains, JTBD, pricing signals |
| `partner` | Calls with transporters/partners | Yes | `segment: partner` — fit, integration, neutrality signals |

The context is stamped into the transcript header (a routing hint for the Perplexity synthesis step) and output is filed under `output/<context>/`. Because everything runs **locally**, third-party audio never leaves the machine — but `customer`/`partner` meetings also print a **GDPR consent reminder**: confirm all participants consented to recording before you transcribe.

## Usage

```powershell
python transcribe.py meeting.m4a                    # founders (default), Norwegian, large-v3
python transcribe.py call.m4a --context customer   # customer-discovery call
python transcribe.py call.m4a --context partner    # partner-discovery call
python transcribe.py meeting.mp4 --language en      # force English
python transcribe.py meeting.m4a --model medium     # smaller/faster on a weak laptop
python transcribe.py meeting.m4a --format md        # timestamped markdown
python transcribe.py meeting.m4a --device cuda      # use an NVIDIA GPU
python transcribe.py meeting.m4a --out notes/2026-07-team.txt
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
