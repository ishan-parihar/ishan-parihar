#!/usr/bin/env python3
"""
Objective project ranking engine — v5 (8 criteria, portfolio-grade).

OpenSSF-Scorecard-inspired, fully machine-measured 2026-08-11.
Criteria & weights:
  1. Engineering Scale        (12%)  log LOC + module/crate count
  2. Test Rigor               (18%)  log tests + density bonus
  3. Architectural Complexity (12%)  modules, language diversity, concurrency/async depth
  4. CI/CD Discipline         ( 8%)  GitHub Actions workflow count
  5. Release Discipline       ( 8%)  tagged releases
  6. Development Velocity     ( 8%)  age-normalized commits per 90d
  7. Agent Surface            (14%)  MCP tools / CLI surface
  8. Utility & Ecosystem      (20%)  docs/README, install path, cross-repo in-degree

Tier thresholds (v5):
  S >= 8.00  A 6.50-7.99  B 4.50-6.49  C 3.25-4.49  D < 3.25

Cap rules (documented, transparent — see RANKING-RUBRIC.md §7):
  - 'deprecated' and 'experimental' categories are capped at C (archived/inactive
    flags; promotion requires reactivation + release + agent surface). The cap is a
    ceiling: a near-zero deprecated repo keeps its natural (lower) tier.
  - 'site' and 'kb' categories are excluded from ranking entirely.
  - FIRST-PARTY RULE (2026-08-11): metrics measure the repo's own code only.
    Vendored copies (e.g. crates/toon-helper, vendored into automaton,
    social-forge, tdg-rust on 2026-08-11) are excluded by measure_repos.py —
    otherwise the same code is counted N times and its sibling-name mentions
    leak into the in-degree scan.
  - NOT RANKED (excluded, documented 2026-08-11):
      * hermes-agent, hermes-agent-ultra, zeroclaw — forks of other orgs'
        projects (nousresearch / sheawinkler / zeroclaw-labs), not original work
      * c-suite-agents-mcp — merged into c-suite-agents (repo removed from GitHub)
      * vectura-labs — deprecated website (site category, excluded)
      * embedded/vendored repos (nested .git dirs inside a ranked repo, not
        standalone portfolio projects): openscript/third_party/*,
        icode/rust/references/*, igs-rust/last30days-skill,
        MCP-AND-CLIS/z.archive/*, webdev-portfolio/my-portfolio

Usage:  python3 scripts/rank_score.py [--all]
Regenerate the dataset with:  python3 scripts/measure_repos.py
"""

import math
import sys

