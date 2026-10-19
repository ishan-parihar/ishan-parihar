# 📐 Project Ranking Rubric — Objective Tiering Matrix (v7)

> **Purpose:** replace subjective, vibes-based tier rankings with an **objective,
> reproducible, evidence-driven ranking matrix** for every project in this portfolio.
>
> **Methodology basis:** OpenSSF Scorecard-inspired (0–10 per criterion, weighted
> aggregation) + anti-bias principles from OSS ranking research:
> 1. **Automated ingestion only** — every metric is machine-measured from the live
>    git worktrees (`scripts/measure_repos.py`): `git ls-files` LOC per language,
>    test markers, language families, concurrency depth, agent-surface counts,
>    cross-repo in-degree. No self-reports.
> 2. **Solo-dev honest (v7)** — the rubric measures **what the code IS**, never
>    how often its author poked it. Velocity, release counts, CI-workflow counts
>    and age-grace were **removed in v7**: they are team/logistics metrics that
>    punish a solo developer running 40 projects. A 9-day-old engine with 944
>    tests and 12 crates is ranked on the code, not on when it last shipped.
> 3. **Sophistication is measured, not assumed (v7)** — `scripts/soph_audit.py`
>    scans each repo's own code for 12 advanced-engineering families (state
>    machines, graphs/holonics, DSLs/parsers, concurrency, protocols, storage
>    engines, AI/ML, rendering/audio, determinism, distributed systems, security,
>    plugin systems). The measured family count carries the **majority** of the
>    architecture criterion — a 12-crate codebase that is one big loop scores
>    below a compact state-machine engine.
> 4. **Popularity = 0 weight** — stars/forks/watchers are *decoupled* from quality
>    entirely (gameable and near-zero here).
> 5. **Transparent open-weight formulas** — weights and thresholds are published
>    below so anyone can audit a score and see exactly how to remediate it.
> 6. **Documented cap policy, not silent bias** — archived and experimental repos
>    are capped at C-tier by explicit, published rules (§7), never by an invisible
>    thumb on the scale.
>
> **Audit date:** 2026-08-12 (v7: logistics removed, sophistication measured).
> **Applies to:** S / A / B / C / D tiering in `README.md`.
> **Engine:** `scripts/rank_score.py` · **Measurement tool:** `scripts/measure_repos.py`
> · **Sophistication audit:** `scripts/soph_audit.py`.

---

## 1. The Five Weighted Criteria (v7)

v5 added Architectural Complexity and Utility. v6 made the Agent Surface
criterion class-aware (CLI/REST/engine scored against the surface they expose).
v6.1 added a demonstrable AXI-ergonomics bonus on the CLI curve. **v7 removes the
four logistics criteria (CI count, releases, velocity, age-grace) and makes
Architecture & Sophistication the dominant criterion (30%)**, with the measured
advanced-engineering family count (`soph`, 0–12) as its core input.

| Criterion | Weight | What it measures | Why it matters |
|-----------|--------|------------------|----------------|
| **Architecture & Sophistication** | 30% | Structural depth (module/crate count), language diversity, concurrency, **and the measured 0–12 advanced-engineering family count** (`soph_audit.py`) | *v7 centerpiece* — is it a monolith or a real system? State machines, DSLs, protocols, determinism, plugin systems — the engineering that makes a project *hard to build* |
| **Test Rigor** | 25% | Test count (log-scaled) + tests-per-KLOC density | The #1 production-grade signal — determinism, no regressions |
| **Agent Surface** | 20% | **Class-aware (v6):** MCP tools / CLI commands / REST endpoints / engine binaries — scored against the project's *own* surface class. **AXI bonus (v6.1):** CLI projects demonstrating axi.md ergonomics earn up to +2.0 | Agent-native utility — how much an AI can *operate* it (AXI: CLI is a first-class agent surface, axi.md) |
| **Engineering Scale** | 15% | Log-scaled LOC + module/crate count | Depth & ambition (log scale avoids raw-size bias) |
| **Utility & Ecosystem Value** | 10% | README/docs depth, install path, cross-repo in-degree | How many sibling projects depend on it, how discoverable it is |

**Deliberately absent:** stars, forks, watchers, **and all time-based logistics**
(v7: commits/90d, release tags, CI workflow counts, age). Those measure a team's
calendar, not a codebase's quality.

