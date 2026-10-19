<!-- ============================================================
  TEMPLATE.md — Portfolio README Baseline (S-grade)

  Copy this file to YOUR_REPO/README.md and fill every [PLACEHOLDER].
  Keep the structure and information order; the quality bar is
  enforced by the readme-craft mandates in the checklist at the bottom.

  Conventions enforced across the ishan-parihar portfolio:
    - GitHub Sponsors + Razorpay support block (MANDATORY, §Support)
    - LOC badge (keep in sync — run ishan-parihar/scripts/check_loc_badges.py)
    - CI badge (only when .github/workflows/ exists)
    - T2I hero spec comment (text-to-image ready) + optional SVG hero
  ============================================================ -->

<!-- T2I HERO SPEC — Subject: [describe the system's one visual essence — a
  production artifact, a flow, the product doing its job — NO generic
  decoration]. Composition: [main subject] + [supporting element] + [accent].
  Palette: [bg hex] / [primary hex] / [accent hex] / [muted hex]. Style:
  [dark editorial / friendly flat / cinematic / technical] vector, subtle
  glow, no text. 16:9. -->

<!-- Optional: inline SVG hero (portfolio style: 1200x320, viewBox, system
     fonts, semantic <title>, NO <script>/<foreignObject>/remote fonts).
     If omitted, the T2I spec above is the contract for a hero image. -->
<div align="center">
  <svg width="100%" height="260" viewBox="0 0 1200 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="[Project name] — [one-line value]">
    <title>[Project name] — [one-line value]</title>
    <rect width="1200" height="260" rx="16" fill="#0B0F19"/>
    <!-- project-native motif shapes here -->
    <text x="600" y="130" font-family="system-ui, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">[PROJECT NAME]</text>
    <text x="600" y="165" font-family="system-ui, sans-serif" font-size="14" fill="#94A3B8" text-anchor="middle">[one-line value statement]</text>
  </svg>
</div>

<!-- Badge row — order: language, LOC, CI, MCP/tools, license, status.
     LOC badge MUST match scripts/check_loc_badges.py output. -->
![Language](https://img.shields.io/badge/Language-[NAME]-blue)
![LOC](https://img.shields.io/badge/LOC-[N]K-informational?style=flat-square)
[![CI](https://github.com/[OWNER]/[REPO]/actions/workflows/ci.yml/badge.svg)](https://github.com/[OWNER]/[REPO]/actions/workflows/ci.yml)
![Tools](https://img.shields.io/badge/[MCP/CLI]-[N]%20Tools-orange?logo=modelcontextprotocol)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)  <!-- or Research-Prototype-orange -->

> **The one sentence.** — what the project does, who it is for, and the single
> outcome it delivers. No jargon, no brand name required to understand it.

## Why this exists

[The problem, stated in the reader's terms — the way it hurts today. 2–4 sentences.
Do NOT start with architecture or commands. This is the first screen's job:
explain the project without requiring prior knowledge.]

## What it does

[The mechanism in plain language — the "how it's different" once, not repeated
promises. If it replaced something (a slower stack, a browser, a manual step),
say the concrete before/after.]

<!-- PROOF BEFORE ABSTRACT CLAIMS: real screenshots/outputs/artifacts, not
     stock images. Alt text on every image. If the artifact is a CLI, show a
     real TOON/YAML output block instead of a mockup. -->

## Proof

![Screenshot/artifact](assets/readme/[screenshot].png)

```
$ [real command]
[real output — copy-pasted, not invented]
```

## How it works

[A short architecture block: 3–7 components and the data flow between them.
A small diagram (mermaid or inline SVG, ≥20px essential text) is preferred.
Keep it at mechanism level — full internals belong in docs/architecture.md.]

```
input → component A → component B → artifact
```

## Quick start

[The SHORTEST working path first. One install command + one working command.
Advanced configuration goes BELOW, never before first use.]

```bash
# install
[install command]

# first run — produces [artifact]
[first command]
```

## Usage

[One end-to-end example beats many disconnected snippets. Tables for commands,
flags, or configuration keys — not prose walls.]

| Command / flag | Purpose |
|---|---|
| `[cmd]` | [what it does] |
| `[flag]` | [what it does] |

## Features

| Area | What it does |
|------|--------------|
| [Feature] | [2–6 word description] |

## Tests

```bash
[test command]   # suite: N tests
```

[What the suite pins (determinism, contracts, golden outputs).]

## Limits & compatibility

[Visible limitations that affect user choice — platforms, formats, resource
requirements. Do not hide them.]

## License

MIT © [Owner]. [Optional: "This project is a fork of X" attribution if real.]

---

## ☕ Support & Sponsorship

If you find this project useful, consider supporting ongoing development:

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?style=flat-square&logo=github)](https://github.com/sponsors/ishan-parihar)
[![Donate](https://img.shields.io/badge/Donate-Razorpay-3395FF?style=flat-square)](https://rzp.io/rzp/ishan-parihar)

Your support funds new features, releases, and infrastructure for the whole ecosystem.

<!-- ============================================================
  README-CRAFT QUALITY CHECKLIST (delete before commit)
  [ ] First screen explains the project without prior knowledge
  [ ] Information order: Value → Proof → Mechanism → First use → Detail
  [ ] Hero material comes from the project, not generic decoration
  [ ] Real proof (output/screenshot) appears before abstract claims
  [ ] Every visual module has a communication job
  [ ] Works when images fail: alt text, headings, commands, links meaningful
  [ ] Removing the repo name would break the hero (project-native, not templated)
  [ ] License is a single short line (portfolio convention); the full license lives in the LICENSE file
  [ ] Emojis used sparingly; no emoji headings
  [ ] Shortest install path appears before advanced configuration
  [ ] One end-to-end example over disconnected snippets
  [ ] GitHub Sponsors + Razorpay block present (§Support)
  [ ] LOC badge present and matches scripts/check_loc_badges.py
  [ ] CI badge present iff .github/workflows/ exists
  [ ] README < 400 lines (detail lives in docs/)
  [ ] Commands are copy-pasteable (no placeholders like "your-key" left in code fences)
  ============================================================ -->
