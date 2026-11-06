#!/usr/bin/env python3
r"""Assert every project list on the profile README is in a defensible order.

Written 2026-11-04 after the operator reported, twice, that "the order of
projects is incorrect in the Complete Project Catalog" — and the first response
fixed the tier HEADERS, which was not the defect. The page still read wrong.
This script is the measurement that says what "right order" means on every
surface the page presents a project list, so the next reader does not have to
re-derive it by eye.

WHY A GATE. The page has five surfaces that present an ordered list of
projects, and the defects measured on 2026-11-04 were spread across all of
them, not just the catalog:

  1. CATALOG (`## 📂 Complete Project Catalog`) — 57 rows in 5 score-band
     blocks. The defect that survived two rounds of fixes: blocks used to be
     grouped by POLICY tier, so a capped repo (private -> B, experimental ->
     C) landed in a block whose score band it could not match, and the
     page-wide score sequence ROSE twice: automaton 6.54 -> sourcehound 9.43
     at the A/B boundary, and project-genome 4.54 -> holosim-infinite 7.48
     at the B/C boundary. Grouping by the band each row's OWN score earns
     gives 0 rises over all 57 rows. That is the invariant this script
     asserts, so the defect cannot come back silently.

  2. ECOSYSTEM TABLES (`## 🛠️ The Complete Ecosystem`) — 3 ranked tables.
     The page's own sentence says "Every row is ranked by the same rubric as
     the software catalog below, so a tool listed here carries the score it
     earned". Measured 2026-11-04: 12 inversions across the three tables
     (6 in Unified MCP, 4 in the -lyr family, 2 in Developer Tooling). The
     claim was false for 12 of 40 rows.

  3. FLAGSHIP TABLE (`## 💎 Flagship Projects`) — a numbered table of 6,
     ordered by score among PUBLIC repos. It IS score-ordered today and is
     asserted as such (R6). The eight `###` deep dives below it are
     OPERATOR-CURATED and deliberately not score-ordered: the page states
     that sourcehound (9.43, private) is "deliberately NOT listed as
     flagship", and the curated set mixes in scorestrata (7.27) between
     operant (9.40) and tdg-rust (8.46). Reordering them would silently
     re-curate the operator's selection, so R7 asserts what the page
     actually promises instead: the deep-dive set must be a SUBSET of the
     flagship table's set, and every deep dive must name a project the
     flagship table names. (Measured 2026-11-04: the deep dives contained
     linkedin-lyr, which the table did not.)

  4. CATALOG HEADING COUNT — the heading claimed "49 Ranked Projects" while
     the catalog held 56 live rows plus 1 struck. The ToC and the hero's raw
     HTML anchor each carried a DIFFERENT count (49 and 56), so the hero link
     was a DEAD ANCHOR on the live page: `#complete-project-catalog-56-ranked-
     projects--1-struck--6-web-sites` matched no heading, because the heading
     said 49. `check_anchors.py` could not see it, because that script only
     matches markdown `](#...)` links and the hero uses a raw `<a href>`.

  5. RAW-HTML ANCHORS — the general case of (4). `check_anchors.py` reads
     `]\((#[^)]+)\)`. A raw `<a href="#...">` is invisible to it. The hero
     line is the only such link on the page today, and it is the one that was
     broken.

WHAT THIS SCRIPT ASSERTS. Each rule is a claim the page makes about itself,
checked against the engine that produces the numbers:

  R1  Catalog: every row's score matches `rank_score.py`, no row is
      duplicated, and the set of rows equals the engine's set.
  R2  Catalog: the score sequence is non-increasing ACROSS THE WHOLE
      catalog, not merely inside each block. This is the rule the defect
      violated, and it is the one that must never be relaxed.
  R3  Catalog: every row sits in the block its own score earns, so each
      block header's stated band is true of the rows beneath it.
  R4  Catalog heading count equals the live row count actually rendered, and
      the ToC and hero anchor agree with the heading.
  R5  Ecosystem tables: scores are non-increasing within each table.
  R6  Flagship table: order is non-increasing in score.
  R6a Value Proposition table: order is non-increasing in score (the page
      says this table's order is computed by the engine, not chosen by hand).
  R7  Flagship table and the deep dives name the SAME set of projects, in
      both directions. The curation itself is the operator's call; the
      disagreement between the page's two flagship surfaces is not.
  R8  Every raw-HTML `<a href="#...">` resolves to a heading on the page.
  R9  The flagship count stated in prose matches the flagship table's rows.
  R10 The Value Proposition test composite equals the sum of its own parts,
      and names the same projects as the table above it.

  MEASURED 2026-11-05, the day R6/R7/R9/R10 were written. R7 was pointing
  at the WRONG table until then: the parser looked for '| # | Project |
  Score |', which is the Value Proposition table, and cut it at 'Those six
  carry'. It compared the eight deep dives against the six public engines of
  the Value Proposition table and reported four dives as 'not in the flagship
  table' - a defect that did not exist, on a table that was not the one the
  rule was written about. The real flagship table is headed '| Flagship |
  What it does |', and comparing it correctly found the actual defects:
  browsefleet was in the table with no dive, linkedin-lyr had a dive with no
  table row, the table carried 4 score rises, the stated count of ten
  matched neither set, and the Value Proposition composite said 11,235
  where its own six parts summed to 11,935.

A failure here is a defect in the page, not a style preference, because the
page asserts each of these as fact in its own text.

Run:  python3 scripts/check_order.py
Exit: 0 = every surface's order holds. 1 = at least one defect, named.
"""
import importlib.util
import io
import contextlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(HERE, "..", "README.md")
RANK = os.path.join(HERE, "rank_score.py")

