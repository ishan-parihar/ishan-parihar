# Hero Spec — ishan-parihar Profile README

Canonical regeneration + maintenance spec for the profile README's hero banner.

## T2I Hero Prompt (for future text-to-image regeneration)

> **Subject:** a systems engineer standing at a control deck orchestrating a
> constellation of agent infrastructure — DAG execution graphs, MCP tool rings,
> memory vectors, and token-optimized protocol beams converging on a central hub
> labeled by the light it emits (no text).
>
> **Composition:** central operator figure with radiating infrastructure nodes;
> depth-of-field glow.
>
> **Palette:** deep charcoal `#0B0F19` background, Rust amber `#DE7F3B`,
> TypeScript blue `#3178C6`, Python gold `#F7E018`, MCP violet `#A855F7`,
> emerald accent `#10B981`.
>
> **Style:** cinematic dark editorial vector, precise geometry, subtle glow,
> no text. **Format:** 16:9.

## Live Hero

The **live hero is the inline SVG at the top of `README.md`** — it is the source
of truth for what visitors see. If a T2I image ever replaces it, keep the visual
language identical to this spec (palette, geometry, node motif).

## Brand Tokens (must stay in sync everywhere)

| Token | Hex | Used for |
|-------|-----|----------|
| Charcoal background | `#0B0F19` | Hero canvas |
| Panel | `#0F172A` | Nodes, central hub |
| Grid | `#1E293B` | Grid overlay, labels |
| Rust amber | `#DE7F3B` | Rust node, Rust badge (`shields.io` `Rust-DE7F3B`) |
| TypeScript blue | `#3178C6` | TS node, TS badge |
| Python gold | `#F7E018` | Python node |
| Python brand blue | `#3776AB` | Python badge (logo brand) |
| MCP violet | `#A855F7` | MCP node, MCP badge (`MCP-800%2B%20Tools-A855F7`) |
| Emerald accent | `#10B981` | Central hub, AVAILABLE badge, visitor counter |
| Success green | `#047857`/`#022C22` | Metrics chip stroke/fill |

## SVG Maintenance Rules

1. **Responsive:** keep `width="100%"`, `style="max-width:880px;height:auto;display:block;margin:0 auto"`, and `preserveAspectRatio="xMidYMid meet"`. Never re-add a fixed `height` — it squashes the hero on mobile.
2. **Zero comments:** the header must contain no HTML comments (no process/meta commentary). Edit the SVG directly.
3. **Metrics chip:** the `42 PROJECTS` chip must always match the **Active Projects** row in the "Engineering by the Numbers" table.
4. **Badge colors:** badges use the tokens above (not ad-hoc colors) so the header reads as one system.
