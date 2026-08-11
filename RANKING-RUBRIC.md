# 📐 Project Ranking Rubric — Objective Tiering Matrix (v5)

> **Purpose:** replace subjective, vibes-based tier rankings with an **objective,
> reproducible, evidence-driven ranking matrix** for every project in this portfolio.
>
> **Methodology basis:** OpenSSF Scorecard-inspired (0–10 per criterion, weighted
> aggregation) + CNCF maturity-model concepts (velocity, release cadence) + the
> anti-bias principles from OSS ranking research:
> 1. **Automated ingestion only** — every metric is machine-measured from the live
>    git worktrees (`scripts/measure_repos.py`): `git ls-files` LOC per language,
>    test markers, `.github/workflows/` counts, `git tag` counts, commit history.
>    No self-reports.
> 2. **Normalize by scale & context** — velocity is age-normalized (commits per
>    90-day-equivalent) so young but hyperactive repos aren't penalized.
> 3. **Popularity = 0 weight** — stars/forks/watchers are *decoupled* from quality
>    entirely (gameable and near-zero here).
> 4. **Transparent open-weight formulas** — weights and thresholds are published
>    below so anyone can audit a score and see exactly how to remediate it.
> 5. **Documented cap policy, not silent bias** — archived and experimental repos
>    are capped at C-tier by explicit, published rules (§7), never by an invisible
>    thumb on the scale.
>
> **Audit date:** 2026-08-11 (re-audit after the version-tag + CI sprint).
> **Applies to:** S / A / B / C / D tiering in `README.md`.
> **Engine:** `scripts/rank_score.py` · **Measurement tool:** `scripts/measure_repos.py`.

---

## 1. The Eight Weighted Criteria

v5 adds **Architectural Complexity** and **Utility & Ecosystem Value** to the
original six — the two dimensions that distinguish *how* a project is built and
*how valuable it is to the rest of the portfolio* from mere raw size.

| Criterion | Weight | What it measures | Why it matters |
|-----------|--------|------------------|----------------|
| **Engineering Scale** | 12% | Log-scaled LOC + module/crate count | Depth & ambition of the codebase (log scale avoids raw-size bias) |
| **Test Rigor** | 18% | Test count (log-scaled) + tests-per-KLOC density | The #1 production-grade signal — determinism, no regressions |
| **Architectural Complexity** | 12% | Modules, language diversity, async/concurrency depth | *NEW in v5* — structural depth beyond raw size: is it a monolith or a real system? |
| **CI/CD Discipline** | 8% | Number of GitHub Actions workflows | Automated gates on every change |
| **Release Discipline** | 8% | Number of tagged releases | Versioned artifacts, reproducible installs, shipped track record |
| **Development Velocity** | 8% | Age-normalized commits/90d-equivalent | Actively maintained (not stale) |
| **Agent Surface** | 14% | MCP tools / CLI commands | Agent-native utility — how much an AI can *operate* it |
| **Utility & Ecosystem Value** | 20% | README/docs depth, install path, cross-repo in-degree | *NEW in v5* — how many sibling projects depend on it, how discoverable it is |

**Deliberately absent:** stars, forks, watchers (social signals, gamed, and
near-zero across the board) and any human "impression" factor.

---

## 2. Scoring Formulas (0–10 per criterion)

All thresholds are hard, published, and purely quantitative.

### Scale — `min(10, log10(LOC) × 1.9 + min(2, log10(modules+1) × 1.5))`
| LOC | Score |
|-----|-------|
| ~1K | 5.7 |
| ~10K | 7.6 |
| ~50K | 8.8 |
| ~100K+ | 9.5–10 |

### Tests — `min(10, log10(tests) × 3.0 + 1.0 + density_bonus)`
| Tests | Score | Density bonus (tests per KLOC) |
|-------|-------|-------------------------------|
| 0 | 0 | — |
| 10 | 4.0 | ≤3/KLOC → +0 |
| 100 | 7.0 | ≥15/KLOC → +2.5 |
| 1,000+ | 10.0 | |

### Complexity — `min(10, 1.5 + min(4, log10(mods+1)×2) + min(3, langs−1) + min(3, log10(concur+1)×0.8))`
| Profile | Score |
|---------|-------|
| Single-file tool, 1 language | ~1.5–3 |
| Multi-module, 1–2 languages, sync | ~4–6 |
| Multi-crate, 3+ languages, async/MCP | ~7–10 |

