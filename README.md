<div align="center">

# Ishan Parihar

**AI Agent Engineer · MCP Infrastructure · Multi-Agent Orchestration · Systems Architecture**

📧 [support@ishanparihar.com](mailto:support@ishanparihar.com) · 🌐 [ishanparihar.com](https://ishanparihar.com) · 🔗 [LinkedIn](https://www.linkedin.com/in/ishan-parihar-111ba3109/)
📍 Noida, India · ✈️ Remote — worldwide

[![Available for Hire](https://img.shields.io/badge/-AVAILABLE%20FOR%20HIRE-brightgreen?style=for-the-badge&color=2ea44f)](mailto:support@ishanparihar.com)
[![Rust](https://img.shields.io/badge/Rust-ed8b00?style=for-the-badge&logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-300%2B%20Tools-555555?style=for-the-badge&logo=github&logoColor=white)](https://modelcontextprotocol.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

*I build the infrastructure that makes AI agents useful in the real world.*  
<!-- PROJECT_COUNT_START -->43<!-- PROJECT_COUNT_END --> projects — 15+ MCP servers, multi-agent orchestration runtimes, and production automation systems.

</div>

---

## 📊 Engineering by the Numbers

| Metric | Value | Detail |
|--------|-------|--------|
| **Active Projects** | **43** | 37 production/active, 6 experimental/archived |
| **MCP Servers** | **15+** | 300+ total tools across intelligence, memory, media, and life-ops |
| **Rust Crates** | **40+** | Across `automaton`, `tdg-rust`, `scorestrata`, `igs-rust`, `slideforge-rust` |
| **Automated Tests** | **3,500+** | `mindstrata` (1,113), `scorestrata` (944), `tdg-rust` (626), `operant` (227) |
| **Data Reduction** | **40–60%** | TOON (Token-Oriented Object Notation) for LLM context optimization |

---

## What I Do

I treat AI infrastructure as **spatial machinery** — not prompt wrappers. Most AI applications today are thin API calls over fragile scripts. I build **load-bearing substrates**:

* **Graph-Native Orchestration**: Replacing linear scripts with Directed Acyclic Graphs (DAGs) that agents can inspect, query, and self-heal at runtime.
* **Token-Efficient Communication**: Custom serialization formats (TOON) that reduce token footprint by 40–60% without losing structural schema validation.
* **Zero-Dependency Runtimes**: Static musl-compiled binaries (~7–14MB) that run anywhere with <10MB idle RSS.
* **Systems Diagnostics**: Translating holonic theory and complex systems modeling into enterprise risk architecture and resilient multi-agent execution.

**What that means for a company:** I own systems end-to-end — from database schema and concurrency engines to custom MCP tool surfaces — without handoffs between specialists. I ship load-bearing systems.

---

## Flagship Projects

### ⚙️ [automaton](https://github.com/ishan-parihar/automaton)
**Graph-native automation substrate for AI agents.** Rust. 38 MCP tools (verified from `automaton-mcp/src/lib.rs`).

Traditional automation tools (shell scripts, CI pipelines, no-code) are designed for humans, not AI agents. Agents can't "see" dependency graphs, can't recover gracefully from partial failures, can't compose capabilities dynamically.

`automaton` replaces the script with a **graph-based module** — every automation unit is a self-contained node with typed inputs/outputs, a content-addressed build cache, and a property graph of capabilities. The engine materializes branching, loops, and parallelism into a DAG, executes with level-based parallel dispatch via Tokio, and exposes the entire lifecycle through MCP.

- **15 Rust crates** (core, SDK with proc macro, CLI, engine, registry, graph, MCP, runtime)
- Dual-backend SQLite/PostgreSQL with unified query layer
- Static musl binary (~14MB), zero runtime dependencies
- Production scheduler with cron expressions and process group isolation

### 📡 [igs-rust-mcp](https://github.com/ishan-parihar/igs-rust-mcp)
**Intelligence Gathering System — Rust flagship.** ~7MB static binary, ~5MB RSS.

411 curated sources across 47 countries, 14 intelligence pools, local NLP enrichment — all in a ~7MB stripped binary with ~5MB idle RSS. TOON (Token-Oriented Object Notation) reduces token consumption by 40–60% for AI agent consumption.

Started as a TypeScript proof-of-concept [published to npm](https://www.npmjs.com/package/igs-mcp-server) — the Rust port is the real flagship: dramatically lower memory/runtime, deployable anywhere including resource-constrained infrastructure.

- **9 custom parsers** (RSS, Atom, HTML, OFAC, WHO, Semantic Scholar, PDF, Google News proxy)
- Pool-based source organization (Global Breaking, Geopolitics, Tech/Cyber, India National, etc.)
- Hybrid pipeline: news feeds + academic archives (arXiv, Semantic Scholar) + Reddit

### 🧠 [TDG](https://github.com/ishan-parihar/tdg-rust)
**Teleological Developmental Graph — pure Rust port.** 626 tests (verified). 36 MCP tools (verified from `src/mcp/mod.rs`).

The most ambitious implementation of an agent's "mind" — using a holonic graph to model goals, constraints, and knowledge. Node = `(Content, Embedding, Telos)`. 55 custom MCP tools for dynamic knowledge capture, synthesis, and temporal query, enabling agents to maintain a durable, evolving memory of a project's entire evolution.

- Self-structuring neural memory with MCP server
- Dual implementations: Python (10K+ LOC) and high-performance Rust port
- Vector search + graph traversal + telos-driven decay

### 🌐 [HoloOS](https://github.com/ishan-parihar/HoloOS) (Private R&D)
**Enterprise systems modeling & risk architecture substrate for Deliberately Developmental Organizations (DDO).** Rust. Python.

A multi-stakeholder systems modeling and risk simulation engine that maps organizational dynamics, resource flows, and structural constraints. Designed as an "enterprise diagnostics" substrate, HoloOS uses holonic theory to model complex systems, simulate structural risk propagation, and optimize resource allocation across adaptive team topologies.

- Multi-dimensional holonic state engine to map structural and process variables
- Monte Carlo simulations to model risk propagation across complex corporate topologies
- Agentic feedback loops that suggest optimal structural and process reconfigurations

### 🤖 [operant](https://github.com/ishan-parihar/operant)
**Multi-agent C-suite — 227 tests, LanceDB memory, systemd deployment.** Rust.

Coordinates specialized agents (CEO, COO, CFO, CRO, CMO) that run periodic operational checks, communicate with escalation/priorities, track work in Kanban boards, and persist context across sessions. The `operant-mcp` component exposes 35 tools for orchestration, 25+ database tables with Drizzle + Postgres.

- Rust multi-agent C-suite with TDG-lite memory and llama.cpp integration
- MCP, REPL, and TUI interfaces for multi-surface operation
- Full-stack TypeScript twin (`c-suite-agents`) with LanceDB + Telegram interface

### 🔄 [social-forge](https://github.com/ishan-parihar/social-forge)
**Multi-platform social media intelligence & posting engine.** Rust + CLI.

Unified Social Media Intel CLI that aggregates inboxes, feeds, and analytics across 6 social platforms (X/Twitter, LinkedIn, Reddit, Instagram, Telegram, WhatsApp) into a single AXI-compliant command surface.

- Automated content scheduling with platform-native format conversion
- Cookie sync across CLI/MCP tools
- Deep analytics aggregation with engagement rate metrics

### 🎬 [openscript](https://github.com/ishan-parihar/openscript)
**AI-directed video editing pipeline — raw footage to 9:16 reel.** Rust + Python + TypeScript.

Transcription → creative brief → multi-track timeline → FFmpeg render → verified output. 109 MCP tools across 9 Rust crates. Handles captions, B-roll selection, music ducking, and SFX insertion from an indexed library of 261 SFX and 16 music tracks.

- Hinglish-optimized Whisper transcription (Apex engine)
- Post-render verification to guarantee video quality before delivery
- Full MCP surface for agent-directed video editing

---

## MCP Ecosystem (300+ Tools Total)

| Server | Stack | Tools | Primary Purpose |
|--------|-------|-------|-----------------|
| **[automaton](https://github.com/ishan-parihar/automaton)** | Rust | 39 | Graph-native automation engine: build, plan, execute, schedule |
| **[igs-rust-mcp](https://github.com/ishan-parihar/igs-rust-mcp)** | Rust | 14 | Multi-source intelligence gathering across 411 global feeds |
| **[tdg-rust](https://github.com/ishan-parihar/tdg-rust)** | Rust | 36 | Teleological developmental graph memory & knowledge synthesis |
| **[c-suite-agents-mcp](https://github.com/ishan-parihar/c-suite-agents-mcp)** | TS/Postgres | 35 | LifeOS MCP: goals, habits, finances, projects, content |
| **[thinking-steroid](https://github.com/ishan-parihar/thinking-steroid)** | TS/Bun | 13 | Epistemic operating system: 13 forced cognitive modalities |
| **[reddit-lyr](https://github.com/ishan-parihar/reddit-lyr)** | Python | 56 | Deep Reddit intelligence: subreddits, threads, user analytics |
| **[instagram-lyr](https://github.com/ishan-parihar/instagram-lyr)** | Python/HTTPX | 24 | Instagram profile recon, post analysis, media extraction |
| **[linkedin-lyr](https://github.com/ishan-parihar/linkedin-lyr)** | Python | 18 | Professional network intelligence & company data extraction |
| **[twitter-lyr](https://github.com/ishan-parihar/twitter-lyr)** | Python | 42 | X/Twitter CLI & MCP: search, post, DM, media, engagement |
| **[andrometry](https://github.com/ishan-parihar/andrometry)** | Kotlin/Go | 12 | Personal context engine: Android collector + Go MCP server |
| **[obscura-core](https://github.com/ishan-parihar/obscura-core)** | Python | 8 | Stealth browser integration: cookie management & CDP daemon |
| **[meme-lyr](https://github.com/ishan-parihar/meme-lyr)** | Python | 6 | AXI-compliant meme generation with aspect ratio optimization |
| **[ishanparihar-cms](https://github.com/ishan-parihar/ishanparihar-cms)** | TS/Postgres | 60+ | Content, products, assessments, newsletter management |

---

## Agent Infrastructure & Systems

| Project | Stack | Description |
|---------|-------|-------------|
| **[mindstrata](https://github.com/ishan-parihar/mindstrata)** | Rust | Deterministic human-society simulation — 1,098 tests, 10 substrates, byte-identical replay |
| **[scorestrata](https://github.com/ishan-parihar/scorestrata)** | Rust | Deterministic music generation compiler — 944 tests, 11 Rust crates, byte-identical WAV output |
| **[slideforge-rust](https://github.com/ishan-parihar/slideforge-rust)** | Rust | Programmatic social media carousel generator with HTML/CSS templates |
| **[lifeos-ops](https://github.com/ishan-parihar/lifeos-ops)** | Rust | Consciousness-prosthetic CLI + MCP on Notion — 29 tools, 5 DBs, 3 functional layers |
| **[lifeos-saas](https://github.com/ishan-parihar/lifeos-saas)** | TS/Docker | Production-grade AI agent stack (NullClaw + LifeOS-mcp + Honcho) |
| **[toon-helper](https://github.com/ishan-parihar/toon-helper)** | Rust | TOON (Token-Oriented Object Notation) encoding library for AXI-compliant CLIs |
| **[toon-helper-ts](https://github.com/ishan-parihar/toon-helper-ts)** | TS | TypeScript twin of the TOON encoding library (~40% token savings) |

---

## Full-Stack Websites

| Site | Tech Stack | Highlights |
|------|------------|------------|
| **[design-aesthetics-website](https://github.com/ishan-parihar/design-aesthetics-website)** | Next.js 16 / SvelteKit | Architectural firm showcase — 49K LOC, GSAP, Three.js, WebGL shaders |
| **[ishanparihar-svelte](https://github.com/ishan-parihar/ishanparihar-svelte)** | SvelteKit 5 / Supabase | Production portfolio & platform — Razorpay integration, MDX blog |
| **[law-of-one-india-website](https://github.com/ishan-parihar/law-of-one-india-website)** | Next.js 15 / Supabase | Regional community publishing platform with role-based auth & MDX CMS |
| **[lifeos-website](https://github.com/ishan-parihar/lifeos-website)** | Next.js 15 / Tailwind | Landing page & documentation hub for the LifeOS platform |
| **[webdev-portfolio](https://github.com/ishan-parihar/webdev-portfolio)** | Next.js 15 / TS | Conversion-focused freelance web development portfolio |

---

## Published Packages

| Package | Platform | Install | Note |
|---------|----------|---------|------|
| **igs-rust-mcp** ⬆️ | [GitHub](https://github.com/ishan-parihar/igs-rust-mcp) | Rust ~7MB binary | Flagship — Rust port, ~5MB RSS, TOON token optimization |
| **igs-mcp-server** | [npm](https://www.npmjs.com/package/igs-mcp-server) | `npm install igs-mcp-server` | Initial TypeScript proof-of-concept |
| **instagram-scraper-mcp** | [Test PyPI](https://test.pypi.org/project/instagram-scraper-mcp/) | `uvx --index-url https://test.pypi.org/simple/ instagram-scraper-mcp` | Python HTTPX-based scraper |

---

## Open Source & Contributions

| Project | Type | Contribution |
|---------|------|--------------|
| **[voicebox](https://github.com/jamiepine/voicebox)** | Python | Voice synthesis pipeline — prompt engineering, voice profile management |
| **[Whisper-Hindi2Hinglish](https://github.com/ishan-parihar/Whisper-Hindi2Hinglish)** | Python | Hinglish-optimized Whisper transcription — code-mixing, code-switching handling |
| **[metatrader5_archlinux](https://aur.archlinux.org/packages/metatrader5)** | AUR | MetaTrader 5 for Arch Linux — Wine packaging, install wrapper |

---

## Tech Stack

| Domain | Technologies |
|--------|--------------|
| **Languages** | Rust, TypeScript, Python, Kotlin, Go, JavaScript, SQL, Zig, MQL5 |
| **Backend** | Axum, Tokio, FastAPI, Next.js API Routes, Express, Bun |
| **Frontend** | Next.js 16, React 19, SvelteKit 5, Tailwind CSS, shadcn/ui, Three.js, GSAP |
| **Database** | PostgreSQL, SQLite, Supabase, Convex, LanceDB, Drizzle ORM, Redis |
| **Protocol Standards** | MCP (300+ tools), AXI (Agent eXperience Interface), TOON |
| **AI / ML** | OpenAI, Anthropic, Gemini, local LLMs, Whisper, TTS, Qwen |
| **Infrastructure** | Docker, systemd, GitHub Actions, Cloudflare Tunnel, n8n |

---

## Complete Project Catalog (43 Projects)

```
S-TIER 6 — Flagship infrastructure
  automaton           Graph-native automation substrate — 15 Rust crates, 38 MCP tools
  igs-rust-mcp        Intelligence Gathering System — ~7MB static Rust binary, 411 sources
  tdg-rust            Teleological Developmental Graph — 626 tests, 36 MCP tools
  HoloOS              Enterprise risk architecture & systems simulation (Private R&D)
  operant             Multi-agent C-suite — 227 tests, LanceDB memory, systemd
  social-forge        Multi-platform social media intel CLI across 6 platforms

A-TIER 5 — Production agent tooling
  mindstrata          Deterministic human-society simulation — 1,098 tests, 10 substrates
  scorestrata         Deterministic music generation compiler — 944 tests, 11 Rust crates
  openscript          AI-directed video editing pipeline — 109 MCP tools, 9 Rust crates
  andrometry          Personal context engine — Kotlin Android collector + Go MCP
  mysterium           Contemplative-assessment RPG — 64-cell matrix, 1,280 items

B-TIER 8 — Agent infrastructure & data
  lifeos-ops          LifeOS CLI + MCP on Notion — 29 tools, 5 DBs, 3 layers
  linkedin-lyr        LinkedIn MCP + CLI — professional network intelligence
  instagram-lyr       Instagram HTTPX MCP — profile recon & media extraction
  twitter-lyr         Twitter/X CLI for AI agents — 42 commands
  reddit-lyr          Reddit MCP — 56 tools for subreddits, threads, analytics
  c-suite-agents-mcp  LifeOS MCP — 35 tools on PostgreSQL + Drizzle
  thinking-steroid    Epistemic operating system — 13 forced cognitive modalities
  obscura-core        Stealth browser cookie/daemon library & CDP pool

C-TIER 8 — CLI/automation suite
  discord-cli         Local-first Discord data CLI
  tg-cli              Telethon Telegram CLI
  facebook-lyr        Facebook automation CLI
  threads-lyr         Threads read-only MCP
  meme-lyr            AXI-compliant meme CLI with aspect ratio support
  lifeos-saas         LifeOS agent stack powered by NullClaw
  ishanparihar-cms    ishanparihar.com MCP — 60+ tools for content/courses
  slideforge-rust     Programmatic social media carousel generator in Rust

D-TIER 6 — Websites & web apps
  design-aesthetics-website  49K LOC GSAP/Three.js showcase
  ishanparihar-svelte         Production portfolio & platform (SvelteKit 5)
  law-of-one-india-website    Regional community publishing platform
  lifeos-website              LifeOS landing page & docs
  webdev-portfolio           Conversion-focused freelance portfolio
  c-suite-agents              Operant orchestration (multi-agent TS twin)

E-TIER 5 — Experimental / utility
  consciousness-fabricator    AI meditation audio generator
  holosim-infinite            Holographic universe simulation engine
  kali-mahabali               Project Chimera — modular intelligence framework
  social-media-platform       Social media platform (WIP/Planning)
  toon-helper / toon-helper-ts TOON encoding libraries (Rust + TypeScript)
```
<!-- PORTFOLIO_END -->

---

<div align="center">

[![GitHub Stats](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=ishan-parihar&theme=tokyonight)](https://github.com/ishan-parihar)

[![Visitors](https://api.visitorbadge.io/api/visitors?path=ishan-parihar&label=Profile%20Views&countColor=%232ea44f)](https://github.com/ishan-parihar)

**Available for remote contract, full-time, and part-time roles worldwide.**  
**[📧 support@ishanparihar.com](mailto:support@ishanparihar.com) — let's talk about what you're building.**

</div>
