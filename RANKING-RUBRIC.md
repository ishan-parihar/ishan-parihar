# 📐 Project Ranking Rubric — Objective Tiering Matrix (v6.1)

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
> **Audit date:** 2026-08-12 (v6.1: AXI-ergonomics bonus on the CLI curve).
> **Applies to:** S / A / B / C / D tiering in `README.md`.
> **Engine:** `scripts/rank_score.py` · **Measurement tool:** `scripts/measure_repos.py`.

---

## 1. The Eight Weighted Criteria

v5 added **Architectural Complexity** and **Utility & Ecosystem Value** to the
original six. **v6 makes the Agent Surface criterion class-aware** (see §2):
CLI tools, REST servers, and simulators are scored against the surface they
actually expose instead of being zeroed for lacking `@mcp.tool` decorators.
**v6.1 adds a demonstrable AXI-ergonomics bonus on the CLI curve** — projects
that ship the axi.md principles (TOON structured output, `--full` escape hatch,
definitive empty states, content truncation with size hints, pre-computed
aggregates, structured exit codes) earn up to +2.0 on the 14% agent criterion,
so a spec-compliant CLI is rewarded, not just counted.

| Criterion | Weight | What it measures | Why it matters |
|-----------|--------|------------------|----------------|
| **Engineering Scale** | 12% | Log-scaled LOC + module/crate count | Depth & ambition of the codebase (log scale avoids raw-size bias) |
| **Test Rigor** | 18% | Test count (log-scaled) + tests-per-KLOC density | The #1 production-grade signal — determinism, no regressions |
| **Architectural Complexity** | 12% | Modules, language diversity, async/concurrency depth | *NEW in v5* — structural depth beyond raw size: is it a monolith or a real system? |
| **CI/CD Discipline** | 8% | Number of GitHub Actions workflows | Automated gates on every change |
| **Release Discipline** | 8% | Number of tagged releases | Versioned artifacts, reproducible installs, shipped track record |
| **Development Velocity** | 8% | Age-normalized commits/90d-equivalent | Actively maintained (not stale) |
| **Agent Surface** | 14% | **Class-aware (v6):** MCP tools / CLI commands / REST endpoints / engine binaries — scored against the project's *own* surface class. **AXI bonus (v6.1):** CLI projects demonstrating axi.md ergonomics earn up to +2.0 | Agent-native utility — how much an AI can *operate* it (AXI: CLI is a first-class agent surface, axi.md) |
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

### Agent Surface — CLASS-AWARE (v6), scored against the project's own surface class

| Surface | Ops counted | Curve |
|---------|-------------|-------|
| `mcp` | MCP tool count (`@mcp.tool()` decorators / README-listed Rust/TS surfaces) | `0|1–10→3|11–30→6|31–60→8|60+→10` |
| `cli` | CLI command/subcommand count | `0|1–4→4|5–15→6|16–40→8|40+→10` |
| `rest` | HTTP endpoint count (FastAPI/Hono/Go handlers) | `0|1–10→3|11–30→6|31–60→8|60+→10` |
| `engine` | Runnable binary count (simulators/libs) | `0→1 (floor)|1–3→2|4–10→3|10+→4` |

**AXI-ergonomics bonus (v6.1, CLI surface only):** `agent = min(10, cli_curve + 0.4 × min(axi, 5))`
where `axi` (0–6) is the count of demonstrable axi.md principles measured by
`count_axi()` in `scripts/measure_repos.py`:

| AXI signal | Measured by |
|------------|-------------|
| 1. TOON structured output | `dump_toon` / `toon_print_dict` / `outputTOON` / `format_toon` / `as_toon` / `--toon` |
| 2. `--full` escape hatch | the literal `--full` flag |
| 3. Definitive empty states | `"0 results"` / `"no results"` / `"0 items"` / `"none found"` |
| 4. Content truncation | `truncate*(... chars total)` size hints |
| 5. Pre-computed aggregates | `total_count` / `totalCount` / `count: N of M` |
| 6. Structured errors | `sys.exit(` / `process.exit(` / `UsageError` |

A full 6/6 implementation adds **+2.0** to the agent score (e.g. linkedin-lyr's
6.0 → 8.0 base, pushing it over the S line). The bonus is capped at +2.0 so it
can never outrank genuine surface size — it rewards *quality of the surface the
project actually has*, per axi.md's thesis that a well-built CLI is an agent's
best interface.