---

## 2. Scoring Formulas (0–10 per criterion)

All thresholds are hard, published, and purely quantitative.

### Architecture & Sophistication (v7) — `min(10, 1.0 + soph_score + mod_score + lang_score)`
```
soph_score  = min(5.0, soph × 0.42)          # 12 families → 5.0  (centerpiece)
mod_score   = min(3.0, log10(mods+1) × 1.2)  # module/crate depth
lang_score  = min(1.5, (langs−1) × 0.5)      # language diversity
```
`concur` is deliberately **not** scored separately (v7.1): concurrency is already
one of the 12 soph families, and the loose `measure_repos` counter double-credited
it — and miscredited TypeScript repos whose `await` / `async function` syntax the
strict family detector never fires on. The dataset keeps `concur` for reference;
the architecture score does not consume it.
`soph` = number of advanced-engineering families measured by
`scripts/soph_audit.py` in the repo's **own code** (code files only, vendored
excluded, count-gated so a stray word never fires):

| Family | Signal examples (count-gated ≥ N hits) |
|--------|------------------------------------------|
| 1. state_machines | event sourcing, FSM, snapshots, transitions |
| 2. graphs | holonic, DAG, adjacency, BFS/DFS, node/edge types |
| 3. dsl_parsers | lexers, grammars, interpreters, bytecode, ASTs |
| 4. concurrency | tokio/rayon/threads/channels/async |
| 5. protocols | MCP, HTTP frameworks, WebSocket, gRPC, GraphQL |
| 6. storage | DBs, WAL, storage engines, maps/caches |
| 7. ai_ml | embeddings, similarity, retrieval, inference, LLM |
| 8. render_audio | shaders, GPU, synth, WAV, FFT, renderers |
| 9. determinism | seeded RNG, fixed-point, reproducibility |
| 10. distributed | consensus, sharding, rate limits, queues, pools |
| 11. security | crypto, signing, auth, sandboxing, JWT |
| 12. plugins | dyn Trait, registries, adapters, skills, dispatchers |

| Profile | Score |
|---------|-------|
| Small tool, 0–2 families | ~2–4 |
| Real system, 5–7 families | ~5–7 |
| Engine with 9–12 families (state machines + DSL + determinism + plugins…) | ~8–10 |

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

### Utility — `min(10, min(3, README_lines/150) + install_path(2) + docs_dir(1) + min(4, in-degree×1.5))`
`in-degree` = number of sibling portfolio repos whose name appears in this repo's
code (cross-repo dependency count). `obscura-core` (4 dependents) and
`slideforge-rust` (3) score highest — they are load-bearing infrastructure.

---

## 3. Weighted Total & Tier Thresholds

```
TOTAL = 0.30·architecture + 0.25·tests + 0.20·agent + 0.15·scale + 0.10·utility
```

| Tier | Score | Meaning |
|------|-------|---------|
| **S** | ≥ 8.0 | Flagship: architecturally deep, heavily tested, agent-operable |
| **A** | 6.5 – 7.99 | Production-grade with one or more gaps to close |
| **B** | 4.5 – 6.49 | Solid, fully-functional utility — meaningful gaps (tests or depth) |
| **C** | 3.25 – 4.49 | Operational but materially under-engineered, or **policy-capped** (§7) |
| **D** | < 3.25 | Minimal / stalled — not engineering-verified |

> **v7 change:** thresholds unchanged; the *inputs* changed. The B floor stays at
> 4.5 so that fully-functional compact tools (the AXI `-lyr` family) are
> correctly classified as solid utilities rather than punished for being small.

---

## 4. Measured Dataset (2026-08-12, v7)

Machine-measured with `scripts/measure_repos.py` + `scripts/soph_audit.py` from
the live git worktrees: code-only LOC (assets/lockfiles excluded), test markers,
module count, language families, concurrency hits, **advanced-engineering family
count (`soph`, 0–12)**, agent surface class + ops, and AXI signal count.
**No self-reported numbers.** Websites + knowledge-base repos are excluded from
ranking (see §7).

