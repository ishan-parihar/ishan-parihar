# Flagship Deep Dives — ishan-parihar Profile

The eight flagship systems in full prose. The profile README carries the table
that points here; this file owns the detail, because the README has a hard 400-line
cap (its own S08 rubric rule) and "detail belongs in `docs/`, not the README".

**Why this file exists.** On 2026-11-02 the catalog was completed with the 22
public repos that were in no register, which took the README to 423 lines and broke
its own gate. The fix was not to delete the flagship write-ups — they are the part a
recruiter actually reads — so they moved here, with the README keeping one line per
flagship and a link to this file. Every figure below was already on the README and
was moved verbatim; nothing here was re-measured or re-phrased.

Each dive states the date and command that measured it, so a figure can be re-checked
against the same source rather than trusted.

---

### 🤖 [operant](https://github.com/ishan-parihar/operant)
**Terminal-native ReAct agent runtime.** Rust. Tests: 7,168 passed, 0 failed, 24 ignored across 72 binaries at `ca33d4c` (2026-10-20, `cargo test --workspace`; the suite is active, so treat the figure as that day's gate, not a current count). MCP client + server, skills, messaging channels.

A production-grade agent runtime written in Rust that runs from your shell: a real think → act → observe loop with a JSON-schema tool registry, memory-context injection every turn, provider fallbacks, and self-healing retries.

* **Memory**: `agentmemory` hybrid semantic memory (BM25 + vector + graph), auto-spawned on first use; optional Postgres backend.
* **Tools**: 60+ JSON-schema tools — fs, git, web, CDP browser, shell, code, http, memory, skills, cron, kanban, notes, checkpoints.
* **Channels**: Telegram · Discord · Slack · WhatsApp via the gateway; WASM plugins; `operant autonomous` dev loop.
* **Local-first**: no telemetry, no account; any OpenAI-compatible endpoint or a local llama.cpp / Ollama model.


### 🎬 [openscript](https://github.com/ishan-parihar/openscript)
**Agent-directed video editing pipeline.** Rust + TypeScript. 109 MCP tools, 158 passing with 1 failing (measured `cargo test` at HEAD on a clean export, 2026-10-28).

A full agent-native media pipeline: take a brief, generate a script, synthesize voices, cut a timeline, and render — driven end-to-end through MCP tools rather than a GUI.

* **Pipeline**: brief → script → TTS → vision → FFmpeg → Remotion render, orchestrated as MCP tool calls.
* **Depth**: 12/12 measured sophistication families (state machines, DSLs, protocols, storage, determinism, plugins…) across 5 languages.
* **Surface**: 109 MCP tools — the widest tool surface in the portfolio after operant.


### 🧠 [mysterium](https://github.com/ishan-parihar/mysterium)
**Education-system replacement — holonic developmental matrix.** TS + Python. 61K LOC, 2,110 of 2,112 cases passing (measured `vitest run` at HEAD, 2026-10-28).

A structured cognitive curriculum engine: a 64-cell developmental matrix with a holonic growth model, plus a **9-command agent-first CLI** (`setup`, `status`, `new-game`, `diagnostic`, `curriculum`, `session`, `glossary`, `profile`, `setup-profile`) — an AXI-style surface agents drive directly from the shell.

* **Matrix**: 64-cell developmental grid; curriculum, session, and profile state machines over it.
* **Surface**: `mysterium` bin globally installable; deterministic, non-interactive commands.
* **Skills**: ships structured skill libraries (workspace-lint, ui-ux-pro-max, ui-styling) as reusable agent tooling.

### 💼 [linkedin-lyr](https://github.com/ishan-parihar/linkedin-lyr)
**Professional profile extraction + Voyager profile-edit surface.** Python. 51K LOC, 1,400 tests passing, 32 skipped (measured `pytest` at HEAD, 2026-10-30), 94 releases.

A full LinkedIn integration with a **25-command agent-first CLI** and the most complete AXI ergonomics in the portfolio (6/6 axi.md signals). Every interaction is machine-parseable: TOON structured output, a `--full` escape hatch from content truncation, definitive empty states, size-hinted truncation, pre-computed `total_count` aggregates, and structured exit codes.

* **AXI 6/6**: the only portfolio repo implementing every axi.md principle end-to-end.
* **Surface**: 25 CLI commands; profile fetch, search, and edit flows agents drive deterministically.
* **Track record**: 94 releases — the most shipped tool in the lyr family.


### 📡 [sourcehound](https://github.com/ishan-parihar/sourcehound)
**Intelligence Gathering System — High-performance Rust engine.** ~7MB static binary, ~5MB RSS.

A lightweight news and data ingestion pipeline scraping 411 distinct sources across 47 countries. It filters, deduplicates, and enriches global national, tech, and financial news, generating optimized intelligence feeds for agent consumption.

* **Serialization**: Outputs natively in TOON, saving 40% to 60% in downstream context window costs.
* **Parsers**: 9 custom-engineered stream parsers handling RSS, Atom, HTML tables, OFAC lists, and PDF archives.
* **Efficiency**: Developed to replace a slow, high-memory Node.js prototype, dropping idle RAM consumption to under 5MB.


### 🌐 [switchpost](https://github.com/ishan-parihar/switchpost)
**Multi-platform intelligence gatherer and scheduler across 25 platforms.** Rust. ~78K LOC.

A Rust backend with an axum REST API + rmcp MCP server, JWT auth, SSE realtime, and an in-process scheduler for cross-platform social content operations — Reddit, LinkedIn, Instagram, Telegram, Threads, Facebook, YouTube, Discord, and X/Twitter.

### 🧠 [tdg-rust](https://github.com/ishan-parihar/tdg-rust)
**Teleological Developmental Graph — Pure Rust cognitive engine.** 626 tests (`cargo test`, 626 passed / 0 failed, measured 2026-10-20 at `44e7f9b`; ledger row 40). 50 MCP tools.

A complex implementation of stateful agent memory using a holonic graph structure. Every memory unit is represented as a node: `(Content, Embedding, Telos)`. The teleological decay algorithm ensures stale or irrelevant context decays over time while highly relevant goal nodes remain active.

* **Interface**: 50 custom MCP tools allowing agents to write, link, prune, and query memories using vector search combined with graph traversal.
* **Validation**: 626 tests total — zero warnings, zero regressions, verified against the current suite (626 passed / 0 failed at `44e7f9b`, 2026-10-20; ledger row 40).
* **Canonical**: The Rust port supersedes the original Python reference (now private); `tdg-rust` is the single canonical TDG project.

### 🎵 [scorestrata](https://github.com/ishan-parihar/scorestrata)
**Contract-first music compiler — from plain-language brief to mastered WAV.** Rust. 12 crates, 944 tests (`cargo test`, 944 passed / 0 failed, measured 2026-10-20 at `c5dc71b5`; ledger row 42).

A deterministic composition compiler that turns a human brief into a full-length WAV: event-sourced composition state, a validator gate with genre/register/layer checks, a production-grade layered synth, and a mastering chain. Same brief → byte-identical audio, every run.

* **Pipeline**: Brief → plan → compile → validate → render → master.
* **Audio**: Production-grade layered synth voices (SF2-sampled drums, doubled guitar, organics) with per-layer spectral auditing.
* **Determinism**: Byte-identical replay from contract + seed; the same 944 tests (`c5dc71b5`, 2026-10-20) enforce no-regression rules.

### 📊 [deckmill](https://github.com/ishan-parihar/deckmill)
**The browserless slide factory.** Rust. 38 of 46 slide types renderable (8 are tombstones, verified 2026-10-27), 192 tests (`cargo test`, green at `18036f4`, ledger row 332), ~35K LOC.

High-quality Instagram / LinkedIn / TikTok / X carousels as HTML → PNG via an embedded Blitz renderer — **no Chromium, no browser, no screenshot hacks**. 4.5× less memory than headless-Chrome pipelines, fully static musl binary, WCAG-AA contrast auditing, and an MCP server for AI-driven generation.

### 🧠 [mindstrata](https://github.com/ishan-parihar/mindstrata)
**Deterministic emergent human-society simulation — every agent a complete mind.** Rust. 82K LOC, 307 passing with 3 failing (measured `cargo test` at HEAD, 2026-10-28).

Not just a "society sim": a full cognitive-science stack — bodies, nervous systems, appraisal-based emotion, belief systems, social bonds, institutions, culture, and noospheric fields. Three architecture plans (AP1 → AP2 → AP3) deepen it from a medieval settlement into a multi-scale civilization simulation where history always emerges from locally bounded agents.