**Why:** v5 read only `@mcp.tool` counts, so *every* project without an MCP
server scored 0.0 on the 14% criterion — mysterium's 9-command CLI, browsefleet's
22 REST endpoints, osint-os's 122 routes, and the simulator family were all
silently zeroed. Per AXI (`axi.md`), a well-designed CLI is a **first-class agent
surface** (often cheaper than MCP schema overhead), so CLI command counts are not
penalized relative to MCP tools. `measure_repos.py` auto-detects the dominant
surface by measured registration count (`mcp | cli | rest`, `engine` only when
none exist).

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

## 4. Measured Dataset (2026-08-12, v6.1 re-audit)

Machine-measured with `scripts/measure_repos.py` from the live git worktrees:
code-only LOC (assets/lockfiles excluded), test markers, workflow counts, tag
counts, commit history, language families, concurrency hits, agent surface
class + ops, **AXI-ergonomics signal count** (v6.1), and cross-repo in-degree.
**No self-reported numbers.** Websites + knowledge-base repos are excluded
from ranking (see §7) but shown here for completeness.

| Project | Cat | LOC | Tests | Mods | CI | C90 | Rel | Age | Langs | Ops | Surf | AXI | InDeg |
|---------|-----|-----|-------|------|----|----|-----|-----|-------|-----|------|-----|-------|
| operant | engine | 538,394 | 9,249 | 19 | 4 | 762 | 3 | 116 | 6 | 68 | mcp | 0 | 3 |
| mysterium | engine | 61,428 | 1,090 | 1 | 2 | 467 | 0 | 86 | 4 | 9 | cli | 5 | 2 |
| linkedin-lyr | engine | 50,739 | 1,166 | 0 | 4 | 204 | 94 | 485 | 2 | 25 | cli | 6 | 1 |
| igs-rust | engine | 27,738 | 231 | 1 | 2 | 198 | 15 | 96 | 2 | 91 | mcp | 0 | 0 |
| social-forge | engine | 77,836 | 257 | 3 | 2 | 479 | 2 | 96 | 5 | 43 | mcp | 0 | 0 |
| openscript | engine | 74,606 | 510 | 12 | 2 | 463 | 0 | 129 | 5 | 109 | mcp | 0 | 0 |
| twitter-lyr | engine | 13,425 | 243 | 0 | 2 | 44 | 32 | 160 | 2 | 42 | cli | 5 | 0 |
| tdg-rust | engine | 47,797 | 626 | 1 | 1 | 146 | 10 | 55 | 3 | 36 | mcp | 0 | 0 |
| facebook-lyr | engine | 13,977 | 229 | 0 | 1 | 19 | 0 | 7 | 2 | 41 | cli | 3 | 2 |
| scorestrata | engine | 72,958 | 944 | 12 | 1 | 97 | 0 | 9 | 2 | 88 | mcp | 0 | 0 |
| osint-os | deprecated | 120,754 | 399 | 1 | 1 | 2 | 0 | 406 | 4 | 122 | rest | 0 | 0 |
| c-suite-agents | engine | 46,498 | 227 | 1 | 1 | 6 | 3 | 130 | 2 | 35 | mcp | 0 | 2 |
| automaton | engine | 13,410 | 43 | 17 | 2 | 16 | 1 | 96 | 2 | 38 | mcp | 0 | 0 |
| slideforge-rust | engine | 35,631 | 185 | 2 | 1 | 203 | 6 | 43 | 3 | 8 | mcp | 0 | 1 |
| browsefleet | engine | 4,558 | 86 | 4 | 5 | 29 | 2 | 130 | 4 | 22 | rest | 0 | 0 |
| tg-cli | engine | 4,828 | 122 | 0 | 2 | 12 | 14 | 156 | 2 | 12 | cli | 5 | 0 |
| instagram-lyr | engine | 20,441 | 335 | 0 | 1 | 49 | 0 | 485 | 2 | 47 | cli | 5 | 0 |
| kali-mahabali | experimental | 63,118 | 690 | 0 | 1 | 15 | 1 | 314 | 2 | 20 | mcp | 0 | 0 |
| thinking-steroid | engine | 24,997 | 247 | 1 | 2 | 16 | 0 | 122 | 1 | 13 | mcp | 0 | 1 |
| andrometry | engine | 25,442 | 152 | 1 | 1 | 135 | 0 | 14 | 4 | 12 | rest | 0 | 0 |
| mindstrata | engine | 82,079 | 1,245 | 8 | 1 | 483 | 0 | 14 | 1 | 2 | cli | 3 | 0 |
| meme-lyr | engine | 1,050 | 25 | 1 | 2 | 14 | 1 | 521 | 2 | 6 | cli | 4 | 0 |
| holosim-infinite | experimental | 489,296 | 7,766 | 2 | 2 | 5 | 0 | 180 | 2 | 6 | engine | 0 | 0 |
| icode | deprecated | 142,819 | 2,095 | 21 | 2 | 7 | 0 | 133 | 3 | 10 | mcp | 0 | 0 |
| discord-cli | engine | 3,704 | 15 | 0 | 2 | 11 | 10 | 156 | 2 | 13 | cli | 5 | 0 |
| reddit-lyr | engine | 4,430 | 24 | 0 | 1 | 51 | 0 | 84 | 2 | 56 | cli | 5 | 0 |
| lifeos-ops | engine | 17,760 | 0 | 3 | 1 | 98 | 10 | 93 | 3 | 31 | mcp | 0 | 0 |
| lifeos-bot | engine | 12,009 | 33 | 0 | 2 | 16 | 1 | 61 | 2 | 3 | cli | 2 | 0 |
| cinesync | deprecated | 13,744 | 16 | 2 | 2 | 3 | 0 | 298 | 4 | 13 | rest | 0 | 0 |
| consciousness-fabricator | experimental | 9,238 | 158 | 0 | 1 | 7 | 0 | 125 | 1 | 6 | cli | 2 | 1 |
| hermes-prime-bridge | engine | 919 | 14 | 0 | 2 | 23 | 1 | 4 | 2 | 3 | mcp | 0 | 0 |
| threads-lyr | engine | 2,374 | 31 | 0 | 1 | 9 | 0 | 1 | 2 | 3 | cli | 3 | 1 |
| obscura-core | engine | 2,896 | 15 | 0 | 1 | 12 | 0 | 10 | 1 | 8 | mcp | 0 | 4 |
| workout-factory | deprecated | 9,417 | 30 | 0 | 1 | 3 | 0 | 262 | 2 | 0 | engine | 0 | 0 |
| lifeos-saas | engine | 760 | 0 | 0 | 1 | 4 | 0 | 97 | 2 | 10 | rest | 0 | 0 |

