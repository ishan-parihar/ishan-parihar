#!/usr/bin/env python3
"""Fail-closed checks on README.md rendering and private-repo honesty.

Written 2026-11-02 after the operator read the rendered page and reported that
"the links on the markdown render are leaking its formatting and are not showing
the output correctly".  Both defects it now guards were found by MEASUREMENT, not
inspection, so both guards are proven to fire on an injected defect before this
check is called clean:

  A. Markup leak inside <details>.
     Root cause, measured against GitHub's own renderer (`gh api -X POST markdown`,
     the same endpoint the site uses, rather than a local parser that renders it
     fine): GitHub stays in raw-text mode for the rest of a <details> block when an
     HTML <br> sits between </summary> and the list.  With <br>, all 57 rows
     emitted the literal string `* **[name](<a href="url">url</a>)**` and NO link
     rendered.  Replacing <br> with one empty line gave 0 leaks and 63 rendered
     links.  Injected-defect proof: inserting a <br> back into one block makes
     this check exit 1.

  B. A private repo presented without a lock.
     Measured with `gh api repos/ishan-parihar/<name>` over every link the page
     emits: 12 of 63 repos are private, and six of them (the software repos,
     including the operator's flagship sourcehound) carried no marker, so a reader
     followed a link straight to a 404.  The six web portfolios were already
     locked.  The row opener now emits the lock from this same GitHub measurement.
     Injected-defect proof: deleting one 🔒 makes this check exit 1.

Also asserted: the 400-line rubric cap the page is deliberately written against.

Exit 0 = clean, 1 = defect found, 2 = could not measure.
Requires `gh` on PATH and network access; it fails closed if either is missing.
"""
import json
import re
import subprocess
import sys

README = "README.md"
OWNER = "ishan-parihar"
MAX_LINES = 400


def github_render(readme_text: str) -> str:
    """Render with GitHub's real endpoint, so the check sees what readers see."""
    try:
        p = subprocess.run(
            ["gh", "api", "-X", "POST", "markdown", "-f", "text=-"],
            input=readme_text, capture_output=True, text=True, timeout=180,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        sys.stderr.write(f"check_readme_render: could not reach GitHub: {exc}\n")
        sys.exit(2)
    if p.returncode != 0:
        sys.stderr.write(f"check_readme_render: render failed: {p.stderr.strip()}\n")
        sys.exit(2)
    return p.stdout


def visibility(readme_text: str):
    """repo -> visibility, from GitHub.  A 404 is kept, never silently dropped."""
    repos = sorted(set(re.findall(
        rf"github\.com/{OWNER}/([A-Za-z0-9_.-]+)\)", readme_text)))
    out = {}
    for r in repos:
        p = subprocess.run(["gh", "api", f"repos/{OWNER}/{r}"],
                           capture_output=True, text=True, timeout=120)
        if p.returncode != 0:
            out[r] = "404"
            continue
        try:
            out[r] = json.loads(p.stdout).get("visibility", "unknown")
        except json.JSONDecodeError:
            out[r] = "unknown"
    return out


def main() -> int:
    text = open(README, encoding="utf-8").read()
    problems = []

    lines = text.count("\n") + 1
    if lines > MAX_LINES:
        problems.append(
            f"README is {lines} lines, over the {MAX_LINES}-line rubric cap "
            "the page is deliberately written against"
        )

    html = github_render(text)
    leaks = re.findall(r"\* \*\*\[", html)
    if leaks:
        problems.append(
            f"{len(leaks)} catalog row(s) render as raw markdown - markup leaks and "
            "no link renders. Cause: an HTML <br> between </summary> and the list "
            "keeps GitHub in raw-text mode. Use one empty line instead."
        )

    vis = visibility(text)
    # Web portfolios are ranked in their own table with their own lock column.
    web_locked = set(re.findall(r"^\| \U0001f512 \*\*\[([A-Za-z0-9_.-]+)\]", text, re.M))

    for r, v in sorted(vis.items()):
        if v == "private" and r not in web_locked:
            if not re.search(rf"^\* (?:~~)?\U0001f512 \*\*\[{re.escape(r)}\]", text, re.M):
                problems.append(
                    f"{r} is PRIVATE per gh api but its catalog row carries no lock - "
                    "a reader follows it to a 404."
                )
        if v == "404" and not re.search(rf"^\* ~~\U0001f512? ?\*\*\[{re.escape(r)}\]", text, re.M):
            # icode is the known case: struck through with its measurement in a
            # comment.  Any other 404 must be handled the same way, not shown live.
            problems.append(
                f"{r} returns 404 from gh api but is not struck through - it must be "
                "struck with its measurement in a comment, not shown as live."
            )

    if problems:
        for p in problems:
            print(f"FAIL {p}")
        return 1

    private = sum(1 for v in vis.values() if v == "private")
    print(f"check_readme_render: {lines}/{MAX_LINES} lines, 0 markup leaks, "
          f"{len(vis)} linked repo(s), {private} private all locked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
