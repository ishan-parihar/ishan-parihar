# Runbook — exact commands, environment traps

| task | command | traps |
|---|---|---|
| check loc badges | `python3 scripts/check_loc_badges.py` | the repo's own script |
| check sponsor links | `python3 scripts/check_sponsor_links.py` | the repo's own script |
| gen rubric tables | `python3 scripts/gen_rubric_tables.py` | the repo's own script. 2026-10-22: fixed to run from any machine layout (SPEC derives from `__file__`); output verified byte-identical to the committed rubric tables. **Do not splice the output while Q30's freeze stands at the meta root** — this row documents how to run it, not when |
| lint readmes | `python3 scripts/lint_readmes.py` | the repo's own script |
| measure repos | `python3 scripts/measure_repos.py` | the repo's own script |
| rank score | `python3 scripts/rank_score.py` | the repo's own script |
| soph audit | `python3 scripts/soph_audit.py` | the repo's own script |
