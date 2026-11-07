#!/usr/bin/env python3
"""Start a Claude Code session scoped to one stakeholder (see docs/tooling-protocol.md).

    python scripts/claude/lens.py <slug> [--lens partner|municipal|funder|customer]
    python scripts/claude/lens.py <slug> --dry-run
    python scripts/claude/lens.py --list
    python scripts/claude/lens.py <slug> --remove

The session runs in a sparse git worktree that holds only the shared WASTR documents, one lens
file and that stakeholder's folder. Settings passed with --settings block reads and writes outside
the worktree, deny shell and MCP tools, and run scripts/claude/scope-guard.py before every file tool.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LENS_ROOT = REPO.parent / (REPO.name + ".lens")
GITHUB_REPO = "wastr-as/wastr-learning-loop"

SHARED = [
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    ".claude",
    "scripts/claude",
    "docs/strategy",
    "docs/knowledge",
    "docs/metrics",
    "docs/architecture/adr",
    "docs/stakeholders/README.md",
    "docs/stakeholders/lenses",
    "docs/tooling-protocol.md",
]
DEFAULT_LENS = {"partners": "partner", "customers": "customer", "funding": "funder"}
LENSES = ["partner", "municipal", "funder", "customer"]


def run(args, cwd=None, check=True, capture=False):
    return subprocess.run(
        args, cwd=cwd, check=check, text=True, encoding="utf-8",
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def git(*args, cwd=REPO, capture=False, check=True):
    return run(["git", *args], cwd=cwd, capture=capture, check=check)


def stakeholder_dirs(ref):
    out = git("ls-tree", "-r", "-d", "--name-only", ref, "docs/stakeholders", capture=True).stdout
    found = {}
    for line in out.splitlines():
        parts = line.split("/")
        if len(parts) == 4 and parts[2] in DEFAULT_LENS:
            found.setdefault(parts[3], []).append(parts[2])
    return found


def issue_numbers(folder):
    numbers = set()
    for notes in (folder / "notes").glob("*.md"):
        match = re.search(r"^signals:\s*\[([^\]]*)\]", notes.read_text(encoding="utf-8"), re.M)
        if match:
            numbers.update(int(n) for n in re.findall(r"\d+", match.group(1)))
    return sorted(numbers)


def prefetch_issues(worktree, numbers):
    if not numbers or not shutil.which("gh"):
        return []
    context = worktree / "context"
    context.mkdir(exist_ok=True)
    written = []
    for number in numbers:
        result = run(
            ["gh", "issue", "view", str(number), "--repo", GITHUB_REPO, "--json", "number,title,state,labels,body"],
            capture=True, check=False,
        )
        if result.returncode != 0:
            continue
        data = json.loads(result.stdout)
        labels = ", ".join(label["name"] for label in data.get("labels", []))
        text = "# #{number} {title}\n\nstate: {state}\nlabels: {labels}\n\n{body}\n".format(
            number=data["number"], title=data["title"], state=data["state"], labels=labels, body=data.get("body", ""))
        (context / "issue-{}.md".format(number)).write_text(text, encoding="utf-8")
        written.append(number)
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", nargs="?")
    parser.add_argument("--lens", choices=LENSES)
    parser.add_argument("--ref", default="HEAD", help="git ref to check out (default HEAD)")
    parser.add_argument("--dry-run", action="store_true", help="prepare the worktree and print the command; do not start Claude")
    parser.add_argument("--no-issues", action="store_true", help="do not pre-fetch issues listed in the notes' signals")
    parser.add_argument("--remove", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        for slug, groups in sorted(stakeholder_dirs(args.ref).items()):
            print("{}  ({})".format(slug, ", ".join(groups)))
        return 0
    if not args.slug:
        parser.error("slug is required")

    if args.remove:
        git("worktree", "remove", "--force", str(LENS_ROOT / args.slug), check=False)
        settings = LENS_ROOT / (args.slug + ".settings.json")
        settings.unlink(missing_ok=True)
        print("removed", LENS_ROOT / args.slug)
        return 0

    groups = stakeholder_dirs(args.ref).get(args.slug)
    if not groups:
        print("No stakeholder folder '{}' in {}. Try --list.".format(args.slug, args.ref), file=sys.stderr)
        return 1
    if len(groups) > 1:
        print("'{}' exists in several groups: {}. Keep one.".format(args.slug, ", ".join(groups)), file=sys.stderr)
        return 1
    group = groups[0]
    lens = args.lens or DEFAULT_LENS[group]

    folder = "docs/stakeholders/{}/{}".format(group, args.slug)
    patterns = ["/" + item + ("" if "." in Path(item).name else "/") for item in SHARED + [folder]]

    worktree = LENS_ROOT / args.slug
    if worktree.exists():
        git("worktree", "remove", "--force", str(worktree), check=False)
        shutil.rmtree(worktree, ignore_errors=True)
    LENS_ROOT.mkdir(parents=True, exist_ok=True)
    git("worktree", "prune")
    git("worktree", "add", "--detach", "--no-checkout", str(worktree), args.ref)
    subprocess.run(
        ["git", "sparse-checkout", "set", "--no-cone", "--stdin"], cwd=worktree,
        input="\n".join(patterns) + "\n", text=True, check=True)
    git("read-tree", "-mu", "HEAD", cwd=worktree)

    numbers = [] if args.no_issues else prefetch_issues(worktree, issue_numbers(worktree / folder))

    allow = SHARED + [folder, "context"]
    write = [folder]
    settings_path = LENS_ROOT / (args.slug + ".settings.json")
    guard = str(worktree / "scripts" / "claude" / "scope-guard.py")
    settings = {
        "permissions": {
            "blockReadsOutsideWorkingDirectories": True,
            "blockWritesOutsideWorkingDirectories": True,
            "deny": ["Bash", "PowerShell", "mcp__*"],
        },
        "hooks": {
            "PreToolUse": [{
                "matcher": "Read|Edit|Write|NotebookEdit|Glob|Grep",
                "hooks": [{"type": "command", "command": sys.executable, "args": [guard], "onFailure": "block"}],
            }]
        },
    }
    settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    prompt = (
        "Scoped session for stakeholder {group}/{slug}, lens '{lens}'. You can see only the shared WASTR "
        "documents, docs/stakeholders/lenses/{lens}.md and docs/stakeholders/{group}/{slug}/. Do not try to "
        "read anything else or refer to any other stakeholder. Follow AGENTS.md, section 'Lens sessions'. "
        "Start by reading the lens file and the stakeholder folder, then use /lens for analysis."
    ).format(group=group, slug=args.slug, lens=lens)

    env = dict(os.environ)
    env["LOOP_LENS_ROOT"] = str(worktree)
    env["LOOP_LENS_ALLOW"] = json.dumps(allow)
    env["LOOP_LENS_WRITE"] = json.dumps(write)

    command = ["claude", "--settings", str(settings_path), "--append-system-prompt", prompt]
    print("worktree : {}".format(worktree))
    print("lens     : {}".format(lens))
    print("settings : {}".format(settings_path))
    print("issues   : {}".format(", ".join("#" + str(n) for n in numbers) or "none pre-fetched"))
    if args.dry_run or not shutil.which("claude"):
        if not args.dry_run:
            print("claude was not found on PATH; command to run from the worktree:")
        print("LOOP_LENS_ROOT={}".format(env["LOOP_LENS_ROOT"]))
        print("LOOP_LENS_ALLOW={}".format(env["LOOP_LENS_ALLOW"]))
        print("LOOP_LENS_WRITE={}".format(env["LOOP_LENS_WRITE"]))
        print(" ".join(json.dumps(part) if " " in part else part for part in command))
        return 0
    return subprocess.call([shutil.which("claude")] + command[1:], cwd=worktree, env=env)


if __name__ == "__main__":
    sys.exit(main())