CATALOG_HEAD = "## 📂 Complete Project Catalog"
ARC_HEAD = "## 🧭 The Arc"
ECOSYSTEM_HEAD = "## 🛠️ The Complete Ecosystem"
FLAGSHIP_HEAD = "## 💎 Flagship Projects"

# The band boundaries each block header states, and the function that decides
# a score's band. Mirrored from rank_score.py's `_natural_tier` because
# rank_score is a script, not a module (importing it runs main()).
BAND_BOUNDS = {
    "S": (8.0, float("inf")),
    "A": (6.5, 8.0),
    "B": (4.5, 6.5),
    "C": (3.25, 4.5),
    "D": (float("-inf"), 3.25),
}


def natural_band(score):
    """The band a score earns with no cap applied. Mirrors rank_score.py."""
    for band, (lo, hi) in BAND_BOUNDS.items():
        if lo <= score < hi:
            return band
    return "D"


def load_engine():
    """Import rank_score.py's DATA without running its main().

    rank_score is a script, not a module: importing it normally executes
    main(), which prints the whole ranking to stdout. The stdout is captured
    so this script's own output stays clean.
    """
    spec = importlib.util.spec_from_file_location("rank_score", RANK)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def engine_rows(rs):
    """name -> (score, tier, category, note), for every ranked (non-site) repo."""
    out = {}
    for row in rs.DATA:
        (name, cat, loc, tests, mods, ci, c90, tags, age, langs, concur,
         ops, soph, surface, axi, indegree, rl, install, docs) = row
        if cat in ("site", "kb"):
            continue
        raw = {
            "architecture": rs.s_architecture(mods, langs, concur, soph),
            "tests": rs.s_tests(tests, loc),
            "agent": rs.s_agent(ops, surface, axi),
            "scale": rs.s_scale(loc, mods),
            "utility": rs.s_utility(rl, install, docs, indegree),
        }
        total = round(sum(rs.WEIGHTS[k] * v for k, v in raw.items()), 2)
        tier, note = rs.tier(total, cat)
        out[name] = (total, tier, cat, note)
    return out


def gh_slug(heading: str) -> str:
    """GitHub-compatible heading id, copied from check_anchors.slug()."""
    t = heading.lower().strip()
    t = re.sub(r"[^\w\s-]", "", t)
    t = re.sub(r"\s", "-", t)
    return "#" + t.strip("-")


CATALOG_ROW = re.compile(
    r"^\* (~~)?(?:🔒 )?\*\*\[([A-Za-z0-9_.-]+)\]"
    r"\(https://github\.com/ishan-parihar/[A-Za-z0-9_.-]+\)\*\* "
    r"`([\d.]+)`", re.M)


def parse_catalog(text):
    """Return (rows, blocks) for the catalog section.

    rows: list of (struck, name, score) in page order.
    blocks: list of (band_letter, [ (name, score), ... ]) in page order.
    """
    start = text.index(CATALOG_HEAD)
    end = text.index(ARC_HEAD)
    sec = text[start:end]

    rows = []
    for m in CATALOG_ROW.finditer(sec):
        rows.append((bool(m.group(1)), m.group(2), float(m.group(3))))

    blocks = []
    for m in re.finditer(
            r"<summary><b>.*?([SABCD])-TIER.*?</summary>(.*?)</details>", sec, re.S):
        band = m.group(1)
        members = [(r.group(2), float(r.group(3)))
                   for r in CATALOG_ROW.finditer(m.group(2))]
        blocks.append((band, members))
    return rows, blocks