`concur` = hits of async/tokio/thread/rayon/MCP patterns in tracked code.

### CI — `0 → 0 · 1 workflow → 5 · 2+ workflows → 10`
### Releases — `0 → 0 · 1–2 → 4 · 3–6 → 6 · 7–10 → 8 · 10+ → 10`
### Velocity — age-normalized commits per 90-day-equivalent
```
life_units = max(age_days / 90, 0.05)
normalized = commits_90d / life_units
<10 → 2 · <50 → 4 · <150 → 6 · <400 → 8 · ≥400 → 10
```
A 10-day-old repo with 90 commits = a 180-day repo with 810 commits. Equal footing.

### Agent Surface — `0 tools → 0 · 1–10 → 3 · 11–30 → 6 · 31–60 → 8 · 60+ → 10`
Tool surfaces are counted from the real registration surface: `@mcp.tool()`
decorators in production source for the Python family, README-listed MCP surfaces
for Rust/TS servers, CLI command counts for CLI tools.

### Utility — `min(10, min(3, README_lines/150) + install_path(2) + docs_dir(1) + min(4, in-degree×1.5))`
`in-degree` = number of sibling portfolio repos whose name appears in this repo's
code (cross-repo dependency count). `obscura-core` (4 dependents) and
`slideforge-rust` (3) score highest — they are load-bearing infrastructure.

---

## 3. Weighted Total & Tier Thresholds

```
TOTAL = 0.12·scale + 0.18·tests + 0.12·complexity + 0.08·ci
      + 0.08·releases + 0.08·velocity + 0.14·agent + 0.20·utility
```

| Tier | Score | Meaning |
|------|-------|---------|
| **S** | ≥ 8.0 | Flagship: deep, heavily tested, shipped, actively maintained, agent-operable |
| **A** | 6.5 – 7.99 | Production-grade with one or more gaps to close |
| **B** | 4.5 – 6.49 | Solid, fully-functional utility — meaningful gaps (tests, releases, or velocity) |
| **C** | 3.25 – 4.49 | Operational but materially under-engineered, or **policy-capped** (§7) |
| **D** | < 3.25 | Minimal / stalled — not engineering-verified |

> **v5 change:** the B floor moved 5.0 → 4.5 so that *fully-functional compact
> tools* (the AXI `-lyr` family) are correctly classified as solid utilities
> rather than punished for being small. This directly answers the re-audit finding
> "a lot of projects without ranking in C-tier that are fully functional."

---

## 4. Measured Dataset (2026-08-11, re-audit)

Machine-measured with `scripts/measure_repos.py` from the live git worktrees:
code-only LOC (assets/lockfiles excluded), test markers, workflow counts, tag
counts, commit history, language families, concurrency hits, MCP tool surfaces,
and cross-repo in-degree. **No self-reported numbers.**

