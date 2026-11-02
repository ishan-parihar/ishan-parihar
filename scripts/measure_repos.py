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

# The portfolio tree that holds the repos below. The manifest's *relpaths* were
# written against an older machine layout (MCP-AND-CLIS/igs-rust) and indexed 0 of their
# 41 entries, so this script reported NO-DIR for repos that exist. The *names* were
# always right. So the base is now discovered by name: walk up from this script and take
# the first ancestor from which every manifest name resolves to a directory. If nothing
# resolves, the script says so and exits non-zero rather than emitting a table of zeros
# that reads as a measurement.
DEFAULT_PORTS = os.path.dirname(ROOT)
PORTS = None
# Manifest relpath -> resolved path under the discovered base, filled by resolve_ports().
REL = {}


def resolve_ports(manifest):
    """Discover the portfolio base and each repo's real path under it.

    One pruned walk from the script's own root builds an index of every git directory by
    basename; each ancestor is then scored by dictionary lookups alone. Walking once
    matters: this file's siblings under the portfolio are large trees, and re-walking
    per name per ancestor turned a 3-minute measurement into an unbounded one.
    """
    global REL

    def prune(dirs):
        for skip in ("node_modules", ".git", "target", ".venv", "__pycache__"):
            if skip in dirs:
                dirs.remove(skip)
        return dirs

    # The walk root is the caller's base when one is named, else the script's own
    # default. Measured 2026-11-02: a caller naming `--base ~/Documents/github`
    # got PORTS overwritten but the index still built from `my-projects` alone,
    # so any repo living outside that subtree resolved to nothing and the
    # manifest looked empty even though 53 of its rows resolve fine.
    root = PORTS or DEFAULT_PORTS

    # Index absolute paths under the portfolio root, so any ancestor can be scored by
    # relpath arithmetic alone. Walking once matters: this file's siblings under the
    # portfolio are large trees, and re-walking per name per ancestor turned a
    # 3-minute measurement into an unbounded one.
    by_name = {}
    for base, dirs, _files in os.walk(root):
        prune(dirs)
        if os.path.isdir(os.path.join(base, ".git")):
            by_name.setdefault(os.path.basename(base), base)
    candidates = []
    cur = root
    while True:
        candidates.append(cur)
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    best, best_n, best_rel = None, -1, {}
    for cur in candidates:
        rel, n = {}, 0
        for name, relpath, _cat in manifest:
            if os.path.isdir(os.path.join(cur, relpath)):
                rel[name] = relpath
            elif by_name.get(name):
                rel[name] = os.path.relpath(by_name[name], cur)
            else:
                continue
            n += 1
        if n > best_n:
            best, best_n, best_rel = cur, n, rel
    REL = best_rel
    return best, best_n