def parse_ecosystem_tables(text):
    """Return [(section_title, [(name, score), ...]), ...] for ranked tables."""
    start = text.index(ECOSYSTEM_HEAD)
    end = text.index(CATALOG_HEAD)
    sec = text[start:end]

    tables = []
    for m in re.finditer(r"### (.+?)\n\n(\|.*?\n)\n", sec, re.S):
        title, table = m.group(1), m.group(2)
        names = re.findall(
            r"\[([A-Za-z0-9_.-]+)\]\(https://github\.com/ishan-parihar/", table)
        tables.append((title, names))
    return tables


def parse_flagship_table(text):
    """The flagships the page calls flagship — the table under the
    '## 💎 Flagship Projects' heading, NOT the Value Proposition table.

    The two tables look alike and the wrong one was parsed until 2026-11-05:
    the Value Proposition table is headed '| # | Project | Score |' and
    carries a 'Score' column, so the old parser found it first and cut it at
    'Those six carry'. It therefore compared the deep dives against the six
    public engines of the Value Proposition table, and reported four of the
    eight deep dives as 'not in the flagship table' — a defect that did not
    exist. The flagship table is headed '| Flagship | What it does |'.

    Both tables are now parsed and both are checked, because the page makes
    an ordering claim about each.
    """
    start = text.index(FLAGSHIP_HEAD)
    end = text.index("### ", start)
    table = text[start:end]
    # A row may carry emoji and/or a lock before the link:
    # '| 🤖 **[operant](...)** |' and '| 🔒 📡 **[sourcehound](...)** |'.
    names = re.findall(r"^\|[^\[]*\*\*\[([A-Za-z0-9_.-]+)\]", table, re.M)
    return names


def parse_value_prop_table(text):
    """The six public engines the Value Proposition ranks, in page order.

    This table IS score-ordered (R6a): the page says its order 'is computed
    by scripts/rank_score.py ... not chosen by hand', and it excludes the
    private repos that cannot be re-run by a reader.
    """
    start = text.index("| # | Project | Score |")
    end = text.index("Those ", start)
    table = text[start:end]
    return re.findall(r"\|\s*\d+\s*\|\s*\*\*\[([A-Za-z0-9_.-]+)\]", table)


def parse_flagship_dives(text):
    """The `###` deep dives that follow the flagship table.

    These are the operator's curated selection, in the page's order. They are
    NOT score-ordered and are not required to be: the page presents them as
    the flagship write-ups, and the curation (which projects earn a full
    write-up) is the operator's call. What is asserted is the RELATIONSHIP
    the page implies, in both directions:
      - every deep dive names a project the flagship table lists, and
      - every flagship table row that the page calls a flagship has a dive.
    """
    start = text.index(FLAGSHIP_HEAD)
    end = text.index(ECOSYSTEM_HEAD)
    sec = text[start:end]
    return re.findall(r"^### .*?\[([A-Za-z0-9_.-]+)\]", sec, re.M)


