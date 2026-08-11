#!/usr/bin/env python3
"""
Objective project ranking engine — v7 (solo-dev honest: architecture &
sophistication first, zero logistics/time-based scoring).

OpenSSF-Scorecard-inspired, fully machine-measured (v7 re-audit 2026-08-12).
Criteria & weights:
  1. Architecture & Sophistication (30%)  modules, language diversity,
                                          concurrency depth, + measured
                                          advanced-engineering families
                                          (state machines, graphs, DSLs,
                                          protocols, storage, AI/ML,
                                          rendering, determinism,
                                          distributed, security, plugins)
  2. Test Rigor               (25%)  log tests + density bonus
  3. Agent Surface            (20%)  CLASS-AWARE (v6): MCP tools / CLI
                                     commands (AXI) / REST endpoints /
                                     engine binaries — per own surface
                                     class + AXI-ergonomics bonus
  4. Engineering Scale        (15%)  log LOC + module/crate count
  5. Utility & Ecosystem      (10%)  docs/README, install path, cross-repo
                                     in-degree

DELIBERATELY REMOVED (v7, 2026-08-12): Development Velocity, Release
Discipline, CI workflow count, and age-grace. These are team/company
logistics — a solo dev maintaining 40 projects cannot (and should not) ship
10 releases or 400 commits/90d per repo, and that says nothing about whether
the CODE is good. The ranking now measures what the code IS, not how often
its author poked it.

Tier thresholds (v7):
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
      * tdg — made private on GitHub and removed from the local portfolio
        (2026-08-11); tdg-rust is the canonical TDG project
      * sovereign — made private + archived on GitHub and removed from the
        local portfolio (2026-08-12); succeeded by lifeos-ops / lifeos-saas

Usage:  python3 scripts/rank_score.py [--all]
Regenerate the dataset with:  python3 scripts/measure_repos.py
"""

import math
import sys

