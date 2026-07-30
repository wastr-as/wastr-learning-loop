"""Meeting-transcript extractor — CLI entrypoint (issue #72, July priority #1).

Transcribes a meeting audio/video recording to clean text using faster-whisper
(a fast, local, CPU/GPU CTranslate2 reimplementation of OpenAI Whisper). Output
is plain UTF-8 text ready for the loop pipeline: Notion (raw capture) ->
Perplexity (synthesis) -> GitHub (canonical).

Why faster-whisper (see issue #72 tooling discussion):
    * Free — runs locally, no per-minute API cost, no subscription.
    * Private — meeting audio never leaves the machine (fits WASTR's neutral,
      data-sovereign positioning).
    * Norwegian — the ``large-v3`` model transcribes Norwegian well, which the
      English-first SaaS tools (Otter etc.) do not.

Two meeting contexts feed the loop differently (see issue #72), selected with
``--context``:
    * ``founders``  — internal ops/strategy talks between the founders.
    * ``customer``  — calls with builders/contractors (customer discovery).
    * ``partner``   — calls with transporters/partners (partner discovery).
The context is stamped into the transcript header as a routing hint for the
synthesis step, and the output is filed under ``output/<context>/``. External
contexts (customer/partner) also print a consent reminder — third parties are
recorded, so GDPR consent must be captured before the meeting.

Drop recordings in ``input/`` (optionally ``input/<context>/``) and pass just the
filename, or give any full path.

Usage:
    python transcribe.py meeting.m4a                      # founders, Norwegian, large-v3
    python transcribe.py call.m4a --context customer      # from input/customer/call.m4a
    python transcribe.py call.m4a --context partner        # partner-discovery call
    python transcribe.py meeting.mp4 --language en        # force English
    python transcribe.py meeting.wav --model medium       # smaller/faster model
    python transcribe.py meeting.m4a --format md          # timestamped markdown
    python transcribe.py meeting.m4a --device cuda        # use an NVIDIA GPU
    python transcribe.py meeting.m4a --out notes/2026-07-team.txt

Requires ffmpeg on PATH (faster-whisper decodes audio through it) and the
packages in requirements.txt. No login, no state — re-run any time.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

# Default to the best-quality multilingual model. It is the slowest and largest
# (~3 GB download, cached after first run) but gives the best Norwegian output.
# Drop to "medium" / "small" on a weak laptop; quality degrades gracefully.
DEFAULT_MODEL = "large-v3"

# Meetings are Norwegian by default. Pass --language to override, or "auto" to
# let Whisper detect it (slightly slower, occasionally wrong on short clips).
DEFAULT_LANGUAGE = "no"

# Meeting contexts. Each tags the transcript with a loop-routing hint and files
# output under output/<key>/. ``external`` flags meetings with third parties,
# which triggers a GDPR consent reminder before transcription.
CONTEXTS = {
    "founders": {
        "label": "Founder / internal meeting",
        "segment": "internal",
        "routing": "Internal ops/strategy. Synthesize into internal signals; "
        "label `segment: internal`.",
        "external": False,
    },
    "customer": {
        "label": "Customer meeting (builder/contractor)",
        "segment": "customer",
        "routing": "Customer discovery. Extract pains, jobs-to-be-done, "
        "pricing and objection signals; label `segment: customer`.",
        "external": True,
    },
    "partner": {
        "label": "Partner meeting (transporter/partner)",
        "segment": "partner",
        "routing": "Partner discovery. Extract fit, integration and "
        "neutrality signals; label `segment: partner`.",
        "external": True,
    },
}
DEFAULT_CONTEXT = "founders"

# Drop recordings here — optionally in a per-context subfolder (input/customer/
# etc.). A bare filename passed as input is resolved against input/<context>/
# and then input/, so you can just drop a file and run the tool by name.
INPUT_DIR = Path(__file__).parent / "input"

# int8 runs comfortably on CPU with a small accuracy cost. On GPU, float16 is
# both faster and more accurate — auto-selected when --device cuda is given.
CPU_COMPUTE_TYPE = "int8"
GPU_COMPUTE_TYPE = "float16"

AUDIO_SUFFIXES = {".m4a", ".mp3", ".wav", ".flac", ".ogg", ".mp4", ".mov", ".webm", ".mkv"}


def _fmt_timestamp(seconds: float) -> str:
    """Render a segment start time as ``HH:MM:SS`` for the markdown format."""
    td = timedelta(seconds=int(seconds))
    return str(td).rjust(8, "0")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="transcribe.py",
        description="Transcribe a meeting recording to text with faster-whisper.",
    )
    parser.add_argument("input", type=Path, help="Audio/video file to transcribe.")
    parser.add_argument(
        "--context",
        choices=tuple(CONTEXTS),
        default=DEFAULT_CONTEXT,
        help=f"Meeting context (default: {DEFAULT_CONTEXT}). Sets the loop-routing "
        "hint and output subfolder. 'customer'/'partner' are external meetings "
        "and trigger a GDPR consent reminder.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output file path. Defaults to output/<context>/<input-stem>.<ext>.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Whisper model size (default: {DEFAULT_MODEL}). "
        "One of: tiny, base, small, medium, large-v3.",
    )
    parser.add_argument(
        "--language",
        default=DEFAULT_LANGUAGE,
        help=f"Spoken language code (default: {DEFAULT_LANGUAGE!r}). "
        "Use 'auto' to detect.",
    )
    parser.add_argument(
        "--device",
        choices=("cpu", "cuda", "auto"),
        default="auto",
        help="Compute device (default: auto — cuda if available, else cpu).",
    )
    parser.add_argument(
        "--format",
        choices=("txt", "md"),
        default="txt",
        help="Output format: plain text (default) or timestamped markdown.",
    )
    return parser.parse_args(argv)


def resolve_output_path(args: argparse.Namespace) -> Path:
    if args.out is not None:
        return args.out
    out_dir = Path(__file__).parent / "output" / args.context
    return out_dir / f"{args.input.stem}.{args.format}"


def resolve_input_path(args: argparse.Namespace) -> Path:
    """Resolve the input file, allowing a bare name dropped in ``input/``.

    An explicit existing path wins. Otherwise a bare filename is looked up in
    ``input/<context>/`` first, then ``input/``. If nothing matches the path is
    returned unchanged so the caller can report a not-found error.
    """
    if args.input.exists():
        return args.input
    for candidate in (INPUT_DIR / args.context / args.input, INPUT_DIR / args.input):
        if candidate.exists():
            return candidate
    return args.input


def transcribe(args: argparse.Namespace) -> str:
    """Run faster-whisper and return the assembled transcript string."""
    # Imported lazily so --help works without the (heavy) dependency installed.
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit(
            "faster-whisper is not installed. Run:\n"
            "    pip install -r requirements.txt"
        )

    device = args.device
    if device == "auto":
        device = "cuda" if _cuda_available() else "cpu"
    compute_type = GPU_COMPUTE_TYPE if device == "cuda" else CPU_COMPUTE_TYPE

    print(
        f"Loading model {args.model!r} on {device} ({compute_type})… "
        "(first run downloads and caches the model)",
        file=sys.stderr,
    )
    model = WhisperModel(args.model, device=device, compute_type=compute_type)

    language = None if args.language == "auto" else args.language
    segments, info = model.transcribe(
        str(args.input),
        language=language,
        vad_filter=True,  # drop silence/cross-talk; cleaner, faster output
    )

    print(
        f"Detected language {info.language!r} "
        f"(p={info.language_probability:.2f}); transcribing…",
        file=sys.stderr,
    )

    if args.format == "md":
        return _render_markdown(args, info, segments)
    return _render_text(args, segments)


def _render_text(args: argparse.Namespace, segments) -> str:
    """Plain, paragraph-joined transcript with a short context header.

    The header gives the synthesis step (Perplexity -> GitHub) the routing hint
    up front; the transcript itself stays a single clean paragraph below it.
    """
    ctx = CONTEXTS[args.context]
    header = (
        f"[{ctx['label']}] {date.today().isoformat()} — source: {args.input.name}\n"
        f"Loop routing: {ctx['routing']}\n\n"
    )
    body = " ".join(seg.text.strip() for seg in segments).strip()
    return header + body + "\n"


def _render_markdown(args: argparse.Namespace, info, segments) -> str:
    """Timestamped markdown, handy for skimming a long meeting before synthesis."""
    ctx = CONTEXTS[args.context]
    lines = [
        f"# Meeting transcript — {args.input.stem}",
        "",
        f"- Context: {ctx['label']}",
        f"- Loop routing: {ctx['routing']}",
        f"- Date processed: {date.today().isoformat()}",
        f"- Source file: `{args.input.name}`",
        f"- Language: {info.language} (p={info.language_probability:.2f})",
        f"- Model: {args.model}",
        "",
        "---",
        "",
    ]
    for seg in segments:
        lines.append(f"**[{_fmt_timestamp(seg.start)}]** {seg.text.strip()}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _cuda_available() -> bool:
    """Best-effort GPU probe without importing torch as a hard dependency."""
    try:
        import ctranslate2

        return ctranslate2.get_cuda_device_count() > 0
    except Exception:
        return False


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    args.input = resolve_input_path(args)
    if not args.input.exists():
        sys.exit(
            f"Input file not found: {args.input}\n"
            f"Drop the recording in input/{args.context}/ (or input/) and pass "
            "its name, or give a full path."
        )

    if CONTEXTS[args.context]["external"]:
        print(
            "Reminder: this is an external meeting — confirm every participant "
            "consented to recording (GDPR) before transcribing.",
            file=sys.stderr,
        )

    if args.input.suffix.lower() not in AUDIO_SUFFIXES:
        print(
            f"Warning: {args.input.suffix!r} is not a recognised audio/video "
            "suffix; attempting transcription anyway.",
            file=sys.stderr,
        )

    transcript = transcribe(args)

    out_path = resolve_output_path(args)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(transcript, encoding="utf-8")

    words = len(transcript.split())
    print(f"Wrote {words} words -> {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
