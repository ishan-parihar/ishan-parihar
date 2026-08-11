#!/usr/bin/env python3
"""
Cross-repo sponsor-coverage checker.

Scans every sibling portfolio repo's README and reports any that are missing
the canonical Support & Sponsorship block (GitHub Sponsors + Razorpay).

Usage:
  python3 scripts/check_sponsor_links.py          # report gaps, exit 1 if any
  python3 scripts/check_sponsor_links.py --fix    # append the block to gaps
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTS = os.path.dirname(ROOT)  # MY-PROJECTS/

SPONSOR = "https://github.com/sponsors/ishan-parihar"
RAZORPAY = "https://rzp.io/rzp/ishan-parihar"

# Repos that are intentionally excluded (the profile repo itself, forks,
# archives, nested repos).
EXCLUDED = {
    "ishan-parihar",  # the profile README itself, not a project repo
    "HERMES/hermes-agent", "HERMES/hermes-agent-ultra", "HERMES/zeroclaw",
    "LIFEOS/c-suite-agents-mcp",  # merged into c-suite-agents
    "MCP-AND-CLIS/igs-rust/last30days-skill",  # nested skill
    "MCP-AND-CLIS/z.archive",  # archived
    "WEBSITES/webdev-portfolio/my-portfolio",  # nested portfolio
    # vendored upstream copies — never add sponsor blocks to other people's code
    "DEVELOPER-TOOLS (Deprecated\u2044Inactive)/icode/rust/references",
    "CONTENT-CREATION/openscript/third_party",
}

# Tool-state directories that are never git repos but may appear as walk roots.
SKIP_DIRS = {".git", "node_modules", "target", ".venv", "__pycache__",
             ".contexty", ".cortexkit", ".opencode", ".hive", ".memsearch"}

BLOCK = (
    "\n## \u2615 Support & Sponsorship\n\n"
    "If you find this project useful, consider supporting ongoing development:\n\n"
    f"[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?style=flat-square&logo=github)]({SPONSOR})\n"
    f"[![Donate](https://img.shields.io/badge/Donate-Razorpay-3395FF?style=flat-square)]({RAZORPAY})\n\n"
    "Your support funds new features, releases, and infrastructure for the whole ecosystem.\n"
)


def find_repos():
    repos = []
    for root, dirs, _files in os.walk(PORTS):
        # Detect a repo BEFORE pruning: .git must not be filtered out ahead
        # of the check (it lives in SKIP_DIRS for other walkers).
        if ".git" in dirs:
            rel = os.path.relpath(root, PORTS)
            if not any(rel == ex or rel.startswith(ex + os.sep) for ex in EXCLUDED):
                repos.append(rel)
            dirs.remove(".git")
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    return sorted(repos)


def main():
    fix = "--fix" in sys.argv
    gaps = []
    for rel in find_repos():
        rm = os.path.join(PORTS, rel, "README.md")
        if not os.path.isfile(rm):
            gaps.append((rel, "NO-README"))
            continue
        text = open(rm, encoding="utf-8").read()
        missing = []
        if SPONSOR not in text:
            missing.append("NO-SPONSOR")
        if RAZORPAY not in text:
            missing.append("NO-RAZORPAY")
        if missing:
            gaps.append((rel, "+".join(missing)))
            # Only auto-fix when the WHOLE canonical section is absent — if one
            # link exists, appending the full block would duplicate the section.
            if fix and len(missing) == 2:
                with open(rm, "a", encoding="utf-8") as fh:
                    fh.write("\n" + BLOCK)
                print(f"FIXED {rel}")
    if not gaps:
        print("ALL CLEAN: every repo README has GitHub Sponsors + Razorpay links")
        return 0
    print("GAPS:")
    for rel, why in gaps:
        print(f"  {rel}: {why}")
    print(f"{len(gaps)} repo(s) missing support links")
    return 1 if not fix else 0


if __name__ == "__main__":
    sys.exit(main())
