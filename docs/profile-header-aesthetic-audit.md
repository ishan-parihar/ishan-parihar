# Profile README Header & Portfolio Alignment Audit

> **Date:** 2026-08-13 · **Method:** read-only evidence (git tree, `rank_score.py`
> DATA, repo READMEs, `check_loc_badges.py`, `lint_readmes.py`) + applied fixes.
> **Scope:** header design gaps in the profile README, data alignment across every
> artifact, and similar aesthetic gaps in other repos.
> **Companion docs:** `docs/hero-spec.md` (canonical hero spec + brand tokens),
> `RANKING-RUBRIC.md` (v7 engine).

---

## 1. Profile README header — implementation gaps (all fixed)

| # | Gap | Severity | Why it was a problem | Fix applied |
|---|-----|----------|----------------------|-------------|
| H1 | Inline-SVG text flattened to a single line — README sanitizers / mobile clients drop the `transform`/`x`/`y` layout attributes on inline `<svg><text>`, so every label stacked at the origin as one unstyled line | **High** | **Root-cause fix:** the hero now lives as a real SVG file (`assets/readme/hero.svg`) mounted via `<img src="./assets/readme/hero.svg">` — the browser's native SVG engine lays it out identically on desktop, mobile web, and mobile apps (verified by headless Chrome: 4 positioned nodes + hub + chips, no flattening) |
| H2 | T2I HERO SPEC meta-comment (5-line block) + `<!-- RAW SVG HERO SYSTEM -->` | Medium | Process/meta commentary in a public profile README; invisible but violates the no-meta-commentary rule | Removed; spec relocated to `docs/hero-spec.md` |
| H3 | 15 structural HTML comments inside the SVG | Low | Same class; bloats the header | All stripped — the header is now zero-comment |
| H4 | Badge palette mismatch — SVG uses `#10B981`/`#DE7F3B`/`#A855F7`; badges used `2ea44f`/`ed8b00`/grey `555555` | Medium | Header reads as two different designs; the MCP badge was bland grey | Badges aligned to SVG tokens (`10b981`, `DE7F3B` — Rust's official brand orange, `A855F7`); visitor badge aligned too |
| H5 | Tagline rendered as one flat bold line duplicating the SVG subtitle | Low | No hierarchy; lead descriptor lost | Lead descriptor bolded; kept as the SEO keyword line |
| H6 | Emoji collisions — `🛠️` twice; `🧠` on both A-TIER and KNOWLEDGE-BASE | Low | Two sections shared an identity marker | `🛠️ Unified Tech Stack Matrix` → `🔬`; KNOWLEDGE-BASE → `📚` |
| H7 | Double blank line under `## 💎 Flagship Projects` | Trivial | Ragged spacing | Collapsed |

## 2. Data alignment matrix (profile README vs authoritative dataset)

Every claim cross-checked against `rank_score.py` DATA (machine-measured) and the
owning repo's README. **5 real inconsistencies found and fixed:**

| Claim | README said | Verified | Fix |
|-------|-------------|----------|-----|
| operant tests | `9,200+` | 9,249 (dataset + catalog) | → `9,249` |
| scorestrata crates | `11 crates` | 12 (dataset `mods=12`, catalog) | → `12 crates` |
| mindstrata tests | `1,238` | 1,245 (dataset `tests=1,245`, catalog) | → `1,245` |
| tdg-rust tests | `637` + value-prop `430+8+66+5=509` (≠626) | 626; repo README: `449 lib + 68 MCP e2e + 44 plugin + integration + property` | → `626 tests total`; breakdown → `449+68+44+integration+property` |
| reddit-lyr tools | `56 Tools` (×2 places) | 32 MCP tools (repo README: "32 tools for agents") | → `32 Tools` (ecosystem) / `32 MCP tools` (catalog); removed the vague `10.0 agent score` |
| Rust crates display | `90+` (evidence: 99) | 99 manifests | → `99+` for exactness |

**Verified-clean on re-check:** all catalog scores/LOC/tests (`operant 538K/9,249/19` ·
`scorestrata 73K/944/12/88` · `social-forge 78K/328` · `igs-rust 93` · `openscript 109/510`
· ecosystem surface counts for the other 20 rows), tier math (8+8+9+9+1+1+6 = 42),
numbers table totals, and header `42 PROJECTS` chip.

## 3. Similar aesthetic gaps elsewhere (inventory)

### 3.1 T2I HERO SPEC meta-comments — 12 repos (recommended purge)
The same invisible hero-generation spec comment sits at the top of:
`andrometry` · `hermes-prime-bridge` · `LIFEOS/lifeos-ops` · `lifeos-website` ·
`lifeos-saas` · `lifeos-bot` · `c-suite-agents` · `c-suite-agents-mcp` ·
`WEBSITES/ishanparihar-svelte` · `webdev-portfolio` · `webdev-portfolio/my-portfolio` ·
`design-aesthetics-website`.

**Recommendation:** batch-move each block into the owning repo's `docs/hero-spec.md`
(same treatment as this README) — one commit per repo. Keeps regeneration intent,
removes meta-commentary.

### 3.2 LOC badge staleness — fixed
`check_loc_badges.py` flagged 2 stale badges; both fixed with `--fix`:
- `HERMES/operant` `537K` → `548K`
- `mindstrata` `82.3K` → `84.2K`

**Open item:** `measure_repos.py` (ranking dataset) counts operant at `538,394` while
`check_loc_badges.py` counts `548K` — two LOC measurements disagree (~2%). Recommend
unifying `measure_repos.py` on `check_loc_badges.py`'s counting (tracked code files,
docs/assets excluded) so catalog numbers and repo badges can never diverge again.

### 3.3 lint_readmes.py residuals (accepted for archived repos)
- Deprecated repos (`cinesync`, `icode`, `workout-factory`, `vectura-labs`) lack CI/LOC
  badges (S06/S07) — acceptable for archived dirs.
- `osint-os` (deprecated): missing Sponsors link (S01), 469 lines > 400 (S08) —
  archived; skip unless it is un-archived.

### 3.4 User-policy flag
`lifeos-bot` sits in **B-tier** (v7 score `4.76`, B range 4.5–6.49). An earlier
directive suggested C-tier for it. The v7 engine's class-aware scoring put it in B —
confirm whether the score or the tier should change.

## 4. Ordered remediation plan

1. ✅ Header redesign + data alignment (this pass) — landed in the commit that ships this doc
2. ✅ LOC badge refresh (`check_loc_badges.py --fix`) — operant, mindstrata
3. [ ] Purge T2I meta-comments across the 12 repos (batch, one commit each)
4. [ ] Unify LOC measurement (point `measure_repos.py` at `check_loc_badges.py` counting) and regenerate the catalog
5. [ ] Confirm `lifeos-bot` tier policy (score vs placement)
6. [ ] Regenerate the `.pdf` resume variants from the corrected MDs (flagged by prior review)