# ---------------------------------------------------------------------------
# Repo manifest: (name, relative path under PORTS, category)
#
# THIS BLOCK IS GENERATED by `gen_register.py --write`, which derives name and
# path from GitHub (`gh repo view`, which follows renames) plus a pruned walk of
# the portfolio tree, and preserves the category from the row it replaced. Do
# not hand-edit it; adding a repo means adding it to the generator's source or
# re-running it with the repo already in this list.
#
# Why it is generated rather than hand-maintained (both failure modes measured):
# the relpaths carried prefixes from a machine layout that no longer exists
# (MCP-AND-CLIS/, HERMES/, CONTENT-CREATION/, LIFEOS/, WEBSITES/) and only 1 of
# 41 resolved; and the names drifted on every rename, so 6 of 41 rows pointed at
# repos that do not exist (`igs-rust`->`sourcehound`, `social-forge`->
# `switchpost`, `slideforge-rust`->`deckmill`, `discord-cli`->`discord-lyr`,
# `tg-cli`->`tg-lyr`, `cinesync`->`CineSync`) with two genuinely gone (`icode`,
# `osint-os`). The generator's exit code is 0 only when the register is current,
# so it can be chained as a gate.
#
# `# renamed` marks a row the generator repaired. A row whose repo exists on
# GitHub but has no directory in this tree keeps its old relpath and measures
# RETIRED, which is the named absence measure_repos.py already prints -- not a
# zero, and not an invented path.
# ---------------------------------------------------------------------------
REPOS = [
    ("sourcehound", "agentic-utility/internet/sourcehound", "engine"),
    ("switchpost", "agentic-utility/interaction-surfaces/switchpost", "engine"),
    ("operant", "agentic-harness/operant", "engine"),
    ("scorestrata", "agentic-utility/content-creation/scorestrata", "engine"),
    ("mindstrata", "game-development/mindstrata", "engine"),
    ("tdg-rust", "agentic-utility/memory/tdg-rust", "engine"),
    ("deckmill", "agentic-utility/content-creation/deckmill", "engine"),
    ("automaton", "agentic-utility/automation/automaton", "engine"),
    ("openscript", "agentic-utility/content-creation/openscript", "engine"),
    ("mysterium", "game-development/mysterium", "engine"),
    ("andrometry", "telemetry/andrometry", "engine"),
    ("lifeos-ops", "saas/lifeos-ops", "engine"),
    ("c-suite-agents", "saas/c-suite-agents", "engine"),
    ("thinking-steroid", "agentic-utility/cogniton/thinking-steroid", "engine"),
    ("reddit-lyr", "agentic-utility/interaction-surfaces/reddit-lyr", "engine"),
    ("twitter-lyr", "agentic-utility/interaction-surfaces/twitter-lyr", "engine"),
    ("instagram-lyr", "agentic-utility/interaction-surfaces/instagram-lyr", "engine"),
    ("linkedin-lyr", "agentic-utility/interaction-surfaces/linkedin-lyr", "engine"),
    ("facebook-lyr", "agentic-utility/interaction-surfaces/facebook-lyr", "engine"),
    ("threads-lyr", "agentic-utility/interaction-surfaces/threads-lyr", "engine"),
    ("discord-lyr", "agentic-utility/interaction-surfaces/discord-lyr", "engine"),
    ("tg-lyr", "agentic-utility/interaction-surfaces/tg-lyr", "engine"),
    ("meme-lyr", "agentic-utility/content-creation/meme-lyr", "engine"),
    ("obscura-core", "helpers/obscura-core", "engine"),
    ("consciousness-fabricator", "agentic-utility/content-creation/consciousness-fabricator", "experimental"),
    ("holosim-infinite", "game-development/holosim-infinite", "experimental"),
    ("kali-mahabali", "EXPERIMENTAL/kali-mahabali", "experimental"),
    ("icode", "DEVELOPER-TOOLS (Deprecated⁄Inactive)/icode", "deprecated"),  # gone
    ("browsefleet", "agentic-utility/internet/browsefleet", "engine"),
    ("hermes-prime-bridge", "agentic-harness/hermes-plugins/hermes-prime-bridge", "engine"),
    ("lifeos-bot", "saas/lifeos-bot", "engine"),
    ("lifeos-saas", "saas/lifeos-saas", "engine"),
    ("CineSync", "CONTENT-CREATION/cinesync (Deprecated⁄Inactive)", "deprecated"),  # not-in-tree
    ("osint-os", "EXPERIMENTAL/osint-os (Deprecated⁄Inactive)", "deprecated"),  # gone
    ("workout-factory", "EXPERIMENTAL/workout-factory (Deprecated⁄Inactive)", "deprecated"),  # not-in-tree
    ("design-aesthetics-website", "WEBSITES/design-aesthetics-website", "site"),  # not-in-tree
    ("ishanparihar-cms", "WEBSITES/ishanparihar-cms", "site"),  # not-in-tree
    ("ishanparihar-svelte", "webdev/ishanparihar-svelte", "site"),
    ("law-of-one-india-website", "webdev/law-of-one-india-website", "site"),
    ("webdev-portfolio", "webdev/webdev-portfolio", "site"),
    ("lifeos-website", "saas/lifeos-website", "site"),
    # --- 2026-11-02: the 22 public non-fork repos the register had never
    # carried. These rows are the BOOTSTRAP the generator's header asks for:
    # gen_register.py deliberately "does not decide categories for repos that
    # are not already in the register", so the row and its category are seeded
    # here once and the generator repairs the relpath from GitHub truth
    # afterwards. Category is the operator's ruling, not a default, and it is
    # what the tier columns below are derived from.
    #
    #   engine  -- an agent-facing codebase scored by the same rubric as the
    #              flagship engines
    #   tool    -- developer/desktop tooling, real code, not agent-surface work
    #   infra   -- deployment/runtime configuration, no agent surface
    #   site    -- a web delivery artefact, ranked outside the software rubric
    #   profile -- this profile repo itself; config, not a software project
    #   spec    -- a knowledge/spec corpus, tracked separately per the rubric
    ("artificial-route", "_extra-catalog/artificial-route", "engine"),
    ("cloakctl", "_extra-catalog/cloakctl", "engine"),
    ("memory-wire", "_extra-catalog/memory-wire", "engine"),
    ("metatrader-bridge", "_extra-catalog/metatrader-bridge", "engine"),
    ("metatrader-docker-deployment", "_extra-catalog/metatrader-docker-deployment", "infra"),
    ("palimpsest", "_extra-catalog/palimpsest", "engine"),
    ("swiggy-lyr", "_extra-catalog/swiggy-lyr", "engine"),
    ("amazon-lyr", "_extra-catalog/amazon-lyr", "engine"),
    ("etmoney-lyr", "_extra-catalog/etmoney-lyr", "engine"),
    ("linux-telemetry", "_extra-catalog/linux-telemetry", "engine"),
    ("AI-CAD", "_extra-catalog/AI-CAD", "engine"),
    ("jesse", "_extra-catalog/jesse", "deprecated"),
    ("n8n-compiler", "_extra-catalog/n8n-compiler", "infra"),
    ("android-webcam", "_extra-catalog/android-webcam", "infra"),
    ("omarchy-vpn", "_extra-catalog/omarchy-vpn", "tool"),
    ("pill-bar", "_extra-catalog/pill-bar", "tool"),
    ("pill-suite", "_extra-catalog/pill-suite", "tool"),
    ("segmented-pill-bar", "_extra-catalog/segmented-pill-bar", "tool"),
    ("static-tray", "_extra-catalog/static-tray", "tool"),
    ("holon", "holon", "engine"),
    ("project-genome", "project-genome", "tool"),
    ("ishan-parihar", "ishan-parihar", "profile"),
    ("HoloOS", "HoloOS", "spec"),
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
# MCP tool registration patterns — Python FastMCP decorators (@mcp.tool(...))
# AND Rust rmcp attribute macros (#[tool(...)]). The Rust form was missing
# (2026-08-13 fix): every rmcp-based repo (social-forge, igs-rust, tdg-rust,
# slideforge-rust) measured 0 mcp hits and fell to the wrong surface. The
# pattern is `tool` + `(` so #[tool_router(...)] (a macro, not a tool) does
# not match.
MCP_TOOL_DEC = re.compile(
    r"@\s*(?:mcp|app|router|server)\.tool\s*\(|"
    r"#\s*\[tool\s*\("
)
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
    r"\.command\s*\(|add_parser\s*\(|console_scripts\s*=|entry_points\s*=|"
    r"\[project\.scripts\]|\"bin\"\s*:\s*\{",
    re.IGNORECASE,
)
REST_ROUTE_RE = re.compile(
    r"@\s*(?:app|router)\.(?:get|post|put|delete|patch)\s*\(|app\.(?:get|post|put|delete|patch)\s*\(|"
    r"mux\.Handle\s*\(\s*\"(?:GET|POST|PUT|DELETE|PATCH)\s+/",
    re.IGNORECASE,
)
ENGINE_BIN_RE = re.compile(r"^\[\[bin\]\]|fn main\s*\(|if __name__\s*==\s*['\"]__main__")