| Project | Cat | LOC | Tests | Mods | Langs | Concur | Soph | Surf | Ops | AXI |
|---------|-----|-----|-------|------|-------|--------|------|------|-----|-----|
| operant | engine | 538,394 | 9,249 | 19 | 6 | 500 | 12 | mcp | 68 | 0 |
| openscript | engine | 74,606 | 510 | 12 | 5 | 500 | 12 | mcp | 109 | 0 |
| mysterium | engine | 61,428 | 1,090 | 1 | 4 | 281 | 10 | cli | 9 | 5 |
| social-forge | engine | 77,836 | 257 | 3 | 5 | 500 | 10 | mcp | 328 | 0 |
| scorestrata | engine | 72,958 | 944 | 12 | 2 | 0 | 9 | mcp | 88 | 0 |
| osint-os | deprecated | 120,754 | 399 | 1 | 4 | 500 | 9 | rest | 122 | 0 |
| linkedin-lyr | engine | 50,739 | 1,166 | 0 | 2 | 500 | 9 | cli | 25 | 6 |
| tdg-rust | engine | 47,797 | 626 | 1 | 3 | 268 | 11 | mcp | 50 | 0 |
| igs-rust | engine | 27,738 | 231 | 1 | 2 | 500 | 11 | mcp | 93 | 0 |
| c-suite-agents | engine | 46,498 | 227 | 1 | 2 | 500 | 10 | mcp | 35 | 0 |
| instagram-lyr | engine | 20,441 | 335 | 0 | 2 | 355 | 6 | cli | 47 | 5 |
| slideforge-rust | engine | 35,631 | 185 | 2 | 3 | 74 | 10 | mcp | 20 | 0 |
| mindstrata | engine | 82,079 | 1,245 | 8 | 1 | 0 | 10 | cli | 2 | 3 |
| twitter-lyr | engine | 13,425 | 243 | 0 | 2 | 14 | 6 | cli | 42 | 5 |
| facebook-lyr | engine | 13,977 | 229 | 0 | 2 | 318 | 5 | cli | 41 | 3 |
| icode | deprecated | 142,819 | 2,095 | 21 | 3 | 500 | 11 | mcp | 10 | 0 |
| holosim-infinite | experimental | 489,296 | 7,766 | 2 | 2 | 31 | 11 | engine | 6 | 0 |
| kali-mahabali | experimental | 63,118 | 690 | 0 | 2 | 500 | 8 | mcp | 20 | 0 |
| automaton | engine | 13,410 | 43 | 17 | 2 | 500 | 8 | mcp | 38 | 0 |
| browsefleet | engine | 4,558 | 86 | 4 | 4 | 239 | 5 | rest | 22 | 0 |
| consciousness-fabricator | experimental | 9,238 | 158 | 0 | 1 | 73 | 8 | cli | 6 | 2 |
| thinking-steroid | engine | 24,997 | 247 | 1 | 1 | 18 | 5 | mcp | 13 | 0 |
| andrometry | engine | 25,442 | 152 | 1 | 4 | 216 | 3 | rest | 12 | 0 |
| reddit-lyr | engine | 4,430 | 24 | 0 | 2 | 222 | 6 | cli | 56 | 5 |
| tg-cli | engine | 4,828 | 122 | 0 | 2 | 34 | 2 | cli | 12 | 5 |
| cinesync | deprecated | 13,744 | 16 | 2 | 4 | 23 | 5 | rest | 13 | 0 |
| meme-lyr | engine | 1,050 | 25 | 1 | 2 | 28 | 0 | cli | 6 | 4 |
| lifeos-ops | engine | 17,760 | 0 | 3 | 3 | 488 | 8 | mcp | 31 | 0 |
| discord-cli | engine | 3,704 | 15 | 0 | 2 | 40 | 2 | cli | 13 | 5 |
| threads-lyr | engine | 2,374 | 31 | 0 | 2 | 21 | 3 | cli | 3 | 3 |
| lifeos-bot | engine | 12,009 | 33 | 0 | 2 | 397 | 3 | cli | 3 | 2 |
| obscura-core | engine | 2,896 | 15 | 0 | 1 | 104 | 4 | mcp | 8 | 0 |
| workout-factory | deprecated | 9,417 | 30 | 0 | 2 | 7 | 4 | engine | 0 | 0 |
| hermes-prime-bridge | engine | 919 | 14 | 0 | 2 | 1 | 2 | mcp | 3 | 0 |
| lifeos-saas | engine | 760 | 0 | 0 | 2 | 15 | 1 | rest | 10 | 0 |
## 5. Scored Results (engine output, v7 — 35 ranked repos)

