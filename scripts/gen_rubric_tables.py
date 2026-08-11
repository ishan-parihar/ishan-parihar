#!/usr/bin/env python3
"""Regenerate the RANKING-RUBRIC.md §4 dataset and §5 scored tables from the
live `scripts/rank_score.py` DATA, so the rubric can never drift from the
engine. Run:  python3 scripts/gen_rubric_tables.py > /tmp/tables.md

The output markdown is spliced into RANKING-RUBRIC.md (see the workflow's
`update_rubric.py` helper) — the important invariant is that every number in
the two tables is produced by the scoring engine itself.

v7: criteria are architecture (30%), tests (25%), agent (20%), scale (15%),
utility (10%). Velocity, releases and CI count were removed — logistics are
not architecture. `soph` (0-12) is the measured advanced-engineering family
count from scripts/soph_audit.py and carries the majority of the architecture
score.
"""
import importlib.util
import sys

SPEC = "/home/ishanp/Documents/GitHub/MY-PROJECTS/ishan-parihar/scripts/rank_score.py"

spec = importlib.util.spec_from_file_location("rank_score", SPEC)
rs = importlib.util.module_from_spec(spec)
sys.modules["rank_score"] = rs
spec.loader.exec_module(rs)


def total(r):
    """Weighted total for a DATA row (mirrors main())."""
    (name, cat, loc, tests, mods, ci, c90, tags, age, langs, concur,
     ops, soph, surface, axi, indegree, rl, install, docs) = r
    raw = {
        "architecture": rs.s_architecture(mods, langs, concur, soph),
        "tests":        rs.s_tests(tests, loc),
        "agent":        rs.s_agent(ops, surface, axi),
        "scale":        rs.s_scale(loc, mods),
        "utility":      rs.s_utility(rl, install, docs, indegree),
    }
    return round(sum(rs.WEIGHTS[k] * v for k, v in raw.items()), 2)


def main():
    rows = [r for r in rs.DATA if r[1] not in ("site", "kb")]
    rows.sort(key=lambda r: -total(r))

    print("=== DATASET TABLE (§4) ===")
    print("| Project | Cat | LOC | Tests | Mods | Langs | Concur | Soph | Surf | Ops | AXI |")
    print("|---------|-----|-----|-------|------|-------|--------|------|------|-----|-----|")
    for r in rows:
        (name, cat, loc, tests, mods, ci, c90, tags, age, langs, concur,
         ops, soph, surface, axi, indegree, rl, install, docs) = r
        print(f"| {name} | {cat} | {loc:,} | {tests:,} | {mods} | {langs} | {concur} | {soph} | {surface} | {ops} | {axi} |")

    print()
    print("=== SCORED RESULTS TABLE (§5) ===")
    print("| # | Project | Arch | Test | Agnt | Scale | Util | **Total** | Tier |")
    print("|---|---------|------|------|------|-------|------|-----------|------|")
    for i, r in enumerate(rows, 1):
        (name, cat, loc, tests, mods, ci, c90, tags, age, langs, concur,
         ops, soph, surface, axi, indegree, rl, install, docs) = r
        t, note = rs.tier(total(r), cat)
        marker = "*" if note else ""
        print(f"| {i} | {name} | {rs.s_architecture(mods, langs, concur, soph):.1f} | "
              f"{rs.s_tests(tests, loc):.1f} | {rs.s_agent(ops, surface, axi):.1f} | "
              f"{rs.s_scale(loc, mods):.1f} | {rs.s_utility(rl, install, docs, indegree):.1f} | "
              f"**{total(r):.2f}** | {t}{marker} |")

    print()
    print("=== TIER COUNTS ===")
    for t in "SABCD":
        n = sum(1 for r in rows if rs.tier(total(r), r[1])[0] == t)
        print(f"{t}: {n}")


if __name__ == "__main__":
    main()
