# Audit — HoloOS · KosmOS · Sovereign (with sovereign clone + test)

> **Purpose:** audit the three systems the user pointed to — `~/Documents/HoloOS`,
> `~/Documents/GitHub/KosmOS`, and the local/remote `sovereign` — verify how the profile
> catalog describes them, and clone + test sovereign to answer "what is it?".
>
> **Method:** git-measured stats + README/architecture inspection + live test runs.
> Audit date: 2026-08-12.

---

## 1. HoloOS — `~/Documents/HoloOS` (in the profile catalog, KB tier)

**What it is:** "Research OS for collective actualization" — a holonic-science research
knowledge base. Formalizes one invariant systems architecture (holons: atoms → cells →
organisms → civilizations → galaxies) with two metabolic cycles (lesser M·P·C·E, greater
S·T·G·Ch) on three substrates across seven densities. Self-evolving — runs the same
5-phase optimization protocol on itself. Ships a CLI (`holos` → `_INSTRUMENTS/cli/holos.py`)
and an MCP server for agents.

**Health:** 162 commits · last push 2026-07-11 · GitHub `origin` present (gitlab remote
also configured) · 0 tags · **0 CI workflows**.

**Measured scale:**

| Metric | Value |
|---|---|
| YAML / YML | **14,144** |
| Markdown | **1,191** |
| Python files | **98** |
| Python LOC | 43,647 |
| Total tracked files | 15,562 |
| Python test markers | **448** |

