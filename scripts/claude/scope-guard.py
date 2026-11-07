#!/usr/bin/env python3
"""PreToolUse hook for scoped stakeholder sessions (see docs/tooling-protocol.md).

Reads the hook JSON on stdin and exits 2 (block) when a file tool touches a path outside the
session's allow-list. Fails closed: missing configuration blocks the call.

Environment (set by scripts/claude/lens.py):
  LOOP_LENS_ROOT   absolute path of the scoped worktree
  LOOP_LENS_ALLOW  JSON list of path prefixes (relative to the root) that may be read
  LOOP_LENS_WRITE  JSON list of path prefixes (relative to the root) that may be written
"""

import json
import os
import sys
import tempfile

READ_TOOLS = {"Read"}
WRITE_TOOLS = {"Edit", "Write", "NotebookEdit"}
SEARCH_TOOLS = {"Glob", "Grep"}
PATH_KEYS = ("file_path", "path", "notebook_path")


def _norm(path):
    return os.path.normcase(os.path.realpath(path))


def _inside(path, base):
    try:
        return os.path.commonpath([path, base]) == base
    except ValueError:  # different drives on Windows
        return False


def _relative(path, root):
    return os.path.relpath(path, root).replace("\\", "/")


def _matches(rel, prefixes):
    for prefix in prefixes:
        prefix = os.path.normcase(prefix).strip("/\\").replace("\\", "/")
        if rel == prefix or rel.startswith(prefix + "/"):
            return True
    return False


def check(payload, root, allow, write):
    """Return None when the call is allowed, otherwise a reason string."""
    tool = payload.get("tool_name", "")
    if tool not in READ_TOOLS | WRITE_TOOLS | SEARCH_TOOLS:
        return None

    tool_input = payload.get("tool_input") or {}
    cwd = payload.get("cwd") or root
    root_real = _norm(root)

    if tool == "Glob":
        pattern = str(tool_input.get("pattern", ""))
        parts = pattern.replace("\\", "/").split("/")
        if os.path.isabs(pattern) or ".." in parts or pattern.startswith("~"):
            return "glob pattern leaves the session scope: " + pattern

    paths = [tool_input.get(key) for key in PATH_KEYS if tool_input.get(key)]
    if tool in SEARCH_TOOLS and not paths:
        paths = [cwd]
    if not paths:
        return "no path in tool input; refusing"

    for raw in paths:
        expanded = os.path.expanduser(str(raw))
        if not os.path.isabs(expanded):
            expanded = os.path.join(cwd, expanded)
        resolved = _norm(expanded)
        if not _inside(resolved, root_real):
            return "path is outside the session scope: " + str(raw)
        rel = _relative(resolved, root_real)
        if rel == ".git" or rel.startswith(".git/") or "/.git/" in "/" + rel + "/":
            return "git internals are not readable in a scoped session: " + str(raw)
        if tool in SEARCH_TOOLS:
            continue  # searching inside the worktree is fine; it only holds allowed files
        prefixes = write if tool in WRITE_TOOLS else allow
        if not _matches(rel, prefixes):
            kind = "writable" if tool in WRITE_TOOLS else "readable"
            return "path is not " + kind + " in this scope: " + rel
    return None


def _deny(reason):
    sys.stderr.write("Blocked by scope-guard: " + reason + "\n")
    sys.exit(2)


def main():
    root = os.environ.get("LOOP_LENS_ROOT")
    try:
        allow = json.loads(os.environ.get("LOOP_LENS_ALLOW", "null"))
        write = json.loads(os.environ.get("LOOP_LENS_WRITE", "null"))
    except ValueError:
        _deny("LOOP_LENS_ALLOW or LOOP_LENS_WRITE is not valid JSON")
    if not root or allow is None or write is None:
        _deny("scope is not configured; start the session with scripts/claude/lens.py")
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        _deny("hook input is not valid JSON")
    reason = check(payload, root, allow, write)
    if reason:
        _deny(reason)
    sys.exit(0)


def selftest():
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "wt")
        outside = os.path.join(tmp, "other")
        for folder in ("docs/strategy", "docs/stakeholders/partners/a", ".git"):
            os.makedirs(os.path.join(root, folder))
        os.makedirs(outside)
        allow = ["docs/strategy", "docs/stakeholders/partners/a", "AGENTS.md"]
        write = ["docs/stakeholders/partners/a"]

        def call(tool, **tool_input):
            return check({"tool_name": tool, "tool_input": tool_input, "cwd": root}, root, allow, write)

        cases = [
            ("read allowed", call("Read", file_path=os.path.join(root, "docs/strategy/x.md")), True),
            ("read relative", call("Read", file_path="docs/strategy/x.md"), True),
            ("read root file", call("Read", file_path="AGENTS.md"), True),
            ("read other stakeholder", call("Read", file_path="docs/stakeholders/partners/b/x.md"), False),
            ("read outside", call("Read", file_path=os.path.join(outside, "x.md")), False),
            ("read dotdot", call("Read", file_path="docs/strategy/../../../other/x.md"), False),
            ("read git", call("Read", file_path=".git/config"), False),
            ("write own folder", call("Write", file_path="docs/stakeholders/partners/a/analysis/x.md"), True),
            ("write shared", call("Write", file_path="docs/strategy/x.md"), False),
            ("grep default cwd", call("Grep", pattern="x"), True),
            ("grep outside", call("Grep", pattern="x", path=outside), False),
            ("glob inside", call("Glob", pattern="docs/**/*.md"), True),
            ("glob dotdot", call("Glob", pattern="../**/*.md"), False),
            ("glob absolute", call("Glob", pattern=os.path.join(outside, "*.md")), False),
            ("other tool ignored", check({"tool_name": "WebFetch", "tool_input": {}}, root, allow, write), True),
        ]
        failed = [name for name, reason, should_allow in cases if (reason is None) != should_allow]
        for name, reason, should_allow in cases:
            print(("ok   " if (reason is None) == should_allow else "FAIL ") + name + ("" if reason is None else "  -> " + reason))
        return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    main()
