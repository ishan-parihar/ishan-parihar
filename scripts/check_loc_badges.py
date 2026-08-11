#!/usr/bin/env python3
"""
LOC badge cross-checker for the ishan-parihar GitHub portfolio.

Scans every git repo under MY-PROJECTS, computes the *actual* tracked-source
LOC (git ls-files, code extensions only — no docs, lockfiles, images, or
generated/build artifacts), then compares it against the LOC badge value in
each repo's README. Any mismatch means the badge has gone stale.

Usage:
  python3 scripts/check_loc_badges.py              # report only (exit 1 if any stale)
  python3 scripts/check_loc_badges.py --fix        # rewrite stale badge values in place
  python3 scripts/check_loc_badges.py --root PATH  # scan a different root
  python3 scripts/check_loc_badges.py --json       # machine-readable output
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

# Root of the portfolio; this script lives at <root>/ishan-parihar/scripts/.
DEFAULT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

# Code file extensions that count toward LOC (everything else — md/json/yaml/
# toml/png/svg/lockfiles — is excluded).
CODE_EXTS = {
    ".rs", ".go", ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".svelte", ".vue", ".java", ".kt", ".kts", ".c", ".h", ".cpp", ".hpp",
    ".cc", ".cs", ".rb", ".php", ".swift", ".lua", ".sh", ".bash", ".zsh",
    ".fish", ".ps1", ".sql", ".scala", ".hs", ".zig", ".dart", ".ex", ".exs",
    ".ml", ".r", ".groovy", ".gradle", ".proto", ".asm", ".clj", ".elm",
    ".erl", ".f", ".f90", ".jl", ".nim", ".pl", ".rkt", ".tcl", ".v", ".vh",
    ".gd", ".css", ".scss", ".less",
}

# Directories that are never counted even if tracked.
EXCLUDE_DIRS = {
    ".git", "node_modules", "target", "dist", "build", ".next", ".turbo",
    "vendor", "__pycache__", ".venv", "venv", ".cargo", "docs", "assets",
    "coverage", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".gradle",
}

# Badge shape: img.shields.io/badge/LOC-73.0K-informational
BADGE_RE = re.compile(r"badge/LOC-([0-9]+(?:\.[0-9]+)?K?)-informational")

MAX_LINES = 10_000_000  # sanity cap against pathological files


def fmt_loc(n: int) -> str:
    """Canonical badge format: 834 -> '834', 72958 -> '73.0K', 537083 -> '537K'.

    Rule (matches existing badge convention): plain number below 1000, one
    decimal for 1K..99.9K, whole K at 100K and above.
    """
    if n < 1000:
        return str(n)
    k = n / 1000.0
    if n >= 100_000:
        return f"{round(k)}K"
    return f"{k:.1f}K"


def stale_diff(actual: int, badge: int) -> bool:
    """A badge is stale only when it drifts beyond rounding noise.

    Tolerance: 200 lines or 2% of actual, whichever is larger. This keeps pure
    representation diffs (489K vs 489.3K) from false-flagging.
    """
    return abs(actual - badge) > max(200, actual * 0.02)


def parse_loc_badge(value: str) -> int | None:
    """'73.0K' -> 73000, '834' -> 834, garbage -> None."""
    value = value.strip()
    if value.endswith("K") or value.endswith("k"):
        try:
            return int(round(float(value[:-1]) * 1000))
        except ValueError:
            return None
    try:
        return int(value)
    except ValueError:
        return None


def repo_locs(root: pathlib.Path) -> dict[str, int]:
    """Map repo-relpath -> tracked source LOC, for every git repo under root.

    The portfolio is nested (MCP-AND-CLIS/*, LIFEOS/*, HERMES/*, WEBSITES/*),
    so we walk the whole tree and treat any directory containing a .git entry
    (dir for a real repo, file for a worktree/submodule) as a repo.
    """
    out: dict[str, int] = {}
    for dirpath, dirnames, _filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        cur = pathlib.Path(dirpath)
        if not (cur / ".git").exists():
            continue
        try:
            listed = subprocess.run(
                ["git", "-C", str(cur), "ls-files", "-z"],
                capture_output=True, check=True, text=False,
            ).stdout.split(b"\0")
        except subprocess.CalledProcessError:
            continue
        total = 0
        for raw in listed:
            p = raw.decode(errors="replace")
            if not p or p.startswith(".git"):
                continue
            path = pathlib.Path(p)
            if any(part in EXCLUDE_DIRS for part in path.parts):
                continue
            if path.suffix not in CODE_EXTS:
                continue
            full = cur / path
            try:
                with full.open("r", errors="replace") as fh:
                    total += min(MAX_LINES, sum(1 for _ in fh))
            except (OSError, UnicodeDecodeError):
                continue
        out[str(cur.relative_to(root))] = total
        dirnames[:] = []  # don't descend into a repo's internals
    return out


def find_badges(readme: pathlib.Path) -> list[tuple[int, str, str]]:
    """(line_number, full_badge_value, raw_match) for each LOC badge in a README."""
    found = []
    try:
        lines = readme.read_text(errors="replace").splitlines()
    except OSError:
        return found
    for i, line in enumerate(lines, 1):
        for m in BADGE_RE.finditer(line):
            found.append((i, m.group(1), m.group(0)))
    return found


def repo_owner(root: pathlib.Path, repo: str) -> str:
    """GitHub owner from the origin remote, '' if none/not GitHub."""
    r = subprocess.run(
        ["git", "-C", str(root / repo), "config", "--get", "remote.origin.url"],
        capture_output=True, text=True,
    )
    url = r.stdout.strip()
    m = re.search(r"(?:github\.com[:/])([^/]+)/", url)
    return m.group(1) if m else ""


def main() -> int:
    ap = argparse.ArgumentParser(description="Cross-check LOC badges against real code.")
    ap.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT,
                    help="portfolio root (default: parent of this repo)")
    ap.add_argument("--fix", action="store_true",
                    help="rewrite stale badge values in place")
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable JSON")
    ap.add_argument("--owner", type=str, default="ishan-parihar",
                    help="GitHub owner whose repos are fixable (default ishan-parihar)")
    args = ap.parse_args()

    locs = repo_locs(args.root)
    stale: list[dict] = []
    upstream: list[dict] = []
    ok_count = 0

    for name, actual in sorted(locs.items()):
        repo_dir = args.root / name
        owner = repo_owner(args.root, name)
        readmes = sorted(repo_dir.glob("README.md"))
        for readme in readmes:
            for line_no, badge_val, raw in find_badges(readme):
                parsed = parse_loc_badge(badge_val)
                if parsed is None:
                    continue
                expected = fmt_loc(actual)
                if not stale_diff(actual, parsed):
                    ok_count += 1
                    continue
                record = {
                    "repo": name,
                    "readme": str(readme.relative_to(args.root)),
                    "line": line_no,
                    "badge": badge_val,
                    "actual": expected,
                    "actual_loc": actual,
                }
                if owner and owner != args.owner:
                    record["owner"] = owner
                    upstream.append(record)  # upstream-authored badge; report only
                else:
                    stale.append(record)

    if args.json:
        print(json.dumps({
            "checked_repos": len(locs),
            "stale": stale,
            "upstream_skipped": upstream,
        }, indent=2))
        return 1 if stale else 0

    print(f"scanned {len(locs)} repos; {ok_count} badges OK, "
          f"{len(stale)} stale, {len(upstream)} upstream-authored (not ours to fix)\n")
    if stale:
        print(f"{'repo':<32}{'badge':>10}{'actual':>10}  readme:line")
        print("-" * 78)
    for r in stale:
        print(f"{r['repo']:<32}{r['badge']:>10}{r['actual']:>10}  {r['readme']}:{r['line']}")
        if args.fix:
            path = args.root / r["readme"]
            try:
                text = path.read_text(errors="replace")
            except OSError:
                continue
            new_text, count = BADGE_RE.subn(
                lambda m: m.group(0).replace(m.group(1), r["actual"]),
                text, count=1,
            )
            if count:
                path.write_text(new_text)
                print(f"    -> fixed to {r['actual']}")
    if upstream:
        print("\nupstream-authored (badge authored elsewhere; report-only, no fix):")
        for r in upstream:
            print(f"  {r['repo']:<32}{r['badge']:>10}{r['actual']:>10}  owner={r['owner']}")

    if not stale:
        print("All LOC badges are current. Nothing to do.")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