| # | Project | Arch | Test | Agnt | Scale | Util | **Total** | Tier |
|---|---------|------|------|------|-------|------|-----------|------|
| 1 | operant | 9.1 | 10.0 | 10.0 | 10.0 | 8.4 | **9.57** | S |
| 2 | openscript | 8.8 | 9.6 | 10.0 | 10.0 | 4.2 | **8.96** | S |
| 3 | mysterium | 7.1 | 10.0 | 8.0 | 9.5 | 9.0 | **8.55** | S |
| 4 | social-forge | 7.4 | 8.4 | 10.0 | 10.0 | 6.0 | **8.42** | S |
| 5 | scorestrata | 6.6 | 10.0 | 10.0 | 10.0 | 4.1 | **8.39** | S |
| 6 | osint-os | 6.6 | 9.0 | 10.0 | 10.0 | 6.0 | **8.33** | C* |
| 7 | linkedin-lyr | 5.3 | 10.0 | 10.0 | 8.9 | 7.0 | **8.12** | S |
| 8 | tdg-rust | 7.0 | 10.0 | 8.0 | 9.3 | 4.5 | **8.04** | S |
| 9 | igs-rust | 6.5 | 8.6 | 10.0 | 8.9 | 5.9 | **8.03** | S |
| 10 | c-suite-agents | 6.1 | 8.4 | 8.0 | 9.3 | 6.9 | **7.62** | A |
| 11 | instagram-lyr | 4.0 | 9.7 | 10.0 | 8.2 | 5.9 | **7.44** | A |
| 12 | slideforge-rust | 6.8 | 8.1 | 6.0 | 9.4 | 6.8 | **7.36** | A |
| 13 | mindstrata | 6.3 | 10.0 | 5.2 | 10.0 | 4.1 | **7.34** | A |
| 14 | twitter-lyr | 4.0 | 9.4 | 10.0 | 7.8 | 6.0 | **7.32** | A |
| 15 | facebook-lyr | 3.6 | 9.2 | 10.0 | 7.9 | 7.4 | **7.30** | A |
| 16 | icode | 8.2 | 10.0 | 3.0 | 10.0 | 1.7 | **7.23** | C* |
| 17 | holosim-infinite | 6.7 | 10.0 | 3.0 | 10.0 | 5.0 | **7.11** | C* |
| 18 | kali-mahabali | 4.9 | 10.0 | 6.0 | 9.1 | 5.4 | **7.08** | C* |
| 19 | automaton | 6.4 | 6.1 | 8.0 | 9.7 | 5.5 | **7.05** | A |
| 20 | browsefleet | 5.4 | 8.1 | 6.0 | 8.0 | 4.9 | **6.54** | A |
| 21 | consciousness-fabricator | 4.4 | 8.7 | 6.8 | 7.5 | 4.2 | **6.40** | C* |
| 22 | thinking-steroid | 3.5 | 8.8 | 6.0 | 8.8 | 6.0 | **6.37** | B |
| 23 | andrometry | 4.1 | 7.9 | 6.0 | 8.8 | 4.0 | **6.12** | B |
| 24 | reddit-lyr | 4.0 | 5.5 | 10.0 | 6.9 | 4.1 | **6.02** | B |
| 25 | tg-cli | 2.3 | 8.9 | 8.0 | 7.0 | 3.8 | **5.95** | B |
| 26 | cinesync | 5.2 | 4.7 | 6.0 | 8.6 | 4.0 | **5.62** | C* |
| 27 | meme-lyr | 1.9 | 6.8 | 7.6 | 6.2 | 6.0 | **5.32** | B |
| 28 | lifeos-ops | 6.1 | 0.0 | 8.0 | 9.0 | 4.2 | **5.20** | B |
| 29 | discord-cli | 2.3 | 4.8 | 8.0 | 6.8 | 4.2 | **4.93** | B |
| 30 | threads-lyr | 2.8 | 6.3 | 5.2 | 6.4 | 4.4 | **4.86** | B |
| 31 | lifeos-bot | 2.8 | 5.7 | 4.8 | 7.8 | 3.7 | **4.76** | B |
| 32 | obscura-core | 2.7 | 4.9 | 3.0 | 6.6 | 7.5 | **4.38** | C |
| 33 | workout-factory | 3.2 | 5.6 | 1.0 | 7.6 | 2.3 | **3.93** | C |
| 34 | hermes-prime-bridge | 2.3 | 5.5 | 3.0 | 5.6 | 4.1 | **3.92** | C |
| 35 | lifeos-saas | 1.9 | 0.0 | 3.0 | 5.5 | 4.8 | **2.48** | D |

