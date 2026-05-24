<div align="center">

# Ishan Parihar

**AI Agent Engineer · MCP Infrastructure · Multi-Agent Orchestration · Systems Architecture**

📧 [support@ishanparihar.com](mailto:support@ishanparihar.com) · 🌐 [ishanparihar.com](https://ishanparihar.com) · 🔗 [LinkedIn](https://www.linkedin.com/in/ishan-parihar-111ba3109/)
📍 Noida, India · ✈️ Remote — worldwide

[![Available for Hire](https://img.shields.io/badge/-AVAILABLE%20FOR%20HIRE-brightgreen?style=for-the-badge&color=2ea44f)](mailto:support@ishanparihar.com)
[![Rust](https://img.shields.io/badge/Rust-ed8b00?style=for-the-badge&logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-555555?style=for-the-badge&logo=github&logoColor=white)](https://modelcontextprotocol.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

*I build the infrastructure that makes AI agents useful in the real world.*  
<!-- PROJECT_COUNT_START -->30<!-- PROJECT_COUNT_END --> projects — 15+ MCP servers, multi-agent orchestration runtimes, and production automation systems.

</div>

---

## What I Do

I architect and ship **production Rust infrastructure for autonomous AI agents** — the servers, runtimes, and orchestration layers that turn LLMs into reliable, auditable systems. My work spans systems programming (Rust, Tokio, Axum, SQLx) to full-stack applications (SvelteKit, Next.js, TypeScript) to multi-agent orchestration with test-driven deployment.

Unlike specialists who work in one layer, I **design across the entire stack** using first-principles systems thinking — taking a problem from concept through architecture to deployed binary, whether it's a ~7MB static Rust MCP server or a multi-agent C-suite with 227 passing tests. I decompose complex requirements into clean, testable, shippable systems.

**What that means for a company:** I can own entire features end-to-end — from database schema to API design to deployment config — without handoffs between specialists. I ship production Rust infrastructure in days, not weeks.

---

## Flagship Projects

### ⚙️ [automaton](https://github.com/ishan-parihar/automaton)
**Graph-native automation substrate for AI agents.** Rust. 39 MCP tools.

Traditional automation tools (shell scripts, CI pipelines, no-code) are designed for humans, not AI agents. Agents can't "see" dependency graphs, can't recover gracefully from partial failures, can't compose capabilities dynamically.

`automaton` replaces the script with a **graph-based module** — every automation unit is a self-contained node with typed inputs/outputs, a content-addressed build cache, and a property graph of capabilities. The engine materializes branching, loops, and parallelism into a DAG, executes with level-based parallel dispatch via Tokio, and exposes the entire lifecycle through MCP.

- 8 Rust crates (core, SDK with proc macro, CLI, engine, registry, graph, MCP, runtime)
- Dual-backend SQLite/PostgreSQL with unified query layer
- Static musl binary (~14MB), zero runtime dependencies
- Production scheduler with cron expressions

### 📡 [igs-rust-mcp](https://github.com/ishan-parihar/igs-rust-mcp)
**Intelligence Gathering System — Rust flagship.** ~7MB static binary, ~5MB RSS.

223+ curated sources across 45 countries, 14 intelligence pools, local NLP enrichment — all in a ~7MB stripped binary with ~5MB idle RSS. TOON (Token-Oriented Object Notation) reduces token consumption by 40–60% for AI agent consumption.

Started as a TypeScript proof-of-concept [published to npm](https://www.npmjs.com/package/igs-mcp-server) — the Rust port is the real flagship: dramatically lower memory/runtime, deployable anywhere including resource-constrained infrastructure.

- 9 custom parsers (RSS, Atom, HTML, OFAC, WHO, Semantic Scholar, PDF, Google News proxy)
- Pool-based source organization (Global Breaking, Geopolitics, Tech/Cyber, India National, etc.)
- Hybrid pipeline: news feeds + academic archives (arXiv, Semantic Scholar) + Reddit
- TOON format for token-efficient AI agent output (~40-60% reduction)

### 🧠 [TDG](https://github.com/ishan-parihar/tdg)
**Teleological Developmental Graph — a recursive, holonic knowledge architecture.** 55 MCP tools. Python (10K+ LOC).

The most ambitious implementation of an agent's "mind" — using a holonic graph to model goals, constraints, and knowledge. 55 custom MCP tools for dynamic knowledge capture, synthesis, and temporal query, enabling agents to maintain a durable, evolving memory of a project's entire evolution.

### 🤖 [operant](https://github.com/ishan-parihar/operant)
**Multi-agent C-suite — 227 tests, LanceDB memory, systemd deployment.**

Coordinates specialized agents (CEO, COO, CFO, CRO, CMO) that run periodic operational checks, communicate with escalation/priorities, track work in Kanban boards, and persist context across sessions. The `operant-mcp` component exposes 35 tools for orchestration, 25+ database tables with Drizzle + Postgres.

### 🔄 [social-forge](https://github.com/ishan-parihar/social-forge)
**Dual-interface social media orchestration engine (REST + MCP).** Rust. Axum. SQLx.

Most social media tools serve one audience: humans via GUI or developers via API. `social-forge` implements a **Shared AppState Architecture** that serves both — a SvelteKit frontend via Axum REST and AI agents via MCP — through the same business logic layer with zero code duplication.

- Trait-based provider registry — add new social networks without touching core engine
- In-process Tokio scheduler with exponential-backoff retry (solves "ghost post" problem)
- SSE event stream for real-time publish/fail notifications
- JWT + Argon2 auth with multi-account cookie profile management
- Static musl binary, ~15MB Docker image

### 🧠 [hermes-rs](https://github.com/ishan-parihar/hermes-rs)
**Streaming-first, fault-tolerant agent orchestration loop.** Rust. Ratatui TUI.

The hardest problem in agentic systems isn't making the LLM smart — it's keeping the loop running when the LLM produces malformed output. Standard parsers crash on unclosed XML tags or broken JSON, taking down the entire agent.

`hermes-rs` implements a custom **state-machine parser** that detects tool calls incrementally. It can recover intent from truncated output, execute tools before the response finishes streaming, and maintain loop integrity even with unstable network connections. The "validated autonomous" mode enforces a strict Plan → Implement → Validate → Push cycle — the agent *cannot* push unless `cargo test` passes.

### 🎬 [openscript](https://github.com/ishan-parihar/openscript)
**AI-directed video editing pipeline — raw footage to polished reel.** 43 MCP tools. Rust + Python + TS. *(Active R&D)*

Most "AI video" tools generate from text. This takes real raw footage and edits it professionally through a structured pipeline: transcription → creative brief → multi-track timeline → rendered 9:16 reel with captions, b-roll, music ducking, and SFX. The AI agent directs like a human editor — choosing b-roll concepts, music mood, SFX placement — and the engine executes.

- 6-track Edit Decision List (EDL v2) — dialogue, voiceover, captions, b-roll, music, SFX
- Apex transcription (Hinglish-optimized Whisper) with word-level timestamps
- TTS voiceover engine with voice profile registry and duration estimation
- 261 indexed SFX + 16 music tracks with mood/role-based search
- FFmpeg rendering with automatic audio ducking
- Post-render verification (audio levels, caption sync, render fidelity)

---

## MCP Ecosystem

| Server | Tools | What It Does |
|--------|-------|------|
| **[gog-cli-mcp](https://github.com/ishan-parihar/gog-cli-mcp)** | 53 | Google Workspace (Calendar, Gmail, Contacts, Drive, Forms, Documents) with per-agent tool scoping |
| **[wacli-mcp](https://github.com/ishan-parihar/wacli-mcp)** | 28 | WhatsApp bridge — session-aware transport, per-agent access control |
| **[instagram-mcp-server](https://pypi.org/project/instagram-scraper-mcp/)** | 28+ | Instagram content scraping — anti-detection, innerText extraction, 3 browser modes |
| **[ishanparihar-com-mcp](https://github.com/ishan-parihar/ishanparihar.com-mcp)** | 60+ | Content, courses, products, newsletter, analytics, orders |
| **[thinking-steroid](https://github.com/ishan-parihar/thinking-steroid)** | 12 | Cognitive modalities — forced reasoning topologies, epistemic status framework |
| **operant-mcp** | 35 | Multi-agent orchestration bridge |
| **[carousel-mcp](https://github.com/ishan-parihar/carousel-mcp)** | — | Carousel generation with OKLCH color system, WCAG-AA |
| **n8n-compiler** | — | n8n workflow → MCP compilation |

I've also built several infrastructure-level MCP servers for internal use — including reverse-engineered integrations for 8 AI providers (Kimi, Qwen, Gemini, GLM, Perplexity, ChatGPT, Claude, DeepSeek) with zero API keys, and multi-model Perplexity access. These are private/prototype work.

---

## Agent Infrastructure

| Project | Tech | What It Does |
|---------|------|------|
| **[icode](https://github.com/ishan-parihar/icode)** | Rust (20 crates, 156K LOC) | Policy-driven agent runtime — hierarchical delegation, MCP lifecycle, SQLite session snapshots, permission engine |
| **[operant](https://github.com/ishan-parihar/operant)** | TypeScript (227 tests) | Multi-agent C-suite — Kanban boards, LanceDB memory, Telegram, systemd |
| **hermes-agent / openclaw** | Python / TypeScript | Upstream agent frameworks (forks) — hermes-rs is the primary Rust implementation |
| **[lifeos-ops](https://github.com/ishan-parihar/lifeos-ops)** | Rust + MCP | CLI & MCP server for the LifeOS personal operating system — goal tracking, habit logging, metrics |
| **[lifeos-saas](https://github.com/ishan-parihar/lifeos-saas)** | Supabase + Agent | SaaS layer for LifeOS — Notion-ingested goal management, autonomous coaching agent |

---

## Full-Stack Websites

| Project | Stack | Scale |
|---------|-------|-------|
| **[design-aesthetics-website](https://github.com/ishan-parihar/design-aesthetics-website)** | Next.js 16, React 19, Three.js, GSAP, OGL shaders | ~86K LOC, 227 files |
| **[ishanparihar-svelte](https://github.com/ishan-parihar/ishanparihar-svelte)** | SvelteKit 5, Razorpay, Redis, Supabase | Production SaaS |
| **[law-of-one-india-website](https://github.com/ishan-parihar/nextjs-site)** | Next.js 15, Auth.js, Supabase, MDX | ~74K LOC, 409 files |
| **[vectura-labs](https://github.com/ishan-parihar/vectura-labs)** | — | Company website with brand psychology design system |
| **[webdev-portfolio](https://github.com/ishan-parihar/webdev-portfolio)** | — | Conversion-focused freelance portfolio |

---

## Published Packages

| Package | Platform | Install | Note |
|---------|----------|---------|------|
| **igs-rust-mcp** ⬆️ | [GitHub](https://github.com/ishan-parihar/igs-rust-mcp) | Rust ~7MB binary | Flagship — Rust port, ~5MB RSS, TOON token optimization |
| **igs-mcp-server** | [npm](https://www.npmjs.com/package/igs-mcp-server) | `npm install igs-mcp-server` | Initial TypeScript proof-of-concept |
| **instagram-scraper-mcp** | [PyPI](https://pypi.org/project/instagram-scraper-mcp/) | `uvx instagram-scraper-mcp` | — |

---

## Open Source & Contributions

| Project | Type | Contribution |
|---------|------|------|
| **[voicebox](https://github.com/jamiepine/voicebox)** | Python | Voice synthesis pipeline — prompt engineering, voice profile management |
| **[Whisper-Hindi2Hinglish](https://github.com/ishan-parihar/Whisper-Hindi2Hinglish)** | Python | Hinglish-optimized Whisper transcription — code-mixing, code-switching handling |
| **[metatrader5_archlinux](https://aur.archlinux.org/packages/metatrader5)** | AUR | MetaTrader 5 for Arch Linux — Wine packaging, install wrapper |

---

## Tech Stack

| Domain | Technologies |
|--------|------|
| **Languages** | Rust, TypeScript, Python, JavaScript, SQL, Zig, MQL5 |
| **Backend** | Axum, FastAPI, Next.js API Routes, Express |
| **Frontend** | Next.js 16, React 19, SvelteKit 5, Tailwind CSS, shadcn/ui, Three.js, GSAP |
| **Database** | PostgreSQL, SQLite, Supabase, Convex, LanceDB, Redis |
| **Protocol** | MCP — 15+ servers, 300+ tools total |
| **AI/ML** | OpenAI, Anthropic, Gemini, local LLMs, Whisper, TTS |
| **Infrastructure** | Docker, systemd, GitHub Actions, n8n |

---

## Portfolio

<!-- PORTFOLIO_START -->
```
MCP-AND-CLIS       15 — Production AI agent infrastructure  
WEBSITES            5 — Full-stack production applications  
FRAMEWORKS          1 — TDG knowledge graph, agent framework patterns  
HERMES              3 — Agent orchestration runtimes  
CONTENT-CREATION    2 — Video editing pipeline, cinematography  
DEVELOPER-TOOLS     2 — AI coding runtimes  
SOCIAL              1 — Multi-platform publishing automation  
N8N-WORKFLOWS       1 — Automation configurations
```
<!-- PORTFOLIO_END -->

---

<div align="center">

[![GitHub Stats](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=ishan-parihar&theme=tokyonight)](https://github.com/ishan-parihar)

[![Visitors](https://api.visitorbadge.io/api/visitors?path=ishan-parihar&label=Profile%20Views&countColor=%232ea44f)](https://github.com/ishan-parihar)

**Available for remote contract and part-time roles worldwide.**  
**[📧 support@ishanparihar.com](mailto:support@ishanparihar.com) — let's talk about what you're building.**

</div>