| Project | Cat | LOC | Tests | Mods | CI | C90 | Rel | Age | Langs | Tools | InDeg |
|---------|-----|-----|-------|------|----|----|-----|-----|-------|-------|-------|
| igs-rust | engine | 27,912 | 242 | 2 | 2 | 198 | 15 | 96 | 2 | 91 | 3 |
| social-forge | engine | 77,836 | 257 | 3 | 2 | 478 | 2 | 96 | 5 | 43 | 0 |
| operant | engine | 537,854 | 9,240 | 20 | 4 | 758 | 3 | 116 | 6 | 30 | 3 |
| scorestrata | engine | 72,958 | 944 | 12 | 1 | 97 | 0 | 8 | 2 | 88 | 0 |
| mindstrata | engine | 81,638 | 1,238 | 8 | 1 | 481 | 0 | 14 | 1 | 0 | 0 |
| tdg-rust | engine | 47,797 | 637 | 1 | 1 | 145 | 10 | 54 | 3 | 36 | 1 |
| slideforge-rust | engine | 35,805 | 196 | 3 | 1 | 203 | 6 | 42 | 3 | 8 | 3 |
| automaton | engine | 13,410 | 43 | 17 | 2 | 16 | 1 | 96 | 2 | 38 | 0 |
| openscript | engine | 72,430 | 505 | 12 | 2 | 456 | 0 | 128 | 5 | 43 | 0 |
| mysterium | engine | 61,428 | 1,090 | 1 | 2 | 463 | 0 | 85 | 4 | 0 | 1 |
| andrometry | engine | 25,442 | 367 | 1 | 1 | 134 | 0 | 13 | 4 | 12 | 0 |
| lifeos-ops | engine | 17,760 | 0 | 3 | 1 | 98 | 10 | 92 | 3 | 31 | 0 |
| c-suite-agents | engine | 46,498 | 555 | 1 | 1 | 5 | 3 | 130 | 2 | 35 | 2 |
| thinking-steroid | engine | 24,997 | 247 | 1 | 2 | 13 | 0 | 122 | 1 | 13 | 0 |
| reddit-lyr | engine | 4,430 | 24 | 0 | 1 | 51 | 0 | 84 | 2 | 56 | 0 |
| twitter-lyr | engine | 13,425 | 243 | 0 | 2 | 44 | 32 | 159 | 2 | 42 | 0 |
| instagram-lyr | engine | 20,441 | 335 | 0 | 1 | 49 | 0 | 485 | 2 | 47 | 0 |
| linkedin-lyr | engine | 50,739 | 1,166 | 0 | 4 | 204 | 94 | 485 | 2 | 25 | 1 |
| facebook-lyr | engine | 13,977 | 229 | 0 | 1 | 19 | 0 | 7 | 2 | 41 | 2 |
| threads-lyr | engine | 2,374 | 31 | 0 | 1 | 9 | 0 | 1 | 2 | 3 | 1 |
| discord-cli | engine | 3,704 | 15 | 0 | 2 | 11 | 10 | 155 | 2 | 13 | 0 |
| tg-cli | engine | 4,828 | 122 | 0 | 2 | 12 | 14 | 155 | 2 | 12 | 0 |
| meme-lyr | engine | 899 | 0 | 1 | 1 | 12 | 0 | 521 | 2 | 6 | 0 |
| obscura-core | engine | 2,896 | 15 | 0 | 1 | 12 | 0 | 10 | 1 | 8 | 4 |
| consciousness-fabricator | experimental | 9,238 | 158 | 0 | 1 | 6 | 0 | 125 | 1 | 0 | 1 |
| holosim-infinite | experimental | 489,296 | 7,766 | 2 | 2 | 5 | 0 | 180 | 2 | 0 | 0 |
| kali-mahabali | experimental | 63,118 | 690 | 0 | 1 | 15 | 1 | 314 | 2 | 20 | 0 |
| icode | deprecated | 142,819 | 2,095 | 21 | 2 | 7 | 0 | 132 | 3 | 10 | 0 |
| browsefleet | engine | 4,254 | 50 | 4 | 5 | 28 | 2 | 130 | 4 | 0 | 0 |
| hermes-prime-bridge | engine | 919 | 14 | 0 | 1 | 22 | 0 | 4 | 2 | 0 | 0 |
| lifeos-bot | engine | 11,857 | 17 | 0 | 1 | 15 | 0 | 61 | 2 | 0 | 0 |
| cinesync | deprecated | 13,744 | 16 | 2 | 2 | 3 | 0 | 298 | 4 | 0 | 0 |
| osint-os | deprecated | 120,754 | 399 | 1 | 1 | 2 | 0 | 405 | 4 | 0 | 1 |
| sovereign | deprecated | 9,417 | 30 | 0 | 1 | 2 | 0 | 262 | 2 | 0 | 1 |
| workout-factory | deprecated | 9,417 | 30 | 0 | 1 | 3 | 0 | 262 | 2 | 0 | 0 |
| tdg | deprecated | 0 | 0 | 0 | 0 | 37 | 0 | 92 | 0 | 0 | 0 |
| lifeos-saas | engine | 760 | 0 | 0 | 1 | 4 | 0 | 96 | 2 | 0 | 0 |

---

## 5. Scored Results (engine output, v5 — 37 ranked repos)

