"""Partner-discovery extractor — CLI entrypoint (issue #70, Phase 0).

Pulls construction & demolition waste (CDW) actors from Brreg, applies WASTR's
prioritisation, and writes a ranked ~200-row CSV for hand-off to Iteo.

Usage:
    python extract.py                      # Oslo + inner ring, default ~200 rows
    python extract.py --oslo-only          # Oslo (0301) only
    python extract.py --size 150           # cap shortlist size
    python extract.py --no-cap             # write every qualified company (audit)
    python extract.py --out path/file.csv  # custom output path

Repeatable by design: re-run any time the register refreshes. No state, no login.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

import config
import scoring
from connectors import BrregConnector
from models import Company

DEFAULT_OUTPUT = Path(__file__).parent / "output" / "iteo-shortlist.csv"


def dedup_by_orgnr(companies: list[Company]) -> list[Company]:
    """Collapse duplicates by org.nr, keeping the most contactable record.

    The same company can surface under multiple NACE codes (and, in Phase 1, from
    multiple sources). We keep whichever record carries the most contact signal.
    """
    best: dict[str, Company] = {}
    for c in companies:
        if not c.org_nr:
            continue
        existing = best.get(c.org_nr)
        if existing is None or _contact_rank(c) > _contact_rank(existing):
            best[c.org_nr] = c
    return list(best.values())


def _contact_rank(c: Company) -> int:
    return sum(bool(x) for x in (c.phone, c.email, c.website)) + int(c.mva_registered)


def build_shortlist(kommuner: list[str], size: int | None) -> list[Company]:
    """Run the full pipeline: fetch -> dedup -> quality filter -> score -> select."""
    connector = BrregConnector()
    nace_codes = list(config.NACE_TO_SEGMENT.keys())

    print(f"Fetching from Brreg: {len(nace_codes)} NACE codes x {len(kommuner)} kommune(r)...")
    raw = list(connector.fetch(nace_codes, kommuner))
    print(f"  fetched {len(raw)} raw records")

    deduped = dedup_by_orgnr(raw)
    print(f"  {len(deduped)} after de-dup by org.nr")

    qualified = [c for c in deduped if scoring.passes_quality(c)]
    print(f"  {len(qualified)} after quality filters")

    scored = [scoring.score(c) for c in qualified]

    if size is None:
        shortlist = sorted(scored, key=lambda c: c.priority_score, reverse=True)
    else:
        shortlist = scoring.select_shortlist(scored, size=size)
    print(f"  {len(shortlist)} in final shortlist")
    return shortlist


def write_csv(companies: list[Company], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(config.CSV_COLUMNS)
        for c in companies:
            writer.writerow([
                c.name,
                c.org_nr,
                c.segment or "",
                c.nace_primary or "",
                c.kommune_name or config.KOMMUNE_NAMES.get(c.kommune_nr or "", ""),
                c.employees if c.employees is not None else "",
                c.founded_year or "",
                c.phone or "",
                c.email or "",
                c.website or "",
                c.priority_score,
                c.why_prioritised,
            ])


def print_summary(companies: list[Company]) -> None:
    """Print the acceptance-criteria-relevant stats for the run."""
    total = len(companies)
    if total == 0:
        print("No companies in shortlist — check filters.")
        return
    seg_a = sum(1 for c in companies if c.segment == config.SEGMENT_A)
    seg_b = sum(1 for c in companies if c.segment == config.SEGMENT_B)
    with_contact = sum(1 for c in companies if c.has_contact)
    mva = sum(1 for c in companies if c.mva_registered)
    reachable = sum(1 for c in companies if c.has_contact or c.mva_registered)
    print("\n--- Shortlist summary ---")
    print(f"  Total:                 {total}")
    print(f"  Segment A (haul):      {seg_a} ({seg_a / total:.0%})")
    print(f"  Segment B (cont):      {seg_b} ({seg_b / total:.0%})")
    print(f"  Org.nr present:        {total} (100%)  <- universal enrichment key")
    print(f"  Direct contact field:  {with_contact} ({with_contact / total:.0%})  (website only; Brreg has no phone/email)")
    print(f"  MVA-registered:        {mva} ({mva / total:.0%})")
    print(f"  Reachable (contact|MVA): {reachable} ({reachable / total:.0%})")
    print(f"  Score range:           {companies[-1].priority_score}-{companies[0].priority_score}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Brreg-first CDW partner shortlist for Iteo (#70).")
    p.add_argument("--oslo-only", action="store_true", help="Restrict to Oslo (0301).")
    p.add_argument("--size", type=int, default=config.SHORTLIST_SIZE,
                   help=f"Shortlist size (default {config.SHORTLIST_SIZE}).")
    p.add_argument("--no-cap", action="store_true",
                   help="Write every qualified company, ranked (ignores --size).")
    p.add_argument("--out", type=Path, default=DEFAULT_OUTPUT, help="Output CSV path.")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    kommuner = [config.OSLO] if args.oslo_only else config.DEFAULT_KOMMUNER
    size = None if args.no_cap else args.size

    shortlist = build_shortlist(kommuner, size)
    if not shortlist:
        print("Nothing to write.", file=sys.stderr)
        return 1

    out_path = args.out
    if out_path == DEFAULT_OUTPUT:
        out_path = out_path.with_name(f"iteo-shortlist-{date.today():%Y%m%d}.csv")
    write_csv(shortlist, out_path)
    print_summary(shortlist)
    print(f"\nWrote {len(shortlist)} rows -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
