#!/usr/bin/env python3
"""
Companion to rank_score.py — machine-measures every portfolio repo into the
exact row format the ranking engine consumes.

  name, category, loc, tests, mods, ci, c90, tags, age, langs, concur,
  ops, surface, indegree, readme_lines, install, docs

All values are measured from the live git worktrees (no self-reports):
  - loc:       tracked CODE lines (assets/data/lockfiles excluded)
  - tests:     test markers by language (#[test], def test_, it(, func Test, @Test)
  - mods:      Cargo.toml + package.json module count
  - ci:        .github/workflows/*.yml file count
  - c90:       commits in the last 90 days
  - tags:      git tag count (release discipline)
  - age:       days since first commit
  - langs:     distinct language families among tracked code
  - concur:    concurrency/async pattern hits (tokio, async, threads, mcp, ...)
  - ops:       agent-callable operations on the project's OWN surface class
               (CLASS-AWARE v6): MCP tool count | CLI command count | REST
               endpoint count | runnable binary count
  - surface:   detected surface class: mcp | cli | rest | engine (dominant
               by measured registration count; engine only when none exist)
  - indegree:  number of sibling portfolio repos referenced in this repo's code
  - readme:    README.md line count
  - install:   1 if an install/build entry point exists (Cargo.toml/pyproject/
               package.json/Makefile/install.sh/Dockerfile)
  - docs:      1 if a docs/ directory exists

First-party rule (2026-08-11): vendored/embedded third-party code is excluded
from every metric. These are identical copies maintained inside multiple
portfolio repos (e.g. crates/toon-helper vendored into automaton,
social-forge, tdg-rust). Counting them would (a) double-count the same code
across the portfolio and (b) pollute the in-degree signal with sibling-name
mentions that live in the vendored copy, not the repo's own code.

Usage:
  python3 scripts/measure_repos.py > /tmp/measured.csv
  python3 scripts/measure_repos.py --total   # portfolio-scope totals (README headlines)
  # then fold the numbers into the DATA table of scripts/rank_score.py
"""

import datetime
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# By default measure the sibling portfolio repos next to this repo.
PORTS = os.path.dirname(ROOT)

# ---------------------------------------------------------------------------
# Repo manifest: (name, relative path under PORTS, category)
# Add new repos here — the audit tool picks them up automatically.
# ---------------------------------------------------------------------------
REPOS = [
    # engines
    ("igs-rust",               "MCP-AND-CLIS/igs-rust", "engine"),
    ("social-forge",           "MCP-AND-CLIS/social-forge", "engine"),
    ("operant",                "HERMES/operant", "engine"),
    ("scorestrata",            "scorestrata", "engine"),
    ("mindstrata",             "mindstrata", "engine"),
    ("tdg-rust",               "tdg-rust", "engine"),
    ("slideforge-rust",        "MCP-AND-CLIS/slideforge-rust", "engine"),
    ("automaton",              "MCP-AND-CLIS/automaton", "engine"),
    ("openscript",             "CONTENT-CREATION/openscript", "engine"),
    ("mysterium",              "mysterium", "engine"),
    ("andrometry",             "andrometry", "engine"),
    ("lifeos-ops",             "LIFEOS/lifeos-ops", "engine"),
    ("c-suite-agents",         "LIFEOS/c-suite-agents", "engine"),
    ("thinking-steroid",       "MCP-AND-CLIS/thinking-steroid", "engine"),
    # AXI CLI family
    ("reddit-lyr",             "MCP-AND-CLIS/reddit-lyr", "engine"),
    ("twitter-lyr",            "MCP-AND-CLIS/twitter-lyr", "engine"),
    ("instagram-lyr",          "MCP-AND-CLIS/instagram-lyr", "engine"),
    ("linkedin-lyr",           "MCP-AND-CLIS/linkedin-lyr", "engine"),
    ("facebook-lyr",           "MCP-AND-CLIS/facebook-lyr", "engine"),
    ("threads-lyr",            "MCP-AND-CLIS/threads-lyr", "engine"),
    ("discord-cli",            "MCP-AND-CLIS/discord-cli", "engine"),
    ("tg-cli",                 "MCP-AND-CLIS/tg-cli", "engine"),
    ("meme-lyr",               "MCP-AND-CLIS/meme-lyr", "engine"),
    ("obscura-core",           "MCP-AND-CLIS/obscura-core", "engine"),
    # experimental / archived (capped at C by policy)
    ("consciousness-fabricator", "EXPERIMENTAL/consciousness-fabricator", "experimental"),
    ("holosim-infinite",       "EXPERIMENTAL/holosim-infinite", "experimental"),
    ("kali-mahabali",          "EXPERIMENTAL/kali-mahabali", "experimental"),
    ("icode",                  "DEVELOPER-TOOLS (Deprecated\u2044Inactive)/icode", "deprecated"),
    # engines added in the 2026-08-11 full-coverage pass
    ("browsefleet",            "browsefleet", "engine"),
    ("hermes-prime-bridge",    "hermes-prime-bridge", "engine"),
    ("lifeos-bot",             "LIFEOS/lifeos-bot", "engine"),
    # utility/private
    ("lifeos-saas",            "LIFEOS/lifeos-saas", "engine"),
    # deprecated / inactive (capped at C by policy)
    ("cinesync",               "CONTENT-CREATION/cinesync (Deprecated\u2044Inactive)", "deprecated"),
    ("osint-os",               "EXPERIMENTAL/osint-os (Deprecated\u2044Inactive)", "deprecated"),
    ("workout-factory",        "EXPERIMENTAL/workout-factory (Deprecated\u2044Inactive)", "deprecated"),
    # (tdg — removed from portfolio 2026-08-11: made private on GitHub, local
    #  folder deleted; tdg-rust is the canonical TDG project)
    # websites / portfolios (separate category, never ranked)
    ("design-aesthetics-website", "WEBSITES/design-aesthetics-website", "site"),
    ("ishanparihar-cms",       "WEBSITES/ishanparihar-cms", "site"),
    ("ishanparihar-svelte",    "WEBSITES/ishanparihar-svelte", "site"),
    ("law-of-one-india-website", "WEBSITES/law-of-one-india-website", "site"),
    ("webdev-portfolio",       "WEBSITES/webdev-portfolio", "site"),
    ("lifeos-website",         "LIFEOS/lifeos-website", "site"),
]