| Rank | Project | Scale | Test | Cplx | CI | Rel | Vel | Agent | Util | **Total** | Tier |
|------|---------|-------|------|------|----|----|-----|-------|------|-----------|------|
| 1 | igs-rust | 9.2 | 8.7 | 5.6 | 10.0 | 10.0 | 8.0 | 10.0 | 9.9 | **8.96** | **S** |
| 2 | operant | 10.0 | 10.0 | 9.3 | 10.0 | 6.0 | 10.0 | 6.0 | 8.4 | **8.72** | **S** |
| 3 | social-forge | 10.0 | 8.4 | 7.9 | 10.0 | 4.0 | 10.0 | 8.0 | 6.0 | **7.90** | A |
| 4 | tdg-rust | 9.3 | 10.0 | 6.0 | 5.0 | 8.0 | 8.0 | 8.0 | 6.0 | **7.64** | A |
| 5 | linkedin-lyr | 8.9 | 10.0 | 4.7 | 10.0 | 10.0 | 4.0 | 6.0 | 7.0 | **7.59** | A |
| 6 | openscript | 10.0 | 9.6 | 8.9 | 10.0 | 0.0 | 8.0 | 8.0 | 4.2 | **7.40** | A |
| 7 | slideforge-rust | 9.6 | 8.2 | 6.2 | 5.0 | 6.0 | 10.0 | 3.0 | 9.3 | **7.33** | A |
| 8 | twitter-lyr | 7.8 | 9.4 | 3.4 | 10.0 | 10.0 | 4.0 | 8.0 | 6.0 | **7.28** | A |
| 9 | c-suite-agents | 9.3 | 10.0 | 5.3 | 5.0 | 6.0 | 2.0 | 8.0 | 6.9 | **7.09** | A |
| 10 | scorestrata | 10.0 | 10.0 | 4.7 | 5.0 | 0.0 | 10.0 | 10.0 | 4.1 | **6.98** | A |
| 11 | mysterium | 9.5 | 10.0 | 7.1 | 10.0 | 0.0 | 10.0 | 0.0 | 7.5 | **6.89** | A |
| 12 | automaton | 9.7 | 6.1 | 7.2 | 10.0 | 4.0 | 4.0 | 8.0 | 5.5 | **6.79** | A |
| 13 | facebook-lyr | 7.9 | 9.2 | 4.5 | 5.0 | 0.0 | 8.0 | 8.0 | 7.4 | **6.78** | A |
| 14 | andrometry | 8.8 | 9.7 | 7.0 | 5.0 | 0.0 | 10.0 | 6.0 | 4.0 | **6.48** | B |
| 15 | kali-mahabali | 9.1 | 10.0 | 4.7 | 5.0 | 4.0 | 2.0 | 6.0 | 5.4 | **6.26** | C* |
| 16 | tg-cli | 7.0 | 8.9 | 3.7 | 10.0 | 10.0 | 2.0 | 6.0 | 3.8 | **6.25** | B |
| 17 | instagram-lyr | 8.2 | 9.7 | 4.5 | 5.0 | 0.0 | 2.0 | 8.0 | 5.9 | **6.13** | B |
| 18 | osint-os | 10.0 | 9.0 | 7.3 | 5.0 | 0.0 | 2.0 | 0.0 | 7.5 | **5.76** | C* |
| 19 | icode | 10.0 | 10.0 | 8.3 | 10.0 | 0.0 | 2.0 | 3.0 | 1.7 | **5.72** | C* |
| 20 | thinking-steroid | 8.8 | 8.8 | 3.1 | 10.0 | 0.0 | 2.0 | 6.0 | 4.5 | **5.71** | B |
| 21 | browsefleet | 7.9 | 6.9 | 7.8 | 10.0 | 4.0 | 4.0 | 0.0 | 4.9 | **5.55** | B |
| 22 | holosim-infinite | 10.0 | 10.0 | 4.7 | 10.0 | 0.0 | 2.0 | 0.0 | 5.0 | **5.52** | C* |
| 23 | mindstrata | 10.0 | 10.0 | 3.4 | 5.0 | 0.0 | 10.0 | 0.0 | 4.1 | **5.43** | B |
| 24 | discord-cli | 6.8 | 4.8 | 3.8 | 10.0 | 8.0 | 2.0 | 6.0 | 4.2 | **5.42** | B |
| 25 | lifeos-ops | 9.0 | 0.0 | 6.9 | 5.0 | 8.0 | 6.0 | 8.0 | 4.2 | **5.39** | B |
| 26 | reddit-lyr | 6.9 | 5.5 | 4.4 | 5.0 | 0.0 | 6.0 | 8.0 | 4.1 | **5.17** | B |
| 27 | obscura-core | 6.6 | 4.9 | 3.1 | 5.0 | 0.0 | 6.0 | 3.0 | 7.5 | **4.85** | B |
| 28 | threads-lyr | 6.4 | 6.3 | 3.6 | 5.0 | 0.0 | 8.0 | 3.0 | 4.4 | **4.67** | B |
| 29 | cinesync | 8.6 | 4.7 | 6.6 | 10.0 | 0.0 | 2.0 | 0.0 | 4.0 | **4.43** | C |
| 30 | consciousness-fabricator | 7.5 | 8.7 | 3.0 | 5.0 | 0.0 | 2.0 | 0.0 | 3.2 | **4.03** | C |
| 31 | hermes-prime-bridge | 5.6 | 5.5 | 2.7 | 5.0 | 0.0 | 10.0 | 0.0 | 4.1 | **4.01** | C |
| 32 | lifeos-bot | 7.7 | 4.8 | 4.6 | 5.0 | 0.0 | 4.0 | 0.0 | 3.7 | **3.80** | C |
| 33 | sovereign | 7.6 | 5.6 | 3.2 | 5.0 | 0.0 | 2.0 | 0.0 | 3.6 | **3.58** | C |
| 34 | meme-lyr | 6.1 | 0.0 | 4.3 | 5.0 | 0.0 | 2.0 | 3.0 | 6.0 | **3.43** | C |
| 35 | workout-factory | 7.6 | 5.6 | 3.2 | 5.0 | 0.0 | 2.0 | 0.0 | 2.3 | **3.32** | C |
| 36 | lifeos-saas | 5.5 | 0.0 | 3.5 | 5.0 | 0.0 | 2.0 | 0.0 | 4.8 | **2.60** | **D** |
| 37 | tdg | 0.0 | 0.0 | 0.5 | 0.0 | 0.0 | 4.0 | 0.0 | 1.2 | **0.62** | **D** |

