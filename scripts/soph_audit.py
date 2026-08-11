#!/usr/bin/env python3
"""Sophistication audit — measures advanced-engineering families per repo.

v7 philosophy: the ranking must measure what the CODE is (architecture,
technical sophistication), not how often its author poked it (velocity,
releases — removed in v7). This tool provides the `soph` component (0-12)
of the Architecture & Sophistication criterion in scripts/rank_score.py.

Method (discriminating, anti-gaming):
  - scans ONLY real code files (no .toml/.json/.yaml/.md config noise)
  - excludes vendored/third-party/test/example dirs (first-party rule)
  - each family is COUNT-gated: it only counts once its signal appears
    >= min_hits times in the repo's own code, so a stray word never fires
  - each family is binary per repo (present/absent) to avoid LOC-bias

Families (12):
  1. state_machines   event sourcing, FSM, snapshots, transitions
  2. graphs           holonic, adjacency, DAG, BFS/DFS, node/edge types
  3. dsl_parsers      lexers, grammars, interpreters, bytecode, ASTs
  4. concurrency      tokio/rayon/threads/channels/async
  5. protocols        MCP, HTTP frameworks, WebSocket, gRPC, GraphQL
  6. storage          DBs, WAL, storage engines, maps/caches
  7. ai_ml            embeddings, similarity, retrieval, inference, LLM
  8. render_audio     shaders, GPU, synth, WAV, FFT, renderers
  9. determinism      seeded RNG, fixed-point, reproducibility
  10. distributed     consensus, sharding, rate limits, queues, pools
  11. security        crypto, signing, auth, sandboxing, JWT
  12. plugins         dyn Trait, registries, adapters, skills, dispatchers

Usage:  python3 scripts/soph_audit.py            # full table
        python3 scripts/soph_audit.py <name>...  # one or more repos
Fold the `soph` values into rank_score.py DATA, then re-rank.
"""
import os
import re
import subprocess
import sys

PORTS = "/home/ishanp/Documents/GitHub/MY-PROJECTS"

REPOS = {
    "igs-rust": "MCP-AND-CLIS/igs-rust", "social-forge": "MCP-AND-CLIS/social-forge",
    "operant": "HERMES/operant", "scorestrata": "scorestrata", "mindstrata": "mindstrata",
    "tdg-rust": "tdg-rust", "slideforge-rust": "MCP-AND-CLIS/slideforge-rust",
    "automaton": "MCP-AND-CLIS/automaton", "openscript": "CONTENT-CREATION/openscript",
    "mysterium": "mysterium", "andrometry": "andrometry", "lifeos-ops": "LIFEOS/lifeos-ops",
    "c-suite-agents": "LIFEOS/c-suite-agents", "thinking-steroid": "MCP-AND-CLIS/thinking-steroid",
    "reddit-lyr": "MCP-AND-CLIS/reddit-lyr", "twitter-lyr": "MCP-AND-CLIS/twitter-lyr",
    "instagram-lyr": "MCP-AND-CLIS/instagram-lyr", "linkedin-lyr": "MCP-AND-CLIS/linkedin-lyr",
    "facebook-lyr": "MCP-AND-CLIS/facebook-lyr", "threads-lyr": "MCP-AND-CLIS/threads-lyr",
    "discord-cli": "MCP-AND-CLIS/discord-cli", "tg-cli": "MCP-AND-CLIS/tg-cli",
    "meme-lyr": "MCP-AND-CLIS/meme-lyr", "obscura-core": "MCP-AND-CLIS/obscura-core",
    "consciousness-fabricator": "EXPERIMENTAL/consciousness-fabricator",
    "holosim-infinite": "EXPERIMENTAL/holosim-infinite", "kali-mahabali": "EXPERIMENTAL/kali-mahabali",
    "icode": "DEVELOPER-TOOLS (Deprecated\u2044Inactive)/icode",
    "browsefleet": "browsefleet", "hermes-prime-bridge": "hermes-prime-bridge",
    "lifeos-bot": "LIFEOS/lifeos-bot", "lifeos-saas": "LIFEOS/lifeos-saas",
    "cinesync": "CONTENT-CREATION/cinesync (Deprecated\u2044Inactive)",
    "osint-os": "EXPERIMENTAL/osint-os (Deprecated\u2044Inactive)",
    "workout-factory": "EXPERIMENTAL/workout-factory (Deprecated\u2044Inactive)",
    "design-aesthetics-website": "WEBSITES/design-aesthetics-website",
    "ishanparihar-cms": "WEBSITES/ishanparihar-cms",
    "ishanparihar-svelte": "WEBSITES/ishanparihar-svelte",
    "law-of-one-india-website": "WEBSITES/law-of-one-india-website",
    "webdev-portfolio": "WEBSITES/webdev-portfolio", "lifeos-website": "LIFEOS/lifeos-website",
}