CODE_EXT = {
    ".rs": "Rust", ".py": "Python", ".ts": "TS", ".tsx": "TS", ".js": "JS",
    ".jsx": "JS", ".go": "Go", ".kt": "Kotlin", ".java": "Java", ".c": "C",
    ".cpp": "C++", ".h": "C", ".hpp": "C++", ".zig": "Zig", ".mql5": "MQL5",
    ".sh": "Shell", ".rb": "Ruby", ".swift": "Swift", ".scala": "Scala",
    ".php": "PHP", ".lua": "Lua",
}
DATA_DIR_RE = re.compile(
    r"(^|/)(samples?|media|assets?|voices?|recordings?|fonts?|images?|icons?|"
    r"srt-word|meditation-repo|references|datasets?|static|public|golden|"
    r"golden-runs)/", re.IGNORECASE,
)
# Vendored/embedded third-party code — excluded from ALL metrics (first-party
# rule). Keep this list explicit and event-driven: add a path pattern ONLY when
# a shared library is actually vendored into a portfolio repo (as toon-helper
# was on 2026-08-11), so the identical copy is not counted N times and does not
# leak sibling-name references into the in-degree scan. Do NOT add generic
# dirs like vendor/ or third_party/ — several repos track real code there and
# silently excluding it would change unrelated measurements.
# toon-helper is vendored at crates/toon-helper/ (automaton, social-forge,
# tdg-rust, slideforge-rust) AND at top-level toon-helper/ (igs-rust).
VENDORED_DIR_RE = re.compile(r"(^|/)(crates/)?toon-helper/")
# (igs-rust/last30days-skill is excluded at ranking time — it is a nested repo,
#  not tracked code, so it needs no pattern here.)
TEST_PATTERNS = {
    ".rs": [re.compile(r"#\[(tokio::)?test\]")],
    ".py": [re.compile(r"\bdef test_")],
    ".ts": [re.compile(r"\bit\(|^\s*it\(|\btest\(|describe\(")],
    ".tsx": [re.compile(r"\bit\(|^\s*it\(|\btest\(|describe\(")],
    ".js": [re.compile(r"\bit\(|^\s*it\(|\btest\(|describe\(")],
    ".jsx": [re.compile(r"\bit\(|^\s*it\(|\btest\(|describe\(")],
    ".go": [re.compile(r"func Test")],
    ".kt": [re.compile(r"@Test")],
    ".java": [re.compile(r"@Test")],
    ".zig": [re.compile(r"test \"")],
}
CONCUR_RE = re.compile(
    r"\basync\s+fn\b|\bawait\b|\btokio::|\brayon::|\bthread::spawn\b|"
    r"\bactix\b|\basync_trait\b|\bmpsc::|\bArc<Mutex>\b|modelcontextprotocol|\brmcp\b",
    re.IGNORECASE,
)
MCP_TOOL_DEC = re.compile(r"@\s*(?:mcp|app|router|server)\.tool\s*\(")
# Class-aware surface detection (v6, 2026-08-12). A project is scored against
# the surface it actually exposes — never zeroed for lacking MCP:
#   mcp   -> @mcp.tool / FastMCP / mcp.server registrations
#   cli   -> click/typer @command, clap derive(Parser), commander .command(,
#            argparse subparsers, console_scripts entry points
#   rest  -> FastAPI @app/@router.(get|post|...), Hono app.(get|post|...),
#            Go mux.Handle("METHOD /path"
#   engine-> runnable binaries ([[bin]] targets / main() entry points) with
#            no interactive surface
CLI_CMD_RE = re.compile(
    r"@\s*(?:click|typer)\.(?:command|group)\s*\(|derive\s*\([^)]*Parser|"
    r"\.command\s*\(|add_parser\s*\(|console_scripts\s*=|entry_points\s*=",
    re.IGNORECASE,
)
REST_ROUTE_RE = re.compile(
    r"@\s*(?:app|router)\.(?:get|post|put|delete|patch)\s*\(|app\.(?:get|post|put|delete|patch)\s*\(|"
    r"mux\.Handle\s*\(\s*\"(?:GET|POST|PUT|DELETE|PATCH)\s+/",
    re.IGNORECASE,
)
ENGINE_BIN_RE = re.compile(r"^\[\[bin\]\]|fn main\s*\(|if __name__\s*==\s*['\"]__main__")