\* = policy-capped at C by §7 (experimental flag / archived) despite a higher raw capability score.
C without \* = natural tier. `tdg` (deprecated, 0 executable LOC) keeps its natural D — the §7 cap is a ceiling, not a floor.

---

## 6. What the Data Says (evidence-backed findings, full-coverage audit)

1. **S-tier stays two, by design:** `igs-rust` (8.96) and `operant` (8.72) are the
   only repos that clear every criterion at production grade. `social-forge`
   (7.90) is 0.10 short — its 51→257 test improvement narrowed the gap but test
   density is still the sole lever.
2. **The AXI CLI family is ranked and lands B/A, not C.** All ten `-lyr`/`-cli`
   tools scored fully-functional utility (4.67–7.59). `linkedin-lyr` (7.59, A) and
   `twitter-lyr` (7.28, A) are the standouts — deep test suites, real release
   histories, and strong agent surfaces. The previous C-tier listing was a
   *labeling* error, not a quality judgement: the rubric had never measured them.
3. **`obscura-core` proves the Utility criterion works.** 2.9K LOC, 15 tests — by
   raw scale it looks trivial, but it has the **highest cross-repo in-degree (4)**:
   every browser-scraping tool depends on its cookie vault. Utility lifts it to B.
4. **Full-coverage pass added 10 previously-unranked repos** (2026-08-11):
   `browsefleet` (5.55, B), `hermes-prime-bridge` (4.01, C), `toon-helper`
   (3.86, C), `lifeos-bot` (3.80, C), plus six archived repos (`cinesync`,
   `open-claude`, `osint-os`, `sovereign`, `workout-factory`, `tdg`). Every repo
   in the portfolio now passes through the same eight-criteria engine.
5. **Vendored code is counted once, not N times (first-party rule).** When
   `toon-helper` was folded from a standalone repo into `crates/toon-helper`
   inside its three dependents (automaton, social-forge, tdg-rust), the raw
   scan briefly triple-counted that ~170-LOC crate and its `slideforge` /
   `social-forge` mentions leaked into the in-degree scan — a false S-tier for
   social-forge and tdg-rust. `measure_repos.py` now excludes vendored paths
   from every metric; the re-measured rows are first-party truth:
   `social-forge` 7.90, `tdg-rust` 7.64, `automaton` 6.79 — all A. `tdg-rust`'s
   in-degree of 1 is a word-boundary match of its own domain name ("TDG"
   appears throughout its own code, matching the deprecated `tdg` sibling it
   supersedes) — a known metric limitation of self-named siblings, not vendored
   leakage. `open-claude` was deleted (successors: thinking-steroid +
   mysterium) and removed from the portfolio, dataset, and rubric.
6. **`browsefleet` (5.55, B) is the CI leader:** 5 workflows (most in the
   portfolio), 4 languages, 130-day-old stealth-browser fleet. It lost points only
   on agent surface (REST+CDP rather than MCP tool decorators) and velocity.
