# Register Segregation Audit — 2026-10-31

Question asked: is the my-projects register segregated correctly for the GitHub
README at `./ishan-parihar`, so all relevant projects can be pooled into the
README with correct categorisation, segmentation, and contextual depth.

Answer: the register is **segregated by relpath, not by category**, and those
relpaths describe a machine layout that no longer exists. The README is
therefore built over a stale map. Measured below, each claim with its command.

## The three sources, and which one is the register

| source | file | what it holds |
|---|---|---|
| **the register** | `scripts/measure_repos.py` → `REPOS = [...]` | 41 tuples: `(name, relpath, category)`, category ∈ {engine 28, experimental 3, deprecated 4, site 6} |
| ranking input | `scripts/rank_score.py` → `DATA = [...]` | 41 hand-carried per-repo measurements, one row per repo, no category column |
| README | `README.md` | hand-written prose, tiers, and links |

`fleet/manifest.json` is **not** the register. It holds 106 repos, has no
category field, and 85 of 106 have `bundle: null`. It is the local tree census,
not the portfolio register. Anyone reading it as the register will conclude the
portfolio is 106 projects; the README answers 42. Both are arithmetically
defensible against their own source and they disagree by 64 repos.

## Defect 1 — the register's relpaths describe a machine that no longer exists

Only **1 of 41** register relpaths resolves under
`/home/ishanp/Documents/github/my-projects`.

```
resolved 1 of 41 register relpaths under /home/ishanp/Documents/github/my-projects
```

Every relpath is prefixed with a dead top-level directory: `MCP-AND-CLIS`,
`HERMES`, `CONTENT-CREATION`, `LIFEOS`, `WEBSITES`, `EXPERIMENTAL`. The tree
reorganised under `agentic-utility/{interaction-surfaces,content-creation,...}`,
`agentic-harness/`, `webdev/`, `saas/`, `telemetry/`, `game-development/`,
`helpers/`, `EXPERIMENTAL/`.

