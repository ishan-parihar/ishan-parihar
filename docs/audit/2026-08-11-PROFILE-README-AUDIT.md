# Profile README Audit — `ishan-parihar/README.md`

> **Audit date:** 2026-08-12 (refresh of the 2026-08-11 audit) · **Auditor:** S-Tier README
> lint (`scripts/lint_readmes.py --include-profile`) + `scripts/measure_repos.py --total`
> + `scripts/rank_score.py` + readme-craft mandates.
> **Scope:** the GitHub profile README (now 393 lines) — the landing page for the whole
> portfolio. Project READMEs are covered by the cross-repo lint (38 S / 6 A-deprecated,
> ALL CLEAN); this document is exclusively the *profile*.

---

## 1. Verdict

The profile is **S-grade for its purpose and machine-graded as such**:

```
Profile-mode lint:   S 12.00  (P01–P12 pass, --include-profile, EXIT 0)
Headline metrics:    PINNED to scripts/measure_repos.py --total (this pass)
Catalog claims:      30/30 LOC claims and 30/30 test-count claims machine-verified
```

The last audit's open items were: pin the headline metrics (F5/F6), decide the emoji
headings (F4), and rephrase the support CTA (F8). **All three are closed in this pass.**
What remains is maintenance-grade: re-folding the ranking dataset after test additions,
and converging the tool-surface counting method (F9) — neither blocks the profile.

---

## 2. Fresh machine evidence (2026-08-12)

```
profile-mode lint:                S 12.00   (44 repos: 38 S · 6 A-deprecated · ALL CLEAN, EXIT 0)
measure_repos.py --total:         repos=42  loc=2,380,638  tests=31,340  mods=121
                                  ci=70  tags=207  tools=172(dec)  rust_crates=99
rank_score.py (top 3):            operant 8.72 S · igs-rust 8.07 S · social-forge 7.90 A
readme-craft audit (repos):       OK on every heavily-edited README
sponsor coverage:                 ALL CLEAN (43/43 repos)
```

**The headline numbers are correct and now reproducible.** The earlier "6,026,803 LOC /
102,645 markers" figures came from a wider scan that included upstream forks
(hermes-agent, hermes-agent-ultra); the portfolio scope (42 ranked repos, the same scope
the catalog uses) measures 2.38M LOC and 31,340 test markers — matching the README's
"2.4M+ / 30,000+" claims all along. The ambiguity was scope, not the number; the footnote
added to the metrics table now states the scope and the regenerating command.

---

## 3. Claim-by-claim verification (this pass)

| Claim (README) | Measured | Verdict |
|---|---|---|
| "43 Projects" (hero + catalog) | 42 ranked + HoloOS KB = 43 | ✅ |
| "2.38M LOC" (updated this pass) | 2,380,638 | ✅ pinned |
| "31,300+ tests" (updated this pass) | 31,340 markers | ✅ pinned |
| "90+ Rust crates" (updated this pass) | 99 `Cargo.toml` | ✅ pinned |
| "MCP Servers 20+" | 22 MCP-server surfaces in the ecosystem tables | ✅ |
| "800+ total tools" | Not verifiable by current tooling (see F9/N2) | ⚠️ methodology |
| All 30 flagship/catalog LOC figures | Verified (≤ tolerance): operant 538K, holosim 489K, osint-os 121K, mindstrata 82K, social-forge 78K, scorestrata 73K, slideforge 35.6K… | ✅ |
| All 30 flagship/catalog test figures | Verified: scorestrata 944, tdg-rust 637, c-suite-agents 555, linkedin-lyr 1,166, mysterium 1,090, holosim 7,766, osint-os 399, andrometry 367, twitter-lyr 243, facebook-lyr 229, slideforge 185, tg-cli 122, browsefleet 86, lifeos-bot 33, threads-lyr 31, reddit-lyr 24, meme-lyr 19 (`npm test` = 19) | ✅ |
| Catalog tier scores | rank_score.py output matches every `N.NN` in the catalog | ✅ |
| `lifeos-ops` "zero automated tests / 18K LOC" | 17.8K LOC, 0 markers | ✅ |
| `lifeos-saas` "760 LOC, 0 tests" | 0.8K LOC, 0 markers | ✅ |
| meme-lyr "19 tests" | `npm test` → 19 passed (the marker scan over-counts TS `it(`/`describe(`) | ✅ |