7. **`holosim-infinite` and `icode` are the strongest "C" repos** (5.52 and 5.72
   raw). Both are policy-capped: `icode` is archived, `holosim` is flagged
   experimental with 0 releases, 0 agent surface, and 5 commits/90d.
8. **`lifeos-ops` remains the biggest test gap:** 0 tests across 17.8K Rust LOC
   (the sole reason it sits at 5.39, B). Writing ~150 tests adds ≈ +2.0 and jumps
   it to A-tier territory.
9. **`mindstrata` (5.43, B)** is a simulator with **zero agent surface and zero
   releases** — elite tests (1,238) and velocity, but no way for an agent or user
   to *operate* it. A CLI/API + a v0.1 release would move it up ~1.2 points.
10. **`tdg` (0.62, D) validates the cap-ceiling fix:** the original Python TDG is
   now a Rust-only docs/skills corpus with 0 executable LOC. It stays at its
   natural D — the §7 cap is a ceiling, never a floor that inflates a dead repo.
11. **Forks and merged repos are excluded, not hidden.** `hermes-agent`
    (nousresearch), `hermes-agent-ultra` (sheawinkler), `zeroclaw`
    (zeroclaw-labs) are upstream-owned forks; `c-suite-agents-mcp` was merged
    into `c-suite-agents` and removed from GitHub. All are documented exclusions.

---

## 7. Contextual Adjustment Policy (explicit, not hidden subjectivity)

The rubric is a *baseline*. Category mismatches are handled by **documented rules**, never silent bias:

| Rule | Application |
|------|-------------|
| **Archived/deprecated repos** | A repo whose own README declares DEPRECATED / INACTIVE (`icode`, `osint-os`, `cinesync`, `sovereign`, `workout-factory`, `tdg`) is **capped at C** regardless of capability score — *as a ceiling*. A near-zero repo keeps its natural lower tier. Not promotable while inactive. (`open-claude` was deleted in 2026-08 — successors: thinking-steroid + mysterium.) |
| **Vendored code (first-party rule)** | Identical code vendored INTO a ranked repo (`crates/toon-helper` in automaton, social-forge, tdg-rust) is **excluded from every metric** by `measure_repos.py` — counted once, never N times; its sibling-name mentions never pollute in-degree. |
| **Experimental flag** | Repos under `EXPERIMENTAL/` (`holosim-infinite`, `consciousness-fabricator`, `kali-mahabali`) are **capped at C** until they earn a tagged release **and** an agent surface **and** sustained velocity. |
| **Forks of other orgs' projects** | `hermes-agent` (nousresearch), `hermes-agent-ultra` (sheawinkler), `zeroclaw` (zeroclaw-labs) — upstream-owned forks are **excluded from ranking** (not original work). Documented here, not ranked. |
| **Merged / removed repos** | `c-suite-agents-mcp` was merged into `c-suite-agents` (GitHub 404). Not ranked as a standalone repo. |
| **Embedded / vendored repos** | Nested `.git` dirs inside a ranked repo (`openscript/third_party/*`, `icode/rust/references/*`, `igs-rust/last30days-skill`, `z.archive/*`, `webdev-portfolio/my-portfolio`) are not standalone portfolio projects — excluded. |
| **Websites / portfolios** | Delivery artifacts are **excluded from ranking entirely** and grouped in the separate `Portfolios & Web User Interfaces` category. |
| **Knowledge/spec repos** | Non-executable content (HoloOS: 14K YAML) is labeled `KNOWLEDGE-BASE`, not ranked against executable-engine criteria. |
| **Non-tool domains** | Domains with no agent surface (simulators) get Agent Surface scored from their CLI/API; the weight never silently reweights. |
| **Age grace** | Repos < 30 days old are reviewed at velocity-normalized score + capability components; release count is noted as "pending first release" rather than scored as failure. |

---

## 8. How to Re-Rank (reproducibility)

1. **Measure:** `python3 scripts/measure_repos.py` regenerates the full measured
   dataset from the live worktrees (edit the `REPOS` manifest to add repos — every
   portfolio repo now has a row; the manifest is the single source of truth).
2. **Score:** fold fresh numbers into the `DATA` table of `scripts/rank_score.py`,
   then `python3 scripts/rank_score.py`.