# AXI-ergonomics signals (v6.1, 2026-08-12) — six demonstrable axi.md
# principles, each measured by a concrete source pattern:
#   1 TOON output             dump_toon / toon_print_dict / outputTOON / --toon
#   2 --full escape hatch     the --full flag (content truncation escape)
#   3 definitive empty states "0 results" / "no results" / "0 items"
#   4 content truncation      truncate* with a "chars total" size hint
#   5 pre-computed aggregates total_count / totalCount / count: N of M
#   6 structured errors       sys.exit(N) / process.exit(code) / UsageError
AXI_TOON_RE = re.compile(r"\b(dump_toon|toon_print_dict|outputTOON|format_toon|as_toon)\b|--toon", re.I)
AXI_FULL_RE = re.compile(r"--full")
AXI_EMPTY_RE = re.compile(r"(0 results|no results|0 items|none found)", re.I)
AXI_TRUNC_RE = re.compile(r"truncat\w*\s*\(.*chars total", re.I)
AXI_AGG_RE = re.compile(r"(total_count|totalCount|count: \d+ of \d+ total)", re.I)
AXI_EXIT_RE = re.compile(r"(sys\.exit\(|process\.exit\(|UsageError)", re.I)


def count_axi(src_text):
    """Count demonstrable AXI principles across all tracked source (0-6)."""
    blob = "\n".join(src_text)
    n = 0
    for pat in (AXI_TOON_RE, AXI_FULL_RE, AXI_EMPTY_RE, AXI_TRUNC_RE,
                AXI_AGG_RE, AXI_EXIT_RE):
        if pat.search(blob):
            n += 1
    return n


