<div align="center">

# Ishan Parihar

**AI Tradesman · Rust + Agent Infrastructure · Multi-Agent Orchestration**

📧 [support@ishanparihar.com](mailto:support@ishanparihar.com) · 🌐 [ishanparihar.com](https://ishanparihar.com) · 🔗 [LinkedIn](https://www.linkedin.com/in/ishan-parihar-111ba3109/)
📍 Noida, India · ✈️ Open to remote

[![Available for Work](https://img.shields.io/badge/-AVAILABLE%20FOR%20WORK-brightgreen?style=for-the-badge&color=2ea44f)](https://github.com/ishan-parihar)
[![Rust](https://img.shields.io/badge/Rust-ed8b00?style=for-the-badge&logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-555555?style=for-the-badge&logo=github&logoColor=white)](https://modelcontextprotocol.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

*I build the infrastructure that makes AI agents useful in the real world.*  
47 projects across MCP ecosystems, agent runtimes, and systems engineering.

</div>

---

## What I Do

I am an **AI Tradesman** — not a researcher, not a consultant, but a craftsman who builds the production infrastructure that AI agents operate through. My work sits at the intersection of **systems programming (Rust)** and **agentic AI**: MCP servers that give agents real-world capabilities, runtimes that keep them reliable, and pipelines that turn raw capability into finished output.

Everything I build is **shippable** — published to npm/PyPI, compiled to static binaries, deployable via systemd or Docker.

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

### 🔄 [social-forge](https://github.com/ishan-parihar/postiz-rust)
**Dual-interface social media orchestration engine (REST + MCP).** Rust. Axum. SQLx.

Most social media tools serve one audience: humans via GUI or developers via API. `social-forge` (née postiz-rust) implements a **Shared AppState Architecture** that serves both — a SvelteKit frontend via Axum REST and AI agents via MCP — through the same business logic layer with zero code duplication.

- Trait-based provider registry — add new social networks without touching core engine
- In-process Tokio scheduler with exponential-backoff retry (solves "ghost post" problem)
- SSE event stream for real-time publish/fail notifications
- JWT + Argon2 auth with multi-account cookie profile management
- Static musl binary, ~15MB Docker image

### 🧠 [hermes-rs](https://github.com/ishan-parihar/hermes-rs)
**Streaming-first, fault-tolerant agent orchestration loop.** Rust. Ratatui TUI.

The hardest problem in agentic systems isn't making the LLM smart — it's keeping the loop running when the LLM produces malformed output. Standard parsers crash on unclosed XML tags or broken JSON, taking down the entire agent.

`hermes-rs` implements a custom **state-machine parser** that detects tool calls incrementally. It can recover intent from truncated output, execute tools before the response finishes streaming, and maintain loop integrity even with unstable network connections. The "validated autonomous" mode enforces a strict Plan → Implement → Validate → Push cycle — the agent *cannot* push unless `cargo test` passes.

### 📡 [igs-mcp](https://www.npmjs.com/package/igs-mcp-server) (npm) → Rust Port
**Intelligence Gathering System — 223+ sources across 45 countries.**

Started as a TypeScript MCP server published to npm. The Rust port (`igs-rust-mcp`) is the real flagship — it dramatically reduces memory footprint and eliminates Node.js runtime dependency, enabling deployment on resource-constrained infrastructure. Same 223+ curated sources, 14 intelligence pools, local NLP enrichment — but now a ~8MB static binary instead of a 100MB+ Node process.

- 9 custom parsers (RSS, Atom, HTML, OFAC, WHO, Semantic Scholar, PDF, Google News proxy)
- Pool-based source organization (Global Breaking, Geopolitics, Tech/Cyber, India National, etc.)
- Hybrid pipeline: news feeds + academic archives (arXiv, Semantic Scholar) + Reddit
- ~90% cache hit ratio, ~2s cold start

### 🎬 [openscript](https://github.com/ishan-parihar/openscript)
**AI-directed video editing pipeline — raw footage to polished reel.** 43 MCP tools. Rust + Python + TS.

Most "AI video" tools generate from text. This takes real raw footage and edits it professionally through a structured pipeline: transcription → creative brief → multi-track timeline → rendered 9:16 reel with captions, b-roll, music ducking, and SFX. The AI agent directs like a human editor — choosing b-roll concepts, music mood, SFX placement — and the engine executes.

- 6-track Edit Decision List (EDL v2) — dialogue, voiceover, captions, b-roll, music, SFX
- Apex transcription (Hinglish-optimized Whisper) with word-level timestamps
- TTS voiceover engine with voice profile registry and duration estimation
- 261 indexed SFX + 16 music tracks with mood/role-based search
- FFmpeg rendering with automatic audio ducking
- Post-render verification (audio levels, caption sync, render fidelity)

### 🤖 [operant](https://github.com/ishan-parihar/operant)
**Multi-agent C-suite — 227 tests, LanceDB memory, systemd deployment.**

Coordinates specialized agents (CEO, COO, CFO, CRO, CMO) that run periodic operational checks, communicate with escalation/priorities, track work in Kanban boards, and persist context across sessions. The `operant-mcp` component exposes 35 tools for orchestration, 25+ database tables with Drizzle + Postgres.

Experimental. Needs funding to continue development. The multi-agent coordination patterns here are genuinely novel — role-based autonomy with shared memory, not just prompt-chaining.

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

## LifeOS — Personal Sovereignty Infrastructure

The LifeOS ecosystem is my most ambitious product concept: a personal operating system that coordinates health, executive function, finances, psychology, relationships, strategy, and time through a unified event-driven core.

**The vision**: Package LifeOS with IGS (intelligence), social-forge (social distribution), and operant (autonomous staffing) into a SaaS platform for **personal sovereignty** — the infrastructure layer for an AI-managed life. Each component works independently but compounds when integrated.

| Component | Status | Role |
|-----------|--------|------|
| **lifeos-ops** | Rust CLI + MCP | Notion-based personal OS with 3-way merge sync, role-based intelligence briefing, strategic simulator |
| **lifeos-saas** | Zig + TS + Python | Multi-tenant SaaS backend, 6-container Docker stack |
| **lifeos-website** | SvelteKit + Rust + Convex | Production website with user management |
| **sovereign** | Python (7 domains) | Event-driven domain architecture — Nexus pub/sub, Telegram/Notion gateways |
| **workout-factory** | Python (9.4K LOC) | Offline TTS fitness trainer — adaptive progressive overload, 4-tier audio caching |

These projects are private — source isn't public. I'm building them as a product, not a portfolio piece. Happy to walk through the architecture and vision in conversation.

---

## Agent Infrastructure

| Project | Tech | What It Does |
|---------|------|------|
| **[icode](https://github.com/ishan-parihar/icode)** | Rust (20 crates, 156K LOC) | Policy-driven agent runtime — hierarchical delegation, MCP lifecycle, SQLite session snapshots, permission engine |
| **[operant](https://github.com/ishan-parihar/operant)** | TypeScript (227 tests) | Multi-agent C-suite — Kanban boards, LanceDB memory, Telegram, systemd |
| **hermes-agent / openclaw** | Python / TypeScript | Upstream agent frameworks (forks) — hermes-rs is the primary Rust implementation |

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

## Experiments & Explorations

| Project | Scale | What It Is |
|---------|-------|------|
| **[holosim-infinite](https://github.com/ishan-parihar/holosim-infinite)** | 650+ Rust files | Cosmic simulation — MERA tensor compression, 22-archetype consciousness, fractal multi-scale |
| **[osint-os](https://github.com/ishan-parihar/OSINT-OS)** | — | Intelligence investigation platform — multi-agent framework, zero-trust architecture |
| **[social-forge](https://github.com/ishan-parihar/social-media-platform)** | Planning | Decentralized social platform — ActivityPub/AT Protocol, portable identity, anti-blockchain |
| **[cinesync](https://github.com/ishan-parihar/CineSync)** | 1.7K LOC | Emotion-aware ML cinematography — 8-emotion shot selection |
| **[consciousness-fabricator](https://github.com/ishan-parihar/consciousness-fabricator)** | — | Voice clone + binaural TTS |
| **[MT5-mcp](https://github.com/ishan-parihar/MT5-mcp)** | — | MetaTrader 5 trading MCP — market regime detection, position sizing |

---

## Published Packages

| Package | Platform | Install | Note |
|---------|----------|---------|------|
| **igs-mcp-server** | [npm](https://www.npmjs.com/package/igs-mcp-server) | `npm install igs-mcp-server` | TypeScript version — Rust port in development |
| **instagram-scraper-mcp** | [PyPI](https://pypi.org/project/instagram-scraper-mcp/) | `uvx instagram-scraper-mcp` | — |

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

```
MCP-AND-CLIS      15 — AI agent infrastructure, real-world tool access
EXPERIMENTAL       7 — Cosmic simulation, OSINT, decentralized social
LIFEOS             5 — Personal sovereignty operating system (private)
WEBSITES           5 — Production full-stack applications
HERMES             4 — Agent orchestration runtimes
CONTENT-CREATION   2 — Video editing pipeline, cinematography
DEVELOPER-TOOLS    2 — AI coding runtimes
SOCIAL             2 — Social-forge, decentralized social
N8N-WORKFLOWS      1 — Automation configurations
```

---

<div align="center">

[![GitHub Stats](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=ishan-parihar&theme=tokyonight)](https://github.com/ishan-parihar)

[![Visitors](https://api.visitorbadge.io/api/visitors?path=ishan-parihar&label=Profile%20Views&countColor=%232ea44f)](https://github.com/ishan-parihar)

**AI Tradesman · Building the infrastructure for autonomous systems**

</div>