# ---------------------------------------------------------------------------
# Measured dataset. Row:
#   name, category, loc, tests, mods, ci, c90, tags, age, langs, concur,
#   tools, indegree, readme_lines, install, docs
# categories: engine | experimental | deprecated | site | kb
# Tool surfaces (measured 2026-08-11): @mcp.tool decorator counts for the
# Python family (production source only, tests excluded); README-listed MCP
# surfaces for Rust/TS servers; CLI command counts for CLI tools.
# ---------------------------------------------------------------------------
DATA = [
    # --- engines -----------------------------------------------------------
    ("igs-rust",           "engine",     27912,  242,   2, 2, 198, 15,  96, 2, 500, 91, 3, 432, 1, 1),
    ("social-forge",       "engine",     77836,  257,   3, 2, 478,  2,  96, 5, 500, 43, 0, 554, 1, 1),
    ("operant",            "engine",    537854, 9240,  20, 4, 758,  3, 116, 6, 500, 30, 3, 205, 1, 1),
    ("scorestrata",        "engine",     72958,  944,  12, 1,  97,  0,   8, 2,   0, 88, 0, 158, 1, 1),
    ("mindstrata",         "engine",     81638, 1238,   8, 1, 481,  0,  14, 1,   0,  0, 0, 169, 1, 1),
    ("tdg-rust",           "engine",     47797,  637,   1, 1, 145, 10,  54, 3, 268, 36, 1, 225, 1, 1),
    ("slideforge-rust",    "engine",     35805,  196,   3, 1, 203,  6,  42, 3,  74,  8, 3, 346, 1, 1),
    ("automaton",          "engine",     13410,   43,  17, 2,  16,  1,  96, 2, 500, 38, 0, 380, 1, 1),
    ("openscript",         "engine",     72430,  505,  12, 2, 456,  0, 128, 5, 500, 43, 0, 185, 1, 1),
    ("mysterium",          "engine",     61428, 1090,   1, 2, 463,  0,  85, 4, 281,  0, 1, 585, 1, 1),
    ("andrometry",         "engine",     25442,  367,   1, 1, 134,  0,  13, 4, 216, 12, 0, 449, 0, 1),
    ("lifeos-ops",         "engine",     17760,    0,   3, 1,  98, 10,  92, 3, 488, 31, 0, 324, 1, 0),
    ("c-suite-agents",     "engine",     46498,  555,   1, 1,   5,  3, 130, 2, 500, 35, 2, 139, 1, 1),
    ("thinking-steroid",   "engine",     24997,  247,   1, 2,  13,  0, 122, 1,  18, 13, 0, 219, 1, 1),
    # --- AXI CLI family (ranked this audit) --------------------------------
    ("reddit-lyr",         "engine",      4430,   24,  0, 1,  51,  0,  84, 2, 222, 56, 0, 168, 1, 1),
    ("twitter-lyr",        "engine",     13425,  243,   0, 2,  44, 32, 159, 2,  14, 42, 0, 483, 1, 1),
    ("instagram-lyr",      "engine",     20441,  335,   0, 1,  49,  0, 485, 2, 355, 47, 0, 433, 1, 1),
    ("linkedin-lyr",       "engine",     50739, 1166,   0, 4, 204, 94, 485, 2, 500, 25, 1, 379, 1, 1),
    ("facebook-lyr",       "engine",     13977,  229,   0, 1,  19,  0,   7, 2, 318, 41, 2, 206, 1, 1),
    ("threads-lyr",        "engine",      2374,   31,  0, 1,   9,  0,   1, 2,  21,  3, 1, 133, 1, 0),
    ("discord-cli",        "engine",      3704,   15,  0, 2,  11, 10, 155, 2,  40, 13, 0, 333, 1, 0),
    ("tg-cli",             "engine",      4828,  122,   0, 2,  12, 14, 155, 2,  34, 12, 0, 271, 1, 0),
    ("meme-lyr",           "engine",       899,    0,  1, 1,  12,  0, 521, 2,  28,  6, 0, 459, 1, 1),
    ("obscura-core",       "engine",      2896,   15,  0, 1,  12,  0,  10, 1, 104,  8, 4, 231, 1, 0),
    # --- experimental / archived (capped at C by policy) --------------------
    ("consciousness-fabricator", "experimental", 9238, 158, 0, 1, 6, 0, 125, 1, 73, 0, 1, 249, 0, 0),
    ("holosim-infinite",   "experimental", 489296, 7766, 2, 2, 5, 0, 180, 2, 31, 0, 0, 296, 1, 1),
    ("kali-mahabali",      "experimental",  63118,  690, 0, 1, 15, 1, 314, 2, 500, 20, 0, 355, 1, 1),
    ("icode",              "deprecated",   142819, 2095, 21, 2, 7, 0, 132, 3, 500, 10, 0, 100, 0, 1),
    # --- engines added in the 2026-08-11 full-coverage pass -----------------
    ("browsefleet",        "engine",      4254,   50,  4, 5,  28,  2, 130, 4, 219,  0, 0, 282, 1, 1),
    ("hermes-prime-bridge","engine",       919,   14,  0, 1,  22,  0,   4, 2,   1,  0, 0, 162, 1, 1),
    ("lifeos-bot",         "engine",     11857,   17,  0, 1,  15,  0,  61, 2, 397,  0, 0, 107, 1, 1),
    # --- deprecated / inactive (capped at C by policy) -----------------------
    ("cinesync",           "deprecated", 13744,   16,  2, 2,   3,  0, 298, 4,  23,  0, 0, 150, 1, 1),
    ("osint-os",           "deprecated",120754,  399,  1, 1,   2,  0, 405, 4, 500,  0, 1, 469, 1, 1),
    ("sovereign",          "deprecated",  9417,   30,  0, 1,   2,  0, 262, 2,   7,  0, 1, 161, 0, 1),
    ("workout-factory",    "deprecated",  9417,   30,  0, 1,   3,  0, 262, 2,   7,  0, 0, 192, 0, 1),
    ("tdg",                "deprecated",     0,    0,  0, 0,  37,  0,  92, 0,   0,  0, 0,  31, 0, 1),
    # --- unranked: utility/private ------------------------------------------
    ("lifeos-saas",        "engine",       760,    0,  0, 1,   4,  0,  96, 2,  15,  0, 0, 277, 1, 1),
    # --- websites / portfolios (separate category, never ranked) ------------
    ("design-aesthetics-website", "site", 17084,    8,  2, 1,  40,  0, 1209, 3,  58, 15, 0, 144, 1, 1),
    ("ishanparihar-cms",   "site",       14271,  355,   1, 2,  38,  1, 126, 2, 352, 20, 1,  96, 1, 1),
    ("ishanparihar-svelte","site",       64567,  666,   1, 3, 303,  0, 299, 4, 500,  4, 1, 203, 1, 1),
    ("law-of-one-india-website", "site", 69626,   63,  1, 1,   5,  0, 503, 3, 500, 29, 0, 176, 1, 1),
    ("webdev-portfolio",   "site",           0,    0,  0, 1,   4,  0, 128, 0,   0,  0, 0, 109, 0, 0),
    ("lifeos-website",     "site",       71179, 1156,   2, 1,   5,  0,  96, 3, 500,  8, 1, 188, 1, 1),
]

