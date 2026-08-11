# 📐 Project Ranking Rubric — Objective Tiering Matrix

> **Purpose:** replace subjective, vibes-based tier rankings with an **objective,
> reproducible, evidence-driven ranking matrix** for every project in this portfolio.
>
> **Methodology basis:** OpenSSF Scorecard-inspired (0–10 per criterion, weighted
> aggregation) + CNCF maturity-model concepts (velocity, release cadence) + the
> anti-bias principles from OSS ranking research:
> 1. **Automated ingestion only** — every metric is machine-measured (git history,
>    `cargo test`/`go test`/test-runner counts, GitHub API). No self-reports.
> 2. **Normalize by scale & context** — velocity is age-normalized (commits per
>    90-day-equivalent) so young but hyperactive repos aren't penalized.
> 3. **Popularity = 0 weight** — stars/forks are *decoupled* from quality entirely
>    (they are gameable and mostly zero here anyway).
> 4. **Transparent open-weight formulas** — weights and thresholds are published
>    below so anyone can audit a score and see exactly how to remediate it.
>
> **Audit date:** 2026-08-11 · **Applies to:** S / A / B tiering in `README.md`.
> The scoring engine is `scripts/rank_score.py` (committed alongside this doc).

---

## 1. The Six Weighted Criteria

| Criterion | Weight | What it measures | Why it matters |
|-----------|--------|------------------|----------------|
| **Engineering Scale** | 20% | Log-scaled LOC + module/crate count | Depth & ambition of the codebase (log scale avoids raw-size bias) |
| **Test Rigor** | 25% | Test count (log-scaled) + tests-per-KLOC density | The #1 production-grade signal — determinism, no regressions |
| **CI/CD Discipline** | 15% | Number of GitHub Actions workflows | Automated gates on every change |
| **Release Discipline** | 15% | Number of tagged releases | Versioned artifacts, reproducible installs, shipped track record |
| **Development Velocity** | 15% | Age-normalized commits/90d-equivalent | Actively maintained (not stale) |
| **Agent Surface** | 10% | MCP tools / CLI surface | Agent-native utility — how much an AI can *operate* it |

**Deliberately absent:** stars, forks, watchers (social signals, gamed, and near-zero
across the board) and any human "impression" factor.

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

---

## 3. Weighted Total & Tier Thresholds

```
TOTAL = 0.20·scale + 0.25·tests + 0.15·ci + 0.15·releases + 0.15·velocity + 0.10·agent
```

| Tier | Score | Meaning |
|------|-------|---------|
| **S** | ≥ 8.0 | Flagship: deep, heavily tested, shipped, actively maintained, agent-operable |
| **A** | 6.5 – 7.99 | Production-grade with one or more gaps to close |
| **B** | 5.0 – 6.49 | Solid utility, meaningful gaps (tests, releases, or velocity) |
| **C** | 3.5 – 4.99 | Operational but materially under-engineered |
| **D** | < 3.5 | Spec/knowledge repo or stalled — not engineering-verified |

---

## 4. Measured Dataset (2026-08-11)

Machine-measured: `git ls-files | wc -l` per language, test-runner output, GitHub
REST API (`gh api repos/...`). No self-reported numbers.

| Project | LOC | Tests | Modules | CI | Commits/90d | Releases | MCP tools | Age (d) |
|---------|-----|-------|---------|----|-------------|----------|-----------|---------|
| igs-rust | 27,563 | 231 | 1 | 2 | 197 | 14 | 91 | 97 |
| social-forge | 95,578 | 51 | 1 | 2 | 475 | 1 | 43 | 96 |
| operant | 537,083 | 8,581 | 18 | 4 | 757 | 2 | 30 | 92 |
| scorestrata | 72,958 | 944 | 11 | 1 | 93 | 0 | 88 | 9 |
| mindstrata | 74,998 | 1,238 | 7 | 1 | 480 | 0 | 0 | 8 |
| tdg-rust | 47,365 | 626 | 6 | 0 | 143 | 9 | 36 | 55 |
| slideforge-rust | 35,484 | 185 | 1 | 1 | 202 | 6 | 8 | 42 |
| automaton | 11,727 | 43 | 15 | 2 | 14 | 1 | 38 | 97 |
| openscript | 65,241 | 470 | 9 | 2 | 449 | 0 | 10 | 129 |
| mysterium | 56,747 | 806 | 1 | 2 | 461 | 0 | 0 | 86 |
| andrometry | 12,244 | 153 | 1 | 1 | 133 | 0 | 0 | 14 |
| HoloOS | 44,879* | 0 | 0 | 0 | 95 | 0 | 0 | 101 |
| lifeos-ops | 15,265 | 0 | 2 | 1 | 97 | 8 | 7 | 93 |
| c-suite-agents | 45,493 | 339 | 1 | 1 | 3 | 0 | 10 | 130 |
| thinking-steroid | 24,997 | 96 | 1 | 2 | 12 | 0 | 13 | 123 |

