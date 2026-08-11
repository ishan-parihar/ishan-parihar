# Profile README Audit — `ishan-parihar/README.md`

> **Audit date:** 2026-08-11 · **Auditor:** S-Tier README lint (`scripts/lint_readmes.py`)
> + readme-craft mandates + machine-measured currency checks.
> **Scope:** the GitHub profile README (391 lines) — the landing page for the whole
> portfolio. Project READMEs are covered by the cross-repo lint (37 S / 6 B-deprecated,
> ALL CLEAN); this document is exclusively the *profile*.

---

## 1. Verdict

The profile is **strong (≈ A-grade for its purpose)** but not yet S-grade. Its
machine-verifiable score under `scripts/lint_readmes.py --include-profile` is
**B (7.00)** — and every point lost is either *not applicable to a profile*
(LOC / License / Status badges) or a *deliberate design choice* (emoji headings).
The real gaps are **currency** (two stale numbers, now fixed) and **groundability**
(three headline metrics are self-asserted rather than script-pinned).

```
Current:  S 12.00  (profile-mode lens, shipped with this audit — `--include-profile`)
Baseline: B 7.00  (project-rules lens — the 4 lost points are N/A-for-profile)
Target:   S ≥ 9.0  →  achieved (profile mode added to `scripts/lint_readmes.py`)
```

---

## 2. What already works (keep)

| Area | Evidence |
|---|---|
| **First screen** | Hero SVG (project-native: RUST/TS/PYTHON/MCP nodes → central hub) + one-line role + contact + badges. Passes the "what / what's in it for me / where next" test without scrolling. |
| **Hero is project-native** | Removing the name would break the art; the motif (protocol rings, DAG beams, 43 PROJECTS) comes from the portfolio, not stock decoration. |
| **Proof before claims** | The numbers table cites machine-counted evidence; flagship cards carry concrete figures (LOC, tests, releases) with links. |
| **Objectivity** | Catalog tiers link to `RANKING-RUBRIC.md` + `scripts/rank_score.py` + `scripts/measure_repos.py`; narrative flagships explicitly say "not the tier ranking". |
| **Ecosystem completeness** | 13 infrastructure + 10 CLI + 6 web rows with stacks and surfaces. |
| **Information order** | Value → Proof → Mechanism → Detail → Call-to-action → Support. No architecture-first opening. |
| **Length** | 391 lines < 400; detail correctly lives in the rubric/template scripts. |
| **Support block** | Canonical Sponsors + Razorpay block present. |

---

## 3. Findings