`measure_repos.py` already documents the failure and works around it by
**walking up until names resolve** (the "manifest's *relpaths* were written
against an older machine layout" comment at line 51). That fallback resolves
**30 of 41 by name**. So the register's own consumer already stopped trusting
the register's paths.

**Consequence:** the `category` column is now the only live segregation signal,
and it is a free-text tag on a stale row — nothing derives it, nothing checks
it, and nothing re-checks it against GitHub.

## Defect 2 — the register and the ranking input describe different reposets

`REPOS` has 41 names. `DATA` has 41 rows. They are **not the same 41**.

| name | in `REPOS` | in `DATA` | on GitHub |
|---|---|---|---|
| `deckmill` | ✗ | ✗ | public |
| `sourcehound` | ✗ | ✗ | private |
| `HoloOS` | ✗ | ✗ | public |
| `CineSync` | ✗ | ✗ | public |
| `cinesync` | ✓ | ✓ | **ABSENT** |
| `slideforge-rust` | ✓ | ✓ | **ABSENT** |
| `igs-rust` | ✓ | ✓ | **ABSENT** |

`deckmill` is S-tier in the README (7.36, 192 tests, 20 MCP tools) and appears
in **neither** `REPOS` nor `DATA`. Its numbers in the README are hand-carried
prose with a real commit cite (`18036f4`), so the claim is not fabricated — but
the register and the rank engine cannot reproduce it. `genome`'s own
`refresh_repo_count.py --check` counts a different population again.

## Defect 3 — the ranking engine still ranks repos that do not exist

Six register names are absent from GitHub outright. Five are honest leftovers
(deleted/retired, and the README or record already says so). One is not:

- `social-forge` — **renamed to `switchpost`** (HTTP 301 confirmed, 2026-10-31).
  Both `REPOS` and `DATA` still carry `social-forge`; the README links it 3×
  and gives it an 8.42 S-tier row.
- `tg-cli` — **renamed to `tg-lyr`** (HTTP 301 confirmed). README links it 3×;
  B-tier 5.95.
- `discord-cli` — **renamed to `discord-lyr`** (HTTP 301 confirmed). README
  links it 2×; B-tier 4.93.
- `slideforge-rust` — **renamed to `deckmill`** (HTTP 301 confirmed). Ranked
  but **not in the README catalog at all**; `deckmill` is instead.
- `igs-rust` — **renamed to `sourcehound`** (HTTP 404, no redirect; `sourcehound`
  was created 2026-05-06 and its GitHub description still reads "IGS MCP Server
  (Rust)"). Ranked #1 in `DATA`, absent from the README catalog.
- `icode`, `cinesync`, `osint-os` — genuinely gone; README correctly labels
  icode "Archived" and "cannot be re-measured here". These are fine.

So the register is not merely stale, it points at four projects under names that
now resolve to *different* projects, and the ranking input inherits every one
of those rows.

## Defect 4 — the README's own counts do not close

The README title says **42 Projects**. Summing the catalog's own sections gives
**43**, and `kali-mahabali` appears **twice** (C-tier rows `8.33 capped` and
`7.08 capped 🔒` — clearly two different experiments, same name, one row pair
that reads as a duplication error). Every individual tier's stated count is
correct against its own contents, so the error is only visible at the top-level
sum.

## Defect 5 — 25 public, non-fork repos are in no register, no ranking, no README

Measured as `PUBLIC` on GitHub, `isFork == false`, and absent from `REPOS`,
`DATA`, **and** the README. All 25 carry real descriptions and most are
actively pushed (dates 2026-09-03 to 2026-10-31). Notably:

| repo | pushed | language | why it matters to the README |
|---|---|---|---|
| `switchpost` | 2026-10-31 | Rust | the renamed `social-forge`; S-tier flagship under a name the README never links |
| `tg-lyr` | 2026-10-31 | Python | the renamed `tg-cli`; B-tier, 281 tests |
| `discord-lyr` | 2026-10-31 | Python | the renamed `discord-cli`; B-tier, 41 tests |
| `amazon-lyr` | 2026-10-30 | Python | `-lyr` family MCP server — same family as five already-tiered repos |
| `swiggy-lyr` | 2026-10-30 | Python | `-lyr` family MCP server |
| `etmoney-lyr` | 2026-10-30 | Python | `-lyr` family MCP server, 10 tools |
| `memory-wire` | 2026-10-27 | Rust | agent memory at ~1% of rivals' RAM — competes with `tdg-rust`'s own A-tier slot |
| `artificial-route` | 2026-10-29 | Rust | LLM proxy over 276 providers, 19 routing strategies, static musl |
| `holon` | 2026-10-27 | Python | self-healing agentic OS — arguably the strongest single thesis statement in the fleet |
| `project-genome` | 2026-10-31 | Python | the genome tool that runs the gates on this README's numbers |
| `metatrader-bridge` / `-docker-` | 2026-10-27 | Python | quant-infra pair |
| `cloakctl` | 2026-10-27 | Python | stealth browser per profile + agent automation registry |
| `android-webcam`, `omarchy-vpn`, `pill-bar`, `pill-suite`, `segmented-pill-bar`, `static-tray` | Aug–Oct | QML/Python | the Omarchy desktop control-plane cluster — 6 repos, zero representation |
| `AI-CAD` | 2026-10-24 | Python | **7 stars** — the only starred non-fork repo in the fleet |
| `palimpsest` | 2026-10-27 | Python | training system |
| `linux-telemetry`, `n8n-compiler`, `jesse` | 2026-07/10 | Python | mixed, lower signal |

This is the direct answer to the question. The register is not missing
*categories* — it is missing **25 whole projects**, and among them are the three
the README currently links under dead names. The README's "42" is a complete
population in the wrong direction: it is neither the 106-repo tree nor the
123-repo GitHub account, and it no longer contains four flagship names it
already ranks and scores.

## What the README already gets right

Stated so the fix does not damage it:

- The `🔒` lock convention matches GitHub visibility exactly — all 12 locked
  names are `PRIVATE` on GitHub, with no exceptions.
- All 5 website repos in the separate category are genuinely private and
  genuinely excluded from tiering. The category boundary is correct.
- Tier counts are internally consistent (each tier's stated number matches its
  own bullets); only the top-level sum (42 vs 43) and the duplicated
  `kali-mahabali` break.
- Every README score has a rank engine row behind it, except `deckmill`,
  `sourcehound`, `HoloOS`, `AI-CAD`.
- The "NOT measured, not claimed" language in the metrics table is exactly the
  right posture (14,523 markers named rather than counted).

## Proposed segregation, for decision

Four categories already exist in the register. The README has six sections.
Aligning them one-to-one, with the 25 missing repos assigned by measured
category:

1. **engines** (register `engine`) — the tiered S/A/B/C software. Requires the
   renames applied first (`social-forge`→`switchpost`, `tg-cli`→`tg-lyr`,
   `discord-cli`→`discord-lyr`, `igs-rust`→`sourcehound`, `slideforge-rust`→
   `deckmill`).
2. **the `-lyr` interaction-surface family** — already its own README section;
   add `amazon-lyr`, `swiggy-lyr`, `etmoney-lyr`; retitle `tg-cli`/`discord-cli`
   to their `-lyr` names so the family is one naming scheme.
3. **desktop control plane** (new category) — `android-webcam`, `omarchy-vpn`,
   `pill-bar`, `pill-suite`, `segmented-pill-bar`, `static-tray`. 6 repos
   currently invisible, coherent as one platform story.
4. **sites** — unchanged, already correct.
5. **experimental / deprecated** — `consciousness-fabricator`, `holosim-infinite`,
   `kali-mahabali` (deduplicate the two rows), retired `icode`/`cinesync`/`osint-os`.
6. **knowledge-base spec corpora** — `HoloOS` already here.

`memory-wire`, `artificial-route`, `holon`, `project-genome`, `cloakctl`,
`metatrader-*`, `AI-CAD`, `palimpsest`, `linux-telemetry`, `n8n-compiler`,
`jesse` need a category ruling, not an edit — they are real and measured, but
whether `holon` displaces an S-tier slot or sits beside it, and whether the
quant and Omarchy clusters are portfolio work or private practice, is the
operator's call, not a classification default.

## Rule for the register going forward

The register should be **derived from GitHub, not hand-maintained**: the
`gh repo list` JSON already carries `name`, `visibility`, `isFork`,
`isArchived`, `updatedAt`, `description`, and `primaryLanguage`. A script that
regenerates `REPOS` from that JSON would make the renames structural rather than
a four-line patch that must be found by an audit again.