**Profile-catalog claims vs reality (KB entry: "14K YAML + 1.2K MD, 98 executable Python
files … **0 tests, 0 CI, 0 tools** — needs engineering verification before it can be tiered"):**

| Claim | Reality | Verdict |
|---|---|---|
| 14K YAML + 1.2K MD + 98 py | 14,144 / 1,191 / 98 | ✅ exact |
| 0 tests | 448 Python test markers across `_INSTRUMENTS` | ❌ stale |
| 0 CI | 0 workflows | ✅ |
| 0 tools | Working `holos` CLI (80+ subcommand surface) + MCP server + 27 scripts | ❌ stale |

**Action:** the "0 tests / 0 tools" line is outdated — the KB has real tooling and tests;
re-run its suite to capture a passing count before re-tiering.

**⚠ Confidentiality:** HoloOS **tracks session artifacts** — `.opencode/agent_metadata.json`
and `.pi/continue/<session>.md`. These match the "no cortexkit-like artifacts" rule (they can
carry session-chat content). `.cortexkit/.gitignore` (a path ignore, not content) is benign.

---

## 2. KosmOS — `~/Documents/GitHub/KosmOS` (NOT in the profile catalog)

**What it is:** "A unified consciousness-prosthetic and multi-domain research knowledge
base. Plain markdown + YAML frontmatter + SQLite derived indexes." Combines **four systems
in one vault** — LifeOS (teleological cycle), Research KB (6 disciplines / 100+ sub-domains),
Cross-Domain synthesis, and auto-detected Emergent domains — plus a `kosmos` CLI with a
huge agent-facing surface (**~80 subcommands**: orient, map, synthesize, emerge, zettel,
drift-audit, cycle-health, actualization-score, …).

**Health:** **1,054 commits** · last push 2026-08-01 · GitHub `origin` ✓ · 0 tags ·
**0 CI** (`.github/workflows/` exists but is empty).

**Measured scale:**

| Metric | Value |
|---|---|
| Markdown | 21,879 |
| YAML / YML | 11,524 |
| Python (223 files) test markers | 1,149 |
| TSX/TS (150+48) test markers | 114 |
| Code LOC (py/ts) | 113,346 |
| Total tracked files | 34,884 |
| CLI surface | ~80 subcommands |

**Test run (live):** `pytest` → **1,520 passed · 13 failed · 7 errors** in 15.8 s. A real,
mostly-passing suite — but nothing runs it (no CI).

**Findings:**
1. **Portfolio gap** — KosmOS is absent from the profile catalog entirely, despite being
   the most active vault in the family (1,054 commits vs HoloOS's 162) with a passing test
   suite. It belongs in the catalog (KB or ranked-engine tier) and the ecosystem tables.
2. **README clone URLs are stale/wrong** — quickstart says
   `git clone https://github.com/ishan-parihar/lifeos-local.git` (lines 38–39) and
   line 167 references `gitlab.../lifeos-local.git` — the repo is `KosmOS`.
3. **0 CI + 13 failed / 7 errored tests** — add CI (tag-gated per the portfolio rule) and
   fix the failing collection errors so 1,520 passing is CI-enforced.
4. `.cortexkit/.gitignore` is tracked (benign path-ignore).

---

## 3. Sovereign — what it is, clone + test

### What it is
SOVEREIGN is the **foundational architecture for Titan LifeOS — a personal-sovereignty /
life-automation framework** (deprecated, tombstones to `lifeos-ops` / `lifeos-saas`):

- **Domain-driven core** — seven life domains (bio_physio, executive, financial,
  psycho_spiritual, socio_relational, strategy, temporal)
- **Event-driven Nexus** pub/sub core decoupling domains, gateways, scheduler
- **Cron scheduler** (daily briefings, journal checks, finance/social nudges)
- **Gateways** to Telegram and Notion
- Plus a large **Kokoro TTS voice-cache toolkit** (371 WAV caches, 92 MB `kokoro-v1.0.int8.onnx`,
  ~10 cache scripts, `install_kokoro_deps.sh`)

**Health:** 23 commits · 0 tags · 1 CI workflow · last push 2026-08-11 · 9,404 code LOC ·
30 py test markers · no build entry point (no pyproject/Makefile/Dockerfile).

### Clone + test (fresh `git clone` of ishan-parihar/sovereign → `/tmp/sovereign_test`)
| Step | Result |
|---|---|
| Clone | ✅ HEAD `e048f6b` (workspace-lint layout commit) |
| `python main` (import smoke) | ❌ fails at `core.config` import chain |
| `pytest -q` | ❌ **2 collection errors** (`test_run.py` FileNotFoundError, `test_voice_fixes.py`) |
| Install entry point | ❌ none (requirements.txt only; no pyproject) |

**Verdict:** sovereign is **not runnable/testable out of the box** — operationally confirms
its deprecated status. The 92 MB ONNX model + 371 WAVs are tracked, which bloats the repo.

**Profile claim ("Archived agent framework (voice/cache tooling)", 3.58 C-tier):** partially
right — the voice/cache tooling is real — but it misses the primary identity (**Titan LifeOS
personal-sovereignty framework**). The catalog description should be corrected. No tracked
`.cortexkit`-style artifacts (clean).

---

## 4. Actions needed (not yet applied — awaiting go-ahead)

| # | Repo | Action |
|---|---|---|
| 1 | KosmOS | Add to profile catalog (KB or ranked); add ecosystem row |
| 2 | KosmOS | Fix README clone URLs (`lifeos-local` → `KosmOS`) |
| 3 | KosmOS | Add tag-gated CI; fix the 13 failed / 7 errored tests |
| 4 | HoloOS | Update KB entry: "0 tests / 0 tools" → verified tooling + 448 markers (re-run suite for passing count) |
| 5 | HoloOS | Untrack `.opencode/agent_metadata.json` + `.pi/continue/<session>.md` (session confidentiality) |
| 6 | sovereign | Correct profile description to "Titan LifeOS foundation — personal-sovereignty framework (voice/TTS tooling)" |
| 7 | sovereign | (optional) untrack the 92 MB onnx + 371 WAVs |

---

## 5. Evidence appendix

| | HoloOS | KosmOS | sovereign |
|---|---|---|---|
| Location | `~/Documents/HoloOS` | `~/Documents/GitHub/KosmOS` | `MY-PROJECTS/EXPERIMENTAL/sovereign (Deprecated⁄Inactive)` |
| Remote | github (+ gitlab) | github | github (+ gitlab history) |
| Commits / tags | 162 / 0 | 1,054 / 0 | 23 / 0 |
| Last push | 2026-07-11 | 2026-08-01 | 2026-08-11 |
| Tracked files | 15,562 | 34,884 | ~470 (371 wav) |
| Code LOC | 43,647 py | 113,346 | 9,404 py |
| Tests (markers) | 448 py | 1,149 py + 114 ts | 30 py |
| Test run | not run | **1,520 ✓ / 13 ✗ / 7 err** | collection errors |
| CI | 0 | 0 (empty dir) | 1 |
| Session artifacts tracked | `.opencode/`, `.pi/` | `.cortexkit/.gitignore` | none |