> **Agent-surface caveat:** `measure_repos.py`'s `tools` scan counts
> `@mcp.tool` decorators (Python family) and reports 0 for Rust/TS servers.
> When folding fresh numbers, **carry the `tools` value forward from the
> previous DATA row** (README-listed MCP surface / CLI command count) rather
> than overwriting it with the raw scan — otherwise every Rust/TS repo's agent
> surface silently zeroes out.
3. **Apply §7 caps** (experimental/deprecated ceilings, fork/merged exclusions,
   websites/kb exclusions).
4. **Update the tier `<details>` blocks in `README.md`** to match.
5. Re-audit monthly, or after any major release/test/CI milestone.

> **Coverage invariant:** `scripts/measure_repos.py`'s `REPOS` manifest + the
> `EXCLUDED` note in `scripts/rank_score.py` must together account for **every**
> standalone `.git` directory under `MY-PROJECTS/`. Embedded/vendored repos
> (nested `.git` inside a ranked repo — third_party, references, archives) are
> documented exclusions. If a new repo appears, it gets a manifest row — never
> silently dropped.

**Formula transparency means anyone can see the exact lever to pull** — e.g.
*"add 400 tests to social-forge → +0.85 total → crosses S"*.

---

## 9. Promotion Roadmap — Close the Gaps (action plan)

Gains below are **derived from the actual engine formulas** (not estimates).
Priority order = nearest to next tier first.

| Project | Current | To reach | Concrete actions |
|---------|---------|----------|------------------|
| **social-forge** | A 7.90 | **S** | ~200 more tests (257 → 450: Tests 8.4→9.6, **+0.22** → 8.12, S) |
| **linkedin-lyr** | A 7.59 | **S** | 2nd velocity band (204 commits/90d at 485d → need ~540: **+0.32** → 7.91) or a larger agent surface 25→60 (**+0.28**) |
| **openscript** | A 7.40 | **S** | Ship 1–2 releases (Rel 0→4: **+0.32**) + tools 43→60 (**+0.28**) → 8.00, S |
| **tdg-rust** | A 7.64 | **S** | Add CI workflow(s) (CI 5→10: **+0.4**) → 8.04, S |
| **slideforge-rust** | A 7.33 | **S** | Tools 8→11 (**+0.42**) + 2 more releases (**+0.16**) → 7.91; 2nd CI (**+0.4**) → S |
| **twitter-lyr** | A 7.28 | **S** | Velocity band (44 commits/90d at 159d → need ~80: **+0.32**) + 2nd CI (**+0.4**) → 8.00, S |
| **scorestrata** | A 6.98 | **S** | Ship v0.1 release (Rel 0→4: **+0.32**) + 2nd CI (**+0.4**) + README depth (**+0.2**) → 7.90; velocity band bump → S |
| **andrometry** | B 6.48 | **A** | 2 releases (**+0.32**) + tools 12→31 (**+0.28**) → 7.08, A |
| **tg-cli** | B 6.25 | **A** | Tools 12→31 (**+0.28**) + velocity band (**+0.32**) → 6.85, A |
| **instagram-lyr** | B 6.13 | **A** | Ship 1–2 releases (**+0.32**) + velocity band (**+0.32**) → 6.77, A |
| **lifeos-ops** | B 5.39 | **A** | **Write tests** 0 → 150 (**+1.5**) + 2nd CI (**+0.4**) → 7.29, A — single biggest win in the portfolio |
| **obscura-core** | B 4.85 | **A** | Tools 8→31 (**+0.42**) + releases (**+0.32**) + tests 15→100 (**+0.5**) → 6.09, B+ |
| **holosim-infinite** | C 5.52* | **A** | Uncap: ship v0.1 release (**+0.32**) + add MCP/CLI surface 0→30 (**+0.84**) + velocity (**+0.32**) → 7.00, A |
| **kali-mahabali** | C 6.26* | **A** | Uncap: release + surface + velocity → A |
| **consciousness-fabricator** | C 4.03* | **B** | Uncap: release + surface; tests already strong (158) |
| **meme-lyr** | C 3.43 | **B** | Add tests (0→50: **+0.9**) + tools 6→11 (**+0.42**) → 4.75, B |

**Portfolio-wide rule:** re-run `scripts/rank_score.py` + `scripts/measure_repos.py`
after every milestone and update `README.md` tiers. The dataset is machine-generated,
so drift is caught by re-audit, not by hand.