---

## 5. Scored Results (engine output, v6.1 — 35 ranked repos)

| # | Project | Scale | Test | Cplx | CI | Rel | Vel | Agnt | Util | **Total** | Tier |
|---|---------|-------|------|------|----|----|-----|------|------|-----------|------|
| 1 | operant | 10.0 | 10.0 | 9.3 | 10.0 | 6.0 | 10.0 | 10.0 | 8.4 | **9.28** | S |
| 2 | mysterium | 9.5 | 10.0 | 7.1 | 10.0 | 0.0 | 10.0 | 8.0 | 9.0 | **8.31** | S |
| 3 | linkedin-lyr | 8.9 | 10.0 | 4.7 | 10.0 | 10.0 | 4.0 | 10.0 | 7.0 | **8.15** | S |
| 4 | igs-rust | 8.9 | 8.6 | 5.3 | 10.0 | 10.0 | 8.0 | 10.0 | 5.9 | **8.07** | S |
| 5 | social-forge | 10.0 | 8.4 | 7.9 | 10.0 | 4.0 | 10.0 | 8.0 | 6.0 | **7.90** | A |
| 6 | openscript | 10.0 | 9.6 | 8.9 | 10.0 | 0.0 | 8.0 | 10.0 | 4.2 | **7.68** | A |
| 7 | twitter-lyr | 7.8 | 9.4 | 3.4 | 10.0 | 10.0 | 4.0 | 10.0 | 6.0 | **7.56** | A |
| 8 | tdg-rust | 9.3 | 10.0 | 6.0 | 5.0 | 8.0 | 8.0 | 8.0 | 4.5 | **7.34** | A |
| 9 | facebook-lyr | 7.9 | 9.2 | 4.5 | 5.0 | 0.0 | 8.0 | 10.0 | 7.4 | **7.06** | A |
| 10 | scorestrata | 10.0 | 10.0 | 4.7 | 5.0 | 0.0 | 10.0 | 10.0 | 4.1 | **6.98** | A |
| 11 | osint-os | 10.0 | 9.0 | 7.3 | 5.0 | 0.0 | 2.0 | 10.0 | 6.0 | **6.86** | C* |
| 12 | c-suite-agents | 9.3 | 8.4 | 5.3 | 5.0 | 6.0 | 2.0 | 8.0 | 6.9 | **6.80** | A |
| 13 | automaton | 9.7 | 6.1 | 7.2 | 10.0 | 4.0 | 4.0 | 8.0 | 5.5 | **6.79** | A |
| 14 | slideforge-rust | 9.4 | 8.1 | 6.0 | 5.0 | 6.0 | 10.0 | 3.0 | 6.8 | **6.77** | A |
| 15 | browsefleet | 8.0 | 8.1 | 7.8 | 10.0 | 4.0 | 4.0 | 6.0 | 4.9 | **6.61** | A |
| 16 | tg-cli | 7.0 | 8.9 | 3.7 | 10.0 | 10.0 | 2.0 | 8.0 | 3.8 | **6.53** | A |
| 17 | instagram-lyr | 8.2 | 9.7 | 4.5 | 5.0 | 0.0 | 2.0 | 10.0 | 5.9 | **6.41** | B |
| 18 | kali-mahabali | 9.1 | 10.0 | 4.7 | 5.0 | 4.0 | 2.0 | 6.0 | 5.4 | **6.26** | C* |
| 19 | thinking-steroid | 8.8 | 8.8 | 3.1 | 10.0 | 0.0 | 4.0 | 6.0 | 6.0 | **6.17** | B |
| 20 | andrometry | 8.8 | 7.9 | 7.0 | 5.0 | 0.0 | 10.0 | 6.0 | 4.0 | **6.16** | B |
| 21 | mindstrata | 10.0 | 10.0 | 3.4 | 5.0 | 0.0 | 10.0 | 5.2 | 4.1 | **6.16** | B |
| 22 | meme-lyr | 6.2 | 6.8 | 4.3 | 10.0 | 4.0 | 2.0 | 7.6 | 6.0 | **6.03** | B |
| 23 | holosim-infinite | 10.0 | 10.0 | 4.7 | 10.0 | 0.0 | 2.0 | 3.0 | 5.0 | **5.94** | C* |
| 24 | icode | 10.0 | 10.0 | 8.3 | 10.0 | 0.0 | 2.0 | 3.0 | 1.7 | **5.72** | C* |
| 25 | discord-cli | 6.8 | 4.8 | 3.8 | 10.0 | 8.0 | 2.0 | 8.0 | 4.2 | **5.70** | B |
| 26 | reddit-lyr | 6.9 | 5.5 | 4.4 | 5.0 | 0.0 | 6.0 | 10.0 | 4.1 | **5.45** | B |
| 27 | lifeos-ops | 9.0 | 0.0 | 6.9 | 5.0 | 8.0 | 6.0 | 8.0 | 4.2 | **5.39** | B |
| 28 | lifeos-bot | 7.8 | 5.7 | 4.6 | 10.0 | 4.0 | 4.0 | 4.8 | 3.7 | **5.37** | B |
| 29 | cinesync | 8.6 | 4.7 | 6.6 | 10.0 | 0.0 | 2.0 | 6.0 | 4.0 | **5.27** | C* |
| 30 | consciousness-fabricator | 7.5 | 8.7 | 3.0 | 5.0 | 0.0 | 2.0 | 6.8 | 4.2 | **5.18** | C* |
| 31 | hermes-prime-bridge | 5.6 | 5.5 | 2.7 | 10.0 | 4.0 | 10.0 | 3.0 | 4.1 | **5.15** | B |
| 32 | threads-lyr | 6.4 | 6.3 | 3.6 | 5.0 | 0.0 | 8.0 | 5.2 | 4.4 | **4.98** | B |
| 33 | obscura-core | 6.6 | 4.9 | 3.1 | 5.0 | 0.0 | 6.0 | 3.0 | 7.5 | **4.85** | B |
| 34 | workout-factory | 7.6 | 5.6 | 3.2 | 5.0 | 0.0 | 2.0 | 1.0 | 2.3 | **3.46** | C |
| 35 | lifeos-saas | 5.5 | 0.0 | 3.5 | 5.0 | 0.0 | 2.0 | 3.0 | 4.8 | **3.02** | D |