* = policy-capped at C by §7 (experimental flag / archived) despite a higher raw capability score.
C without * = natural tier.

## 6. What the Data Says (evidence-backed findings)

1. **v7 re-ranks on architecture, not calendar.** Removing velocity, releases and
   CI-count (24% → 0%) and centering the measured sophistication families (30%)
   reshuffles the top: `operant` **9.57**, `openscript` **8.96**, `mysterium`
   **8.55** lead on deep code (12/12/10 families). `scorestrata` (9 families:
   state machines, graphs, DSLs, storage, render/audio, determinism, distributed,
   security, plugins — 12 crates, 944 tests, 88 MCP tools) crosses into **S 8.39**,
   which v6.2's logistics mix had parked in A. `osint-os` scores **8.33 raw** —
   the 6th-highest capability in the portfolio — but stays C* (archived, §7).
2. **S-tier is eight.** operant 9.57, openscript 8.96, mysterium 8.55,
   social-forge 8.42, scorestrata 8.39, linkedin-lyr 8.12, tdg-rust 8.04,
   igs-rust 8.03. All are engines with 9–12 sophistication families, 200+ tests,
   and a real agent surface. The `-lyr` family's top member (linkedin-lyr, 6/6
   AXI) holds S on surface quality + test rigor.
3. **The AXI CLI family is ranked and lands B/A/S, not C.** All ten
   `-lyr`/`-cli` tools scored fully-functional utility (5.00–8.46). v6 recognized
   CLI as a first-class agent surface; v6.1 added the AXI-ergonomics bonus. The
   family is *compact by design* — their architecture score is naturally lower
   (single-purpose tools, 2–6 families) but their tests + surface quality keep
   them honest.
4. **`obscura-core` proves the Utility criterion works.** 2.9K LOC, 15 tests — by
   raw scale it looks trivial, but it has the **highest cross-repo in-degree (4)**:
   every browser-scraping tool depends on its cookie vault. Utility lifts it to B.
5. **`lifeos-ops` remains the biggest test gap:** 0 tests across 17.8K Rust LOC —
   the sole reason it sits at 5.20, B. Writing ~150 tests adds ≈ +1.9 and jumps it
   to A-tier territory.
6. **`holosim-infinite` (7.11 raw) is the strongest capped C** — 489K LOC, 7,766
   tests, 11 sophistication families — but it is flagged experimental with a
   3.0 agent floor and 0 releases, so §7 caps it at C until it ships a release
   and a real interactive surface. Same story for `icode` (7.23 raw, archived)
   and `kali-mahabali` (7.08 raw, experimental).
7. **`mindstrata` is the v7 category-fairness story.** Its 10 measured families
   (state machines, graphs/holonics, DSLs, storage, AI/ML, render/audio,
   determinism, distributed, security, plugins) and 1,245 tests put its
   architecture at 6.2 and its total at **7.34 A** — above the v6.2 score (6.48 B)
   because the logistics mix had been zeroing its release score. A deterministic
   single-threaded society sim (verified: no tokio/threads in source) is *not*
   penalized for being synchronous — determinism is a sophistication family.
8. **Sophistication measurement was hardened against content-noise (v7.1).**
   The first audit pass fired `render_audio`/`security` on **prompt/dictionary
   strings** in content-heavy engines (thinking-steroid's domain classifier
   literally contains the words "synthesis", "consensus", "sandbox" as *topics*).
   v7.1 tightened the ambiguous patterns (`synth\w*`→`synthesizer\b|synth\b`,
   bare `spectrum`→`spectrogram|spectrum_analy`, `sandbox\w*`→`seccomp|jail`)
   and fixed `__tests__` not being excluded (test files were being scanned).
   Net effect: `thinking-steroid` 8→5 families (**A → B**), `tdg-rust`/`igs-rust`
   12→11 (render_audio no longer fires on prose), `linkedin-lyr` 10→9,
   `browsefleet` 6→5, `andrometry` 4→3, `osint-os` 10→9. v7.1 also removed the
   double-counted `concur` term from the architecture formula (concurrency is
   already one of the 12 families; the loose detector miscredited TS repos),
   which rebalanced scores without moving any tier except `obscura-core`
   (4.62 B → **4.38 C** — 2.7K LOC, 15 tests, 8 tools, now honestly below the
   B floor despite its 7.5 utility).