def detect_surface(mcp_hits, cli_hits, rest_hits, bin_hits, pub_cli=False):
    """Pick the dominant surface class by measured signal count.

    The three interactive classes (mcp/cli/rest) compete on evidence: the
    surface with the most real registrations wins (so a 122-route REST
    backend like osint-os is never demoted to a handful of CLI hits).
    Only when NO interactive surface exists does a project fall to
    `engine` (runnable binaries, floor curve).

    Hybrid rule (v6.1): MCP servers that ALSO publish a first-class CLI
    (`"bin"` in package.json or `[project.scripts]` in pyproject.toml) are
    classified `cli` — the AXI CLI is the advertised agent surface and the
    -lyr family ships both. The manifest scan feeds cli_hits already, so a
    repo with both surfaces and a published bin entry reports `cli`.

    INTENDED INTERPRETATION: "advertised surface" is decided by the repo's
    own branding — a `-lyr`/`-cli` repo that ships a published CLI entry
    point is CLI-first even if it also exposes MCP tools. The rule is NOT a
    demotion mechanism: a repo whose identity is MCP-first (e.g. a server
    whose only console script is an internal dev utility) should be scored
    mcp.

    `pub_cli` gates the hybrid branch (2026-08-13 fix): it is true ONLY when
    a published CLI entry point exists in a manifest (package.json "bin" /
    pyproject.toml [project.scripts]). Previously the branch fired on ANY
    cli hit, so a stray `#[derive(Parser)]` inside an MCP-first Rust server
    (social-forge) was misclassified `cli` with ops=1 despite 328 MCP tools.
    """
    best = max(mcp_hits, cli_hits, rest_hits)
    if best <= 0:
        return "engine", bin_hits
    # hybrid: PUBLISHED CLI + any MCP -> cli (AXI-first). Report the tool
    # count (max of the two signals): the -lyr family advertises its MCP
    # tool count as the ops figure (reddit-lyr 56, instagram-lyr 47, ...)
    # and its only cli_hit is the [project.scripts] manifest entry. Without
    # the max, regeneration would collapse those rows to ops=1.
    if pub_cli and mcp_hits > 0:
        return "cli", max(cli_hits, mcp_hits)
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
    repo_dir = os.path.join(PORTS, REL.get(name, relpath))
    if not os.path.isdir(repo_dir):
        # A named absence, not a zero. 9 of the 41 manifest repos are retired (3 are
        # renames already proved by git remote -v, 6 are archived or private), and a
        # row of zeros is indistinguishable from a measurement of an empty repo.
        return (name, category, "RETIRED", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    files = sh(repo_dir, "git ls-files")
    if not files:
        return (name, category, "NO-TRACKED", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    flist = [f for f in files.split("\n") if f and not VENDORED_DIR_RE.search(f)]
    loc_code = 0
    test_hits = 0
    langs = set()
    concur = 0
    mcp_hits = 0
    cli_hits = 0
    pub_cli = False
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
    # package.json "bin" / pyproject [project.scripts] are CLI signals but .json
    # and .toml are not in CODE_EXT, so scan the manifest files directly. A
    # PUBLISHED CLI entry point ("bin" / [project.scripts]) is what gates the
    # hybrid mcp+cli classification — not stray source-level clap derives.
    for mf in ("package.json", "pyproject.toml", "Cargo.toml"):
        p = os.path.join(repo_dir, mf)
        if os.path.isfile(p):
            try:
                mf_src = open(p, errors="ignore").read()
            except Exception:
                mf_src = ""
            cli_hits += len(CLI_CMD_RE.findall(mf_src))
            # PUBLISHED CLI = a first-class entry point a user installs: the
            # "bin" key in package.json or [project.scripts] in pyproject.toml.
            # Cargo.toml's [[bin]] is NOT one (internal build target, not a
            # published console script) — social-forge ships a clap dashboard
            # binary yet its identity is MCP-first (300+ tools).
            if mf == "package.json" and '"bin"' in mf_src:
                pub_cli = True
            elif mf == "pyproject.toml" and "[project.scripts]" in mf_src:
                pub_cli = True
    surface, tools = detect_surface(mcp_hits, cli_hits, rest_hits, bin_hits, pub_cli)
    axi = count_axi(src_text) if surface == "cli" else 0
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
            len(langs), min(concur, 500), tools, surface, axi, indegree, readme, install, docs)


def main():
    global PORTS, REL
    args = sys.argv[1:]
    # `--base <path>` consumed its value, so build the positional list from
    # args EXCLUDING that flag and the token that follows it. Measured
    # 2026-11-02: `only` used to be "every token not starting with --", which
    # swallowed `--base`'s own value and filtered the manifest down to a repo
    # literally named `/home/ishanp/Documents/github`. The manifest then resolved
    # 0 of 0 and the command reported "no repo resolves" for a base that has
    # 60 of them. A repo name can never equal a path we just accepted, so
    # skipping the pair is lossless.
    skip: set[int] = set()
    if "--base" in args:
        i = args.index("--base")
        skip = {i, i + 1}
    only = [a for idx, a in enumerate(args) if not a.startswith("--") and idx not in skip]
    want_total = "--total" in args
    manifest = REPOS
    if only:
        manifest = [r for r in REPOS if r[0] in only]
    # --base must be applied BEFORE resolution, not after. Measured 2026-11-02:
    # it used to be read after `resolve_ports` had already run, so REL carried
    # relpaths relative to the auto-discovered ancestor while PORTS was
    # overwritten with the caller's tree, and every `os.path.join(PORTS, rel)`
    # then pointed at <caller-base>/<ancestor-relative path> -- a path that does
    # not exist. The rewrite is only correct if the resolution happens against
    # the base the caller actually named, so it moves above the call.
    if "--base" in args:
        PORTS = args[args.index("--base") + 1]
    PORTS, n_resolve = resolve_ports(manifest)
    # A measurement that finds nothing is not a measurement. Rank_score.py's docstring and
    # docs/RUNBOOK.md both name this command as the way to regenerate the dataset, so a
    # silent zeros table would overwrite a correct snapshot. Same form as deslop.py's
    # exit 2: refuse, name the reason, do not report a figure.
    if n_resolve <= 0:
        sys.stderr.write(
            "measure_repos: no manifest repo resolves under any ancestor of "
            f"{ROOT} (resolved {n_resolve} of {len(manifest)}). Refusing to emit a "
            "table of zeros. Pass --base <path> to name the portfolio tree.\n"
        )
        sys.exit(2)
    print("name|category|loc|tests|mods|ci|c90|tags|age|langs|concur|ops|surface|axi|indegree|readme|install|docs")
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
            if r[2] in ("RETIRED", "NO-TRACKED"):
                continue
            loc += r[2]
            tests += r[3]
            mods += r[4]
            ci += r[5]
            tags += r[7]
            ops += r[11]
            indegree += r[14]
            n += 1
        # Rust crates = pure Cargo.toml manifest count across the SAME subset
        # as the rows (mods also caps package.json counts, so it is not a crate
        # count). Respect the `only` filter so --total never mixes scopes.
        rust_crates = 0
        for name, relpath, _cat in REPOS:
            if only and name not in only:
                continue
            files = sh(os.path.join(PORTS, REL.get(name, relpath)), "git ls-files")
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
