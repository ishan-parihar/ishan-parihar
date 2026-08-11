# Profile README — Technical & Logical Discrepancy Audit

> **Purpose:** verify every mention of a project inside `README.md` (the profile) against
> (a) that project's own README and (b) machine-measured reality from the live git
> worktrees. Delivers a prioritized fix list so the profile never contradicts its own
> repositories.
>
> **Method:** read-only investigation (one new doc written; no source changes).
> Evidence: per-repo README inspection + `git ls-files` LOC / test-marker / tag / CI /
> crate-directory measurement for all 43 catalog entries. Companion: `PROFILE-README-AUDIT.md`
> (metric-verification audit) and `RANKING-RUBRIC.md`.
>
> **Audit date:** 2026-08-12 · Repos measured at their local HEADs.

---

## 0. TL;DR — the three headline findings

1. **The profile's `operant` entry describes a different product.** The flagship + catalog
   text ("Multi-agent corporate runtime … CFO/COO/CRO/CMO … LanceDB … Drizzle … systemd …
   twin `c-suite-agents`") matches the **old TypeScript operant — which is now `c-suite-agents`**
   (its README still literally calls itself "Operant"). The current Rust `operant` is a
   terminal-native ReAct agent runtime with `agentmemory` (BM25+vector+graph) memory. The two
   entries have been conflated.
2. **Tool/test surfaces are materially wrong for four repos** — openscript (profile 43 tools,
   README 109), andrometry (profile 367 tests, actual 152–153), c-suite-agents (profile 555
   tests / "Postgres+Drizzle", actual 227 passing / no DB stack in code), social-forge (profile
   "9 networks", README "30 platforms", code ~16).
3. **Five catalog entries have no local checkout** — `osint-os`, `cinesync`, `sovereign`,
   `workout-factory`, `HoloOS` (all under `(Deprecated⁄Inactive)` dirs or uncloned). Their
   catalog numbers cannot be reproduced and are excluded from the profile's headline aggregates.

---

## 1. `operant` — the deep dive (profile vs README vs code)

### 1.1 What the profile claims (flagship §, line 176, and catalog S-tier)

> "Multi-agent corporate runtime with LanceDB memory & systemd process isolation. Rust. 9,200+ tests."
> — specialized roles (CFO, COO, CRO, CMO) with prioritized escalation logic, Kanban boards,
> "LanceDB vector memory and 25+ relational Postgres tables using Drizzle", "persistent systemd
> services with active health checks", "Twin: TypeScript implementation (c-suite-agents)".

### 1.2 What the current Rust operant actually is (measured at `HERMES/operant`, HEAD `90968053`)

| Claim | Reality | Verdict |
|---|---|---|
| "Multi-agent corporate runtime" | Terminal-native **ReAct agent runtime** — `operant chat`/`run`/`autonomous`, ratatui TUI, local-first | ✗ Identity mismatch |
| CFO/COO/CRO/CMO roles + escalation | No `cfo/coo/cro/cmo` matches anywhere in `crates/` | ✗ Absent |
| "LanceDB vector memory" | Memory = `agentmemory` provider (BM25 + local embeddings, hybrid) per `operant-memory/src/backend.rs`; optional `memory-postgres` feature (sqlite default) | ✗ Wrong engine |
| "25+ Postgres tables using Drizzle" | No Drizzle anywhere (Rust workspace; Drizzle is a TS ORM). Postgres is a Cargo feature flag only | ✗ Impossible / absent |
| "systemd process isolation" | systemd appears only in skill-guard regexes + `doctor`/`gateway` status text; not a capability | ✗ Not a feature |
| Kanban boards | `KanbanDb`, `KanbanTool` registered in `operant-core/src/tools/` | ✓ Real |
| 538K LOC | 537,602 code LOC across tracked code files | ✓ |
| 9,240 tests | 9,220 Rust `#[test]` markers (9,288 incl. TS) | ~ (20 over) |
| 20 crates (catalog) / 19 (metrics) | 18 crate dirs = **19 Cargo.toml manifests** (with root) | ~ catalog "20" is over |
| 4 CI workflows / 3 releases | build, ci, release, test = 4 ✓ · tags v0.1.2–v0.1.4 = 3 ✓ | ✓ |
| 50+ tools (README) | ~92 distinct tool names registered in `operant-core`/`operant-tools`; `rank_score.py` DATA says **30** | rank DATA stale |

### 1.3 Why the confusion happened

`c-suite-agents` (`LIFEOS/c-suite-agents`) **still calls itself "Operant"** in its README:
> "Operant is built as an operations engine rather than a single chatbot. It coordinates
> specialized agents (CEO, COO, CFO, etc.) … LanceDB semantic memory … CLI and Telegram …
> Production Install (systemd)".

Every C-suite / LanceDB / Telegram / systemd claim the profile makes under `operant` belongs to
that TypeScript codebase. The profile's own "Twin: … (c-suite-agents)" sentence is the tell — it
wrote the twin's identity into the primary's entry.

### 1.4 Issues in the operant README itself

- **`LICENSE` is referenced but missing** — README says "MIT or Apache-2.0 — see [LICENSE](LICENSE)";
  the file does not exist in the repo (Cargo.toml declares the dual license, but no LICENSE file is tracked).
- "50+ tools" understates the registry (~92 distinct tool names) — a number the profile then
  inherits (rank DATA = 30).
- Everything else checks out: Rust 1.89 badge = `rust-version = "1.89"` ✓, assets
  (`hero.svg`, `main.png`, `chat.png`) exist ✓, every `operant <subcommand>` in the CLI table
  resolves ✓, quick-start files (`scripts/install.sh`, `operant.example.toml`, `AGENTS.md`) exist ✓.

---

## 2. Portfolio-wide discrepancies (profile vs README vs reality)

Severity legend: **HIGH** = describes the wrong thing / materially false · **MED** = a claim that
misrepresents the repo today · **LOW** = numeric drift.

### 2.1 MED/HIGH — description & surface mismatches

| Repo | Profile says | Repo README / reality says | Severity |
|---|---|---|---|
| **openscript** | "43 MCP tools" (ecosystem + A-tier) | README: "**109 MCP tools** (verified: 103 static + 6 dynamic in `openscript-mcp/src/tools.rs`)" | MED — 2.5× understated |
| **andrometry** | "367 tests" (B-tier) | README badge "152 passing"; 153 Go `func Test` measured | MED — 2.4× overstated |
| **c-suite-agents** | "555 tests" · "Postgres/Drizzle" (A-tier + ecosystem) | README badge "227 passing"; 454 TS markers; Postgres/Drizzle appear **only inside a T2I image-spec comment**, not in code (LanceDB + Telegram are real) | MED |
| **social-forge** | "9 networks" (flagship + catalog) | README hero: "**30 social platforms**"; code contains ~16 platform identifiers | MED — profile vs README contradict |
| **webdev-portfolio** | "Next.js 15 / TypeScript — fast, conversion-optimized landing page" (websites) | Repo tracks **no source code** (3 `.md` + config files only; 0 code LOC) | MED — entry describes a repo that isn't there |
| **mysterium** | "Education-system replacement — 64-cell developmental matrix, holonic curriculum" (A-tier) | README: "contemplative-assessment RPG … eight-stage arc of consciousness … 64-cell module matrix". (Per the user's direction this identity is intended; the README framing lags the architecture docs) | LOW-MED |
| **lifeos-saas** | "760 LOC" (D-tier) | 371 code LOC measured | LOW |

### 2.2 LOW — numeric drift

| Repo | Profile claim | Measured | Notes |
|---|---|---|---|
| tdg-rust | 637 tests | 648 markers; README badge **626 passing** | three conflicting numbers across profile/README/code |
| osint-os | 121K LOC · 399 tests | 115,367 code LOC · 579 markers | LOC ≈ (all-tracked ~121K) ✓; tests drift |
| mysterium | 1,090 tests | 948 markers | 140 over |
| thinking-steroid | 247 tests | 232 markers | |
| social-forge | 257 tests | 278 markers | understated |
| igs-rust | (rank DATA 231) | 242 markers | profile doesn't claim |
| slideforge-rust | 185 tests | 196 markers | matches README badge (185 passing) |
| mindstrata | 1,238 tests | 1,256 markers | matches badge (1238 passing) |
| design-aesthetics-website | 49K LOC | 46,195 code LOC | |
| operant catalog | "20 crates" | 19 manifests / 18 dirs | |

### 2.3 Verified-correct claims (so fixes don't touch these)

- **LOC:** scorestrata 73K ✓, mindstrata 82.3K ✓, operant 538K ✓, holosim 489K ✓, slideforge 35.5K ✓,
  lifeos-ops 17.6K ✓, lifeos-bot 11.9K ✓, openscript 74.6K ✓, tdg-rust 47.4K ✓, andrometry 26.1K ✓, etc.
- **Tests (exact match):** linkedin-lyr 1,166 · twitter-lyr 243 · instagram-lyr 335 · facebook-lyr 229 ·
  reddit-lyr 24 · threads-lyr 31 · lifeos-bot 33 · browsefleet 86 · tg-cli 122 · scorestrata 944 ·
  holosim-infinite 7,766 · consciousness-fabricator 158 · lifeos-ops 0 · lifeos-saas 0 · meme-lyr 19 (npm).
- **Releases/CI:** linkedin 94/4 ✓ · twitter 32/2 ✓ · tg-cli 14/2 ✓ · discord 10/2 ✓ · lifeos-ops 10 ✓ ·
  browsefleet 5 CI ✓ · tdg 10 ✓ · slideforge 6 ✓ · igs 15 ✓ · c-suite 3 ✓ · operant 4/3 ✓ · scorestrata 1 ✓.
- **Identities:** scorestrata, mindstrata, slideforge-rust, igs-rust, tdg-rust, automaton, browsefleet,
  discord-cli, tg-cli, lifeos-bot, lifeos-ops, obscura-core, hermes-prime-bridge, meme-lyr,
  kali-mahabali (Chimera), icode/osint-os/cinesync/workout-factory (deprecated banners) all match.

### 2.4 Missing local checkouts (numbers unverifiable)

| Catalog entry | Local state | Impact |
|---|---|---|
| osint-os | `EXPERIMENTAL/osint-os (Deprecated⁄Inactive)` — measured above | verified in this audit (see §2.2) |
| cinesync | `CONTENT-CREATION/cinesync (Deprecated⁄Inactive)` — 11,336 code LOC · 2 CI ✓ | ✓ |
| workout-factory | `EXPERIMENTAL/workout-factory (Deprecated⁄Inactive)` — 9,404 code LOC · 1 CI | ✓ |
| sovereign | **no repo checked out** (only an unrelated `src/lib/utils/sovereign` folder inside ishanparihar-svelte) | unverifiable |
| HoloOS | **no repo checked out** (only the `02-holoos-salon` initiative folder) | unverifiable |

`measure_repos.py` reports these as NO-DIR, so the profile's headline aggregates
(2.38M LOC / 31,340 tests) structurally **exclude** osint-os + cinesync + workout-factory + sovereign + HoloOS.

---

## 3. Internal inconsistencies inside the profile itself

- **operant tests** appear as "9.2K" (metrics), "9,200+" (flagship), "9,240" (catalog) — three phrasings.
- **operant crates** appear as "19" (metrics footnote) and "20 crates" (catalog S-tier).
- **tdg-rust** "637 tests" (catalog) vs its own README badge "626 passing".
- **crate-count footnote** (operant 19 / automaton 17 / scorestrata 12 / mindstrata 8) is consistent
  when read as *Cargo.toml manifests* (18+1 / 16+1 / 11+1 / 7+1) — but not as crate directories.
- **Metrics "31,340 test markers"** aggregates marker counts; several repos' *passing* counts are lower
  (andrometry 152 vs 367 markers-equivalent, c-suite 227 vs 454), so "tests" and "test markers" must
  stay labeled distinctly.

---

## 4. Open methodology items (carried from PROFILE-README-AUDIT)

- **N2 tool-surface counting:** "800+ tools" (metrics) cannot be reproduced yet — the ecosystem table's
  per-repo counts (igs 91, openscript 109, operant ~92, …) are not all machine-countable by
  `measure_repos.py` (Python-decorator-only counter). Fix N2 before regenerating ecosystem tables.
- **MCP Servers "20+"** holds (22 MCP-capable repos) ✓.

---

## 5. Prioritized fix plan

1. **operant (HIGH):** rewrite the flagship + catalog entries to describe the actual Rust product
   (terminal-native ReAct agent runtime, agentmemory, MCP client+server, skills, channels, kanban).
   Move the C-suite/LanceDB/systemd/Telegram story to `c-suite-agents` — including its own test count.
   Correct catalog "20 crates" → 19 and "9,240 tests" → "9.2K".
2. **openscript (MED):** 43 → 109 tools in ecosystem + A-tier.
3. **andrometry (MED):** 367 → ~152 tests (badge) or re-run its suite; keep "13 days old" only if current.
4. **c-suite-agents (MED):** 555 → verified passing count; drop or verify "Postgres/Drizzle".
5. **social-forge (MED):** reconcile "9 networks" vs "30 platforms" — pick the code-verifiable number.
6. **webdev-portfolio (MED):** either restore the tracked site or relabel the entry.
7. **tdg-rust / mysterium / thinking-steroid / osint-os (LOW):** re-fold `rank_score.py` DATA to the
   measured marker counts and to README badges where they disagree.
8. **sovereign / HoloOS:** re-clone or mark "not in workspace" so the catalog stays auditable.
9. **operant README:** add the missing `LICENSE` file (or fix the link); bump "50+ tools" to the
   registered count.

---

## 6. Evidence appendix (HEADs measured)

| Repo | code LOC | test markers | tags | CI | crates |
|---|---|---|---|---|---|
| operant | 537,602 | 9,220 rs / 68 ts | 3 | 4 | 18 |
| c-suite-agents | 45,493 | 454 ts | 3 | 1 | – |
| openscript | 72,322 | 518 (503 rs) | 0 | 2 | – |
| social-forge | 76,618 | 278 (264 rs) | 2 | 2 | – |
| andrometry | 26,137 | 153 go | 0 | 1 | – |
| linkedin-lyr | 50,200 | 1,166 py | 94 | 4 | – |
| mysterium | 61,092 | 948 (892 ts) | 0 | 2 | – |
| tdg-rust | 47,539 | 648 rs | 10 | 1 | – |
| twitter-lyr | 13,116 | 243 py | 32 | 2 | – |
| instagram-lyr | 20,318 | 335 py | 0 | 1 | – |
| facebook-lyr | 13,702 | 229 py | 0 | 1 | – |
| thinking-steroid | 24,997 | 232 ts | 0 | 2 | – |
| browsefleet | 4,051 | 86 ts | 2 | 5 | – |
| mindstrata | 82,769 | 1,256 rs | 0 | 1 | 7 |
| scorestrata | 72,958 | 944 rs | 0 | 1 | 11 |
| slideforge-rust | 35,484 | 196 rs | 6 | 1 | 1 |
| automaton | 13,437 | 54 rs | 1 | 2 | 16 |
| igs-rust | 27,563 | 242 rs | 15 | 2 | – |
| holosim-infinite | 489,245 | 7,766 rs | 0 | 2 | – |
| consciousness-fabricator | 9,238 | 158 py | 0 | 1 | – |
| osint-os | 115,367 | 579 py | 0 | 1 | – |
| cinesync | 11,336 | 35 | 0 | 2 | – |
| workout-factory | 9,404 | 51 | 0 | 1 | – |
| lifeos-saas | 371 | 0 | 0 | 1 | – |
| lifeos-ops | 17,589 | 0 | 10 | 1 | – |
| lifeos-bot | 11,762 | 33 py | 1 | 2 | – |
| discord-cli | 3,631 | 15 py | 10 | 2 | – |
| tg-cli | 4,651 | 122 py | 14 | 2 | – |
| meme-lyr | 952 | 19 (npm) | 1 | 2 | – |
| reddit-lyr | 4,103 | 24 py | 0 | 1 | – |
| threads-lyr | 2,340 | 31 py | 0 | 1 | – |
| obscura-core | 2,896 | 15 py | 0 | 1 | – |
| hermes-prime-bridge | 834 | 14 | 1 | 2 | – |
| kali-mahabali | 61,408 | 690 py | 1 | 1 | – |
| icode | 142,635 | 2,095 rs | 0 | 2 | – |

*Note: "test markers" counts `#[test]`/`#[tokio::test]`/`def test_`/`it(` occurrences and can exceed
the passing count reported by the project's runner (e.g. disabled/ignored tests).*