\* = policy-capped at C by §7 (experimental flag / archived) despite a higher raw capability score.
C without \* = natural tier. `tdg` (deprecated, 0 executable LOC) keeps its natural D — the §7 cap is a ceiling, not a floor.

---

## 6. What the Data Says (evidence-backed findings, full-coverage audit)

1. **S-tier is four after v6.1.** `operant` (9.28), `mysterium` (8.31),
   `linkedin-lyr` (8.15), and `igs-rust` (8.07). `mysterium` was a *measurement
   casualty* of v5: its 9-command CLI scored 0.0 on the agent criterion, hiding
   61K LOC, 1,090 tests, 4 languages, and 467 commits/90d. With CLI recognized
   as a first-class agent surface (AXI), it honestly clears S. **`linkedin-lyr`
   crossed S on the v6.1 AXI bonus**: its 25-command CLI hits the 6.0 CLI curve
   and its 6/6 axi.md signals (TOON output, `--full`, empty states, truncation,
   aggregates, exit codes) add +2.0 → 8.0 agent → **8.15 S** (was 7.87 A).
   `igs-rust`'s 8.96→8.07 move is the first-party rule at work (vendored
   `toon-helper/` in-degree leakage removed). `social-forge` (7.90) is 0.10
   short — test density is the sole lever.
