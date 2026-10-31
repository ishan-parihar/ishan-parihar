#!/usr/bin/env python3
"""Repo-link liveness gate: every github.com/<owner>/<repo> URL in a README must resolve.

WHY THIS EXISTS. `lint_readmes.py` grades the profile README on twelve structural
conventions (hero present, contact link present, support block, line ceiling). It never
resolves a URL. So the profile README graded **12.00 / ALL CLEAN** on 2026-10-31 while
four of its repo links pointed at repositories that had been renamed:

    the README said   GitHub said      evidence
    social-forge      switchpost       HTTP 301
    tg-cli            tg-lyr           HTTP 301
    discord-cli       discord-lyr      HTTP 301
    slideforge-rust   deckmill         HTTP 301

A rename on GitHub is silent for a while: the old URL keeps redirecting, so a browser
follows it happily while a link checker that treats a redirect as success does not flag
anything. The damage lands when a recruiter reads "tg-cli" in a table and searches GitHub
for exactly that string and finds nothing, or when the README's own tier table and the
repo it names disagree. This check treats a redirect as a verdict: a 301 from a repo URL
means the name in the document is stale, and that is a finding.

DESIGN. The check is deliberately narrow and deliberately offline-capable:

  - It only looks at `github.com/<owner>/...` URLs, in Markdown link syntax. The profile
    README's other links (ishanparihar.com, LinkedIn, shields.io badges, rzp.io) are not
    repo links and are out of scope.
  - A redirect (301/302/307/308) is reported as STALE with the target named, because the
    document's claim is what changed, not the remote's existence.
  - A 404 is reported as DEAD.
  - Resolution is done with `gh repo view` when available (it is the same credential the
    rest of this surface already uses) and falls back to a HEAD request via `curl`. Both
    paths are measured, not assumed: `gh repo view` exits 1 for a missing repo and prints
    nothing, and curl's `-o /dev/null -w '%{redirect_url}'` emits the Location target.
  - FAIL CLOSED. If neither resolver works, the check reports that it could not verify
    rather than passing. A link gate that passes when it did not run is the exact failure
    this surface has been bitten by before, and it is worse than no gate.

  - A link to a repo that really is gone may be kept, but only with a visible marker on
    the SAME LINE naming it retired (`retired-link:`). Without the marker a dead link and
    a dead link someone forgot about are indistinguishable, and a gate with a silent
    allowlist is a gate that can be edited into passing. The one live case is `icode`,
    which the README already describes as archived with a figure that cannot be
    re-measured.

Usage:
    python3 scripts/check_repo_links.py                 # check this repo's README.md
    python3 scripts/check_repo_links.py PATH [PATH ...] # check specific files
    python3 scripts/check_repo_links.py --owner ishan-parihar   # override the owner

Exit 0 only when every repo URL resolves directly. Exit 1 on any DEAD or STALE link.
Exit 2 when the check could not run at all (no resolver), so a broken gate is visible
rather than silent.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_OWNER = "ishan-parihar"

# A repo URL in markdown: the URL itself, captured without the trailing punctuation.
REPO_URL_RE = re.compile(
    r"https://github\.com/(" + re.escape(DEFAULT_OWNER) + r")/([A-Za-z0-9_.\-]+)"
)

# A line marked `retired-link:` is declaring, in the document itself, that this URL
# points at a repo that is deliberately gone. The marker is the escape hatch and it is
# visible, so a reader sees the declaration rather than trusting a hidden allowlist.
RETIRED_MARKER = "retired-link:"

REDIRECT_CODES = {"301", "302", "307", "308"}


def find_repo_urls(paths: list[Path], owner: str) -> list[tuple[str, str]]:
    """Return (repo_name, file) for every distinct repo URL found, in first-seen order."""
    pat = re.compile(
        r"https://github\.com/(" + re.escape(owner) + r")/([A-Za-z0-9_.\-]+)"
    )
    seen: dict[str, str] = {}
    for p in paths:
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            for m in pat.finditer(line):
                if RETIRED_MARKER in line:
                    continue
                seen.setdefault(m.group(2), str(p))
    return sorted(seen.items(), key=lambda kv: kv[0])


def resolve_with_gh(repo: str, owner: str) -> tuple[str, str]:
    """Resolve one repo. Returns (status, detail) where status is OK|DEAD|STALE|UNKNOWN.

    MEASURED, NOT ASSUMED (2026-10-31): `gh repo view` FOLLOWS a GitHub rename and
    reports the *new* name, so it exits 0 for `ishan-parihar/tg-cli` and returns
    `{"name": "tg-lyr"}`. Checking only the exit code would therefore miss every rename
    in the portfolio — which is precisely the defect this gate exists to catch, and a
    first draft of this check did exactly that (it reported 1 finding, `icode`, on a
    README with four stale names).

    So the verdict is the NAME, not the exit code: if `gh` resolves the URL to a repo
    whose name is not the name the document claims, the document is stale and the new
    name is the actionable detail. Measured on the four known renames:

        asked          gh resolves to   verdict
        social-forge   switchpost       STALE
        tg-cli         tg-lyr           STALE
        discord-cli    discord-lyr      STALE
        slideforge-    deckmill         STALE
        switchpost     switchpost       OK
    """
    target = f"{owner}/{repo}"
    r = subprocess.run(
        ["gh", "repo", "view", target, "--json", "name,url"],
        capture_output=True, text=True, timeout=60,
    )
    if r.returncode != 0:
        # gh exits 1 for a missing repo, and also for auth/network problems. Those are
        # different failures and conflating them would let a credential problem read as a
        # dead link.
        err = (r.stderr or r.stdout or "").strip()
        low = err.lower()
        if "could not resolve" in low or "not found" in low \
                or ("graphql" in low and "not found" in low):
            return "DEAD", "gh repo view: repository not found"
        return "UNKNOWN", err[:200] or f"gh repo view exit {r.returncode}"
    # The exit code is 0. Now ask which name came back, because that is the verdict.
    try:
        import json
        payload = json.loads(r.stdout or "{}")
    except Exception as exc:
        return "UNKNOWN", f"unparseable gh output: {exc}"
    actual = payload.get("name") or ""
    url = payload.get("url") or ""
    if not actual:
        return "UNKNOWN", "gh returned no repo name"
    if actual.lower() != repo.lower():
        return "STALE", f"gh resolves {owner}/{repo} -> {actual}"
    del url
    return "OK", f"resolves to {target}"


def resolve_with_curl(repo: str, owner: str) -> tuple[str, str]:
    """HEAD the repo URL. A redirect means the name is stale; a 404 means dead."""
    url = f"https://github.com/{owner}/{repo}"
    r = subprocess.run(
        ["curl", "-s", "-o", "/dev/null",
         "-w", "%{http_code} %{redirect_url}",
         "-L", "--max-redirs", "0", url],
        capture_output=True, text=True, timeout=60,
    )
    out = (r.stdout or "").strip()
    if not out:
        return "UNKNOWN", "curl returned no status line"
    code, _, location = out.partition(" ")
    if code == "200":
        return "OK", "HTTP 200"
    if code in REDIRECT_CODES:
        return "STALE", f"HTTP {code} -> {location or '(no Location)'}"
    if code == "404":
        return "DEAD", "HTTP 404"
    return "UNKNOWN", f"HTTP {code}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", help="files to scan (default: README.md here)")
    ap.add_argument("--owner", default=DEFAULT_OWNER)
    args = ap.parse_args(argv)

    paths = [Path(p) for p in args.paths] or [Path("README.md")]
    pairs = find_repo_urls(paths, args.owner)
    if not pairs:
        # No repo links is not a pass here: the check exists because the profile README
        # is almost entirely repo links, so finding zero means either the file moved or
        # the regex stopped matching. Named absence, and it fails closed.
        print("check_repo_links: no github.com/%s/... links found in %s"
              % (args.owner, ", ".join(str(p) for p in paths)))
        return 2

    use_gh = shutil.which("gh") is not None
    use_curl = shutil.which("curl") is not None
    if not use_gh and not use_curl:
        print("check_repo_links: FAIL CLOSED — neither `gh` nor `curl` is on PATH, so "
              "nothing was verified and this is not a pass.", file=sys.stderr)
        return 2

    bad: list[tuple[str, str, str, str]] = []   # repo, status, detail, file
    unknown: list[tuple[str, str, str]] = []    # repo, detail, file
    for repo, where in pairs:
        if use_gh:
            status, detail = resolve_with_gh(repo, args.owner)
            if status == "UNKNOWN" and use_curl:
                status, detail = resolve_with_curl(repo, args.owner)
        else:
            status, detail = resolve_with_curl(repo, args.owner)
        if status == "OK":
            continue
        if status == "UNKNOWN":
            unknown.append((repo, detail, where))
        else:
            bad.append((repo, status, detail, where))

    for repo, status, detail, where in bad:
        print(f"  {status:6} {args.owner}/{repo}  {detail}   (in {where})")
    for repo, detail, where in unknown:
        print(f"  UNKNOWN {args.owner}/{repo}  {detail}   (in {where})")

    if unknown:
        print(f"\ncheck_repo_links: {len(unknown)} link(s) could not be verified. "
              "That is not a pass.", file=sys.stderr)

    if bad:
        print(f"\ncheck_repo_links: {len(bad)} of {len(pairs)} repo link(s) are "
              f"DEAD or STALE (a 301 means the document names an old name).", file=sys.stderr)
        return 1
    if unknown:
        return 2
    print(f"check_repo_links: {len(pairs)} repo link(s) all resolve to {args.owner}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
