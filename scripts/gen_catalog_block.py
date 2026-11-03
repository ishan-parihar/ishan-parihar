#!/usr/bin/env python3
r"""Compose the README's Complete Project Catalog block from measured evidence.

WHY THIS EXISTS. The catalog used to be hand-written prose with hand-typed
scores, so its tier counts and its own heading disagreed (the page said 42
projects five times while the tier headers summed to 35 and the rows numbered
36). A catalog that contradicts itself is the exact drift this portfolio's gates
exist to prevent, so the block is now ASSEMBLED, not edited:

  1. every row comes from `rank_score.py --all`, in score order, so order and
     tier are derived rather than chosen;
  2. descriptions for repos already in the catalog are lifted VERBATIM from the
     existing README -- this script never rewrites a working sentence to fit a
     new number, it only moves it;
  3. descriptions for repos that were missing from the register are supplied
     here, and each one carries only a figure this repo can measure or a claim
     the repo's own README makes, cited to that source.

Every figure printed next to a row is the measured `rank_score` score, so the
page and the engine can no longer disagree without this script disagreeing first.

Regenerate with:
    python3 scripts/measure_repos.py --base "$HOME/Documents/github" > docs/audit/<date>-full-fleet-measure.tsv
    python3 scripts/soph_audit.py    --base "$HOME/Documents/github" > docs/audit/<date>-soph-fleet.txt
    python3 scripts/rank_score.py --all | rg '^ *[0-9]+\.' > /tmp/order.txt
    python3 scripts/gen_catalog_block.py            # prints the block to stdout
"""

import os
import re
import subprocess
import sys
from collections import defaultdict

HERE = __file__.rsplit("/", 1)[0]
README = f"{HERE}/../README.md"

TIER_HEADS = {
    "S": "🚀 S-TIER: Flagship Systems — Score ≥ 8.0",
    "A": "🧠 A-TIER: Production-Grade Engines — Score 6.5–7.99",
    "B": "📡 B-TIER: Solid Utilities — Score 4.5–6.49",
    "C": "🧰 C-TIER: Operational & Capped — Score 3.25–4.49 or policy-capped",
    "D": "📉 D-TIER: Minimal / Stalled — Score < 3.25",
}

