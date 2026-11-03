#!/usr/bin/env python3
"""Audit every in-page anchor in README.md against the headings that exist.

Written 2026-11-03 after `docs_lint.py` (the portfolio's own boundary check, run
by the pre-commit hook) failed with:

    D004  README.md:72  no matching heading for anchor  (#-engineering-by-the-numbers)

That anchor was mine: I linked `#-engineering-by-the-numbers` (a leading dash for
the emoji) while the Contents entry on line 16 links
`#engineering-by-the-numbers`. Both cannot be right, and GitHub's slug for
"📊 Engineering by the Numbers" is the second. So at least one of the two links
on this page pointed nowhere, and a reader clicking it went to the top.

The rule, stated so it can be checked rather than eyeballed - and taken VERBATIM from the portfolio's own `docs_lint.py` (line 44, `gh_anchor`), which is the authority here rather than my approximation of it:

  1. lowercase and strip
  2. drop every character that is not a word char, whitespace, or a hyphen
     (this is what removes the emoji; `_` and `-` survive)
  3. replace each whitespace char with a hyphen - one per char, NOT collapsing runs
  4. strip leading/trailing hyphens

See `slug()` below for the executable form; docstring-safe because the regexes
live in code, not prose.

Two things my first version of this script got wrong, both caught by comparing
against that function: I collapsed runs of whitespace into one hyphen (GitHub
does not - "49 Ranked + 1 Struck" keeps the doubled hyphen where the `+` was
dropped), and I dropped `_` (GitHub keeps it). Both meant the checker reported
four anchors as dead that resolve fine, which would have been me "fixing"
working links. It now delegates to the same rule the portfolio's gate uses.

Other findings this surfaced when run: several headings carry a raw label (`###
[operant](https://...)`) whose slug therefore contains the URL, which is why
`docs_lint` also reports D002 advisory duplicates against docs/FLAGSHIPS.md.
Those are advisories and out of scope here - a D004 is a broken link a reader
hits, a D002 is a style preference.
"""
import re
import sys

README = "README.md"


def slug(heading: str) -> str:
    """GitHub-compatible heading id. Copied from docs_lint.gh_anchor, not guessed."""
    t = heading.lower().strip()
    t = re.sub(r"[^\w\s-]", "", t)
    t = re.sub(r"\s", "-", t)
    return "#" + t.strip("-")


def main() -> int:
    text = open(README, encoding="utf-8").read()
    slugs = {slug(h) for h in text.splitlines() if h.startswith("#")}
    anchors = sorted(set(re.findall(r"\]\((#[^)]+)\)", text)))
    bad = [a for a in anchors if a not in slugs]
    if bad:
        for a in bad:
            print(f"FAIL {README}: anchor {a} matches no heading on the page")
        print(f"      headings exist for: {', '.join(sorted(slugs))}")
        return 1
    print(f"check_anchors: {len(anchors)} in-page anchor(s) all resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