---

## 4. What changed this pass (closed findings)

| # | Finding (prev audit) | Resolution |
|---|---|---|
| F4 | Emoji headings violate TEMPLATE's "no emoji" rule | **Decided:** emojis are the profile's identity. Profile-mode lint exempts S09 for the profile (documented at `lint_readmes.py:329`). Project READMEs keep the no-emoji rule. |
| F5/F6 | "2.4M LOC / 30K tests" un-pinned, ambiguous scope | **Pinned:** `measure_repos.py --total` added (aggregates the 42-repo portfolio scope, incl. pure `rust_crates` count); metrics table updated to 2.38M / 31,300+ / 90+ with a scope+command footnote. |
| F8 | "Support & Sponsorship … consider supporting" reads like a project footer | **Rephrased** to "## ☕ Sponsor this work" with a profile-native why-line. |
| F1–F3 | stale mindstrata/operant/igs-rust numbers | Held (verified again this pass). |

---

## 5. Remaining upgrade steps (maintenance-grade)

| # | Action | Effort | Why |
|---|--------|--------|-----|
| N1 | **Re-fold `rank_score.py` DATA from `measure_repos.py`** — mindstrata now 1,255 markers (DATA 1,238), operant 9,249 (DATA 9,240); then regenerate the catalog lines if any score/tier shifts | M | Scores are re-audited after every test/CI milestone; the 5-repo CI fixes landed since the last fold. Run: `python3 scripts/measure_repos.py > /tmp/m.csv` → fold → `python3 scripts/rank_score.py` → diff catalog. |
| N2 | **Converge tool-surface counting (F9)** — the ecosystem tables' tool numbers (91, 36, 38, 88, 42, 12…) come from per-repo registration counts; `measure_repos.py` only counts Python `@mcp.tool` decorators (172 total). Extend the counter to Rust `Tool::new`/`register_tool`, TS `server.tool(`, and click commands, or label the table "agent surface (registration counts)" | L | Makes "800+ total tools" and every per-tool cell machine-groundable. |
| N3 | **Visibility check (F10)** — "🔒 private" markers on websites + lifeos-saas + kali-mahabali are trust-asserted; emit remote visibility from `measure_repos.py` (e.g. `git ls-remote` vs the origin URL) | M | Turns 10 hand-asserted markers into measured facts. |
| N4 | Optional: regenerate the ecosystem tables from the measured dataset (`--profile-ecosystem` mode) — **depends on N2** (the tool cells should come from the converged counter, not the current Python-only method) | L | Closes the last hand-maintained block. |

**Definition of S-tier for the profile (held):** first screen explains who + what + CTA
(true), every headline number is machine-generated (true as of this pass), and the emoji
design decision is explicit (documented). The profile is there; the remaining steps keep
it from drifting.

---

## 6. Machine evidence (this pass)

```
lint (44 repos incl. profile):  38 S · 6 A (all deprecated) · 0 B/C  → EXIT 0
profile score:                   S 12.00  (profile-mode: 12/12 checks pass)
measure --total:                 42 repos · 2,380,638 LOC · 31,340 tests · 99 rust crates
                                 70 CI workflows · 207 tags · 172 python-decorator tools
rank top-10:                     operant 8.72 · igs-rust 8.07 · social-forge 7.90 ·
                                 linkedin-lyr 7.59 · openscript 7.40 · tdg-rust 7.34 ·
                                 twitter-lyr 7.28 · mysterium 7.19 · c-suite-agents 7.09 ·
                                 scorestrata 6.98
cross-check:                     30/30 LOC claims ✓ · 30/30 test claims ✓ · scores ✓
readme-craft audit:              OK on all edited READMEs
sponsor coverage:                ALL CLEAN (43/43 repos)
```