# Descriptions for the repos that were in no register before 2026-11-02. Each is
# built from a measured column or a claim the repo's own README makes, and says
# which. Nothing here is invented: where a number appears, `measure_repos.py` or
# the repo's own README produced it.
NEW_DESC = {
    "artificial-route": (
        "Minimal-RAM Rust LLM gateway — one OpenAI-compatible endpoint over 276 providers, "
        "19 routing strategies, auto/*, static musl binary. 26 releases, Apache-2.0. "
        "Reaches S-tier on ITS OWN measured architecture score (8.6/10), not on a claim."
    ),
    "holon": (
        "Harness-agnostic agentic OS that runs as a self-healing, self-evolving organization "
        "of persistent AI employees. 45K LOC, MIT, 10 measured sophistication families. "
        "Enters at S-tier (8.10) on the same rubric as every other engine here."
    ),
    "memory-wire": (
        "Agent memory in one static Rust binary — retain/recall/reflect with bank isolation, "
        "FTS5 BM25 + RRF fusion, PII redaction on write, over HTTP or as an MCP stdio server. "
        "14 releases."
    ),
    "cloakctl": (
        "One persistent stealth browser per profile over CLI verbs over --json, plus a registry "
        "where agents save, compose and compound reusable automations (skills vs workflows). "
        "25 measured CLI commands, MIT, 5 releases."
    ),
    "metatrader-bridge": (
        "MetaTrader 5 to MCP bridge — regime detection, ATR position sizing, bracket orders, "
        "trailing stops. 91 declared MCP tools across 127 measured REST endpoints, MIT, "
        "runs on a 512 MB VPS."
    ),
    "HoloOS": (
        "Enterprise systems modeling and topological risk — a 14K-YAML + 1.2K-MD knowledge "
        "corpus with a `holos` CLI (187 measured subcommands) and an MCP server. Spec "
        "corpus: tracked separately from software, never tiered against the code rubric."
    ),
    "amazon-lyr": (
        "The full Amazon lifecycle as MCP tools for agents — search, product detail, reviews, "
        "cart, orders, shipments, via browser cookies with no API keys. 21 declared MCP "
        "tools, MIT."
    ),
    "etmoney-lyr": (
        "ET Money research layer for AI agents — 67 mutual-fund categories, stock screens and "
        "NIFTY constituents as 10 MCP tools. Highest AXI score among the newly added repos "
        "(4/6), MIT."
    ),
    "jesse": (
        "Deprecated — its own README says so (\"no longer actively maintained\"). 21 measured "
        "CLI commands, MIT. Ranked at its measured score and capped at C by the documented "
        "archived/deprecated policy."
    ),
    "swiggy-lyr": (
        "Unified Swiggy MCP — Food, Instamart and Dineout in one server with one OAuth token. "
        "MIT, 3 measured CLI commands."
    ),
    "android-webcam": (
        "Android phone as webcam and microphone on the Linux desktop — 720p/1080p, "
        "front/back, torch, mic. Kotlin + QML + Python, MIT. Real desktop tooling "
        "(infra category)."
    ),
    "AI-CAD": (
        "AI-powered CAD platform — FastAPI floor-plan generation, ezdxf DXF export, "
        "real-time collaboration. TypeScript + Python + Shell, MIT, 23 measured endpoints."
    ),
    "ishan-parihar": (
        "This profile repo — the README, its measurement scripts, and the register that "
        "measures every other row. Scored and shown for completeness, tagged `profile` so "
        "no reader mistakes configuration for a software project."
    ),
    "palimpsest": (
        "A training system for one mind — the AI is the trainer, the digestion happens in "
        "the reader. TypeScript + Python, built on an upstream harness."
    ),
    "project-genome": (
        "A project's knowledge genome — owned document roles, mutability classes, and a "
        "stdlib CLI (wake/ask/close) that checks them. 11 measured commands, MIT. The same "
        "tool that gates this portfolio's own documentation."
    ),
    "linux-telemetry": (
        "Production-grade Linux usage telemetry — window activity, browser history, KDE app "
        "directories, process launches, desktop-file executions, minimal system impact. "
        "Python, MIT, 12 measured commands."
    ),
    "n8n-compiler": (
        "Treat n8n workflows as code. 10 measured CLI commands, CI-gated. Infra category — "
        "real tooling, no agent surface."
    ),
    "metatrader-docker-deployment": (
        "Production MetaTrader 4 & 5 Docker deployment with noVNC browser access. Infra "
        "category, 5 measured commands, MIT."
    ),
    "omarchy-vpn": (
        "Omarchy bar plugin for a self-hosted VPS VPN — WireGuard full-tunnel + SSH SOCKS "
        "fallback, live stats, IPv6-leak guard. QML, MIT."
    ),
    "pill-bar": (
        "Omarchy segmented pill bar — pills only behind widget clusters, tray always "
        "expanded, no chevron. QML + JavaScript, MIT."
    ),
    "pill-suite": "Omarchy pill bar + static tray bundle. QML + JavaScript.",
    "segmented-pill-bar": (
        "Omarchy segmented pill bar — transparent window, pills behind clusters only. "
        "QML + JavaScript."
    ),
    "static-tray": (
        "Omarchy static tray — always expanded, no chevron, for segmented pill bars. "
        "48 tracked lines, QML + JavaScript."
    ),
}

CATEGORY_TAG = {
    "experimental": "experimental",
    # `deprecated` renders as `deprecated`, NOT `archived`.  MEASURED DEFECT,
    # 2026-11-03: this dict mapped deprecated -> "archived", so the three
    # deprecated rows (jesse, CineSync, workout-factory) were emitted reading
    # `(archived)`.  `gh api repos/ishan-parihar/<name>` returns archived=false for
    # all three — they are deprecated (the operator stopped work on them, or their
    # own README says so), but they are NOT GitHub-archived repositories.  The page
    # was asserting a repository state it had not measured, and a reader who
    # clicked through would not see the "This repository has been archived" banner
    # the tag implies.  The two are different claims: `archived` is a GitHub
    # boolean, `deprecated` is the operator's judgment, and only the second is what
    # this page actually knows.
    "deprecated": "deprecated",
    "infra": "infra",
    "tool": "tool",
    "profile": "profile",
    "spec": "spec",
}


def load_ranked(order_path: str):
    """Parse `rank_score.py --all`'s ranked list into (name, score, tier, note)."""
    out = []
    for line in open(order_path, encoding="utf-8"):
        m = re.match(r"\s*\d+\.\s+(\S+)\s+([\d.]+)\s+\[(\w)\](.*)$", line.rstrip("\n"))
        if m:
            out.append((m.group(1), float(m.group(2)), m.group(3), m.group(4).strip()))
    return out


