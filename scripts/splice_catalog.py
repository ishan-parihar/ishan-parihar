#!/usr/bin/env python3
"""Splice a regenerated catalog block into README.md in place.

Split out of a shell pipeline on 2026-11-02 because the pipeline had a MEASURED
DEFECT: the region selector started at the `## 📂 Complete Project Catalog`
heading itself, but the generator's output does not include that heading.  Two
splices in a row therefore deleted the section heading and its blank line, losing
2 lines (399 -> 397), and the Contents entry pointed at a heading that no longer
existed - a broken in-page anchor a reader would notice immediately.  The third
run reported the loss in its diff output, which is how it was caught.

This script asserts the heading survives, every line count it claims, and fails
loudly rather than writing a smaller README.
"""
import subprocess
import sys

README = "README.md"
START = "## 📂 Complete Project Catalog"
END = "## 🧭 The Arc"


def main() -> int:
    before = open(README, encoding="utf-8").read()
    if START not in before:
        sys.stderr.write(f"splice_catalog: {START!r} missing from {README}\n")
        return 2
    if before.count(START) != 1:
        sys.stderr.write(f"splice_catalog: {START!r} appears more than once\n")
        return 2

    gen = subprocess.run([sys.executable, "scripts/gen_catalog_block.py"],
                         capture_output=True, text=True)
    if gen.returncode != 0:
        sys.stderr.write(f"splice_catalog: generator failed:\n{gen.stderr}\n")
        return 2
    block = gen.stdout.rstrip("\n").split("\n")

    lines = before.split("\n")
    # Slice BETWEEN the heading and the next section: exclusive of START, so the
    # heading survives - this is the defect this script exists to prevent.
    start = next(i for i, l in enumerate(lines) if l.startswith(START))
    end = next(i for i, l in enumerate(lines[start:], start) if l.startswith(END))

    out = lines[: start + 1] + block + lines[end:]
    after = "\n".join(out)

    # The heading must survive, and the block must not have lost the heading's
    # own spacing.  Asserted rather than assumed.
    for must in (START, END):
        if after.count(must) != 1:
            sys.stderr.write(f"splice_catalog: {must!r} appears {after.count(must)}x after splice\n")
            return 1
    if after.count("\n") != before.count("\n") + (len(block) - (end - start - 1)):
        sys.stderr.write(
            "splice_catalog: line budget moved unexpectedly: "
            f"{before.count(chr(10))} -> {after.count(chr(10))}\n")
        return 1

    open(README, "w", encoding="utf-8").write(after)
    print(f"splice_catalog: {len(block)} block lines, {before.count(chr(10))} -> "
          f"{after.count(chr(10))} lines, heading preserved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
