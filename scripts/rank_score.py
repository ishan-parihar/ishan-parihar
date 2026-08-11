#!/usr/bin/env python3
"""
Objective project ranking engine — OpenSSF Scorecard-inspired methodology.
See RANKING-RUBRIC.md for the full rubric. All data measured 2026-08-11.

Usage:  python3 scripts/rank_score.py
Edit the DATA table with fresh measurements to re-rank.
"""

import math

# ---------------------------------------------------------------------------
# Measured dataset (name, LOC, tests, mods, ci, c90, rel, tools, stars, age)
# Re-audited 2026-08-11 after the version-tag + CI sprint: release counts and
# CI workflow counts live-measured. HoloOS stays the Python/Jinja knowledge
# corpus (verified against the live repo: no workflows, no tags).
# ---------------------------------------------------------------------------
DATA = [
    ("igs-rust",         27563,  231,   1,    2,   197, 15,  91,    1,    97),
    ("social-forge",     95578,  51,    1,    2,   475, 2,   43,    0,    96),
    ("operant",          537083, 8581,  18,   4,   757, 3,   30,    0,    92),
    ("scorestrata",      72958,  944,   11,   1,   93,  0,   88,    0,    9),
    ("mindstrata",       74998,  1238,  7,    1,   480, 0,   0,     0,    8),
    ("tdg-rust",         47365,  626,   6,    0,   143, 10,  36,    0,    55),
    ("slideforge-rust",  35484,  185,   1,    1,   202, 6,   8,     0,    42),
    ("automaton",        11727,  43,    15,   2,   14,  1,   38,    0,    97),
    ("openscript",       65241,  470,   9,    2,   449, 0,   10,    2,    129),
    ("mysterium",        56747,  806,   1,    2,   461, 0,   0,     0,    86),
    ("andrometry",       12244,  153,   1,    1,   133, 0,   0,     0,    14),
    ("holoos",           44879,  0,     0,    0,   95,  0,   0,     0,    101),
    ("lifeos-ops",       15265,  0,     2,    1,   97,  10,  7,     0,    93),
    ("c-suite-agents",   45493,  339,   1,    1,   3,   3,   10,    0,    130),
    ("thinking-steroid", 24997,  96,    1,    2,   12,  0,   13,    0,    123),
]

WEIGHTS = {
    "scale":      0.20,
    "tests":      0.25,
    "ci":         0.15,
    "releases":   0.15,
    "velocity":   0.15,
    "agent_surf": 0.10,
}


def s_scale(loc, mods):
    if loc <= 0:
        return 0.0
    base = min(10.0, math.log10(max(loc, 1)) * 1.9)
    mod_bonus = min(2.0, math.log10(mods + 1) * 1.5)
    return round(min(10.0, base + mod_bonus), 1)


def s_tests(tests, loc):
    if tests <= 0:
        return 0.0
    n = min(10.0, math.log10(tests) * 3.0 + 1.0)
    ratio = tests / max(loc / 1000.0, 0.1)
    r = min(2.5, ratio / 15.0)
    return round(min(10.0, n + r), 1)


def s_ci(n):
    return {0: 0.0, 1: 5.0}.get(n, 10.0)


def s_releases(n):
    if n <= 0:
        return 0.0
    if n <= 2:
        return 4.0
    if n <= 6:
        return 6.0
    if n <= 10:
        return 8.0
    return 10.0


def s_velocity(c90, age_days):
    life_units = max(age_days / 90.0, 0.05)
    norm = c90 / life_units
    if norm <= 0:
        return 0.0
    if norm < 10:
        return 2.0
    if norm < 50:
        return 4.0
    if norm < 150:
        return 6.0
    if norm < 400:
        return 8.0
    return 10.0


def s_agent(tools):
    if tools <= 0:
        return 0.0
    if tools <= 10:
        return 3.0
    if tools <= 30:
        return 6.0
    if tools <= 60:
        return 8.0
    return 10.0


def tier(total):
    if total >= 8.0:
        return "S"
    if total >= 6.5:
        return "A"
    if total >= 5.0:
        return "B"
    if total >= 3.5:
        return "C"
    return "D"


def main():
    print(f"{'project':<18}{'scale':>6}{'tests':>6}{'ci':>5}{'rel':>5}{'vel':>5}{'tools':>6}  {'TOTAL':>6}  tier")
    print("-" * 72)
    results = []
    for row in DATA:
        name, loc, tests, mods, ci, c90, rel, tools, _stars, age = row
        raw = {
            "scale":      s_scale(loc, mods),
            "tests":      s_tests(tests, loc),
            "ci":         s_ci(ci),
            "releases":   s_releases(rel),
            "velocity":   s_velocity(c90, age),
            "agent_surf": s_agent(tools),
        }
        total = round(sum(WEIGHTS[k] * v for k, v in raw.items()), 2)
        t = tier(total)
        results.append((total, name, raw, t))
        print(
            f"{name:<18}{raw['scale']:>6}{raw['tests']:>6}{raw['ci']:>5}"
            f"{raw['releases']:>5}{raw['velocity']:>5}{raw['agent_surf']:>6}"
            f"  {total:>6.2f}  {t}"
        )

    print()
    print("=== SORTED RANKING ===")
    results.sort(reverse=True)
    for i, (total, name, raw, t) in enumerate(results, 1):
        print(f"{i:>2}. {name:<18} {total:>6.2f}  [{t}]")

    print()
    print("=== TIER SUMMARY ===")
    for t in "SABC":
        members = [r[1] for r in results if r[3] == t]
        print(f"{t}: {', '.join(members) if members else '(none)'}")


if __name__ == "__main__":
    main()
