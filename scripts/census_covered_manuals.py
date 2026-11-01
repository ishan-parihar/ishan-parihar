#!/usr/bin/env python3
"""Citation census: which manuals are load-bearing, and which are unguarded.

WHY THIS EXISTS. The doc-drift guardrail (`W401`-`W404`) only reaches manuals
that declare `covers:` in their front-matter. Measured across every repo with a
`genome.toml`:

    repos with a genome.toml        80
    repos declaring covers:          4   (automaton 3, deckmill 2, mysterium 1)
    total covered manuals           12
    repos declaring nothing         76

The other 76 are a silent blind spot: the kernel cannot flag drift in a manual
that declares nothing, because nothing is declared to break. That is the
fleet's largest documentation gap, and it is invisible precisely because
nothing fires.

THE OBVIOUS FIX IS THE WRONG ONE. Adding `covers:` to 76 repos mechanically
would give every manual a glob and every glob a `verified` sha nobody reviewed,
which fires W402 on all of them. A fleet that cries wolf on 76 repos is worse
than a blind spot: the warnings get ignored, and the four repos where the
mechanism already works (automaton caught four real defects at `33dd3eb`) lose
their signal to the noise.

SO THE CENSUS MEASURES CITATION, NOT SIZE. A manual is load-bearing when
something else points at it: a README, an INDEX, a PAGE-INDEX, or an AGENTS.md
links to it. Citation is the fleet's own existing declaration of importance,
which means declaring `covers:` on a cited manual is a repair the fleet already
asked for, not a new policy.

THREE COUNTING TRAPS, all hit and all recorded here so the next run does not
re-hit them:

  1. THE FLEET ROOT IS A GENOME REPO WHOSE TREE CONTAINS EVERY OTHER GENOME
     REPO. Walking the root descends into automaton, so automaton's manuals are
     visited twice and the W404 report lists a manual the kernel itself passes.
     Fixed by pruning the other roots during the walk. The root repo's own
     lint reports 0 cover-related findings precisely because it declares none
     of its own -- the 6 it appears to hold are automaton's, deckmill's and
     mysterium's seen from above.
  2. THE MANIFEST'S third_party FLAG MUST BE HONOURED AT THE DIRECTORY LEVEL,
     not just the repo level, because the flagged repos are NESTED. A first run
     ranked `deepseek-harness/packages/client/ui-conversation/README.md` as the
     fleet's most-cited manual at 19 citations, which is DeepSeek's
     documentation.
  3. `covers:` IS A LIST WITH QUOTES. The kernel splits on commas and brackets
     and strips quotes (`18c_federation.py:98`); matching the raw string makes
     every manual report W404.

The number that matters: **12 total, 6 unique first-party.** The 12 counts the
fleet root's view of the same 6 manuals, so a fleet-wide "declaring covers:" of
12 is the same 6 counted twice. This script reports the 6, and names the 4
repos holding them.

Usage:
    python3 scripts/census_covered_manuals.py                 # whole fleet
    python3 scripts/census_covered_manuals.py --repo PATH     # one repo
    python3 scripts/census_covered_manuals.py --top 20        # the 20 most cited

Exit 0 when the census completes. The output is a ranking to act on, not a pass
or fail -- this is a measurement, and the rollout it recommends is a ruling.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Where a manual is cited FROM. These are the surfaces a reader actually reaches
# a manual through, which is what makes it load-bearing rather than merely
# present.
CITING_SURFACES = ("README.md", "PAGE-INDEX.md", "INDEX.md", "AGENTS.md",
                   "AGENTS_CN.md", "TEMPLATE.md")

# Front-matter fields the kernel reads, so the census uses the same source.
COVERS_RE = re.compile(r"^covers:\s*(.+)$", re.M)
VERIFIED_RE = re.compile(r"^verified:\s*(.+)$", re.M)

SKIP_DIRS = {".git", ".genome-backups", "node_modules", "target", ".venv",
             "__pycache__", ".svelte-kit", "dist", "build", ".next", "vendor",
             ".agents", ".devin", ".genome"}

# The first-party rule, already documented in measure_repos.py: vendored and
# upstream code is excluded from every metric, because counting it would
# double-count the same code across repos and pollute the signal. A census that
# ranks `deepseek-harness/packages/client/README.md` as the fleet's most-cited
# manual is measuring DeepSeek's documentation. The manifest carries
# `third_party`, which is the fleet's own declaration, so it is the source.
THIRD_PARTY_HINT = "third_party"


def is_third_party(path: Path, manifest: dict[str, bool]) -> bool:
    return manifest.get(str(path), False)

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def is_manual(path: Path) -> bool:
    return path.suffix == ".md"


def front_matter(text: str) -> str:
    """The YAML header, if the file has one. Cheap read, not a YAML parse."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1]
    return ""