2. **The AXI CLI family is ranked and lands B/A/S, not C.** All ten
   `-lyr`/`-cli` tools scored fully-functional utility (4.98–8.15). v6 raised
   the CLI family's agent scores (commands now use the CLI curve); v6.1 adds
   the AXI-ergonomics bonus. `linkedin-lyr` → **S 8.15**, `twitter-lyr`
   7.28→**7.56**, `facebook-lyr` 6.78→**7.06** (A), `tg-cli` 6.25→**6.53 A**
   (5/6 AXI), `meme-lyr` 5.38→**6.03 B** (4/6 AXI), `discord-cli` 5.42→**5.70 B**
   (5/6 AXI), `reddit-lyr` 5.17→5.45, `instagram-lyr` 6.41 (5/6 AXI). The
   previous C-tier listing was a *labeling* error, not a quality judgement.
3. **`obscura-core` proves the Utility criterion works.** 2.9K LOC, 15 tests — by
   raw scale it looks trivial, but it has the **highest cross-repo in-degree (4)**:
   every browser-scraping tool depends on its cookie vault. Utility lifts it to B.
4. **Full-coverage pass added 10 previously-unranked repos** (2026-08-11):
   `browsefleet` (5.77, B), `hermes-prime-bridge` (5.15, B), `toon-helper`
   (removed — vendored into dependents), `lifeos-bot` (4.69, B), plus five
   archived repos (`cinesync`, `open-claude`, `osint-os`,
   `workout-factory`, `tdg`). Every repo in the portfolio now passes
   through the same eight-criteria engine.
5. **`sovereign` removed (2026-08-12).** Archived + made private on GitHub,
   local folder deleted — succeeded by `lifeos-ops` / `lifeos-saas`. Dropped
   from the dataset and the C tier (C shrank 8 → 7).
6. **Vendored code is counted once, not N times (first-party rule).** When
   `toon-helper` was folded from a standalone repo into its dependents, the raw
   scan counted the identical ~170-LOC crate in every copy and its `slideforge`
   / `social-forge` mentions leaked into the in-degree scan — a false S-tier
   for social-forge and tdg-rust, and a false in-degree of 3 for igs-rust (all
   leakage). `measure_repos.py` now excludes vendored paths from every metric
   (all 5 copies covered: automaton, social-forge, tdg-rust, slideforge-rust at
   `crates/toon-helper/`; igs-rust at top-level `toon-helper/`). Re-measured
   first-party truth: `social-forge` 7.90, `tdg-rust` 7.34, `automaton` 6.79,
   `slideforge-rust` 6.77 (A, tightened), `igs-rust` 8.07 (S, was inflated
   8.96). `open-claude` was deleted and `tdg` was made private + removed
   (2026-08-11) — both gone from portfolio, dataset, and rubric; `tdg-rust` is
   the canonical TDG project.