# ---------------------------------------------------------------------------
# Measured dataset. Row:
#   name, category, loc, tests, mods, ci, c90, tags, age, langs, concur,
#   ops, soph, surface, axi, indegree, readme_lines, install, docs
# soph = measured advanced-engineering family count (0-12) from
#        scripts/soph_audit.py — code-only, count-gated. ci/c90/tags/age are
#        retained for reference but are NOT scored in v7 (logistics removed).
# categories: engine | experimental | deprecated | site | kb
# Agent surface is CLASS-AWARE (v6.1, measured 2026-08-12): ops is the count
# on the project's own surface class — mcp (MCP tool count), cli (CLI
# command count, AXI first-class), rest (HTTP endpoint count), or engine
# (runnable binary count). Projects are never zeroed for lacking MCP.
# axi = number of demonstrable AXI principles (0-6, CLI-only bonus): TOON
# output, --full escape hatch, definitive empty states, content truncation
# w/ size hint, pre-computed aggregates, structured errors/exit codes.
# Bonus: cli agent = min(10.0, curve(ops) + 0.4*min(axi, 5)).
# ---------------------------------------------------------------------------
DATA = [
    # --- engines -----------------------------------------------------------
    ("igs-rust", "engine", 27738, 231, 1, 2, 198, 15, 96, 2, 500, 91, 11, "mcp", 0, 0, 432, 1, 1),
    ("social-forge", "engine", 77836, 257, 3, 2, 479, 2, 96, 5, 500, 43, 10, "mcp", 0, 0, 557, 1, 1),
    ("operant", "engine", 538394, 9249, 19, 4, 762, 3, 116, 6, 500, 68, 12, "mcp", 0, 3, 206, 1, 1),
    ("scorestrata", "engine", 72958, 944, 12, 1, 97, 0, 9, 2, 0, 88, 9, "mcp", 0, 0, 158, 1, 1),
    ("mindstrata", "engine", 82079, 1245, 8, 1, 483, 0, 14, 1, 0, 2, 10, "cli", 3, 0, 169, 1, 1),
    ("tdg-rust", "engine", 47797, 626, 1, 1, 146, 10, 55, 3, 268, 36, 11, "mcp", 0, 0, 227, 1, 1),
    ("slideforge-rust", "engine", 35631, 185, 2, 1, 203, 6, 43, 3, 74, 8, 10, "mcp", 0, 1, 346, 1, 1),
    ("automaton", "engine", 13410, 43, 17, 2, 16, 1, 96, 2, 500, 38, 8, "mcp", 0, 0, 380, 1, 1),
    ("openscript", "engine", 74606, 510, 12, 2, 463, 0, 129, 5, 500, 109, 12, "mcp", 0, 0, 186, 1, 1),
    ("mysterium", "engine", 61428, 1090, 1, 2, 467, 0, 86, 4, 281, 9, 10, "cli", 5, 2, 584, 1, 1),
    ("andrometry", "engine", 25442, 152, 1, 1, 135, 0, 14, 4, 216, 12, 3, "rest", 0, 0, 449, 0, 1),
    ("lifeos-ops", "engine", 17760, 0, 3, 1, 98, 10, 93, 3, 488, 31, 8, "mcp", 0, 0, 324, 1, 0),
    ("c-suite-agents", "engine", 46498, 227, 1, 1, 6, 3, 130, 2, 500, 35, 10, "mcp", 0, 2, 140, 1, 1),
    ("thinking-steroid", "engine", 24997, 247, 1, 2, 16, 0, 122, 1, 18, 13, 5, "mcp", 0, 1, 229, 1, 1),
    # --- AXI CLI family (ranked this audit) --------------------------------
    ("reddit-lyr", "engine", 4430, 24, 0, 1, 51, 0, 84, 2, 222, 56, 6, "cli", 5, 0, 168, 1, 1),
    ("twitter-lyr", "engine", 13425, 243, 0, 2, 44, 32, 160, 2, 14, 42, 6, "cli", 5, 0, 483, 1, 1),
    ("instagram-lyr", "engine", 20441, 335, 0, 1, 49, 0, 485, 2, 355, 47, 6, "cli", 5, 0, 433, 1, 1),
    ("linkedin-lyr", "engine", 50739, 1166, 0, 4, 204, 94, 485, 2, 500, 25, 9, "cli", 6, 1, 379, 1, 1),
    ("facebook-lyr", "engine", 13977, 229, 0, 1, 19, 0, 7, 2, 318, 41, 5, "cli", 3, 2, 206, 1, 1),
    ("threads-lyr", "engine", 2374, 31, 0, 1, 9, 0, 1, 2, 21, 3, 3, "cli", 3, 1, 133, 1, 0),
    ("discord-cli", "engine", 3704, 15, 0, 2, 11, 10, 156, 2, 40, 13, 2, "cli", 5, 0, 333, 1, 0),
    ("tg-cli", "engine", 4828, 122, 0, 2, 12, 14, 156, 2, 34, 12, 2, "cli", 5, 0, 271, 1, 0),
    ("meme-lyr", "engine", 1050, 25, 1, 2, 14, 1, 521, 2, 28, 6, 0, "cli", 4, 0, 459, 1, 1),
    ("obscura-core", "engine", 2896, 15, 0, 1, 12, 0, 10, 1, 104, 8, 4, "mcp", 0, 4, 231, 1, 0),
    # --- experimental / archived (capped at C by policy) --------------------
    ("consciousness-fabricator", "experimental", 9238, 158, 0, 1, 7, 0, 125, 1, 73, 6, 8, "cli", 2, 1, 249, 0, 1),
    ("holosim-infinite", "experimental", 489296, 7766, 2, 2, 5, 0, 180, 2, 31, 6, 11, "engine", 0, 0, 296, 1, 1),
    ("kali-mahabali", "experimental", 63118, 690, 0, 1, 15, 1, 314, 2, 500, 20, 8, "mcp", 0, 0, 355, 1, 1),
    ("icode", "deprecated", 142819, 2095, 21, 2, 7, 0, 133, 3, 500, 10, 11, "mcp", 0, 0, 100, 0, 1),
    # --- engines added in the 2026-08-11 full-coverage pass -----------------
    ("browsefleet", "engine", 4558, 86, 4, 5, 29, 2, 130, 4, 239, 22, 5, "rest", 0, 0, 282, 1, 1),
    ("hermes-prime-bridge", "engine", 919, 14, 0, 2, 23, 1, 4, 2, 1, 3, 2, "mcp", 0, 0, 162, 1, 1),
    ("lifeos-bot", "engine", 12009, 33, 0, 2, 16, 1, 61, 2, 397, 3, 3, "cli", 2, 0, 107, 1, 1),
    # --- deprecated / inactive (capped at C by policy) -----------------------
    ("cinesync", "deprecated", 13744, 16, 2, 2, 3, 0, 298, 4, 23, 13, 5, "rest", 0, 0, 150, 1, 1),
    ("osint-os", "deprecated", 120754, 399, 1, 1, 2, 0, 406, 4, 500, 122, 9, "rest", 0, 0, 469, 1, 1),
    ("workout-factory", "deprecated", 9417, 30, 0, 1, 3, 0, 262, 2, 7, 0, 4, "engine", 0, 0, 192, 0, 1),
    # --- unranked: utility/private ------------------------------------------
    ("lifeos-saas", "engine", 760, 0, 0, 1, 4, 0, 97, 2, 15, 10, 1, "rest", 0, 0, 277, 1, 1),
    # --- websites / portfolios (separate category, never ranked) ------------
    ("design-aesthetics-website", "site", 17084, 8, 2, 1, 40, 0, 1209, 3, 58, 15, 6, "rest", 0, 0, 144, 1, 1),
    ("ishanparihar-cms", "site", 14271, 355, 1, 2, 38, 1, 126, 2, 352, 20, 3, "rest", 0, 1, 96, 1, 1),
    ("ishanparihar-svelte", "site", 64567, 666, 1, 3, 303, 0, 299, 4, 500, 4, 8, "rest", 0, 1, 203, 1, 1),
    ("law-of-one-india-website", "site", 69626, 63, 1, 1, 5, 0, 503, 3, 500, 29, 8, "rest", 0, 0, 176, 1, 1),
    ("webdev-portfolio", "site", 0, 0, 0, 1, 4, 0, 128, 0, 0, 0, 0, "engine", 0, 0, 109, 0, 0),
    ("lifeos-website", "site", 71179, 1156, 2, 1, 5, 0, 96, 3, 500, 8, 9, "rest", 0, 1, 188, 1, 1),
]

