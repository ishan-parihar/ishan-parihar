# TODO — the register

One row per work item; rows update in place, verdicts append — never delete.
`genome status <id> <state> --evidence <path>` is the supervised transition.

| id | status | item / verdict | notes |
|---|---|---|---|
| R1 | done | Repair the flagship order defect: 10 flagships, engine-score descending, table and deep dives agreeing → [2026-11-06] `README.md` + `scripts/check_order.py` | the gate exits 0 on the page and exits 1 on an injected swapped row (R6a + R10). The live page at `raw.githubusercontent.com/ishan-parihar/ishan-parihar/main/README.md` is byte-identical to the committed file |
| R2 | done | Fix the two engine defects behind the page's figures → [2026-11-06] `scripts/measure_repos.py` + `docs/kb/WORKLOG.md` | `MCP_TOOL_DEC` now matches 4 more registration forms (openscript 113, c-suite-agents 72, twitter-lyr 0); the portfolio root engine no longer counts `operant/.tmpwork` (13.4M -> 3.46M LOC, 851 -> 95 crates) — the root-side fix and its re-derivation are recorded in the worklog and in the root repo |
| R3 | done | Restate every stale figure on the page and regenerate the vitals from the corrected artefact → [2026-11-06] `README.md` + `portfolio-measurements.json` | `python3 scripts/gen_vitals.py --check` exits 0; page figures carry their own commit and date |
| R4 | done | Push the corrected README and verify the live page → [2026-11-06] `README.md` | pushed `6ab7ee8..b37d077` to origin/main; the live `raw.githubusercontent.com/ishan-parihar/ishan-parihar/main/README.md` fetch is byte-identical to the committed file, carries the 56 count, the 12,494 composite and the ten dives in score order |
| R5 | done | Re-measure the flagship test counts at workspace scope, not crate scope → [2026-11-06] `docs/kb/WORKLOG.md` | measured on clean `git archive` exports: mindstrata 1,258 passed / 3 failed at `6834297`, openscript 546 / 1 at `d9a1924`, switchpost 1,031 / 19 at `2104084`. The composite is recomputed to 12,494 and the page names the red binaries |