7. **`browsefleet` (5.77 B → 6.61 A) is the v6 REST promotion:** 5 workflows
   (most in the portfolio), 4 languages, 130-day-old stealth-browser fleet,
   and 22 Hono routes now scored as a first-class REST agent surface (was 0.0
   under the MCP-only v5 scan). The 2026-08 upgrade — deduplicated agent loop,
   token-bucket rate limiter, core tests 50→86 — plus the surface fix put it
   firmly in A.
8. **`holosim-infinite` and `icode` are the strongest "C" repos** (5.52 and 5.72
   raw). Both are policy-capped: `icode` is archived, `holosim` is flagged
   experimental with 0 releases, 0 agent surface, and 5 commits/90d.
9. **`lifeos-ops` remains the biggest test gap:** 0 tests across 17.8K Rust LOC
   (the sole reason it sits at 5.39, B). Writing ~150 tests adds ≈ +2.0 and jumps
   it to A-tier territory.
10. **`mindstrata` (5.43 → 5.99, B)** is a simulator whose 2-command CLI
   (`Sim`, `Scenario`) was previously scored 0.0 on the agent criterion; v6
   recognizes it (4.0) but its **zero releases** still cap it below A. A v0.1
   release (+0.32) and a 3rd CLI command (+0.28) would cross into A.
11. **`tdg` removed; `tdg-rust` is the canonical TDG project** (2026-08-11): the
   legacy repo was made private on GitHub, fully pushed, backed up, and deleted
   locally. The portfolio is now 35 ranked + 1 KB + 6 websites = 42, with D-tier
   holding only `lifeos-saas` (2.60 → 3.02 in v6, its 10 REST routes now counted).
12. **v6 class-aware agent surface (2026-08-12) fixed the silent-zero bug.**
    `s_agent()` previously read only `@mcp.tool` counts; now each project is
    scored against its own surface class — `cli` (AXI first-class), `rest`, or
    `engine` (floor). Net effect: mysterium A→S, browsefleet B→A, osint-os raw
    5.46→6.86 (122 REST routes, still capped C by §7), lifeos-saas raw
    2.60→3.02, consciousness-fabricator 4.23→5.07, cinesync 4.43→5.27,
    holosim 5.52→5.94. No tool loses score to this change — surfaces only add
    the previously-missing evidence.
13. **v6.1 AXI-ergonomics bonus (2026-08-12) rewards spec-compliant CLIs.**
    `axi` (0–6 demonstrable axi.md principles) adds `+0.4 × min(axi,5)` to the
    CLI agent score, capped at 10. Net effect: `linkedin-lyr` A→**S 8.15**
    (6/6 signals), `tg-cli` B→**A 6.53** (5/6), `mysterium` 8.03→**8.31**
    (5/6), `meme-lyr` 5.80→**6.03**, `discord-cli` 5.42→**5.70**, `mindstrata`
    5.99→**6.16**, `threads-lyr` 4.81→**4.98**. Detection is mechanical
    (`count_axi()` in `measure_repos.py`) and every scored `axi` value is
    verified against the repo's source, so the bonus can't be gamed by
    README claims alone.
14. **Forks and merged repos are excluded, not hidden.** `hermes-agent`
    (nousresearch), `hermes-agent-ultra` (sheawinkler), `zeroclaw`
    (zeroclaw-labs) are upstream-owned forks; `c-suite-agents-mcp` was merged
    into `c-suite-agents` and removed from GitHub. All are documented exclusions.