def detect_surface(mcp_hits, cli_hits, rest_hits, bin_hits):
    """Pick the dominant surface class by measured signal count.

    The three interactive classes (mcp/cli/rest) compete on evidence: the
    surface with the most real registrations wins (so a 122-route REST
    backend like osint-os is never demoted to a handful of CLI hits).
    Only when NO interactive surface exists does a project fall to
    `engine` (runnable binaries, floor curve).
    """
    best = max(mcp_hits, cli_hits, rest_hits)
    if best <= 0:
        return "engine", bin_hits
    if best == mcp_hits:
        return "mcp", mcp_hits
    if best == cli_hits:
        return "cli", cli_hits
    return "rest", rest_hits


def sh(repo_dir, cmd, timeout=120):
    try:
        r = subprocess.run(cmd, shell=True, cwd=repo_dir, capture_output=True,
                           text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


def measure(name, relpath, category):
    repo_dir = os.path.join(PORTS, relpath)
    if not os.path.isdir(repo_dir):
        return (name, category, "NO-DIR", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    files = sh(repo_dir, "git ls-files")
    if not files:
        return (name, category, "NO-TRACKED", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    flist = [f for f in files.split("\n") if f and not VENDORED_DIR_RE.search(f)]
    loc_code = 0
    test_hits = 0
    langs = set()
    concur = 0
    mcp_hits = 0
    cli_hits = 0
    rest_hits = 0
    bin_hits = 0
    src_text = []
    for f in flist:
        ext = os.path.splitext(f)[1].lower()
        if ext not in CODE_EXT or DATA_DIR_RE.search(f) or "node_modules/" in f \
                or "target/" in f or ".venv/" in f:
            continue
        full = os.path.join(repo_dir, f)
        if not os.path.isfile(full):
            continue
        try:
            with open(full, "r", errors="ignore") as fh:
                content = fh.read()
        except Exception:
            continue
        loc_code += content.count("\n")
        langs.add(CODE_EXT[ext])
        for pat in TEST_PATTERNS.get(ext, []):
            test_hits += len(pat.findall(content))
        concur += len(CONCUR_RE.findall(content))
        mcp_hits += len(MCP_TOOL_DEC.findall(content))
        cli_hits += len(CLI_CMD_RE.findall(content))
        rest_hits += len(REST_ROUTE_RE.findall(content))
        if f.endswith("Cargo.toml") or ext in (".rs", ".py"):
            bin_hits += len(ENGINE_BIN_RE.findall(content))
        src_text.append(content)
    surface, tools = detect_surface(mcp_hits, cli_hits, rest_hits, bin_hits)
    cargo = [f for f in flist if f.endswith("Cargo.toml")]
    pkgjson = [f for f in flist if f.endswith("package.json")]
    mods = len(cargo) + max(0, min(len(pkgjson), 6))
    ci = sh(repo_dir, "ls .github/workflows/*.yml 2>/dev/null | wc -l")
    try:
        ci = int(ci)
    except ValueError:
        ci = 0
    tags = sh(repo_dir, "git tag 2>/dev/null | wc -l")
    try:
        tags = int(tags)
    except ValueError:
        tags = 0
    now = datetime.datetime.now(datetime.timezone.utc)
    first = sh(repo_dir, "git log --reverse --format=%ct 2>/dev/null | head -1")
    try:
        age = max(1, int((now.timestamp() - int(first)) / 86400))
    except Exception:
        age = 1
    c90 = sh(repo_dir, f"git log --since='{int(now.timestamp()) - 90 * 86400}' --oneline 2>/dev/null | wc -l")
    try:
        c90 = int(c90)
    except ValueError:
        c90 = 0
    all_text = "\n".join(src_text)
    siblings = [r[0] for r in REPOS if r[0] != name]
    indegree = sum(1 for sib in siblings if re.search(rf"\b{sib}\b", all_text, re.IGNORECASE))
    readme = 0
    for rn in ("README.md", "readme.md", "Readme.md"):
        p = os.path.join(repo_dir, rn)
        if os.path.isfile(p):
            try:
                readme = sum(1 for _ in open(p, errors="ignore"))
            except Exception:
                readme = 0
            break
    install = 0
    for f in ("Cargo.toml", "pyproject.toml", "package.json", "Makefile",
              "install.sh", "Dockerfile", "docker-compose.yml"):
        if os.path.isfile(os.path.join(repo_dir, f)):
            install = 1
            break
    docs = 1 if os.path.isdir(os.path.join(repo_dir, "docs")) else 0
    return (name, category, loc_code, test_hits, mods, ci, c90, tags, age,
            len(langs), min(concur, 500), tools, surface, indegree, readme, install, docs)


def main():
    args = sys.argv[1:]
    only = [a for a in args if not a.startswith("--")]
    want_total = "--total" in args
    print("name|category|loc|tests|mods|ci|c90|tags|age|langs|concur|ops|surface|indegree|readme|install|docs")
    rows = []
    for name, relpath, category in REPOS:
        if only and name not in only:
            continue
        r = measure(name, relpath, category)
        print("|".join(str(x) for x in r))
        rows.append(r)
    if want_total:
        # Portfolio-scope totals — the exact numbers behind the profile README's
        # headline metrics. Scope is REPOS above (the 41 ranked portfolio repos;
        # upstream forks and nested repos are excluded by manifest design).
        n = loc = tests = mods = ci = tags = ops = indegree = 0
        for r in rows:
            if r[2] in ("NO-DIR", "NO-TRACKED"):
                continue
            loc += r[2]
            tests += r[3]
            mods += r[4]
            ci += r[5]
            tags += r[7]
            ops += r[11]
            indegree += r[13]
            n += 1
        # Rust crates = pure Cargo.toml manifest count across the SAME subset
        # as the rows (mods also caps package.json counts, so it is not a crate
        # count). Respect the `only` filter so --total never mixes scopes.
        rust_crates = 0
        for name, relpath, _cat in REPOS:
            if only and name not in only:
                continue
            files = sh(os.path.join(PORTS, relpath), "git ls-files")
            rust_crates += sum(
                1 for f in files.split("\n")
                if f.endswith("Cargo.toml") and not VENDORED_DIR_RE.search(f)
            )
        print(
            f"# TOTAL|repos={n}|loc={loc}|tests={tests}|mods={mods}|"
            f"ci={ci}|tags={tags}|ops={ops}|indegree={indegree}|rust_crates={rust_crates}"
        )


if __name__ == "__main__":
    main()
