# State

Current snapshot only (no history: that is the worklog). The first `## ` block is
what `genome wake` shows.

## State — (date)

<!-- genome:zone status sha=3c05967a2670 -->
| status | items |
|---|---|
<!-- genome:end status -->

<!-- genome:zone handoff sha=18cd9e6a0a18 -->
## Handoff — 2026-10-28

Repo branch `main`, HEAD `77192ccca753adc836a796b37e00c957a1060e86`. Tree clean.

## Open register rows
  (none)

## Recent worklog
# Worklog

Append-only: `genome log "<entry>"`, one per unit of work.
- **2026-10-23T03:06** — scripts/gen_rubric_tables.py executes again: SPEC now derives rank_score.py from the script's own directory (Path(__file__).parent) instead of a dead MY-PROJECTS absolute path from an older machine layout, which raised FileNotFoundError and made the RUNBOOK's documented 'gen rubric tables' regeneration step unrunnable (root register V-82, refresh outline A2). Verified: exit 0, 84 lines out, and all 35 generated dataset rows are byte-identical to RANKING-RUBRIC.md's committed §4 rows, so the fix is idempotent against the frozen snapshot. RANKING-RUBRIC.md is deliberately untouched and the regeneration step remains unrun per Q30's freeze at the root: the path fix makes the documented command honest, it does not run it.

Regenerate with `genome handoff --write`.
<!-- genome:end handoff -->