\* HoloOS: 14,144 of those lines are YAML (knowledge/spec content), 1,191 are Markdown.
Executable Python is 98 files. See §7.

---

## 5. Scored Results (engine output)

| Rank | Project | Scale | Tests | CI | Rel | Vel | Tools | **Total** | Tier |
|------|---------|-------|-------|----|----|-----|-------|-----------|------|
| 1 | igs-rust | 8.9 | 8.6 | 10 | 10 | 8.0 | 10 | **9.13** | **S** |
| 2 | operant | 10.0 | 10.0 | 10 | 4 | 10 | 6.0 | **8.70** | **S** |
| 3 | social-forge | 9.9 | 6.2 | 10 | 4 | 10 | 8.0 | **7.93** | A |
| 4 | scorestrata | 10.0 | 10.0 | 5 | 0 | 10 | 10 | **7.75** | A |
| 5 | tdg-rust | 10.0 | 10.0 | 0 | 8 | 8.0 | 8.0 | **7.70** | A |
| 6 | mysterium | 9.5 | 10.0 | 10 | 0 | 10 | 0 | **7.40** | A |
| 7 | openscript | 10.0 | 9.5 | 10 | 0 | 8.0 | 3.0 | **7.38** | A |
| 8 | slideforge-rust | 9.1 | 8.1 | 5 | 6 | 10 | 3.0 | **7.29** | A |
| 9 | automaton | 9.5 | 6.1 | 10 | 4 | 4.0 | 8.0 | **6.92** | A |
| 10 | mindstrata | 10.0 | 10.0 | 5 | 0 | 10 | 0 | **6.75** | A |
| 11 | andrometry | 8.2 | 8.4 | 5 | 0 | 10 | 0 | **5.99** | B |
| 12 | thinking-steroid | 8.8 | 7.2 | 10 | 0 | 2.0 | 6.0 | **5.96** | B |
| 13 | c-suite-agents | 9.3 | 9.1 | 5 | 0 | 2.0 | 3.0 | **5.49** | B |
| 14 | lifeos-ops | 8.7 | 0.0 | 5 | 8 | 6.0 | 3.0 | **4.89** | C |
| 15 | HoloOS | 8.8 | 0.0 | 0 | 0 | 6.0 | 0 | **2.66** | D |

---

## 6. What the Data Says (evidence-backed findings)

1. **S-tier is genuinely two projects:** `igs-rust` (9.13) and `operant` (8.70) are the
   only repos clearing 8.0. Both are deep, heavily tested, shipped, and active.
2. **social-forge (7.93) misses S by 0.07** — 95K LOC and extreme velocity, but only
   **51 tests** for its size. Closing that test gap would promote it.
3. **scorestrata (7.75) is the strongest 9-day-old repo in the portfolio** — 944 tests,
   88 MCP tools, 73K LOC. It scores S-tier capability on every criterion except
   **releases (0)** and CI (1). Shipping a v0.x release + a second workflow = S.
4. **mindstrata (6.75) is dragged down by zero agent surface and zero releases** — a
   simulator, not a tool server, so Agent Surface is structurally 0. Tests (1,238) and
   velocity are elite.
5. **HoloOS (2.66, D) is not an engineering project today** — it's a knowledge/spec
   corpus (14K YAML + 1.2K MD), with **zero tests, zero CI, zero tools**, last pushed
   30+ days ago. Ranking it as software is why it lands last.
6. **lifeos-ops (4.89, C) has zero automated tests** across 15K Rust LOC — the single
   biggest test gap in the portfolio.
7. **c-suite-agents (5.49, B) and thinking-steroid (5.96, B)** have near-dormant
   velocity (3 and 12 commits/90d) — they need sustained maintenance to rise.
8. **andrometry (5.99, B)** — only 14 days old; velocity-normalized score is strong and
   will climb as test coverage and releases accumulate.

---

## 7. Contextual Adjustment Policy (explicit, not hidden subjectivity)

The rubric is a *baseline*. Category mismatches are handled by **documented rules**,
never silent bias:

| Rule | Application |
|------|-------------|
| **Knowledge/spec repos** | Repos that are predominantly non-executable content (HoloOS: 14K YAML) are not ranked against executable-engine criteria. They are labeled `KNOWLEDGE-BASE` and tiered by their spec depth, not software scores. |
| **Non-tool domains** | Domains with no agent surface (simulators, websites) get Agent Surface scored from their CLI/API instead of MCP tools; the 10% reweights to Test Rigor when the surface is structurally zero. |
| **Age grace** | Repos < 30 days old are reviewed at velocity-normalized score + the *capability* components only; release count is noted as "pending first release" rather than scored as a failure. |

---

## 8. How to Re-Rank (reproducibility)

1. Measure: `scripts/rank_score.py` (committed) — edit the `DATA` table with fresh
   numbers, run `python3 scripts/rank_score.py`.
2. The engine prints per-criterion scores, the total, and the tier for each repo.
3. Apply the Contextual Adjustment Policy from §7.
4. Update the tier `<details>` blocks in `README.md` to match.
5. Re-audit monthly, or after any major release/test milestone.

**Formula transparency means anyone can see the exact lever to pull** — e.g.
*"add 400 tests → +0.4 total → crosses the S boundary"*.

---

## 9. Promotion Roadmap — Close the Gaps (action plan)

The tier gaps are all *mechanical*: **releases, CI workflows, test density, and agent
surface**. None require new features — they are release-engineering work. Priority
order = nearest to next tier first. Gains below are **derived from the actual engine
formulas** (not estimates). Remember velocity is age-normalized: for a repo `A` days
old, `norm = commits_90d ÷ (A/90)`, so the *commits needed* to move a velocity band
scales with repo age.

| Project | Current | To reach | Concrete actions (each ~1 session) |
|---------|---------|----------|-------------------------------------|
| **social-forge** | A 7.93 | **S** | Add ~400 unit tests (51 → 450: Tests 6.2→9.6, **+0.85** total → 8.78, S). Tests are the only real lever (releases already at 4/10) |
| **scorestrata** | A 7.75 | **S** | Ship v0.1 release (Rel 0→4: **+0.6**) · add 2nd CI workflow (CI 5→10: **+0.75**) → **9.10, S** |
| **tdg-rust** | A 7.70 | **S** | Add CI workflow(s) (CI 0→10: **+1.5** → 9.20, S). Releases already strong (8/10) |
| **mysterium** | A 7.40 | **S** | Ship 1–2 releases (**+0.6**) · add a CLI/API surface 0→11 tools (**+0.3**) → 8.30, S |
| **openscript** | A 7.38 | **S** | Ship 1–2 releases (**+0.6**) · grow agent surface 10→31 (**+0.3**) → 8.28, S |
| **slideforge-rust** | A 7.29 | **S** | 2 more releases →8 (**+0.3**) · tools 8→11 (**+0.3**) · 2nd CI (**+0.75**) → 8.64, S |
| **automaton** | A 6.92 | **S** | Age 97d: velocity needs 54+ commits/90d for one band (**+0.3**) · ship 2 releases (**+0.6**) → ~7.8, A+. Velocity band 6.0 needs 108+/90d (**+0.6**) |
| **mindstrata** | A 6.75 | **S** | Add CLI/API agent surface 0→30 (**+0.6**) · ship v0.1 release (**+0.6**) → 7.95; add 2nd CI (**+0.75**) → 8.70, S. Tests & velocity already elite |
| **andrometry** | B 5.99 | A | Age 14d: accumulate releases 0→2 (**+0.6**) · MCP surface 0→10 (**+0.3**) · 2nd CI (**+0.75**) → 7.64, A |
| **thinking-steroid** | B 5.96 | A | Age 123d: velocity 6.0 band needs 68+ commits/90d (**+0.6**) · ship 2 releases (**+0.6**) → ~7.2, A |
| **c-suite-agents** | B 5.49 | A | Age 130d: velocity 6.0 band needs 72+ commits/90d (**+0.6**) · ship 2 releases (**+0.6**) → 6.69, A. (50 commits alone would only give +0.3 — still B) |
| **lifeos-ops** | C 4.89 | B | **Write tests** 0 → 150 (**+2.05**) — single biggest win in the portfolio · 2nd CI (**+0.75**) → 7.69, A |
| **HoloOS** | KB | KB→ranked | Add tests, CI, and an executable API to the spec corpus, or keep as KNOWLEDGE-BASE |

**Portfolio-wide release & CI sprint** (user directive): every A/B/C project gets
1. a `v0.1.x` tagged release, 2. at least 2 CI workflows (build+test, lint), and
3. a documented agent surface (MCP tools or CLI). Estimated: ~2 sessions per repo.
Re-run `scripts/rank_score.py` after each milestone and update `README.md` tiers.