def rel_references(text: str) -> list[str]:
    """Every relative .md link target in a document, normalised to a path."""
    out = []
    for m in MD_LINK_RE.finditer(text):
        tgt = m.group(1).strip()
        if tgt.startswith(("http://", "https://", "mailto:", "#")):
            continue
        tgt = tgt.split("#", 1)[0].strip()
        if tgt and (tgt.endswith(".md") or "/" in tgt):
            out.append(tgt)
    return out


def matches_glob(target: str, manual: Path, root: Path) -> bool:
    """Does a covers: glob actually match a tracked file? (the W404 question)

    MEASURED, and the first attempt was wrong: `covers` globs name CODE the
    manual covers, not the manual itself, and the kernel matches them against
    TRACKED FILE PATHS with its own glob dialect
    (`project-genome/src/05_pointers.py: gmatch` -- `**/` for zero or more
    segments, `*` within a segment, a leading `/` anchored at the root). A first
    draft matched the pattern against `manual.name`, so every one of the 12
    declared manuals reported W404 -- including the ones the kernel itself
    passes, because `crates/**` is not the name of any manual.
    """
    try:
        r = subprocess.run(["git", "-C", str(root), "ls-files"],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            return True  # not a git repo; do not claim a match failure
        tracked = [f for f in r.stdout.splitlines() if f]
    except Exception:
        return True

    # Reimplement gmatch's dialect rather than shelling to it, so the census
    # stays a pure measurement with one dependency.
    pat = target[1:] if target.startswith("/") else target
    rx = "".join(
        "(?:.*/)?" if tok == "**/" else ".*" if tok == "**" else
        "[^/]*" if tok == "*" else "[^/]" if tok == "?" else re.escape(tok)
        for tok in re.findall(r"\*\*/?|\*|\?|[^*?]+", pat)
    )
    return any(re.fullmatch(rx, f) for f in tracked)


def covers_globs(raw: str) -> list[str]:
    """Split a `covers:` value the way the kernel does.

    `project-genome/src/18c_federation.py:98`: split on commas and YAML list
    brackets, then strip quotes and whitespace. A `covers:` value is usually a
    LIST (`"a/**,b/**"` or `[a, b]`), and the first draft matched the whole raw
    string as one glob -- quotes included, since the front-matter is
    `covers: "crates/**"` -- so every one of the 12 declared manuals reported
    W404 while the kernel passed them. Verified against the kernel's own output:
    it reports W401 stale for `docs/ARCHITECTURE.md` and lists `crates/
    automaton-cli/Cargo.toml` as a changed covered path, so `crates/**` does
    match.
    """
    return [c.strip().strip('"\'')
            for c in re.split(r"[,\[\]]", raw)
            if c.strip().strip('"\'')]


def census_repo(root: Path, skip_names: set[str] | None = None,
                other_roots: set[Path] | None = None) -> list[dict]:
    """Every front-matter manual in this repo, with its citation count and covers: state.

    `skip_names` prunes directory BASENAMES during the walk, for the nested
    third-party repos (see the note in main()).

    `other_roots` prunes the OTHER genome repos, which matters because the fleet
    root is itself a genome repo whose tree contains every other genome repo.
    Without this a single census visits automaton's five manuals twice -- once as
    automaton and once as part of the root -- and the duplicated ARCHITECTURE.md
    row makes the W404 report list a manual that the kernel itself passes.
    """
    skip = set(SKIP_DIRS) | (skip_names or set())
    others = {str(p) for p in (other_roots or set())}

    def descend(dp: str, dn: list[str]) -> None:
        keep = []
        for d in dn:
            full = str((Path(dp) / d).resolve())
            if d in skip or full in others:
                continue
            keep.append(d)
        dn[:] = keep

    rows: list[dict] = []
    manuals: list[Path] = []
    for dp, dn, fn in os.walk(root):
        descend(dp, dn)
        for f in fn:
            if f.endswith(".md"):
                manuals.append(Path(dp) / f)

    # citation count, per manual, from the surfaces that link it
    citations: dict[str, set[str]] = {}
    for surface in CITING_SURFACES:
        for dp, dn, fn in os.walk(root):
            descend(dp, dn)
            if surface not in fn:
                continue
            src = Path(dp) / surface
            try:
                text = src.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for ref in rel_references(text):
                resolved = (src.parent / ref).resolve()
                citations.setdefault(str(resolved), set()).add(str(src))

    # Dedupe the citing surfaces by their identity, not their basename: two
    # different repos both have a README.md and they are different declarations.
    # The set above already holds distinct paths, so `citations` is right; the
    # bug was in the reporting, which printed every element of a set of paths as
    # if each were a separate citation. Fixed by reporting the set's size and
    # NAMING the source, which is what makes the ranking actionable.

    for manual in manuals:
        text = manual.read_text(encoding="utf-8", errors="replace")
        fm = front_matter(text)
        if not fm:
            continue  # not a genome manual (no front-matter to declare covers)
        cov = COVERS_RE.search(fm)
        ver = VERIFIED_RE.search(fm)
        globs = covers_globs(cov.group(1)) if cov else []
        row = {
            "path": str(manual),
            "rel": manual.relative_to(root).as_posix() if manual.is_relative_to(root) else str(manual),
            "covers": cov.group(1).strip() if cov else None,
            "globs": globs,
            "verified": ver.group(1).strip().strip('"\'') if ver else None,
            "citations": len(citations.get(str(manual.resolve()), ())),
            "cited_from": sorted(os.path.basename(p)
                                 for p in citations.get(str(manual.resolve()), ())),
        }
        if globs:
            row["w404"] = not any(matches_glob(g, manual, root) for g in globs)
        rows.append(row)
    return rows


def third_party_paths(base: Path) -> set[str]:
    """The repo paths the manifest itself flags `third_party`, as absolute paths.

    The manifest is the fleet's own declaration, so it is the source rather than
    a heuristic on directory names. Measured consequence of skipping this: a
    first run ranked `deepseek-harness/packages/client/ui-conversation/
    README.md` as the fleet's most-cited manual at 19 citations -- which is
    DeepSeek's documentation, not this portfolio's.
    """
    out: set[str] = set()
    for cand in (base / "fleet" / "manifest.json",
                 base.parent / "fleet" / "manifest.json"):
        if not cand.is_file():
            continue
        try:
            data = json.loads(cand.read_text(encoding="utf-8"))
        except Exception:
            continue
        root_of_manifest = cand.parent.parent
        for r in data.get("repos", []):
            if r.get("third_party"):
                out.add(str((root_of_manifest / r["path"]).resolve()))
        return out
    return out


def discover_roots(base: Path) -> list[Path]:
    """Every repo declaring a genome.toml, minus the tree's third-party repos."""
    tp = third_party_paths(base)
    roots: list[Path] = []
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        if "genome.toml" in fn:
            rp = Path(dp).resolve()
            if rp in tp or any(str(rp).startswith(t + os.sep) for t in tp):
                continue
            roots.append(rp)
    return roots


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", action="append", default=None,
                    help="restrict to this repo (repeatable)")
    ap.add_argument("--top", type=int, default=25,
                    help="how many of the most-cited to show")
    args = ap.parse_args()

    base = Path.cwd()
    if args.repo:
        roots = [Path(p).resolve() for p in args.repo]
    else:
        roots = discover_roots(base)

    # THIRD-PARTY, at the directory level. discover_roots drops repos the
    # manifest flags, but the flagged repos are nested INSIDE portfolio repos
    # (`agentic-harness/external-repos/deepseek-harness` lives under
    # `agentic-harness`, which is itself a genome repo), so a per-repo walk
    # descends into them unless the names are pruned during the walk. Measured:
    # excluding only at the root level still ranked deepseek's
    # `ui-conversation/README.md` first at 19 citations, so the exclusion has to
    # happen where the walk happens.
    tp = third_party_paths(base)
    tp_names = {Path(t).name for t in tp}

    all_rows: list[dict] = []
    for r in roots:
        all_rows.extend(census_repo(Path(r), skip_names=tp_names,
                                    other_roots=set(roots) - {Path(r)}))

    declared = [x for x in all_rows if x["covers"]]
    undeclared = [x for x in all_rows if not x["covers"]]
    cited_undeclared = [x for x in undeclared if x["citations"] > 0]
    w404 = [x for x in declared if x.get("w404")]

    print(f"repos scanned:            {len(roots)}")
    print(f"manuals with front-matter: {len(all_rows)}")
    print(f"  declaring covers:        {len(declared)}")
    print(f"  declaring nothing:       {len(undeclared)}")
    print(f"  of those, CITED by another surface: {len(cited_undeclared)}  <-- the actionable set")
    print(f"  covers globs matching nothing (W404): {len(w404)}")
    if w404:
        for x in w404:
            print(f"      W404 {x['rel']}: covers {x['globs']} matches no tracked file")

    print(f"\n=== the {args.top} most-cited manuals that declare NO covers ===")
    for x in sorted(cited_undeclared, key=lambda r: -r["citations"])[:args.top]:
        print(f"  {x['citations']:3} citation(s) from {','.join(x['cited_from']) or '-'}")
        print(f"      {x['rel']}")

    print(f"\n=== the {args.top} most-cited manuals that DO declare covers ===")
    for x in sorted(declared, key=lambda r: -r["citations"])[:args.top]:
        print(f"  {x['citations']:3} citation(s) {x['rel']}  covers={x['globs']} "
              f"verified={x['verified'] or '(none)'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
