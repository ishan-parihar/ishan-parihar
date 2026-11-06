# TODO — the register

One row per work item; rows update in place, verdicts append — never delete.
`genome status <id> <state> --evidence <path>` is the supervised transition.

| id | status | item / verdict | notes |
|---|---|---|---|
| R1 | done | Repair the flagship order defect: 10 flagships, engine-score descending, table and deep dives agreeing | `scripts/check_order.py` exits 0 on the page and exits 1 on an injected swapped row (R6a + R10). Evidence: `README.md`, `scripts/check_order.py` |
| R2 | done | Fix the two engine defects behind the page's figures | `scripts/measure_repos.py` MCP_TOOL_DEC now matches 4 more registration forms (openscript 113, c-suite-agents 72, twitter-lyr 0); the portfolio root `scripts/measure.py` no longer counts `operant/.tmpwork` (13.4M -> 3.46M LOC, 851 -> 95 crates) |
| R3 | done | Restate every stale figure on the page and regenerate the vitals from the corrected artefact | `python3 scripts/gen_vitals.py --check` exits 0; page figures carry their own commit and date |
| R4 | in-progress | Push the corrected README and verify the live page | pending: the live `raw.githubusercontent.com` fetch must show the corrected order and the 56 count |
| R5 | done | Re-measure the flagship test counts at workspace scope, not crate scope | measured 2026-11-06 on clean `git archive` exports: mindstrata 1,258 passed / 3 failed at `6834297`, openscript 546 passed / 1 failed at `d9a1924`, switchpost 1,031 passed / 19 failed at `2104084`. The composite is recomputed to 12,494 and the page names the red binaries. Evidence: `docs/kb/WORKLOG.md` |
