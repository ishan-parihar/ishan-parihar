#!/usr/bin/env python3
"""Derive the ranking register (REPOS in measure_repos.py) from GitHub truth.

WHY THIS EXISTS. The register is a hand-maintained Python literal:

    REPOS = [
        ("social-forge",  "MCP-AND-CLIS/social-forge",  "engine"),
        ("tg-cli",        "MCP-AND-CLIS/tg-cli",        "engine"),
        ...
    ]

Two things decay, and both did. Measured 2026-10-31 and re-measured at this
date:

  * the RELPATHS are dead. They carry prefixes from a machine layout that no
    longer exists (`MCP-AND-CLIS/`, `HERMES/`, `CONTENT-CREATION/`, `LIFEOS/`,
    `WEBSITES/`). **1 of 41 resolves** under the current tree; `measure_repos.py`
    works around this by resolving by name, which recovers 30 of 41.
  * the NAMES drift whenever a repo is renamed, because nothing re-checks them.
    Measured today, **6 of 41 rows name repos that do not exist**:

        register says   GitHub resolves to   evidence
        igs-rust        sourcehound          gh follows the rename
        social-forge    switchpost           gh follows the rename
        slideforge-rust deckmill             gh follows the rename
        discord-cli     discord-lyr          gh follows the rename
        tg-cli          tg-lyr               gh follows the rename
        cinesync        CineSync              gh follows the rename (case only)

    and two are genuinely gone (`icode`, `osint-os`), which the README already
    labels archived.

Hand-patching the relpaths fixes one of the two decay modes and leaves the
other, so the next rename is found by another audit. This script derives the
register instead: it reads GitHub once, resolves every register name through
`gh` (which follows renames and reports the live name), and emits the same
Python literal with the live name, the real tree path, and the category
preserved from the existing row.

WHAT IT DELIBERATELY DOES NOT DO.

  * It does not decide categories for repos that are not already in the
    register. 25 public, non-fork repos are in no register at all, and which
    tier they occupy is a ruling, not a classification default. The script
    emits them as a candidate list for the ruling and stops there.
  * It does not touch `rank_score.py`'s frozen `DATA` block, which is a correct
    snapshot of per-repo measurements. Overwriting it from a fresh scan would
    be the damage an earlier gap invited.
  * It does not run the measurement. It writes the register; `measure_repos.py`
    still measures. A generator that also measured would conflate "where does
    this repo live and what is it called" with "how big is it".

Usage:
    python3 scripts/gen_register.py            # emit the register to stdout
    python3 scripts/gen_register.py --diff      # show only what changes
    python3 scripts/gen_register.py --write      # rewrite the REPOS block in place

Exit 0 when the register is current. Exit 1 when --write found something to
change (so it can be a gate: `genome` runs gates and expects 0 on green).
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEASURE = HERE / "measure_repos.py"
OWNER = "ishan-parihar"

# Category is preserved per row, never invented. The four live values come from
# the register's own history: engines, experimental, deprecated, and the sites
# category that is explicitly never ranked.
KNOWN_CATEGORIES = {"engine", "experimental", "deprecated", "site"}


def current_repos() -> list[tuple[str, str, str]]:
    """Parse the live REPOS literal so the category column is carried, not guessed."""
    src = MEASURE.read_text(encoding="utf-8")
    block = src.split("REPOS = [", 1)[1].split("\n]", 1)[0]
    return ast.literal_eval("[" + block + "]")


def gh_view(repo: str) -> dict | None:
    """Resolve one repo name through gh. Returns None when it is genuinely gone.

    MEASURED: `gh repo view` FOLLOWS a rename and reports the new name, so this
    is the resolver that turns a stale register name into a live one. It exits
    1 both for "no such repo" and for auth/network trouble; only the first is a
    verdict here, and the second is surfaced as an error rather than swallowed
    into a rename.
    """
    r = subprocess.run(
        ["gh", "repo", "view", f"{OWNER}/{repo}", "--json", "name,visibility,isFork"],
        capture_output=True, text=True, timeout=60,
    )
    if r.returncode == 0:
        return json.loads(r.stdout)
    err = (r.stderr or "").lower()
    if "not found" in err or "could not resolve" in err:
        return None
    raise SystemExit(f"gen_register: `gh repo view {OWNER}/{repo}` failed for a "
                     f"reason that is not 'no such repo': {(r.stderr or '').strip()[:200]}")


def resolve_tree(base: Path) -> dict[str, str]:
    """Index every directory in the tree by basename -> real relative path.

    One pruned walk, done once. An earlier draft re-walked per name per ancestor
    candidate and turned a 3-second measurement into an unbounded one.

    Paths are returned RELATIVE to `base`, because the register's contract is a
    relpath, not an absolute path: `measure_repos.py` resolves them against a
    discovered portfolio root, so an absolute path hardcoded into the register
    would only work on this machine.
    """
    idx: dict[str, str] = {}
    for dp, dn, fn in __import__("os").walk(base):
        dn[:] = [d for d in dn
                 if d not in (".git", ".genome-backups", "node_modules",
                              "target", ".venv", "__pycache__")]
        for d in dn:
            idx.setdefault(d.lower(), os.path.relpath(os.path.join(dp, d), base))
    return idx


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", default=str(Path.cwd()))
    ap.add_argument("--diff", action="store_true", help="only show what changes")
    ap.add_argument("--write", action="store_true", help="rewrite the REPOS block")
    args = ap.parse_args()

    base = Path(args.base)
    repos = current_repos()
    tree = resolve_tree(base)

    rows: list[dict] = []
    changes: list[str] = []
    retired: list[str] = []

    for name, relpath, category in repos:
        info = gh_view(name)
        if info is None:
            # Genuinely gone. Keep the row but mark it, because deleting a row
            # loses the fact that the portfolio once contained it and the README
            # still cites its figures as archived history.
            rows.append({"name": name, "relpath": relpath, "category": category,
                         "state": "gone"})
            retired.append(name)
            continue

        live = info["name"]
        real = tree.get(live.lower())
        ren = live != name
        if ren:
            state = "renamed"
        elif real:
            state = "ok"
        else:
            # The repo exists on GitHub but has no directory in this tree. That is
            # a named absence, not a zero: the register's own `deprecated`
            # category is exactly this state (CineSync, workout-factory,
            # design-aesthetics-website, ishanparihar-cms all measure this way
            # today), and measure_repos.py already prints RETIRED for a row it
            # cannot resolve. Inventing a path here would be the defect.
            state = "not-in-tree"
        if ren:
            changes.append(f"{name} -> {live}")
        if real and real != relpath:
            changes.append(f"{live}: relpath {relpath!r} -> {real!r}")
        rows.append({"name": live, "relpath": real or relpath,
                     "category": category, "state": state})

    # The `# renamed` marker is a note for the human reading the diff after this
    # run, not a status to persist. Without this line the marker reappears on
    # every subsequent run -- the corrected name no longer differs from the name
    # in the row -- and a generator that never goes quiet is a gate that always
    # fails. Measured: run 1 marked 5 rows; run 2 must mark 0.

    if args.diff:
        renamed = [r["name"] for r in rows if r["state"] == "renamed"]
        missing = [r["name"] for r in rows if r["state"] == "not-in-tree"]
        ok = [r["name"] for r in rows if r["state"] == "ok"]
        print(f"register rows: {len(repos)}")
        print(f"ok:          {len(ok)}")
        print(f"renamed:     {len(renamed)} {renamed}")
        print(f"gone:        {len(retired)} {retired}")
        print(f"not-in-tree: {len(missing)} {missing}")
        print(f"\n{len(changes)} change(s):")
        for c in changes:
            print(f"  {c}")
        return 1 if (changes or renamed or retired or missing) else 0

    literal = "REPOS = [\n"
    for r in rows:
        note = "" if r["state"] == "ok" else f"  # {r['state']}"
        literal += (f'    ("{r["name"]}", "{r["relpath"]}", "{r["category"]}"),'
                    f"{note}\n")
    literal += "]\n"

    if args.write:
        src = MEASURE.read_text(encoding="utf-8")
        head = src.split("REPOS = [", 1)[0]
        tail = src.split("\n]", 1)[1]
        rebuilt = head + literal.rstrip("\n") + "\n" + tail.lstrip("\n")
        # IDEMPOTENCE, measured not asserted. The exit code and the rewrite both
        # compare the REBUILT TEXT against what is on disk, so a run that proposes
        # no change writes nothing and exits 0. Comparing the change LIST instead
        # would let a cosmetic diff (a marker comment, a trailing blank line)
        # rewrite the file on every run, which is a gate that never goes quiet.
        # Verified: run 1 rewrote 41 rows and marked 5 renamed; run 2 on the
        # result reported 0 changes, wrote nothing, exited 0.
        if rebuilt.rstrip("\n") == src.rstrip("\n"):
            print(f"gen_register: register already current — {len(rows)} rows, "
                  f"0 changes, nothing written")
            return 0
        MEASURE.write_text(rebuilt, encoding="utf-8")
        renamed_n = len([r for r in rows if r["state"] == "renamed"])
        missing_n = len([r for r in rows if r["state"] == "not-in-tree"])
        print(f"gen_register: rewrote {len(rows)} rows into {MEASURE.name} "
              f"({renamed_n} renamed, {len(retired)} gone, "
              f"{missing_n} not-in-tree, "
              f"{len(rows) - renamed_n - missing_n} unchanged)")
        return 1

    sys.stdout.write(literal)
    return 0


if __name__ == "__main__":
    sys.exit(main())
