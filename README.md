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
47 projects across MCP ecosystems, agent runtimes, and systems engineering — all in Rust, TypeScript, and Python.

</div>

---

## What I Do

I am an **AI Tradesman** — not a researcher, not a consultant, but a craftsman who builds the production infrastructure that AI agents operate through. My work sits at the intersection of **systems programming (Rust)** and **agentic AI**: MCP servers that give agents real-world capabilities, runtimes that keep them reliable, and pipelines that turn raw capability into finished output.

Everything I build is **shippable** — published to npm/PyPI, compiled to static binaries, deployable via systemd or Docker. No Jupyter notebooks. No throwaway scripts.

---

## Flagship Projects

These are the projects that best define my engineering identity — solving hard infrastructure problems for AI agents.

### ⚙️ [automaton](https://github.com/ishan-parihar/automaton)
**Graph-native automation substrate for AI agents.** Rust. 39 MCP tools.

The fundamental insight: traditional automation tools (shell scripts, CI pipelines, no-code) are designed for humans, not AI agents. Agents can't "see" dependency graphs, can't recover gracefully from partial failures, can't compose capabilities dynamically.

`automaton` replaces the script with a **graph-based module** — every automation unit is a self-contained node with typed inputs/outputs, a content-addressed build cache, and a property graph of capabilities. The engine materializes branching, loops, and parallelism into a DAG, executes with level-based parallel dispatch via Tokio, and exposes the entire lifecycle through MCP.

- 8 Rust crates (core, SDK with proc macro, CLI, engine, registry, graph, MCP, runtime)
- Dual-backend SQLite/PostgreSQL with unified query layer
- Static musl binary (~14MB), zero runtime dependencies
- Production scheduler with cron expressions
- Process group isolation — no orphan shells on crash

### 🧠 [ai-mcp-server](https://github.com/ishan-parihar/ai-mcp-server)
**Unified AI gateway — 8 providers, zero API keys, real SSE streaming.** Rust. 8.2MB static binary.

The problem: every AI provider has a different auth scheme, different API format, different streaming protocol. Managing API keys for all of them is friction. This server reverse-engineers each provider's session auth and exposes them through a single OpenAI-compatible API — no keys required, just your browser cookies.

The engineering depth is in the provider-specific SSE parsers: Kimi uses JWT-based streaming with `event: cmpl` frames, Perplexity uses custom `blocks[]` → `chunks[]` deduplication, GLM needs xpath-based JSON extraction from nested responses, Gemini requires a Playwright Firefox proxy because its entire API flows through JS-executed protobuf calls. Each has a custom `AiProvider` trait implementation with native byte-stream parsing.

- 46 models across 7/8 working providers (Kimi, Qwen, Gemini, GLM, Perplexity, ChatGPT, Claude — DeepSeek needs re-login)
- OpenAI-compatible `/v1/chat/completions` and `/v1/models` endpoints
- Playwright Firefox sidecar for JS-dependent providers
- Cookie auto-import from Zen/Firefox/Chrome SQLite stores
- Docker compose with read-only cookie mount, non-root user, health checks

### ⚡ [hermes-rs](https://github.com/ishan-parihar/hermes-rs)
**Streaming-first, fault-tolerant agent orchestration loop.** Rust. Ratatui TUI.

The hardest problem in agentic systems isn't making the LLM smart — it's keeping the loop running when the LLM produces malformed output. Standard parsers crash on unclosed XML tags or broken JSON, taking down the entire agent.

`hermes-rs` implements a custom **state-machine parser** that detects tool calls incrementally. It can recover intent from truncated output, execute tools before the response finishes streaming, and maintain loop integrity even with unstable network connections. The "validated autonomous" mode enforces a strict Plan → Implement → Validate → Push cycle — the agent *cannot* push unless `cargo test` passes.

- Streaming-tolerant parsing for malformed LLM output
- Autonomous development mode with hard test gate
- Dynamic ToolRegistry with MCP compatibility
- LTO-optimized, stripped binary

### 🎬 [openscript](https://github.com/ishan-parihar/openscript)
**AI-directed video editing pipeline — raw footage to polished reel.** 43 MCP tools. Rust + Python + TS.

Most "AI video" tools generate from text. This takes real raw footage and edits it professionally: transcription → creative brief → multi-track timeline → rendered 9:16 reel with captions, b-roll, music ducking, and SFX.

The pipeline runs as 43 MCP tools across 6 independent tracks (dialogue, voiceover, captions, b-roll, music, SFX). The AI agent directs like a human editor — choosing which b-roll concepts to use, which music mood fits, where to place sound effects — and the engine executes the technical work.

