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
  Resolves the manifest by repo name against the live portfolio tree: it measures the
  repos it finds, prints `RETIRED` for the ones that are gone, and exits 2 without
  emitting a row of zeros if it resolves nothing at all. That last guard exists so a run
  on the wrong machine cannot silently replace the DATA block below with zeros.
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
    # --- engines -----------------------------------------------------------------
    ("sourcehound", "engine", 280285, 2304, 13, 2, 137, 30, 179, 4, 500, 156, 12, "mcp", 0, 2, 239, 1, 1),
    ("switchpost", "engine", 132144, 1036, 3, 2, 456, 4, 178, 5, 500, 403, 11, "mcp", 0, 4, 337, 1, 1),
    ("operant", "engine", 504966, 5691, 11, 5, 1879, 6, 199, 6, 500, 17, 12, "cli", 3, 7, 323, 1, 1),
    ("scorestrata", "engine", 72958, 944, 12, 1, 75, 0, 91, 2, 0, 1, 9, "cli", 1, 0, 161, 1, 1),
    ("mindstrata", "engine", 155412, 1696, 14, 1, 668, 0, 97, 3, 0, 1, 10, "cli", 2, 1, 190, 1, 1),
    ("tdg-rust", "engine", 47889, 637, 1, 1, 38, 11, 137, 3, 268, 50, 11, "mcp", 0, 3, 236, 1, 1),
    ("deckmill", "engine", 35826, 192, 2, 1, 87, 7, 125, 3, 74, 20, 10, "mcp", 0, 3, 383, 1, 1),
    ("automaton", "engine", 13861, 43, 17, 2, 40, 2, 179, 2, 500, 1, 8, "cli", 1, 1, 443, 1, 1),
    ("openscript", "engine", 152993, 716, 12, 2, 142, 0, 211, 7, 500, 15, 12, "cli", 2, 2, 180, 1, 1),
    ("mysterium", "engine", 124381, 2783, 1, 2, 259, 0, 168, 4, 500, 42, 10, "cli", 2, 4, 54, 1, 1),
    ("andrometry", "engine", 25442, 367, 1, 1, 27, 0, 96, 4, 216, 57, 3, "rest", 0, 0, 481, 0, 1),
    ("lifeos-ops", "engine", 17885, 0, 3, 1, 28, 11, 175, 3, 488, 1, 8, "cli", 2, 3, 305, 1, 1),
    ("c-suite-agents", "engine", 46602, 555, 1, 1, 25, 3, 213, 2, 500, 36, 10, "cli", 3, 3, 140, 1, 1),
    ("thinking-steroid", "engine", 24997, 247, 1, 2, 26, 0, 205, 1, 18, 1, 5, "cli", 1, 0, 228, 1, 1),
    # --- AXI CLI family ----------------------------------------------------------
    ("reddit-lyr", "engine", 6095, 86, 0, 1, 44, 0, 167, 2, 232, 56, 6, "cli", 3, 1, 207, 1, 1),
    ("twitter-lyr", "engine", 14353, 269, 0, 2, 37, 32, 242, 2, 14, 65, 6, "cli", 3, 1, 494, 1, 1),
    ("instagram-lyr", "engine", 21380, 361, 0, 1, 29, 0, 567, 2, 355, 47, 6, "cli", 3, 1, 441, 1, 1),
    ("linkedin-lyr", "engine", 54816, 1211, 0, 4, 73, 95, 567, 2, 500, 25, 10, "cli", 4, 4, 388, 1, 1),
    ("facebook-lyr", "engine", 14920, 255, 0, 1, 36, 0, 90, 2, 318, 41, 5, "cli", 3, 3, 213, 1, 1),
    ("threads-lyr", "engine", 3353, 57, 0, 1, 28, 0, 84, 2, 21, 3, 3, "cli", 2, 2, 140, 1, 1),
    ("discord-lyr", "engine", 4742, 41, 0, 2, 34, 10, 238, 2, 40, 28, 3, "cli", 3, 1, 364, 1, 1),
    ("tg-lyr", "engine", 9390, 281, 0, 2, 46, 18, 238, 2, 71, 39, 4, "cli", 3, 1, 346, 1, 1),
    ("meme-lyr", "engine", 1172, 25, 1, 2, 33, 1, 604, 2, 28, 1, 0, "cli", 2, 1, 503, 1, 1),
    ("obscura-core", "engine", 2938, 15, 0, 1, 25, 0, 93, 1, 104, 8, 4, "rest", 0, 4, 225, 1, 1),
    # --- engines added in the 2026-08-11 full-coverage pass ----------------------
    ("browsefleet", "engine", 5129, 94, 4, 5, 30, 3, 212, 4, 261, 28, 5, "rest", 0, 2, 284, 1, 1),
    ("hermes-prime-bridge", "engine", 1028, 14, 0, 2, 41, 1, 87, 2, 1, 1, 2, "engine", 0, 1, 165, 1, 1),
    ("lifeos-bot", "engine", 12100, 33, 0, 2, 30, 1, 144, 2, 397, 25, 3, "cli", 1, 1, 110, 1, 1),
    # --- experimental / archived (capped at C by policy) -------------------------
    ("consciousness-fabricator", "experimental", 9238, 158, 0, 1, 26, 0, 208, 1, 73, 6, 8, "cli", 1, 1, 263, 0, 1),
    ("holosim-infinite", "experimental", 489296, 7766, 2, 2, 27, 0, 263, 2, 31, 13, 11, "engine", 0, 1, 329, 1, 1),
    ("kali-mahabali", "experimental", 63118, 690, 0, 1, 14, 1, 397, 2, 500, 189, 8, "rest", 0, 0, 366, 1, 1),
    ("icode", "deprecated", 142819, 2095, 21, 2, 1, 0, 82, 3, 500, 1, 0, "cli", 2, 0, 100, 0, 1),
    ("CineSync", "deprecated", 13744, 16, 2, 2, 1, 0, 82, 4, 23, 13, 0, "rest", 0, 0, 150, 1, 1),
    # NOTE: "osint-os" does not resolve on this machine; row carried from the previous snapshot.
    ("workout-factory", "deprecated", 9417, 30, 0, 1, 1, 0, 82, 2, 7, 23, 0, "engine", 0, 0, 192, 0, 1),
    # --- unranked: utility/private -----------------------------------------------
    ("lifeos-saas", "engine", 760, 0, 0, 1, 24, 0, 179, 2, 15, 10, 1, "rest", 0, 1, 287, 1, 1),
    # --- 2026-11-02 catalog completion: the 22 public repos that were in no register -
    ("artificial-route", "engine", 121732, 2502, 17, 2, 376, 27, 32, 4, 500, 1, 11, "cli", 3, 3, 297, 1, 1),
    ("cloakctl", "engine", 11688, 81, 0, 0, 33, 5, 46, 2, 49, 64, 8, "cli", 3, 1, 171, 1, 1),
    ("memory-wire", "engine", 49945, 640, 1, 3, 122, 14, 35, 4, 294, 2, 10, "cli", 3, 4, 1077, 1, 1),
    ("metatrader-bridge", "engine", 50767, 801, 0, 0, 19, 0, 213, 2, 319, 127, 6, "rest", 0, 1, 289, 1, 1),
    ("metatrader-docker-deployment", "infra", 3546, 0, 0, 0, 29, 2, 115, 2, 0, 5, 3, "engine", 0, 1, 138, 0, 1),
    ("palimpsest", "engine", 7247, 186, 0, 0, 39, 0, 33, 2, 149, 0, 2, "engine", 0, 3, 185, 0, 1),
    ("swiggy-lyr", "engine", 4865, 159, 0, 2, 26, 0, 70, 2, 92, 1, 5, "cli", 1, 1, 172, 1, 1),
    ("amazon-lyr", "engine", 5701, 165, 0, 1, 25, 0, 70, 2, 131, 21, 4, "cli", 2, 4, 155, 1, 1),
    ("etmoney-lyr", "engine", 4882, 187, 0, 2, 19, 0, 70, 2, 116, 14, 5, "cli", 4, 3, 169, 1, 1),
    ("linux-telemetry", "engine", 1396, 6, 0, 0, 0, 0, 108, 2, 0, 12, 1, "cli", 1, 0, 255, 1, 0),
    ("AI-CAD", "engine", 19560, 58, 1, 0, 0, 0, 120, 4, 167, 23, 4, "rest", 0, 0, 89, 0, 1),
    ("jesse", "deprecated", 15472, 74, 0, 0, 0, 0, 163, 2, 410, 21, 6, "cli", 1, 0, 100, 1, 0),
    ("n8n-compiler", "infra", 2235, 9, 0, 2, 0, 0, 174, 1, 0, 10, 2, "cli", 0, 0, 111, 1, 0),
    ("android-webcam", "infra", 11393, 106, 0, 0, 120, 0, 66, 4, 1, 1, 3, "cli", 2, 1, 250, 1, 1),
    ("omarchy-vpn", "tool", 29, 0, 0, 0, 1, 0, 59, 1, 0, 0, 0, "engine", 0, 1, 69, 1, 0),
    ("pill-bar", "tool", 545, 3, 0, 0, 1, 0, 58, 1, 0, 0, 0, "engine", 0, 0, 99, 0, 0),
    ("pill-suite", "tool", 452, 3, 0, 0, 1, 0, 69, 1, 0, 0, 0, "engine", 0, 0, 0, 0, 0),
    ("segmented-pill-bar", "tool", 404, 3, 0, 0, 1, 0, 69, 1, 0, 0, 0, "engine", 0, 0, 0, 0, 0),
    ("static-tray", "tool", 48, 0, 0, 0, 1, 0, 69, 1, 0, 0, 0, "engine", 0, 0, 0, 0, 0),
    ("holon", "engine", 44954, 837, 0, 1, 424, 0, 21, 2, 0, 22, 10, "cli", 2, 9, 165, 1, 1),
    ("project-genome", "tool", 11728, 0, 0, 0, 56, 0, 8, 2, 0, 11, 6, "cli", 2, 5, 202, 1, 1),
    ("ishan-parihar", "profile", 2905, 1, 0, 0, 82, 0, 748, 1, 14, 10, 12, "cli", 5, 63, 386, 0, 1),
    ("HoloOS", "spec", 43795, 448, 0, 0, 1, 0, 82, 2, 1, 187, 7, "cli", 3, 1, 171, 0, 0),
    # --- websites / portfolios (separate category, never ranked) -----------------
    # NOTE: "design-aesthetics-website" does not resolve on this machine; row carried from the previous snapshot.
    # NOTE: "ishanparihar-cms" does not resolve on this machine; row carried from the previous snapshot.
    ("ishanparihar-svelte", "site", 65674, 712, 1, 3, 31, 0, 382, 4, 500, 3, 8, "engine", 0, 5, 207, 1, 1),
    ("law-of-one-india-website", "site", 69958, 63, 1, 1, 20, 0, 586, 3, 500, 1, 8, "engine", 0, 0, 178, 1, 1),
    ("webdev-portfolio", "site", 0, 0, 0, 1, 26, 0, 211, 0, 0, 0, 0, "engine", 0, 0, 114, 0, 1),
    ("lifeos-website", "site", 72999, 1156, 2, 1, 34, 0, 179, 3, 500, 1, 9, "engine", 0, 2, 199, 1, 1),
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
    # Categories introduced 2026-11-02 when the catalog was completed with the 22
    # public repos the register had never carried. They are RANKED, not excluded,
    # because each is real code that a recruiter can open and read — but each is
    # tagged so no one reads a system-config repo as a peer of an agent runtime.
    if category == "infra":
        return natural, "infra: deployment/runtime config — no agent surface"
    if category == "tool":
        return natural, "tool: developer/desktop tooling — not an agent surface"
    if category == "profile":
        return natural, "profile: this profile repo — configuration, not a software project"
    if category == "spec":
        return natural, "spec: knowledge/spec corpus — tracked separately from software"
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
