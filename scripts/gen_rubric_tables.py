#!/usr/bin/env python3
"""Regenerate the RANKING-RUBRIC.md §4 dataset and §5 scored tables from the
live `scripts/rank_score.py` DATA, so the rubric can never drift from the
engine. Run:  python3 scripts/gen_rubric_tables.py > /tmp/tables.md

The output markdown is spliced into RANKING-RUBRIC.md by hand (or by the
`update_rubric.py` helper in the same workflow) — the important invariant is
that every number in the two tables is produced by the scoring engine itself.
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
    raw = {
        "scale": rs.s_scale(r[2], r[4]),
        "tests": rs.s_tests(r[3], r[2]),
        "complexity": rs.s_complexity(r[4], r[9], r[10]),
        "ci": rs.s_ci(r[5]),
        "releases": rs.s_releases(r[7]),
        "velocity": rs.s_velocity(r[6], r[8]),
        "agent": rs.s_agent(r[11], r[12], r[13]),
        "utility": rs.s_utility(r[15], r[16], r[17], r[14]),
    }
    return round(sum(rs.WEIGHTS[k] * v for k, v in raw.items()), 2)


def main():
    rows = [r for r in rs.DATA if r[1] not in ("site", "kb")]
    rows.sort(key=lambda r: -total(r))

    print("=== DATASET TABLE (§4) ===")
    print("| Project | Cat | LOC | Tests | Mods | CI | C90 | Rel | Age | Langs | Ops | Surf | AXI | InDeg |")
    print("|---------|-----|-----|-------|------|----|----|-----|-----|-------|-----|------|-----|-------|")
    for r in rows:
        (name, cat, loc, tests, mods, ci, c90, tags, age, langs, concur,
         ops, surface, axi, indegree, rl, install, docs) = r
        print(f"| {name} | {cat} | {loc:,} | {tests:,} | {mods} | {ci} | {c90} | {tags} | {age} | {langs} | {ops} | {surface} | {axi} | {indegree} |")

    print()
    print("=== SCORED RESULTS TABLE (§5) ===")
    print("| # | Project | Scale | Test | Cplx | CI | Rel | Vel | Agnt | Util | **Total** | Tier |")
    print("|---|---------|-------|------|------|----|----|-----|------|------|-----------|------|")
    for i, r in enumerate(rows, 1):
        (name, cat, loc, tests, mods, ci, c90, tags, age, langs, concur,
         ops, surface, axi, indegree, rl, install, docs) = r
        t, note = rs.tier(total(r), cat)
        marker = "*" if note else ""
        print(f"| {i} | {name} | {rs.s_scale(r[2], r[4]):.1f} | {rs.s_tests(r[3], r[2]):.1f} | {rs.s_complexity(r[4], r[9], r[10]):.1f} | "
              f"{rs.s_ci(r[5]):.1f} | {rs.s_releases(r[7]):.1f} | {rs.s_velocity(r[6], r[8]):.1f} | {rs.s_agent(r[11], r[12], r[13]):.1f} | "
              f"{rs.s_utility(r[15], r[16], r[17], r[14]):.1f} | **{total(r):.2f}** | {t}{marker} |")

    print()
    print("=== TIER COUNTS ===")
    for t in "SABCD":
        n = sum(1 for r in rows if rs.tier(total(r), r[1])[0] == t)
        print(f"{t}: {n}")


if __name__ == "__main__":
    main()