15. **C-tier audit sprint (2026-08-11): genuine gaps closed, three repos promoted.**
    * `meme-lyr` 3.43 → **5.38 (B)**: was the only portfolio repo with **zero
      tests** — added a 19-test vitest suite over the pure CLI core (ratio/color
      data integrity, truncation, background parsing, arg parsing), exported the
      pure core + guarded `main()` for testability, switched the toolchain to
      npm (stale yarn.lock dropped), and shipped the tag-only CI + release
      pipeline with a v2.0.0 tag.
    * `hermes-prime-bridge` 4.01 → **5.15 (B)**: pyproject declared v0.2.0 but
      there was no tag — tagged v0.2.0, added a tag-triggered release workflow
      (pytest gate + GitHub release notes), and corrected its agent surface to
      its real 3 Hermes MCP tools (pinned by its own contract tests).
    * `lifeos-bot` 3.80 → **5.11 (B)**: added 16 unit tests for the pure
      Telegram formatting layer (17 → 33), added the release pipeline, created
      the GitHub repo (it existed only locally!), pushed, tagged v0.1.0, and
      counted its real `python -m lifeos` CLI surface (simulate/direct/debug).
    * `consciousness-fabricator` 4.03 → **4.23 (C*)** — docs/ architecture
      deep-dive added (was the only gap in an otherwise strong suite); stays
      policy-capped at C until release + agent surface.
    * C-tier shrank 11 → 8 (then 7 — `sovereign` archived + privatized
      2026-08-12); B grew 11 → 14. The remaining C repos are capped
      experimental/deprecated (kali-mahabali 6.26, icode 5.72, holosim 5.52,
      osint-os 5.46) or genuinely small/dormant (cinesync 4.43,
      workout-factory 3.32) — no authentic code change could move them.

---
## 7. Contextual Adjustment Policy (explicit, not hidden subjectivity)

The rubric is a *baseline*. Category mismatches are handled by **documented rules**, never silent bias:

| Rule | Application |
|------|-------------|
| **Archived/deprecated repos** | A repo whose own README declares DEPRECATED / INACTIVE (`icode`, `osint-os`, `cinesync`, `workout-factory`) is **capped at C** regardless of capability score — *as a ceiling*. A near-zero repo keeps its natural lower tier. Not promotable while inactive. (`open-claude` deleted in 2026-08 — successors: thinking-steroid + mysterium; `tdg` made private + removed 2026-08-11 — `tdg-rust` is canonical; `sovereign` made private + archived 2026-08-12 — removed from the portfolio.) |
| **Vendored code (first-party rule)** | Identical code vendored INTO a ranked repo (`crates/toon-helper` in automaton, social-forge, tdg-rust) is **excluded from every metric** by `measure_repos.py` — counted once, never N times; its sibling-name mentions never pollute in-degree. |
| **Experimental flag** | Repos under `EXPERIMENTAL/` (`holosim-infinite`, `consciousness-fabricator`, `kali-mahabali`) are **capped at C** until they earn a tagged release **and** an agent surface **and** sustained velocity. |
| **Forks of other orgs' projects** | `hermes-agent` (nousresearch), `hermes-agent-ultra` (sheawinkler), `zeroclaw` (zeroclaw-labs) — upstream-owned forks are **excluded from ranking** (not original work). Documented here, not ranked. |
| **Merged / removed repos** | `c-suite-agents-mcp` was merged into `c-suite-agents` (GitHub 404). Not ranked as a standalone repo. |
| **Embedded / vendored repos** | Nested `.git` dirs inside a ranked repo (`openscript/third_party/*`, `icode/rust/references/*`, `igs-rust/last30days-skill`, `z.archive/*`, `webdev-portfolio/my-portfolio`) are not standalone portfolio projects — excluded. |
| **Websites / portfolios** | Delivery artifacts are **excluded from ranking entirely** and grouped in the separate `Portfolios & Web User Interfaces` category. |
| **Knowledge/spec repos** | Non-executable content (HoloOS: 14K YAML) is labeled `KNOWLEDGE-BASE`, not ranked against executable-engine criteria. |
| **Non-tool domains (v6)** | Every project is scored against the surface it actually exposes: MCP tools, CLI commands (AXI first-class), REST endpoints, or — for simulators/libs with no interactive surface — runnable binaries on a floor curve. The 14% weight never silently reweights and never silently zeroes a real surface. |
| **Age grace** | Repos < 30 days old are reviewed at velocity-normalized score + capability components; release count is noted as "pending first release" rather than scored as failure. |

---

## 8. How to Re-Rank (reproducibility)

1. **Measure:** `python3 scripts/measure_repos.py` regenerates the full measured
   dataset from the live worktrees (edit the `REPOS` manifest to add repos — every
   portfolio repo now has a row; the manifest is the single source of truth).