def main() -> int:
    text = open(README, encoding="utf-8").read()
    rs = load_engine()
    eng = engine_rows(rs)

    failures = []

    # -- R1: every catalog row agrees with the engine ------------------------
    rows, blocks = parse_catalog(text)
    seen = {}
    for struck, name, score in rows:
        if name in seen:
            failures.append(
                f"R1 catalog row '{name}' appears {seen[name] + 1}+ times")
        seen[name] = seen.get(name, 0) + 1
        if name not in eng:
            failures.append(f"R1 catalog row '{name}' is not in rank_score.DATA")
            continue
        escore, etier, _cat, _note = eng[name]
        if abs(score - escore) > 0.005:
            failures.append(
                f"R1 catalog row '{name}' shows {score:.2f}, engine says {escore:.2f}")
    for name in eng:
        if name not in seen:
            failures.append(f"R1 engine repo '{name}' is missing from the catalog")

    # -- R2: the score sequence is non-increasing ACROSS THE WHOLE catalog --
    # This is the invariant the defect violated. It is checked on the flat
    # page order (not per block), because a rise inside one block and a rise
    # across a block boundary are the same defect to a reader: the number
    # next to the row goes UP as the reader scrolls down.
    prev = None
    prev_name = None
    for struck, name, score in rows:
        if prev is not None and score > prev + 1e-9:
            failures.append(
                f"R2 catalog order rises {prev:.2f} ({prev_name}) -> "
                f"{score:.2f} ({name})")
        prev, prev_name = score, name

    # -- R3: every row sits in the block its own score earns -----------------
    # A block's header states a score band, so a row outside that band makes
    # the header false. This is what policy-tier grouping broke: sourcehound
    # (9.43) sat in the 4.5-6.49 block.
    for band, members in blocks:
        lo, hi = BAND_BOUNDS[band]
        for name, score in members:
            if not (lo - 1e-9 <= score < hi):
                failures.append(
                    f"R3 row '{name}' ({score:.2f}) is in the {band} block, which "
                    f"holds scores in [{lo}, {hi}) — the block header is false")
            if natural_band(score) != band:
                failures.append(
                    f"R3 row '{name}' ({score:.2f}) earns band "
                    f"{natural_band(score)} but is rendered in the {band} block")

    # -- R4: the heading count, the ToC, and the hero anchor all agree ------
    live = sum(1 for struck, _n, _s in rows if not struck)
    struck_n = sum(1 for struck, _n, _s in rows if struck)
    m = re.search(r"^## 📂 Complete Project Catalog \((\d+) Ranked Projects"
                  r"(?: \+ (\d+) Struck)?(?: \+ (\d+) Web Sites)?\)", text, re.M)
    if not m:
        failures.append("R4 cannot read the catalog heading's counts")
    else:
        h_live = int(m.group(1))
        h_struck = int(m.group(2) or 0)
        if h_live != live:
            failures.append(
                f"R4 catalog heading says {h_live} ranked projects, "
                f"the catalog renders {live}")
        if h_struck != struck_n:
            failures.append(
                f"R4 catalog heading says {h_struck} struck, "
                f"the catalog renders {struck_n}")

    # Every in-page link to the catalog must name the SAME counts, or it is a
    # dead anchor: the slug is derived from the heading text.
    head_slug = gh_slug(m.group(0)) if m else None
    toc = re.findall(r"\]\((#complete-project-catalog[^)]*)\)", text)
    for a in toc:
        if head_slug and a != head_slug:
            failures.append(
                f"R4 the table of contents links {a}, but the heading's anchor "
                f"is {head_slug} — that link goes nowhere")
    raw_hero = re.findall(r'<a\s+href="(#[^"]*catalog[^"]*)"', text)
    for a in raw_hero:
        if head_slug and a != head_slug:
            failures.append(
                f"R4 the hero's raw HTML link points at {a}, but the heading's "
                f"anchor is {head_slug} — that link goes nowhere")

    # -- R5: ecosystem tables are score-ordered ------------------------------
    for title, names in parse_ecosystem_tables(text):
        prev = None
        for name in names:
            if name not in eng:
                continue
            score = eng[name][0]
            if prev is not None and score > prev + 1e-9:
                failures.append(
                    f"R5 ecosystem table '{title.strip()}' is out of order: "
                    f"{prev:.2f} then {score:.2f} ({name})")
            prev = score

    # -- R6: the flagship table is score-ordered ----------------------------
    # The flagship table presents a set of projects as the portfolio's best.
    # It carried 4 score rises since 2026-08 (scorestrata 7.27 -> tdg-rust
    # 8.46 -> openscript 8.70 -> mysterium 8.87 -> sourcehound 9.43), so a
    # reader scrolling it saw the number beside each row go UP while the page
    # presented the list as the ranked best. The order is repaired to the
    # engine's order, and asserted from here on.
    prev = None
    prev_name = None
    for name in parse_flagship_table(text):
        if name not in eng:
            continue
        score = eng[name][0]
        if prev is not None and score > prev + 1e-9:
            failures.append(
                f"R6 flagship table is out of order: {prev:.2f} ({prev_name}) "
                f"then {score:.2f} ({name})")
        prev, prev_name = score, name

    # -- R6a: the Value Proposition table is score-ordered ------------------
    # The page says this table's order 'is computed by scripts/rank_score.py
    # ... not chosen by hand'. That is a claim about the ENGINE's order, so
    # the engine's order is what is checked.
    prev = None
    prev_name = None
    for name in parse_value_prop_table(text):
        if name not in eng:
            continue
        score = eng[name][0]
        if prev is not None and score > prev + 1e-9:
            failures.append(
                f"R6a value proposition table is out of order: {prev:.2f} "
                f"({prev_name}) then {score:.2f} ({name})")
        prev, prev_name = score, name

    # -- R7: the flagship table and the deep dives describe the same set ---
    # The page calls the table 'the ten flagship systems' and then writes up
    # a subset under '### ' headings. Measured 2026-11-05: the table held
    # browsefleet, which had no dive, and the dives held linkedin-lyr, which
    # the table did not list. So the page's two flagship surfaces named
    # different sets, and the stated count described neither.
    #
    # Both directions are asserted, because either alone lets a defect
    # through: subset-only accepted linkedin-lyr's dive with no table row,
    # and superset-only accepted a table row with no dive. The CURATION
    # itself (which projects are flagship) is the operator's call and is not
    # asserted here. Only that the page's two flagship surfaces agree.
    table_names = parse_flagship_table(text)
    dive_names = parse_flagship_dives(text)
    for name in dive_names:
        if name not in table_names:
            failures.append(
                f"R7 flagship deep dive '{name}' is not in the flagship table "
                f"(the page's two flagship surfaces must name the same set)")
    for name in table_names:
        if name not in dive_names:
            failures.append(
                f"R7 flagship table row '{name}' has no deep dive (the page's "
                f"two flagship surfaces must name the same set)")

    # -- R9: the stated flagship count matches the flagship table ------------
    # The page states the count in prose ('The ten flagship systems'). A
    # count that does not match the table it describes is false by
    # inspection, and it was the symptom of the set mismatch in R7.
    m = re.search(r"^The (\w+) flagship systems", text, re.M)
    if not m:
        failures.append("R9 cannot read the flagship count from the prose")
    else:
        word = m.group(1).lower()
        stated = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                  "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
                  "twelve": 12}.get(word)
        if stated is None:
            failures.append(f"R9 cannot read the flagship count '{word}'")
        elif stated != len(table_names):
            failures.append(
                f"R9 the prose says '{word}' flagship systems but the flagship "
                f"table has {len(table_names)} rows")

    # -- R10: the Value Proposition composite equals the sum of its parts ---
    # The page states 'Those six carry 11,235 measured test cases' and then
    # lists the six parts. Measured 2026-11-05: the parts summed to 11,935,
    # so the composite was 700 short of its own arithmetic. A reader can add
    # the parts in a second, so the total has to be their sum.
    m = re.search(
        r"Those (\w+) carry \*\*([\d,]+) measured test cases\*\*[^:]*:\s*"
        r"([\d,]+)\s+([A-Za-z0-9_.-]+)\s*\+\s*([\d,]+)\s+([A-Za-z0-9_.-]+)"
        r"\s*\+\s*([\d,]+)\s+([A-Za-z0-9_.-]+)\s*\+\s*([\d,]+)\s+"
        r"([A-Za-z0-9_.-]+)\s*\+\s*([\d,]+)\s+([A-Za-z0-9_.-]+)\s*\+\s*"
        r"([\d,]+)\s+([A-Za-z0-9_.-]+)", text)
    if not m:
        failures.append("R10 cannot read the Value Proposition test composite")
    else:
        words = m.group(1).lower()
        stated_n = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                    "seven": 7, "eight": 8, "nine": 9, "ten": 10}.get(words)
        stated_total = int(m.group(2).replace(",", ""))
        parts = []
        for i in range(3, 14, 2):
            # The last name carries the sentence's full stop ('holon.').
            parts.append((int(m.group(i).replace(",", "")),
                          m.group(i + 1).rstrip(".")))
        actual_total = sum(p[0] for p in parts)
        if stated_n is not None and stated_n != len(parts):
            failures.append(
                f"R10 the prose says 'those {words}' but the composite lists "
                f"{len(parts)} projects")
        if stated_total != actual_total:
            failures.append(
                f"R10 the composite says {stated_total:,} test cases but its "
                f"parts sum to {actual_total:,} "
                f"({' + '.join(f'{n:,} {p}' for n, p in parts)})")
        # The six projects of the Value Proposition table must be the same
        # six the composite names, in the same order.
        vp = parse_value_prop_table(text)
        composite_names = [p[1] for p in parts]
        if vp != composite_names:
            failures.append(
                f"R10 the composite names {composite_names} but the table "
                f"above it ranks {vp}")

    # -- R8: every raw-HTML anchor resolves ----------------------------------
    slugs = {gh_slug(l) for l in text.splitlines() if l.startswith("#")}
    for a in sorted(set(re.findall(r'<a\s+href="(#[^"]+)"', text))):
        if a not in slugs:
            failures.append(
                f"R8 raw HTML anchor {a} matches no heading on the page")

    if failures:
        print(f"FAIL {os.path.basename(README)}: {len(failures)} order defect(s)")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"check_order: catalog {live} live + {struck_n} struck rows, score "
          f"non-increasing across all {len(blocks)} band blocks; ecosystem, "
          f"flagship and value-proposition tables score-ordered; the flagship "
          f"table and its deep dives name the same {len(table_names)} "
          f"projects; the stated count and test composite match the page; "
          f"every raw-HTML anchor resolves")
    return 0


if __name__ == "__main__":
    sys.exit(main())
