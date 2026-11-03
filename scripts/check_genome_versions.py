#!/usr/bin/env python3
"""Assert every genome that reads this repo agrees about its config.

Written 2026-11-03 from a measured version split that cost me a wrong rollback.

Two `genome` binaries exist on this machine and they answer differently about
`genome.toml`:

  ~/.local/bin/genome   -> 2026.11.02-43   (first on PATH, so `genome` runs this)
  ./scripts/genome     -> 2026.11.02-65   (vendored, executable, tracked 100755)

Version numbers move: I first read the vendored copy as -60 and that was already
stale within the hour, a peer session upgrading all four vendored copies in the
fleet to -65 (byte-identical, one md5 across holon, ishan-parihar,
paperclip-zeroclaw-adapter and project-genome). This check therefore reports the
versions it MEASURES rather than asserting them here.

Run against this repo's config, `-43` raises `E017 genome.toml: unknown key [docs]`
and `... [ops] dir_globs` and makes `genome close` RED; `-60` accepts both and
reports `0 error(s)` with `close: green`. So a bare `genome` invocation in this
repo manufactures two defects that do not exist, and I acted on them: I deleted
the `integrity` module and the `[docs]`/`[ops]` sections as if the peer's config
were broken, then restored them once I measured the split. `my-projects`/ASKS.md
Q36 records the operator's decision as owed.

The repair is not to trust one binary, it is to see the disagreement. This check
runs every genome that can read the repo, lints its genome.toml with each, and
fails when the answers differ - so the next version gap is visible as a version
gap rather than as a config defect someone "fixes".

Exit 0 = all binaries agree (or no binary is installed), 1 = they disagree.
"""
import shutil
import subprocess
import sys
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def version_of(binary):
    p = subprocess.run([binary, "--version"], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else "?"


def lint(binary):
    """(ok, verdict) for `genome lint` in this repo, via that binary.

    `ok` is False when the binary could not lint at all: the stale `-43` copy
    exits 1 with a single line on stderr -- `genome: unknown module(s) in config:
    ['integrity'] (known: ...)` -- and never reaches the lint phase. That is a
    stronger signal than a disagreement, so it must not be collapsed into the
    same bucket: a binary that refuses the config cannot be counted as agreeing
    with one that lints it.
    """
    p = subprocess.run([binary, "lint"], cwd=REPO, capture_output=True, text=True)
    if p.returncode != 0 and "unknown module" in (p.stdout + p.stderr):
        return False, "cannot parse config: " + (p.stderr.strip() or p.stdout.strip())
    tail = [l for l in (p.stdout + p.stderr).splitlines()
            if l.strip() and ("lint:" in l or "E0" in l)]
    return True, (" | ".join(tail[-1:]) if tail else "(no findings)")


def main() -> int:
    candidates = []
    vendored = os.path.join(REPO, "scripts", "genome")
    if os.access(vendored, os.X_OK):
        candidates.append(vendored)
    for name in ("genome",):
        found = shutil.which(name)
        if found and os.path.realpath(found) != os.path.realpath(vendored):
            candidates.append(found)
    installed = os.path.join(os.path.expanduser("~"), ".local", "bin", "genome")
    if os.path.exists(installed) and os.path.realpath(installed) not in {os.path.realpath(c) for c in candidates}:
        candidates.append(installed)

    if not candidates:
        print("check_genome_versions: no genome binary found, nothing to compare")
        return 0

    results = {}
    for b in candidates:
        ok, verdict = lint(b)
        results[b] = (version_of(b), ok, verdict)
        print(f"  {b}\n    version {results[b][0]}\n    {verdict}")

    # Disagreement is defined by the lint ANSWER, not the version string: two
    # binaries at the same version could still differ in what they read. A binary
    # that cannot parse the config at all counts as disagreeing with one that can.
    verdicts = {v[2] for v in results.values()}
    if len(verdicts) > 1:
        print("FAIL: the genome binaries that read this repo disagree:")
        for b, v in results.items():
            print(f"  {b} ({v[0]}) -> {v[2]}")
        print("      A defect reported by only one of them may be a version gap, not a")
        print("      config error. The repo pins its vendored copy, so trust that one and")
        print("      ASKS.md Q36 owns the operator's ruling on which is authoritative.")
        return 1

    print(f"check_genome_versions: {len(results)} binary(ies) agree on this repo's config")
    return 0


if __name__ == "__main__":
    sys.exit(main())