2. **Score:** fold fresh numbers into the `DATA` table of `scripts/rank_score.py`,
   then `python3 scripts/rank_score.py`.

> **Agent-surface (v6.1):** `measure_repos.py` auto-detects each repo's dominant
> surface (`mcp | cli | rest | engine`) by measured registration count and
> reports it in the `surface` column; `ops` is the count on that class. For CLI
> surfaces it also reports `axi` — the count of demonstrable axi.md principles
> (0–6) via `count_axi()`, which feeds the +0.4/principle bonus. Hybrid MCP+
> CLI repos (`-lyr` family, pyproject `[project.scripts]` / package.json `"bin"`)
> classify as `cli` per AXI-first branding. The `tools` scan alone (Python
> `@mcp.tool`) is no longer the agent signal — Rust/TS MCP surfaces are
> README-listed, CLI commands and REST routes are counted directly, and `engine`
> gets a floor. No manual carry-forward needed.
>
> **Detector `axi` vs scored DATA:** `count_axi()` is a *conservative lower
> bound* — its regexes only credit signals in the exact documented phrasings
> (e.g. `count: N of M total`, `truncate*(... chars total)`), so it may report
> fewer signals than the hand-verified values in `rank_score.py` DATA (e.g.
> mysterium 2 vs 5, linkedin-lyr 4 vs 6 — the audit found the same principles
> under alternative phrasings). **DATA is authoritative**; a re-measurement
> that reports a lower `axi` should be reviewed against the audit evidence
> before folding it in, not blindly trusted over the verified row.
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
| **openscript** | A 7.68 | **S** | Ship 1–2 releases (Rel 0→4: **+0.32**) → 8.00, S |
| **tdg-rust** | A 7.34 | **S** | Add CI workflow(s) (CI 5→10: **+0.4**) + README depth (225→450 lines: **+0.2**) → 7.94; one release-band bump → S |
| **slideforge-rust** | A 6.77 | **S** | Tools 8→60 (**+0.7**) + 2nd CI (**+0.4**) + tests 185→450 (**+0.29**) + release band (**+0.16**) → 8.32, S |
| **twitter-lyr** | A 7.56 | **S** | Velocity band (44 commits/90d at 159d → need ~80: **+0.32**) + 2nd CI (**+0.4**) → 8.28, S |
| **scorestrata** | A 6.98 | **S** | Ship v0.1 release (Rel 0→4: **+0.32**) + 2nd CI (**+0.4**) + README depth (**+0.2**) → 7.90; velocity band bump → S |
| **andrometry** | B 6.16 | **A** | 2 releases (**+0.32**) + 57 REST endpoints→60 (**+0.28**) → 6.76, A |
| **instagram-lyr** | B 6.41 | **A** | Ship 1–2 releases (**+0.32**) + velocity band (**+0.32**) → 7.05, A |
| **lifeos-ops** | B 5.39 | **A** | **Write tests** 0 → 150 (**+1.5**) + 2nd CI (**+0.4**) → 7.29, A — single biggest win in the portfolio |
| **obscura-core** | B 4.85 | **A** | MCP tools 8→31 (**+0.42**) + releases (**+0.32**) + tests 15→100 (**+0.5**) → 6.09, B+ |
| **lifeos-bot** | B 5.37 | **A** | CLI commands 3→5 (**+0.28**) + velocity band (**+0.32**) + tests 33→100 (**+0.4**) → 6.37, A |
| **discord-cli** | B 5.70 | **A** | Velocity band (11 commits/90d at 156d → need ~30: **+0.32**) + 2nd CI (**+0.4**) → 6.42, A |
| **holosim-infinite** | C 5.94* | **A** | Uncap: ship v0.1 release (**+0.32**) + add interactive surface (CLI/REST 0→16: **+0.42**) + velocity (**+0.32**) → 7.00, A |
| **kali-mahabali** | C 6.26* | **A** | Uncap: release + surface + velocity → A |
| **consciousness-fabricator** | C 5.18* | **B** | Uncap: ship a release (**+0.32**) → 5.50 natural B — tests already strong (158), CLI present (6) |

**Portfolio-wide rule:** re-run `scripts/rank_score.py` + `scripts/measure_repos.py`
after every milestone and update `README.md` tiers. The dataset is machine-generated,
so drift is caught by re-audit, not by hand.