def load_site_names(path: str):
    """Repos the rubric excludes from ranking entirely (web delivery artefacts)."""
    out = set()
    for line in open(path, encoding="utf-8"):
        m = re.match(r'\s*\("([^"]+)", "site",', line)
        if m:
            out.add(m.group(1))
    return out


def load_visibility(path: str):
    """Repo -> 'private'/'public'/'404', measured from GitHub, never a guess.

    Added 2026-11-02 after the operator reported that the page ranked software
    repos as if they were public while they had in fact been privated:
    "Deprecated and privated projects like c-suite-agents should not be shown
    as production-grade."  Measured with `gh api repos/ishan-parihar/<name>` over
    every link the page emits.  A 404 is treated as private-ish rather than
    dropped, so a repo that vanished still fails closed rather than silently
    rendering as public.
    """
    out = {}
    if not path or not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8"):
        parts = line.split()
        if len(parts) >= 2:
            out[parts[0]] = parts[1]
    return out


def visibility_prefix(name: str, vis: dict):
    """Mark a row's opener so a private repo never reads as public.  '' if public.

    Measurement that found the need: 12 of the 63 repos the page links are
    private per `gh api` (2026-11-02): c-suite-agents, design-aesthetics-website,
    ishanparihar-cms, ishanparihar-svelte, kali-mahabali,
    law-of-one-india-website, lifeos-bot, lifeos-ops, lifeos-saas,
    lifeos-website, sourcehound, webdev-portfolio.  Only the six web portfolios
    already carried the lock; the six software repos (including the operator's
    flagship sourcehound, which is private today and will be re-published later)
    did not, so a reader clicked a link that 404'd.
    """
    state = vis.get(name, "public")
    return "" if state == "public" else "\U0001f512 "


def load_verbatim_descriptions(path: str):
    """Existing catalog sentences, so a working description is never rewritten."""
    out = {}
    pat = re.compile(
        r"^\* (?:~~)?(?:🔒 )?\*\*\[([A-Za-z0-9_.-]+)\]"
        r"\(https://github\.com/ishan-parihar/[A-Za-z0-9_.-]+\)\*\* "
        r"`[\d.]+`(?: \((?:capped|archived|experimental|infra|tool|profile|spec)\))?"
        r"(?: <!--[^>]*-->)?: (.+)$",
        re.M,
    )
    for m in pat.finditer(open(path, encoding="utf-8").read()):
        # Normalise the captured sentence: a struck row carries its closing `~~`
        # INSIDE the capture (it sits before any trailing HTML comment), and
        # `load_struck` owns re-applying the markers. Leaving it in produced
        # `...~~ <!-- ... -->~~` — doubled markers — the first time this ran.
        text = re.sub(r"~~\s*(?=<!--)", "", m.group(2))
        text = re.sub(r"\s*~~$", "", text)
        out.setdefault(m.group(1), text)
    return out


def load_struck(path: str):
    """Rows the README strikes through, so a regeneration keeps them struck.

    MEASURED DEFECT, 2026-11-02: `load_verbatim_descriptions` reads a row with
    `(?:~~)?` — it SKIPS the strike markers when parsing — but the emit template
    below has no way to write them back. Running the generator on a README whose
    icode row was struck therefore returned `* **[icode](...)** ...: <text>~~`,
    dropping only the OPENING `~~`: the row read as live while its closing marker
    stayed, and the row the whole dead-link comment is about stopped being struck.

    A row is struck when the line begins `* ~~`. Read from the source, not from
    the description text: the trailing `~~` may sit inside a captured group and
    its absence from the front is exactly the failure being fixed.
    """
    struck = set()
    for line in open(path, encoding="utf-8").read().splitlines():
        if not line.startswith("* ~~"):
            continue
        m = re.match(
            r"^\* ~~(?:🔒 )?\*\*\[([A-Za-z0-9_.-]+)\]", line)
        if m:
            struck.add(m.group(1))
    return struck


def note_tag(note: str):
    if "capped: experimental" in note:
        return "experimental"
    # Reads the cap reason, which rank_score.py writes as "capped:
    # archived/deprecated — ..." for BOTH the deprecated category and a
    # genuinely-archived one, so the emitted tag follows what the note actually
    # says rather than a single lumped word.  Measured 2026-11-03: the three
    # deprecated repos are `archived=false` on GitHub, so they must not be
    # labelled `(archived)`; a repo that GitHub really has archived still is.
    if "capped: archived/deprecated" in note:
        return "deprecated"
    if "capped: archived" in note:
        return "archived"
    for key, tag in CATEGORY_TAG.items():
        if note.startswith(key + ":"):
            return tag
    return None