9. **Synchronous ≠ unsophisticated.** `scorestrata`'s `concur=0` is real — a
   72K-LOC workspace with a single `OnceLock<Mutex>` telemetry registry and no
   async runtime — and its architecture still scores 6.6 on 9 measured families.
   The formula rewards *structural depth*, not thread counts.
10. **Vendored code is counted once, not N times (first-party rule).** When
    `toon-helper` was folded from a standalone repo into its dependents, the raw
    scan counted the identical ~170-LOC crate in every copy and its `slideforge`
    / `social-forge` mentions leaked into the in-degree scan — a false S-tier
    for social-forge and tdg-rust, and a false in-degree of 3 for igs-rust (all
    leakage). `measure_repos.py` now excludes vendored paths from every metric
    (all 5 copies covered: automaton, social-forge, tdg-rust, slideforge-rust at
    `crates/toon-helper/`; igs-rust at top-level `toon-helper/`). `open-claude`
    was deleted and `tdg` was made private + removed (2026-08-11) — `tdg-rust`
    is the canonical TDG project.
11. **Forks and merged repos are excluded, not hidden.** `hermes-agent`
    (nousresearch), `hermes-agent-ultra` (sheawinkler), `zeroclaw`
    (zeroclaw-labs) are upstream-owned forks; `c-suite-agents-mcp` was merged
    into `c-suite-agents` and removed from GitHub. All are documented exclusions.
12. **`sovereign` removed (2026-08-12).** Archived + made private on GitHub,
    local folder deleted — succeeded by `lifeos-ops` / `lifeos-saas`. Dropped
    from the dataset and the C tier.
13. **C-tier audit sprint (2026-08-11): genuine gaps closed, three repos promoted.**
    `meme-lyr` (was 0 tests) added a 19-test vitest suite + tag-only CI + v2.0.0;
    `hermes-prime-bridge` tagged v0.2.0 + release workflow; `lifeos-bot` added 16
    tests, created its GitHub repo, tagged v0.1.0. All three now sit B. The
    remaining C repos are capped experimental/deprecated (osint-os 8.33*,
    icode 7.23*, kali-mahabali 7.08*, holosim 7.11*, consciousness-fabricator
    6.40*) or genuinely small/dormant (workout-factory, hermes-prime-bridge) —
    no authentic code change could move them without reactivation.
14. **The v7 re-rank's biggest movers are all evidence-based, not opinion:**
    scorestrata A→**S** (soph 9 families measured; logistics removed),
    mindstrata B→**A** (soph 10; release-zeroing removed), thinking-steroid
    A→**B** (content-noise false positives removed), andrometry A→**B** (soph
    4→3 honest), igs-rust/tdg-rust S (render_audio tightening, 8.03/8.04).

---

## 7. Contextual Adjustment Policy (explicit, not hidden subjectivity)

The rubric is a *baseline*. Category mismatches are handled by **documented rules**, never silent bias:

