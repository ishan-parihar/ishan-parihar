#!/usr/bin/env python3
"""
S-Tier README linter for the ishan-parihar portfolio.

Operationalizes the readme-craft mandates + portfolio conventions encoded in
TEMPLATE.md into a machine-checkable score for every repo README under
MY-PROJECTS. Every check below maps to a TEMPLATE.md checklist item or a
readme-craft mandate, so "passing the linter" == "meets the S-grade baseline".

Checks (weight = share of the /10 score):

  S01 support block        (1.5)  GitHub Sponsors + Razorpay links present
  S02 LOC badge in sync    (1.5)  LOC badge matches scripts/check_loc_badges.py
  S03 first-screen value   (1.0)  one-sentence value statement in the first 25 lines
  S04 images & SVG clean   (1.0)  local images exist; SVG has viewBox + <title>,
                                  no <script>/<foreignObject>; alt text on HTML img
  S05 no placeholders      (1.0)  no [PLACEHOLDER]/[N]K/[OWNER]/[REPO]/your-key
                                  tokens left in the README (TEMPLATE leakage)
  S06 CI badge iff CI      (1.0)  badge present <=> .github/workflows/ exists;
                                  no stale CI badge pointing at a dead workflow
  S07 badge row            (0.5)  Language / LOC / License / Status badges present
  S08 length < 400 lines   (0.5)  detail belongs in docs/, not the README
  S09 no emoji headings    (0.5)  headings do not start with an emoji
                                  (the ☕ Support heading is exempt)
  S10 no Contributing/     (0.5)  dedicated files exist for those; the short
      Changelog sections          "## License" line is allowed (portfolio rule)
  S11 T2I spec at top      (0.5)  if a T2I HERO SPEC comment exists it must be
                                  the first thing (lines 1-6), not mid-file
  S12 no glued markdown    (0.5)  no "---" or text glued to a link/paragraph
                                  (missing newline artifacts)

Grading: score = earned / 12 * 10.
  S >= 9.0   A >= 7.5   B >= 6.0   C < 6.0

Active repos must reach B+ (no ERROR-severity issue, score >= 6.0) for the
lint to exit 0. Repos whose path or README marks them Deprecated/Archived/
Inactive are graded report-only at a relaxed bar (S04/S05/S06 still apply).

Usage:
  python3 scripts/lint_readmes.py              # full report, exit 1 on failing repos
  python3 scripts/lint_readmes.py --json       # machine-readable per-repo results
  python3 scripts/lint_readmes.py --repo NAME  # lint a single repo (e.g. --repo MCP-AND-CLIS/meme-lyr)
  python3 scripts/lint_readmes.py --include-profile  # also grade ishan-parihar/README.md
  python3 scripts/lint_readmes.py --root PATH  # different portfolio root
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # MY-PROJECTS/
sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_loc_badges as clb  # noqa: E402  (sibling script: LOC source of truth)

# --------------------------------------------------------------------------
# Portfolio conventions (kept in sync with check_sponsor_links.py)
# --------------------------------------------------------------------------
SPONSOR = "https://github.com/sponsors/ishan-parihar"
RAZORPAY = "https://rzp.io/rzp/ishan-parihar"

EXCLUDED = {
    "ishan-parihar",  # the profile README itself — graded separately (--include-profile)
    "HERMES/hermes-agent", "HERMES/hermes-agent-ultra", "HERMES/zeroclaw",
    "LIFEOS/c-suite-agents-mcp",  # merged into c-suite-agents
    "MCP-AND-CLIS/igs-rust/last30days-skill",  # nested skill
    "MCP-AND-CLIS/z.archive",  # archived
    "WEBSITES/webdev-portfolio/my-portfolio",  # nested portfolio
    # vendored reference repos nested inside icode (upstream copies, not ours)
    "DEVELOPER-TOOLS (Deprecated\u2044Inactive)/icode/rust/references",
    # vendored third-party repo inside openscript (upstream copy, not ours)
    "CONTENT-CREATION/openscript/third_party",
}

# Repos with no meaningful source LOC (pure-content sites) are exempt from the
# LOC badge — a "LOC-0" badge is noise, not signal.
MIN_LOC_FOR_BADGE = 500
SKIP_DIRS = {".git", "node_modules", "target", ".venv", "__pycache__",
             ".contexty", ".cortexkit", ".opencode", ".hive", ".memsearch",
             ".pytest_cache"}

DEPRECATED_MARK = re.compile(r"(deprecated|archived|inactive)", re.I)
T2I_SPEC = "T2I HERO SPEC"

# --- check weights (sum = 12.0 -> /12 * 10) ------------------------------
WEIGHTS = {
    "S01": 1.5, "S02": 1.5, "S03": 1.0, "S04": 1.0, "S05": 1.0, "S06": 1.0,
    "S07": 0.5, "S08": 0.5, "S09": 0.5, "S10": 0.5, "S11": 0.5, "S12": 0.5,
}
TOTAL_W = sum(WEIGHTS.values())

MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
HTML_IMAGE = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>", re.I)
HTML_ALT = re.compile(r"\balt=[\"']([^\"']*)[\"']", re.I)
UNSAFE_SVG_TAGS = {"script", "foreignObject"}

PLACEHOLDER_RE = re.compile(
    r"\[PLACEHOLDER\]|\[N\]K|\[OWNER\]/\[REPO\]|\[NAME\]|\[PROJECT NAME\]"
    r"|\[Owner\]|\[install command\]|\[first command\]|\[cmd\]|\[flag\]"
    r"|your-key|YOUR_KEY|your_api|API_KEY[^\n]*\bxxx\b|\[screenshot\]|\[test command\]"
)
EMOJI_HEADING_RE = re.compile(r"^#{1,3}\s+[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]")
STRAY_MD_RE = re.compile(r"\)---|[\w\]]---[\w\n]|>---")
LOC_BADGE_RE = re.compile(r"badge/LOC-([0-9]+(?:\.[0-9]+)?K?)-informational")

MAX_LINES = 400


# --------------------------------------------------------------------------
# Repo discovery
# --------------------------------------------------------------------------
def find_repos(ports: Path) -> list[str]:
    repos = []
    for root, dirs, _files in os.walk(ports):
        # Detect a repo BEFORE pruning: .git must not be filtered out ahead
        # of the check (it lives in SKIP_DIRS for other walkers).
        if ".git" in dirs:
            rel = os.path.relpath(root, ports)
            if not any(rel == ex or rel.startswith(ex + os.sep) for ex in EXCLUDED):
                repos.append(rel)
            dirs.remove(".git")
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    return sorted(repos)


def is_deprecated(repo: str, text: str) -> bool:
    if DEPRECATED_MARK.search(repo):
        return True
    head = text[:1500]
    return bool(DEPRECATED_MARK.search(head) and "deprecated" in head.lower())


# --------------------------------------------------------------------------
# Individual checks
# --------------------------------------------------------------------------
def check_support(text: str) -> list[str]:
    issues = []
    if SPONSOR not in text:
        issues.append("missing GitHub Sponsors link (S01)")
    if RAZORPAY not in text:
        issues.append("missing Razorpay donate link (S01)")
    return issues


def check_loc_sync(repo: str, readme_text: str, loc_map: dict[str, int],
                   _ports: Path) -> list[str]:
    """LOC badge present AND within tolerance of the measured source LOC."""
    issues = []
    badges = [m.group(1) for m in LOC_BADGE_RE.finditer(readme_text)]
    actual = loc_map.get(repo)
    if actual is not None and actual < MIN_LOC_FOR_BADGE:
        return []  # pure-content repo: LOC badge not meaningful, not required
    if not badges:
        return ["missing LOC badge (S07)"]
    if actual is None:
        return []  # repo not measurable (no tracked code) — skip
    for b in badges:
        parsed = clb.parse_loc_badge(b)
        if parsed is None:
            issues.append(f"LOC badge '{b}' unparseable (S02)")
            continue
        expected = clb.fmt_loc(actual)
        if clb.stale_diff(actual, parsed):
            issues.append(f"LOC badge {b} != measured {expected} (S02)")
    return issues


def check_first_screen(text: str) -> list[str]:
    head = "\n".join(text.splitlines()[:25])
    # Markdown bold, HTML <strong>/<em>, or a paragraph of plain-language value.
    has_quote_value = bool(re.search(r">\s*\*\*[^*]{10,}\*\*", head))
    has_bold = bool(re.search(r"\*\*[^*]{25,}\*\*|<!--[^*]{10,}-->", head))
    has_strong = bool(re.search(r"<strong>[^<]{15,}</strong>", head))
    has_statement = bool(re.search(r"^[A-Z][^\n]{80,}", head, re.MULTILINE))
    if not (has_quote_value or has_bold or has_strong or has_statement):
        return ["no first-screen value statement in first 25 lines (S03)"]
    return []


def audit_images(readme: Path) -> list[str]:
    text = readme.read_text(encoding="utf-8", errors="replace")
    sources = MARKDOWN_IMAGE.findall(text)
    html_tags = re.findall(r"<img\b[^>]*>", text, flags=re.I)
    sources.extend(HTML_IMAGE.findall(text))
    issues = []
    for tag in html_tags:
        m = HTML_ALT.search(tag)
        if not m or not m.group(1).strip():
            issues.append(f"HTML image missing useful alt text: {tag[:80]} (S04)")
    for src in dict.fromkeys(sources):
        if src.startswith(("http://", "https://", "data:", "#")):
            continue
        clean = src.split("#", 1)[0].split("?", 1)[0]
        target = (readme.parent / clean).resolve()
        if not target.is_file():
            issues.append(f"missing image: {src} (S04)")
            continue
        if target.suffix.lower() == ".svg":
            issues.extend(audit_svg(target, src))
    return issues


def audit_svg(path: Path, src: str) -> list[str]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"{src}: invalid SVG XML: {exc} (S04)"]
    out = []
    if "viewBox" not in root.attrib:
        out.append(f"{src}: SVG missing viewBox (S04)")
    has_title = any(n.tag.rsplit("}", 1)[-1] == "title" for n in root.iter())
    if not has_title:
        out.append(f"{src}: SVG missing <title> (S04)")
    for n in root.iter():
        tag = n.tag.rsplit("}", 1)[-1]
        if tag in UNSAFE_SVG_TAGS:
            out.append(f"{src}: SVG contains unsupported <{tag}> (S04)")
    return out


def check_placeholders(text: str) -> list[str]:
    hits = sorted(set(PLACEHOLDER_RE.findall(text)))
    if hits:
        return [f"TEMPLATE placeholder tokens left: {hits} (S05)"]
    return []


def check_ci_badge(repo: Path, text: str) -> list[str]:
    has_workflows = any(repo.glob(".github/workflows/*.yml")) or \
        any(repo.glob(".github/workflows/*.yaml"))
    has_badge = "actions/workflows" in text
    issues = []
    if has_workflows and not has_badge:
        issues.append("has .github/workflows/ but no CI badge (S06)")
    if not has_workflows and has_badge:
        issues.append("CI badge present but no .github/workflows/ exists (S06)")
    return issues


LANG_BADGES = ("Language", "Rust", "Go", "Python", "Kotlin", "TypeScript",
               "JavaScript", "Swift", "Java", "Ruby", "PHP", "Zig", "Dart",
               "HTML", "CSS", "C%2B%2B", "C++", "Solidity", "Scala", "Vue",
               "Svelte", "React", "Terraform", "Shell")
LANG_BADGE_RE = re.compile(
    r"/badge/(Language|Rust|Go|Python|Kotlin|TypeScript|JavaScript|Swift|"
    r"Java|Ruby|PHP|Zig|Dart|HTML|CSS|C%2B%2B|C\+\+|Solidity|Scala|Vue|Svelte|"
    r"React|Terraform|Shell)-", re.I)


def check_badge_row(text: str, skip_loc: bool = False) -> list[str]:
    issues = []
    if not LANG_BADGE_RE.search(text):
        issues.append("missing Language badge (S07)")
    if not skip_loc and "badge/loc-" not in text.lower():
        issues.append("missing LOC badge (S07)")
    if not re.search(r"badge/licen[cs]e-", text, re.I):
        issues.append("missing License badge (S07)")
    if not re.search(r"badge/status-", text, re.I):
        issues.append("missing Status badge (S07)")
    return issues


def check_emoji_headings(text: str) -> list[str]:
    bad = [ln.strip() for ln in text.splitlines()
           if EMOJI_HEADING_RE.match(ln) and "Support & Sponsorship" not in ln]
    if bad:
        return [f"emoji-prefixed headings: {bad[0][:40]} (S09)"]
    return []


def check_contrib_changelog(text: str) -> list[str]:
    issues = []
    for h in re.finditer(r"^##\s+(.+)$", text, re.MULTILINE):
        heading = h.group(1).strip().lower()
        if heading.startswith("contributing") or heading.startswith("changelog"):
            issues.append(f"'{h.group(1).strip()}' section — dedicated file exists (S10)")
    return issues


def check_t2i_top(text: str) -> list[str]:
    if T2I_SPEC not in text:
        return []  # optional per TEMPLATE
    line_no = next(i for i, ln in enumerate(text.splitlines(), 1)
                   if T2I_SPEC in ln)
    if line_no > 6:
        return [f"T2I HERO SPEC misplaced at line {line_no} (must be lines 1-6) (S11)"]
    return []


def check_stray_markdown(text: str) -> list[str]:
    hits = []
    for ln in text.splitlines():
        if STRAY_MD_RE.search(ln) and not ln.startswith(("```", "    ", "\t")):
            hits.append(ln.strip()[:60])
    if hits:
        return [f"glued markdown (missing newline): {hits[0]} (S12)"]
    return []


# --------------------------------------------------------------------------
# Engine
# --------------------------------------------------------------------------
def lint_repo(repo: str, ports: Path, loc_map: dict[str, int]) -> dict:
    repo_dir = ports / repo
    readme_path = repo_dir / "README.md"
    result = {"repo": repo, "score": 0.0, "grade": "F",
              "issues": {"error": [], "warn": []}, "lines": 0}
    if not readme_path.is_file():
        result["issues"]["error"].append("NO README.md (C1)")
        return result

    text = readme_path.read_text(encoding="utf-8", errors="replace")
    result["lines"] = len(text.splitlines())
    deprecated = is_deprecated(repo, text)
    result["deprecated"] = deprecated

    low_loc = loc_map.get(repo, 0) < MIN_LOC_FOR_BADGE
    checks: list[tuple[str, list[str]]] = [
        ("S01", check_support(text)),
        ("S02", check_loc_sync(repo, text, loc_map, ports)),
        ("S03", check_first_screen(text)),
        ("S04", audit_images(readme_path)),
        ("S05", check_placeholders(text)),
        ("S06", check_ci_badge(repo_dir, text)),
        ("S07", check_badge_row(text, skip_loc=low_loc)),
        ("S09", check_emoji_headings(text)),
        ("S10", check_contrib_changelog(text)),
        ("S11", check_t2i_top(text)),
        ("S12", check_stray_markdown(text)),
    ]
    if len(text.splitlines()) > MAX_LINES:
        checks.append(("S08", [f"{result['lines']} lines > {MAX_LINES} (S08)"]))

    earned = 0.0
    for code, issues in checks:
        if not issues:
            earned += WEIGHTS[code]
            continue
        # S04 (broken images) and S05 (leaked placeholders) are hard errors
        # everywhere. For deprecated repos everything else is advisory.
        if deprecated and code not in ("S04", "S05"):
            result["issues"]["warn"].extend(issues)
        elif code == "S08":
            # Length is guidance ("detail lives in docs/"), not a blocker.
            result["issues"]["warn"].extend(issues)
        else:
            result["issues"]["error"].extend(issues)

    result["score"] = round(earned / TOTAL_W * 10, 2)
    if result["score"] >= 9.0:
        result["grade"] = "S"
    elif result["score"] >= 7.5:
        result["grade"] = "A"
    elif result["score"] >= 6.0:
        result["grade"] = "B"
    else:
        result["grade"] = "C"
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="S-Tier README linter")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--repo", type=str, default=None, help="lint a single repo path")
    ap.add_argument("--include-profile", action="store_true",
                    help="also grade the profile README (ishan-parihar)")
    args = ap.parse_args()

    loc_map, _capped = clb.repo_locs(args.root)
    repos = [args.repo] if args.repo else find_repos(args.root)
    if args.include_profile:
        repos.append("ishan-parihar")

    results = [lint_repo(r, args.root, loc_map) for r in repos]
    results.sort(key=lambda r: (r["deprecated"], -r["score"]))

    # Deprecated repos are report-only: only hard errors fail them, and even
    # then only content-integrity ones (S04/S05 are the always-error checks).
    failing = [r for r in results
               if r["issues"]["error"] or (not r.get("deprecated") and r["score"] < 6.0)]

    if args.json:
        print(json.dumps({
            "count": len(results),
            "grades": {g: sum(1 for r in results if r["grade"] == g)
                       for g in ("S", "A", "B", "C")},
            "results": results,
        }, indent=2, default=str))
        return 1 if failing else 0

    print(f"S-Tier README lint — {len(results)} repos "
          f"({sum(1 for r in results if r['grade']=='S')} S, "
          f"{sum(1 for r in results if r['grade']=='A')} A, "
          f"{sum(1 for r in results if r['grade']=='B')} B, "
          f"{sum(1 for r in results if r['grade']=='C')} C)\n")
    for r in results:
        tag = "DEPRECATED " if r.get("deprecated") else ""
        print(f"[{r['grade']}] {r['score']:>5.2f}  {tag}{r['repo']}  "
              f"({r['lines']} lines)")
        for sev in ("error", "warn"):
            for msg in r["issues"][sev]:
                print(f"      {sev:>5}: {msg}")

    if failing:
        print(f"\n{len(failing)} repo(s) FAIL the S-Tier baseline "
              "(ERROR issues or score < 6.0)")
        return 1
    print("\nALL CLEAN: every active repo README meets the S-Tier baseline (B+).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