- 6-track Edit Decision List (EDL v2) with full validation
- Apex transcription (Hinglish-optimized Whisper) with word-level timestamps
- `faster-qwen3-tts` voiceover engine with voice profile registry
- 261 indexed SFX + 16 music tracks with mood/role-based search
- Pexels API b-roll with director-mode concept extraction
- FFmpeg rendering with automatic audio ducking
- Post-render verification layer (audio levels, caption sync, render fidelity)
- 8 Rust crates + Python orchestration + Remotion TypeScript compositions

### 📡 [igs-mcp](https://github.com/ishan-parihar/igs-mcp) — [npm](https://www.npmjs.com/package/igs-mcp-server)
**Intelligence Gathering System — 223+ sources across 45 countries.** TypeScript. Published npm.

An MCP server that treats the global news web as a single queryable database. Monitors 223+ curated RSS/Atom/HTML feeds across 14 pre-configured intelligence pools (Global Breaking, Geopolitics, Tech/Cyber, India National, India Investigative, etc.) with local NLP enrichment for entity extraction and sentiment analysis.

The hybrid research pipeline integrates news feeds with academic archives (arXiv, Semantic Scholar) and community discourse (Reddit), enabling "triangulation" workflows — identify a breaking trend in news, verify via Semantic Scholar paper, gauge sentiment via Reddit — all in one agent reasoning loop.

- 9 custom parsers (RSS, Atom, HTML, OFAC, WHO, Semantic Scholar, PDF, Google News proxy)
- Pool-based source organization for rapid intelligence pivoting
- ~90% cache hit ratio, ~2s cold start, 50-150MB memory

---

## MCP Ecosystem (15+ Servers)

I've built what may be the largest independent MCP server ecosystem — infrastructure that gives AI agents structured access to real-world systems.