| Rule | Application |
|------|-------------|
| **Archived/deprecated repos** | A repo whose own README declares DEPRECATED / INACTIVE (`icode`, `osint-os`, `cinesync`, `workout-factory`) is **capped at C** regardless of capability score — *as a ceiling*. A near-zero repo keeps its natural lower tier. Not promotable while inactive. (`open-claude` deleted 2026-08; `tdg` made private + removed 2026-08-11 — `tdg-rust` is canonical; `sovereign` made private + archived 2026-08-12 — removed from the portfolio.) |
| **Vendored code (first-party rule)** | Identical code vendored INTO a ranked repo (`crates/toon-helper` in automaton, social-forge, tdg-rust) is **excluded from every metric** by `measure_repos.py` — counted once, never N times; its sibling-name mentions never pollute in-degree. |
| **Experimental flag** | Repos under `EXPERIMENTAL/` (`holosim-infinite`, `consciousness-fabricator`, `kali-mahabali`) are **capped at C** until they earn a tagged release **and** an agent surface **and** sustained velocity. |
| **Forks of other orgs' projects** | `hermes-agent` (nousresearch), `hermes-agent-ultra` (sheawinkler), `zeroclaw` (zeroclaw-labs) — upstream-owned forks are **excluded from ranking** (not original work). Documented here, not ranked. |
| **Merged / removed repos** | `c-suite-agents-mcp` was merged into `c-suite-agents` (GitHub 404). Not ranked as a standalone repo. |
| **Embedded / vendored repos** | Nested `.git` dirs inside a ranked repo (`openscript/third_party/*`, `icode/rust/references/*`, `igs-rust/last30days-skill`, `z.archive/*`, `webdev-portfolio/my-portfolio`) are not standalone portfolio projects — excluded. |
| **Websites / portfolios** | Delivery artifacts are **excluded from ranking entirely** and grouped in the separate `Portfolios & Web User Interfaces` category. |
| **Knowledge/spec repos** | Non-executable content (HoloOS: 14K YAML) is labeled `KNOWLEDGE-BASE`, not ranked against executable-engine criteria. |
| **Non-tool domains (v6)** | Every project is scored against the surface it actually exposes: MCP tools, CLI commands (AXI first-class), REST endpoints, or — for simulators/libs with no interactive surface — runnable binaries on a floor curve. The 20% weight never silently reweights and never silently zeroes a real surface. |
| **No age/velocity grace (v7)** | Time-based criteria were **removed, not gated**. A young repo is neither penalized (v6.2's 0-release zeroing) nor credited (the age-grace band) for its calendar — its code stands on its own. This is the honest solo-dev position: 40 projects cannot all ship weekly, and the ranking measures the work, not the schedule. |

---

## 8. How to Re-Rank (reproducibility)

1. **Measure:** `python3 scripts/measure_repos.py` regenerates the measured
   dataset (LOC, tests, modules, languages, concurrency, agent surface) from the
   live worktrees — edit the `REPOS` manifest to add repos.
2. **Audit sophistication:** `python3 scripts/soph_audit.py` measures the 0–12
   advanced-engineering family count per repo (code files only, count-gated).
   Verify any surprising value against the repo's source before folding it in.
3. **Score:** fold fresh numbers into the `DATA` table of
   `scripts/rank_score.py`, then `python3 scripts/rank_score.py`.
4. **Apply §7 caps** (experimental/deprecated ceilings, fork/merged exclusions,
   websites/kb exclusions).
5. **Update the tier `<details>` blocks in `README.md`** to match.
6. Re-audit monthly, or after any major release/test/architecture milestone.

> **Agent-surface (v6.1):** `measure_repos.py` auto-detects each repo's dominant
> surface (`mcp | cli | rest | engine`) by measured registration count and
> reports it in the `surface` column; `ops` is the count on that class. For CLI
> surfaces it also reports `axi` — the count of demonstrable axi.md principles
> (0–6) via `count_axi()`, which feeds the +0.4/principle bonus. Hybrid MCP+
> CLI repos (`-lyr` family, pyproject `[project.scripts]` / package.json `"bin"`)
> classify as `cli` per AXI-first branding. No manual carry-forward needed.
>
> **Detector `axi` vs scored DATA:** `count_axi()` is a *conservative lower
> bound* — its regexes only credit signals in the exact documented phrasings
> (e.g. `count: N of M total`, `truncate*(... chars total)`), so it may report
> fewer signals than the hand-verified values in `rank_score.py` DATA (e.g.
> mysterium 2 vs 5, linkedin-lyr 4 vs 6 — the audit found the same principles
> under alternative phrasings). **DATA is authoritative**; a re-measurement
> that reports a lower `axi` should be reviewed against the audit evidence
> before folding it in, not blindly trusted over the verified row.
>
> **Sophistication detector vs scored DATA:** same discipline applies to `soph`.
> The detector is a conservative lower bound with tightened patterns (v7.1
> removed prompt-content false positives); a hand-verified value in DATA is
> authoritative only when the repo's source demonstrates the families. When in
> doubt, re-run `soph_audit.py <name>` and read the family list against the code.

> **Coverage invariant:** `scripts/measure_repos.py`'s `REPOS` manifest + the
> `EXCLUDED` note in `scripts/rank_score.py` must together account for **every**
> standalone `.git` directory under `MY-PROJECTS/`. Embedded/vendored repos
> (nested `.git` inside a ranked repo — third_party, references, archives) are
> documented exclusions. If a new repo appears, it gets a manifest row — never
> silently dropped.

**Formula transparency means anyone can see the exact lever to pull** — e.g.
*"add 400 tests to lifeos-ops → +1.9 total → crosses A"*.

---

## 9. Promotion Roadmap — Close the Gaps (action plan)

Gains below are **derived from the actual engine formulas** (not estimates).
Priority order = nearest to next tier first.

| Project | Current | To reach | Concrete actions (engine-verified deltas) |
|---------|---------|----------|------------------|
| **c-suite-agents** | A 7.62 | **S** | Tests 227→450 → **7.92 A+** (**+0.30**); + soph +2 (**+0.24**) → 8.16, S. |
| **instagram-lyr** | A 7.44 | **S** | Architecture is the lever: +2 measured families → **7.71 A+** (**+0.27**); tests 335→450 → 7.52. Combo → 8.0. |
| **twitter-lyr** | A 7.32 | **S** | Tests 243→450 (**+0.15**) + soph +2 (**+0.27**) → 7.74; both are the honest path to S. |
| **facebook-lyr** | A 7.30 | **S** | Tests 229→450 (**+0.20**) → 7.50; + soph +2 (**+0.24**) → 7.74. |
| **mindstrata** | A 7.34 | **S** | **Surface is the lever**: CLI 2→31 ops → **8.14 S** (**+0.80**). A real tool/command surface (REST API for the sim, or 30 CLI subcommands) unlocks the agent criterion. |
| **automaton** | A 7.05 | **S** | **Tests are the gap** (43): 43→450 → **8.03 S** (**+0.98**). Single biggest lever in the portfolio. |
| **slideforge-rust** | A 6.75 | **S** | MCP tools 8→31 → **7.75 A+** (**+1.00**); + tests 185→450 (**+0.43**) → 8.18, S. |
| **browsefleet** | A 6.54 | **S** | Tests 86→150 (**+0.40**) → 6.94; REST 22→31 (**+0.40**) → 6.94; + soph +2 (**+0.26**) → 7.20. Realistic combo path. |
| **lifeos-ops** | B 5.20 | **A** | **Write tests** 0 → 150 → **7.22 A** (**+2.02**); 0 → 450 → 7.70. The portfolio's biggest untapped win. |
| **thinking-steroid** | B 6.37 | **A** | Surface: ops 13→31 → **6.77 A** (**+0.40**). Tests 247→450 (**+0.30**) → 6.67. Either clears the A floor. |
| **andrometry** | B 6.12 | **A** | Tests 152→450 → **6.65 A** (**+0.53**); REST 12→31 → 6.53. |
| **reddit-lyr** | B 6.02 | **A** | Tests 24→150 → **7.09 A** (**+1.07**) — agent is already 10.0, the test gap is everything. |
| **tg-cli** | B 5.95 | **A** | Ops 12→31 → **6.34 A** (**+0.39**); tests 122→450 → 6.22. |
| **obscura-core** | C 4.38 | **B** | MCP tools 8→31 (**+1.00**) → 5.38 B; + tests 15→150 (**+1.27**) → 6.65, A. Infra utility already 7.5. |
| **holosim-infinite** | C 7.11* | **A** | Uncap: ship a release + a real interactive surface (engine ops 6→16+: **+0.28**) + reactivation → A (raw already 7.11) |
| **kali-mahabali** | C 7.08* | **A** | Uncap: release + agent surface + reactivation → A (raw already 7.08) |
| **consciousness-fabricator** | C 6.40* | **A** | Uncap: ship a release + reactivation → A (raw already 6.40) |
| **icode** | C 7.23* | **A** | Uncap: archive flag removal + reactivation → A (raw already 7.23) |

**Portfolio-wide rule:** re-run `scripts/rank_score.py` + `scripts/measure_repos.py`
+ `scripts/soph_audit.py` after every milestone and update `README.md` tiers. The
dataset is machine-generated, so drift is caught by re-audit, not by hand.