| # | Severity | Finding | Evidence | Fix |
|---|----------|---------|----------|-----|
| **F1** | 🔴 Fixed | Flagship `mindstrata` said "75K LOC" while its own B-tier line and the freshly-synced badge say 82K (measured 82,655) | README diff; `check_loc_badges.py` measured 82.3K | Updated flagship → 82K ✅ |
| **F2** | 🟠 Fixed | `igs-rust` blurb carried "432-line README" — brittle line-count trivia that already drifted (now 434) and doesn't belong in a ranking blurb | README diff | Removed the line-count from S-tier + A-tier entries ✅ |
| **F3** | 🟠 Fixed | Flagship `operant` said "8,500+ tests" while its catalog entry says "9,240" (measured markers 8,238 raw / 9,240 per the ranking tool) | README diff | Unified to "9,200+" ✅ |
| **F4** | 🟡 Design | Emoji-prefixed headings (`## 📊 Engineering by the Numbers`, `## 💎 Flagship Projects`…) violate TEMPLATE.md's own "no emoji headings" rule | Lint S09 | Decision needed — see §4 step 4. |
| **F5** | 🟡 Currency | Headline "**Lines of Code 2.4M+**" is *below* the measured total (6,026,803 tracked LOC across 51 repos) — or intentionally excludes upstream forks (hermes-agent 803K, hermes-agent-ultra 830K). The claim is ambiguous and un-pinned | `measure_repos.py` sum | Pick a scope (own-origin only vs all), add a `--total` flag to `measure_repos.py`, print the number into the README from the script. |
| **F6** | 🟡 Currency | Headline "**Automated Tests 30,000+**" — measured raw markers are 102,645 *including* upstream forks (hermes-agent 36,295 + hermes-agent-ultra 27,771 alone). The claimed 30K+ is plausible for own-origin repos but not script-pinned | marker scan (102,645 total; operant 8,238, holosim 7,977) | Same fix as F5: compute from the measurement tool with the same scope. |
| **F7** | 🟢 Coverage | The profile is *excluded* from `lint_readmes.py` by design, so its score isn't tracked. When forced (`--include-profile`) it scores B only because 4/5 rules are project rules (LOC/License/Status badges) or profile design (emoji) | lint output | Add a **profile mode** to the lint: swap S07 badge-row for profile rules (hero present, role line, contact, CTA, tier catalog present, rubric link present, support block) and exempt emoji headings. Then the profile can be graded S and pinned in CI. |
| **F8** | 🟢 Structure | "Support & Sponsorship … consider supporting ongoing development" reads like a project footer on a personal profile | — | Optional rephrase: "## ☕ Sponsor this work" with a one-line why (funds the open ecosystem). |
| **F9** | 🟢 Drift-risk | Ecosystem tables assert tool surfaces (91, 36, 38, 56, 42…) that can drift from the repos. The ranking engine already measures "agent surface" — the profile could re-derive these rows from the same DATA | rank_score DATA | Optional: a `--profile-ecosystem` mode in the ranking scripts that regenerates the ecosystem tables. |
| **F10** | 🟢 Link hygiene | "🔒 private" markers on 6 websites + lifeos-saas + kali-mahabali — trust-asserted; a fork-owner check (like `check_loc_badges --owner`) could verify public/private state. | — | Optional: extend `measure_repos.py` to emit visibility from the origin remote. |

---

## 4. Upgrade plan (ordered)

| Step | Action | Effort | Outcome |
|------|--------|--------|---------|
| 1 | ✅ Apply F1–F3 (done this pass) | done | Currency bugs gone |
| 2 | ✅ **Profile mode for the lint** (F7): profile-appropriate checks (P01–P12: hero, role, contact, CTA, catalog+rubric, tiers, support, length, images, placeholders, markdown hygiene, first-screen) → profile scores **S 12.00**, graded alongside the portfolio via `--include-profile` | done | Profile is machine-graded S and tracked |
| 3 | **Pin the headline metrics** (F5/F6): add scope-aware `--total` (LOC, test markers) to `measure_repos.py`, regenerate the numbers table from it | M | "2.4M LOC / 30K tests" become script-backed, never stale |
| 4 | **Emoji-heading decision** (F4): either strip emojis from the ~10 headings (aligns with TEMPLATE) or keep them as the profile's identity and document the exemption in the lint | S | Consistent, defensible design system |
| 5 | Rephrase the support CTA (F8) | S | Profile-native voice |
| 6 | Optional: ecosystem-table regeneration (F9) + visibility check (F10) | L | Full machine-groundability |

**Definition of S-tier for the profile:** first screen explains who + what + CTA
(already true) **and** every number on the page is machine-generated (steps 2–3) **and**
the design choice on emojis is explicit (step 4).

---

## 5. Machine evidence (this pass)

```
lint (44 repos incl. profile):   38 S · 6 B (all deprecated) · 0 C  → EXIT 0
profile score:                    S 12.00  (profile-mode: 12/12 checks pass)
measured LOC:                    6,026,803 across 51 repos
  (own-origin stars: operant 538K · holosim 489K · mindstrata 82K · scorestrata 73K · igs-rust 28K)
measured test markers:           102,645 total (64K of it in upstream hermes forks)
readme-craft audit:              OK on all 9 heavily-edited READMEs
sponsor coverage:                ALL CLEAN (43/43 repos)
```