FAMILIES = [
    ("state_machines", re.compile(
        r"state[_ ]machine|StateMachine|FSM<|finite[_ ]state|event[_ ]sourc|"
        r"\.states\b|current_state|state_transition|transition\s*\(|snapshot\b", re.I), 4),
    ("graphs", re.compile(
        r"holonic|adjacency[_ ]list|DAG\b|graph[_ ](?:node|edge|traversal)|"
        r"topolog(?:ical)?[_ ]sort|NodeId\b|EdgeId\b|BFS\b|DFS\b|graph\s*\{", re.I), 4),
    ("dsl_parsers", re.compile(
        r"lexer|tokenizer|Parser\b|grammar\b|interpreter\b|bytecode\b|"
        r"AbstractSyntaxTree|AstNode|parse_tree|PrattParser|nom\b|pest\b|"
        r"peg\b|evaluate\s*\(|eval_tree|syntax[_ ]tree", re.I), 5),
    ("concurrency", re.compile(
        r"tokio::|async[_ ]fn|async def|\.await\b|rayon::|par[_ ]iter\b|std::thread|"
        r"thread::spawn|tokio::spawn|mpsc::|crossbeam|actix|async[_ ]move|asyncio", re.I), 8),
    ("protocols", re.compile(
        r"FastMCP|@mcp\.tool|rmcp\b|axum|actix[_ ]web|hono\b|FastAPI|telethon|"
        r"websocket|WebSocket|gRPC|protobuf|GraphQL|jsonrpc|JSON-RPC", re.I), 4),
    ("storage", re.compile(
        r"rocksdb|sled\b|sqlx\b|diesel\b|redis::|mongodb|postgres|"
        r"write[_ ]ahead|WAL\b|storage[_ ]engine|BTreeMap|HashMap<|LRU\b|lru::", re.I), 8),
    ("ai_ml", re.compile(
        r"embedding|cosine[_ ]similarity|attention[_ ]mask|transformer\b|"
        r"semantic[_ ]search|vector[_ ]store|tokenize\w*\s*\(|llm\b|RAG\b|"
        r"retrieval|inference\s*\(|classifier\b", re.I), 4),
    ("render_audio", re.compile(
        r"shader\b|wgpu|cuda\b|sdl2|bevy\b|synthesizer\b|synth\b|oscillator|wav\b|"
        r"fft\b|spectrogram|spectrum[_ ]analy|pcm\b|sample[_ ]rate|midi\b|renderer\b|"
        r"voxel", re.I), 4),
    ("determinism", re.compile(
        r"deterministic|seeded\b|fixed[_ ]point|reproducib\w*|byte[-_]identical|"
        r"same brief|rng\s*=|SeedableRng|SmallRng|StdRng|std::collections::BTree", re.I), 3),
    ("distributed", re.compile(
        r"consensus|raft\b|shard\w*|replicat\w*|token[_ ]bucket|rate[_ ]limit|"
        r"load[_ ]balanc|message[_ ]queue|kafka|job[_ ]queue|worker[_ ]pool", re.I), 4),
    ("security", re.compile(
        r"hmac|sha256|sha2::|aes\b|chacha|argon2|bcrypt|signing[_ ]key|"
        r"verify[_ ]signature|crypt\w*::|seccomp|jail\b|jwt\b|oauth2?", re.I), 4),
    ("plugins", re.compile(
        r"dyn Trait|trait object|Box<dyn|plugin\w*\s*\{|extension[_ ]system|"
        r"skill\s*\{|mod_registry|register\w*\s*\(|dispatcher\b", re.I), 4),
]

EXCLUDE_DIRS = {"target", "node_modules", ".git", "venv", ".venv", "__pycache__",
                "third_party", "z.archive", "vendor", "dist", "build", ".next",
                "tests", "test", "__tests__", "spec", "examples", "benches"}
CODE_EXT = {".rs", ".py", ".ts", ".tsx", ".js", ".go", ".rb", ".java", ".kt",
            ".swift", ".c", ".cpp", ".h", ".hpp", ".cs", ".php"}


def tracked_code_files(repo_dir):
    try:
        out = subprocess.run(
            ["git", "-C", repo_dir, "ls-files"], capture_output=True, text=True,
            timeout=60).stdout
    except Exception:
        return []
    files = []
    for f in out.splitlines():
        if not f:
            continue
        parts = f.split("/")
        if any(seg in EXCLUDE_DIRS for seg in parts):
            continue
        if f.endswith(tuple(CODE_EXT)):
            files.append(os.path.join(repo_dir, f))
    return files


def read_bounded(path, limit=1_500_000):
    try:
        if os.path.getsize(path) > limit or os.path.getsize(path) == 0:
            return ""
        with open(path, errors="ignore") as fh:
            return fh.read(limit)
    except Exception:
        return ""


def audit(repo_dir):
    counts = {name: 0 for name, _, _ in FAMILIES}
    for f in tracked_code_files(repo_dir):
        text = read_bounded(f)
        if not text:
            continue
        for name, pat, _ in FAMILIES:
            counts[name] += len(pat.findall(text))
    present = []
    for name, _, min_hits in FAMILIES:
        if counts[name] >= min_hits:
            present.append(name)
    return present


def main():
    names = sys.argv[1:] or sorted(REPOS)
    print(f"{'project':<26}{'soph':>5}  families")
    print("-" * 78)
    for name in names:
        d = os.path.join(PORTS, REPOS.get(name, name))
        if not os.path.isdir(d):
            print(f"{name:<26}  MISSING {d}")
            continue
        fams = audit(d)
        print(f"{name:<26}{len(fams):>5}  {', '.join(fams)}")


if __name__ == "__main__":
    main()