WEIGHTS = {
    "architecture": 0.30,  # sophistication families (majority) + modules + languages
    "tests":        0.25,  # test count + density
    "agent":        0.20,  # class-aware agent surface + AXI bonus
    "scale":        0.15,  # log LOC + modules
    "utility":      0.10,  # docs, install path, cross-repo in-degree
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


def s_architecture(mods, langs, concur, soph):
    """Architecture & Sophistication (v7) — the centerpiece criterion.

    Rewarded: structural depth (module/crate count), language diversity,
    concurrency/async complexity, and the measured count of advanced
    engineering families in the repo's own code (0-12): state machines,
    graphs/holonic structures, DSLs/parsers, concurrency, protocols, storage
    engines, AI/ML, rendering/audio, determinism, distributed systems,
    security, plugin systems. `soph` is machine-measured by
    `scripts/soph_audit.py` (code files only, count-gated — no README/config
    noise). A repo that is architecturally deep but young or unreleased is
    NOT penalized: that is logistics, not code quality.
    """
    # v7.1 (2026-08-12): sophistication is the centerpiece, not an afterthought.
    # The measured engineering-family count (0-12) carries the majority of the
    # architecture score; module count and language diversity are supporting
    # evidence. `concur` is deliberately NOT scored separately: concurrency is
    # already one of the 12 soph families, and the loose `measure_repos`
    # counter double-credits it (and miscredits TS repos whose `await`/
    # `async function` syntax the strict family detector never fires on).
    soph_score = min(5.0, soph * 0.42)  # 12 families -> 5.0
    mod_score = min(3.0, math.log10(mods + 1) * 1.2)
    lang_score = min(1.5, (langs - 1) * 0.5)
    return round(min(10.0, 1.0 + soph_score + mod_score + lang_score), 1)


def s_agent(ops, surface, axi=0):
    """Class-aware agent surface (v6.1) + optional AXI-ergonomics bonus.

    v6 fixed the gap where any project without `@mcp.tool` decorators scored
    0.0 on the 14% agent criterion — CLI tools (AXI: a first-class agent
    surface, often cheaper than MCP schema overhead), REST servers, and
    simulators were all silently zeroed.

    v6.1 adds an AXI-ergonomics bonus for CLI surfaces that demonstrably
    implement axi.md principles (TOON output, --full escape hatch, definitive
    empty states, truncation w/ size hint, pre-computed aggregates,
    structured errors/exit codes): cli agent = curve(ops) + 0.4*min(axi,5),
    capped at 10.0. A CLI with the same command count but agent-ergonomic
    output out-scores a bare one — the AXI thesis made measurable.

    Curves (all hard, published):
      mcp:    0|1-10->3|11-30->6|31-60->8|60+->10        (tool count)
      cli:    0|1-4->4|5-15->6|16-40->8|40+->10 + AXI    (command count)
      rest:   0|1-10->3|11-30->6|31-60->8|60+->10        (endpoint count)
      engine: 0->1 (floor)|1-3->2|4-10->3|10+->4         (runnable bins)
    """
    if surface == "engine":
        if ops <= 0:
            return 1.0
        if ops <= 3:
            return 2.0
        if ops <= 10:
            return 3.0
        return 4.0
    if surface == "cli":
        if ops <= 0:
            return 0.0
        if ops <= 4:
            base = 4.0
        elif ops <= 15:
            base = 6.0
        elif ops <= 40:
            base = 8.0
        else:
            base = 10.0
        # AXI-ergonomics bonus: +0.4 per demonstrated principle, cap +2.0
        return round(min(10.0, base + 0.4 * min(axi, 5)), 1)
    # mcp / rest share the tool/endpoint curve
    if ops <= 0:
        return 0.0
    if ops <= 10:
        return 3.0
    if ops <= 30:
        return 6.0
    if ops <= 60:
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
    print(f"{'project':<24}{'arch':>6}{'test':>6}{'agnt':>6}{'scale':>6}"
          f"{'util':>6}  {'TOTAL':>6}  tier")
    print("-" * 70)
    results = []
    for row in DATA:
        (name, cat, loc, tests, mods, ci, c90, tags, age, langs, concur,
         ops, soph, surface, axi, indegree, rl, install, docs) = row
        if cat in ("site", "kb") and not show_all:
            continue
        raw = {
            "architecture": s_architecture(mods, langs, concur, soph),
            "tests":        s_tests(tests, loc),
            "agent":        s_agent(ops, surface, axi),
            "scale":        s_scale(loc, mods),
            "utility":      s_utility(rl, install, docs, indegree),
        }
        total = round(sum(WEIGHTS[k] * v for k, v in raw.items()), 2)
        t, note = tier(total, cat)
        results.append((total, name, cat, raw, t, note))
        print(
            f"{name:<24}{raw['architecture']:>6}{raw['tests']:>6}{raw['agent']:>6}"
            f"{raw['scale']:>6}{raw['utility']:>6}  {total:>6.2f}  {t}"
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
        print(f"  {k:<14} {v*100:.0f}%")
    print("  (removed v7: velocity, releases, CI count, age-grace — logistics)")


if __name__ == "__main__":
    main()