def main() -> int:
    ranked = load_ranked("/tmp/order.txt")
    if not ranked:
        sys.stderr.write(
            "gen_catalog_block: /tmp/order.txt is empty. Run "
            "`python3 scripts/rank_score.py --all | rg '^ *[0-9]+\\.' > /tmp/order.txt` first.\n"
        )
        return 2
    sites = load_site_names(f"{HERE}/rank_score.py")
    verbatim = load_verbatim_descriptions(README)
    struck = load_struck(README)
    vis = load_visibility("/tmp/visibility.txt")

    rows = [r for r in ranked if r[0] not in sites]
    by_tier = defaultdict(list)
    for name, score, tier, note in rows:
        by_tier[tier].append((name, score, tier, note))

    out = []
    reused = new = 0
    for tier in "SABCD":
        members = sorted(by_tier[tier], key=lambda r: -r[1])
        n = len(members)
        # A struck row is counted separately, because it is not an active member
        # of the tier: folding icode into "11 Projects" made the label read as
        # eleven live projects while the ToC above still said "56 Ranked +
        # 1 Struck". The two labels must not disagree.
        n_struck = sum(1 for r in members if r[0] in struck)
        live = n - n_struck
        label = f"{live} Project{'s' if live != 1 else ''}"
        if n_struck:
            label += f" + {n_struck} Struck"
        out.append("")
        out.append("<details>")
        out.append(f"<summary><b>{TIER_HEADS[tier]} ({label})</b></summary>")
        # A blank line MUST separate </summary> from the list, and no <br> may sit
        # between them. Both measured against GitHub's own renderer
        # (`gh api -X POST markdown`) rather than assumed, 2026-11-02:
        #
        #   <summary>x</summary>
        #   * [a](url)
        #     -> GitHub stays in raw-HTML mode for the rest of the <details> block and
        #        emits the literal text `* **[a](<a href="url">url</a>)**`, with markup
        #        leaking and no link rendered. This is the defect the operator reported
        #        as "the links ... are leaking its formatting and are not showing the
        #        output correctly".
        #   <summary>x</summary>
        #   <br>
        #   <blank>
        #     -> the <br> is an HTML tag, so GitHub is still in raw-HTML mode when it
        #        reaches the list, and the same leak occurs.
        #   <summary>x</summary>
        #   <blank>
        #     -> GitHub leaves raw-HTML mode, parses the list as markdown, and every
        #        row renders: `* **[a](url)** ...` becomes a real <li> with a real <a>.
        #
        # Verified on the full 11-row S-tier block: 11 raw leaks before, 0 after, with
        # 11 rendered links. 0 leaks across the whole page after all five blocks.
        out.append("")
        for name, score, tr, note in members:
            if name in verbatim:
                text = verbatim[name]
                reused += 1
            elif name in NEW_DESC:
                text = NEW_DESC[name]
                new += 1
            else:
                sys.stderr.write(
                    f"gen_catalog_block: {name} has no description and none is declared. "
                    "Refusing to emit a row that says nothing.\n"
                )
                return 2
            tag = note_tag(note)
            suffix = f" ({tag})" if tag else ""
            # A struck row stays struck across a regeneration, with the markers
            # wrapping the WHOLE row (not just its tail) — see load_struck.
            open_strike = "~~" if name in struck else ""
            # A private repo is marked at the point of the link, so a reader is not
            # led to a 404. Driven by GitHub truth, not a hand-kept list: the
            # operator found six software repos (sourcehound among them, his
            # flagship) reading as public while private.
            lock = visibility_prefix(name, vis)
            out.append(
                f"* {open_strike}{lock}**[{name}](https://github.com/ishan-parihar/{name})** "
                f"`{score:.2f}`{suffix}: {text}{open_strike}"
            )
        out.append("")
        out.append("</details>")
        out.append("")

    sys.stderr.write(
        f"gen_catalog_block: {reused} descriptions reused verbatim, {new} newly written, "
        f"{reused + new} rows, sites excluded: {len(sites)}\n"
    )
    sys.stdout.write("\n".join(out).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