WEIGHTS = {
    "scale":     0.12,
    "tests":     0.18,
    "complexity": 0.12,
    "ci":        0.08,
    "releases":  0.08,
    "velocity":  0.08,
    "agent":     0.14,
    "utility":   0.20,
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


def s_complexity(mods, langs, concur):
    mod_score = min(4.0, math.log10(mods + 1) * 2.0)
    lang_score = min(3.0, (langs - 1) * 1.0)
    concur_score = min(3.0, math.log10(concur + 1) * 0.8)
    return round(min(10.0, 1.5 + mod_score + lang_score + concur_score), 1)


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


def s_utility(readme_lines, install, docs, indegree):
    readme_score = min(3.0, readme_lines / 150.0)
    install_score = 2.0 if install else 0.0
    docs_score = 1.0 if docs else 0.0
    indegree_score = min(4.0, indegree * 1.5)
    return round(min(10.0, readme_score + install_score + docs_score + indegree_score), 1)


_TIER_ORDER = {"S": 0, "A": 1, "B": 2, "C": 3, "D": 4}


def _natural_tier(total):
    if total >= 8.0:
        return "S"
    if total >= 6.5:
        return "A"
    if total >= 4.5:
        return "B"
    if total >= 3.25:
        return "C"
    return "D"


def tier(total, category):
    natural = _natural_tier(total)
    if category == "deprecated":
        if _TIER_ORDER[natural] < _TIER_ORDER["C"]:
            return "C", "capped: archived/deprecated — not promotable while inactive"
        return natural, ""
    if category == "experimental":
        if _TIER_ORDER[natural] < _TIER_ORDER["C"]:
            return "C", "capped: experimental flag — promote via release + agent surface"
        return natural, ""
    return natural, ""


def main():
    show_all = "--all" in sys.argv
    print(f"{'project':<24}{'scale':>6}{'test':>6}{'cplx':>6}{'ci':>5}{'rel':>5}"
          f"{'vel':>5}{'agnt':>6}{'util':>6}  {'TOTAL':>6}  tier")
    print("-" * 90)
    results = []
    for row in DATA:
        (name, cat, loc, tests, mods, ci, c90, tags, age, langs, concur,
         tools, indegree, rl, install, docs) = row
        if cat in ("site", "kb") and not show_all:
            continue
        raw = {
            "scale":      s_scale(loc, mods),
            "tests":      s_tests(tests, loc),
            "complexity": s_complexity(mods, langs, concur),
            "ci":         s_ci(ci),
            "releases":   s_releases(tags),
            "velocity":   s_velocity(c90, age),
            "agent":      s_agent(tools),
            "utility":    s_utility(rl, install, docs, indegree),
        }
        total = round(sum(WEIGHTS[k] * v for k, v in raw.items()), 2)
        t, note = tier(total, cat)
        results.append((total, name, cat, raw, t, note))
        print(
            f"{name:<24}{raw['scale']:>6}{raw['tests']:>6}{raw['complexity']:>6}"
            f"{raw['ci']:>5}{raw['releases']:>5}{raw['velocity']:>5}{raw['agent']:>6}"
            f"{raw['utility']:>6}  {total:>6.2f}  {t}"
        )

    print()
    print("=== SORTED RANKING ===")
    ranked = sorted(results, reverse=True)
    for i, (total, name, cat, raw, t, note) in enumerate(ranked, 1):
        extra = f"  [{note}]" if note else ""
        print(f"{i:>2}. {name:<24} {total:>6.2f}  [{t}]{extra}")

    print()
    print("=== TIER SUMMARY ===")
    tiers = {}
    for (total, name, cat, raw, t, note) in ranked:
        tiers.setdefault(t, []).append(name)
    for t in "SABC":
        print(f"{t}: {', '.join(tiers.get(t, [])) if tiers.get(t) else '(none)'}")
    print(f"D: {', '.join(tiers.get('D', [])) if tiers.get('D') else '(none)'}")
    print("EXCLUDED: websites (site) + knowledge-base (kb) + upstream forks")
    print("          + merged/embedded repos (see docstring for the full list)")

    print()
    print("=== WEIGHTS ===")
    for k, v in WEIGHTS.items():
        print(f"  {k:<10} {v*100:.0f}%")


if __name__ == "__main__":
    main()