| Server | Tools | What It Does |
|--------|-------|------|
| **[gog-cli-mcp](https://github.com/ishan-parihar/gog-cli-mcp)** | 53 | Google Workspace (Calendar, Gmail, Contacts, Drive, Forms, Documents) with per-agent tool scoping |
| **[wacli-mcp](https://github.com/ishan-parihar/wacli-mcp)** | 28 | WhatsApp messaging, groups, contacts, media — session-aware transport, per-agent access control |
| **[instagram-mcp-server](https://github.com/stickerdaniel/instagram-mcp-server)** → [PyPI](https://pypi.org/project/instagram-scraper-mcp/) | 28+ | Instagram profile, content, messaging, insights — three-mode browser architecture, innerText extraction, zero CSS dependency |
| **[postiz-rust](https://github.com/ishan-parihar/postiz-rust)** | 15+ | Social media scheduling engine — dual-interface (REST + MCP), trait-based providers, SSE event stream |
| **[ishanparihar-com-mcp](https://github.com/ishan-parihar/ishanparihar.com-mcp)** | 60+ | Full website backend — content, products, courses, assessments, newsletter, analytics, orders |
| **[thinking-steroid](https://github.com/ishan-parihar/thinking-steroid)** | 12 | Cognitive modality library — forced reasoning topologies, DAG-based orchestration, epistemic status framework |
| **[operant-mcp](https://github.com/ishan-parihar/operant)** | 35 | Multi-agent orchestration — 25+ DB tables, Drizzle + PostgreSQL, MCP bridge |
| **[carousel-mcp](https://github.com/ishan-parihar/carousel-mcp)** | — | Carousel content generation with OKLCH color system, WCAG-AA compliance |
| **[perplexity-mcp-server](https://github.com/ishan-parihar/perplexity-mcp-server)** | — | 15 Perplexity models, browser-cookie auth |
| **n8n-compiler** | — | n8n workflow compilation to MCP tools |

---

## Agent Infrastructure

| Project | Tech | What It Does |
|---------|------|------|
| **[icode](https://github.com/ishan-parihar/icode)** | Rust (20 crates, 156K LOC) | Hardened runtime for AI coding agents — policy-driven permission engine, hierarchical agent delegation, SQLite-backed session management with atomic snapshots, tool parity harness |
| **[operant](https://github.com/ishan-parihar/operant)** | TypeScript (227 tests) | Multi-agent C-suite — CEO, COO, CFO, CRO, CMO, CPO agents with Kanban boards, LanceDB memory, Telegram interface, systemd deployment |
| **[lifeos-ops](https://github.com/ishan-parihar/lifeos-ops)** | Rust (CLI + MCP) | Notion-based personal operating system — bidirectional sync with 3-way merge, role-based intelligence briefing, strategic simulator |

---

## LifeOS Ecosystem

A personal sovereignty system spanning 5+ integrated projects:

| Project | Tech | Purpose |
|---------|------|---------|
| **lifeos-ops** | Rust CLI + MCP | Notion sync, data science, strategic simulation |
| **lifeos-saas** | Zig + TypeScript + Python | 6-container Docker SaaS, NullClaw + Honcho |
| **lifeos-website** | SvelteKit + Rust + Convex | Production multi-tenant website |
| **operant** | TypeScript | Multi-agent C-suite with memory + Telegram |
| **sovereign** | Python (7 domains) | Event-driven domain architecture — Nexus pub/sub, cron scheduler, Telegram/Notion gateways |
| **workout-factory** | Python (9.4K LOC) | Offline TTS AI fitness trainer — progressive overload, 4-tier audio caching (<0.1s) |

---

## Full-Stack Websites

| Project | Stack | Scale |
|---------|-------|-------|
| **[design-aesthetics-website](https://github.com/ishan-parihar/design-aesthetics-website)** | Next.js 16, React 19, Three.js, GSAP, OGL shaders | ~86K LOC, 227 files |
| **[ishanparihar-svelte](https://github.com/ishan-parihar/ishanparihar-svelte)** | SvelteKit 5, Razorpay, Redis, Supabase | Production SaaS |
| **[nextjs-site](https://github.com/ishan-parihar/nextjs-site)** | Next.js 15, Auth.js, Supabase, MDX | ~74K LOC, 409 files, content platform |
| **[vectura-labs](https://github.com/ishan-parihar/vectura-labs)** | — | Company website with brand psychology design system |
| **[webdev-portfolio](https://github.com/ishan-parihar/webdev-portfolio)** | — | Conversion-focused freelance portfolio |

---

## Experiments & Explorations

| Project | Scale | What It Is |
|---------|-------|------|
| **[holosim-infinite](https://github.com/ishan-parihar/holosim-infinite)** | 650+ Rust files | Cosmic simulation engine — MERA tensor compression ($O(n^{2/3})$ memory), 22-archetype consciousness system, fractal multi-scale (9 levels, 61 orders of magnitude) |
| **[osint-os/scrapecraft](https://github.com/ishan-parihar/OSINT-OS)** | 23+ AI agents | Intelligence agency-grade OSINT platform — zero-trust architecture, WebSocket real-time collaboration, 100+ REST endpoints |
| **[social-media-platform](https://github.com/ishan-parihar/social-media-platform)** | Planning | Rust-first decentralized social — DID/WebAuthn, ActivityPub/AT Protocol, portable identity layer, anti-blockchain stance |
| **[cinesync](https://github.com/ishan-parihar/CineSync)** | 1.7K LOC | Emotion-aware ML cinematography — 8-emotion model for shot selection |
| **[consciousness-fabricator](https://github.com/ishan-parihar/consciousness-fabricator)** | — | Voice clone + binaural TTS system |

---

## Published Packages

| Package | Platform | Install |
|---------|----------|---------|
| **igs-mcp-server** | [npm](https://www.npmjs.com/package/igs-mcp-server) | `npm install igs-mcp-server` |
| **instagram-scraper-mcp** | [PyPI](https://pypi.org/project/instagram-scraper-mcp/) | `uvx instagram-scraper-mcp` |

---

## Tech Stack

| Domain | Technologies |
|--------|------|
| **Languages** | Rust, TypeScript, Python, JavaScript, SQL, Zig, MQL5 |
| **Backend** | Axum, FastAPI, Next.js API Routes, Express, Deno |
| **Frontend** | Next.js 16, React 19, SvelteKit 5, Tailwind CSS, shadcn/ui, Three.js, GSAP |
| **Database** | PostgreSQL, SQLite, Supabase, Convex, LanceDB, Redis |
| **Protocol** | MCP (Model Context Protocol) — 15+ servers, 300+ total tools |
| **AI/ML** | OpenAI API, Anthropic API, Gemini, local LLMs (Ollama), Whisper, TTS |
| **Infrastructure** | Docker, systemd, GitHub Actions, n8n, Docker Compose |

---

## Portfolio Summary

```
47 projects across 9 categories:

MCP-AND-CLIS      15 — AI agent infrastructure, real-world tool access
EXPERIMENTAL       7 — Cosmic simulation, OSINT, decentralized social, TTS
LIFEOS             5 — Personal sovereignty operating system
WEBSITES           5 — Production full-stack applications
HERMES             4 — Agent orchestration runtimes
CONTENT-CREATION   2 — Video editing pipeline, cinematography
DEVELOPER-TOOLS    2 — AI coding runtimes
N8N-WORKFLOWS      1 — Automation configurations
SOCIAL-MEDIA       1 — Decentralized social platform
```

---

<div align="center">

[![GitHub Stats](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=ishan-parihar&theme=tokyonight)](https://github.com/ishan-parihar)

[![Visitors](https://api.visitorbadge.io/api/visitors?path=ishan-parihar&label=Profile%20Views&countColor=%232ea44f)](https://github.com/ishan-parihar)

**AI Tradesman · Building the infrastructure for autonomous systems**  
*Rust + MCP + Agent Orchestration*

</div>
