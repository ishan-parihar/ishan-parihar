# Hero Spec — ishan-parihar Profile README

Canonical regeneration + maintenance spec for the profile README's hero banner.

## How the hero is served

The hero lives as a **real SVG file** — `assets/readme/hero.svg` — and is mounted
in `README.md` with a native image tag:

```html
<img src="./assets/readme/hero.svg" alt="…" style="max-width:880px;width:100%;height:auto;display:block;margin:0 auto">
```

**Why a file, not inline SVG:** GitHub's README sanitizer and the mobile clients
flatten inline `<svg><text>` content into a single line of unstyled text (the
`transform` / `x` / `y` layout attributes are dropped). Referenced through `<img>`,
the browser's native SVG engine renders the full layout everywhere — desktop,
mobile web, and mobile apps.

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
> no text. **Format:** 16:9 (1200×320).

## Brand Tokens (must stay in sync everywhere)

| Token | Hex | Used for |
|-------|-----|----------|
| Charcoal background | `#0B0F19` | Hero canvas |
| Panel | `#0F172A` (gradient `#16213A`→`#0F172A`) | Nodes, central hub |
| Grid | `#1E293B` | Grid overlay |
| Rust amber | `#DE7F3B` | Rust node, Rust badge (`shields.io` `Rust-DE7F3B`) |
| TypeScript blue | `#3178C6` | TS node, TS badge |
| Python gold | `#F7E018` | Python node |
| Python brand blue | `#3776AB` | Python badge (logo brand) |
| MCP violet | `#A855F7` | MCP node, MCP badge (`MCP-800%2B%20Tools-A855F7`) |
| Emerald accent | `#10B981` | Central hub, AVAILABLE badge, visitor counter |
| Success green | `#022C22` / `#047857` / `#34D399` | Stat-chip fill / stroke / text |

## SVG Maintenance Rules

1. **Keep it a file, keep it mounted via `<img>`.** Never inline the SVG back into
   the README — that is what broke the layout (single-line text).
2. **Lint contract (S04):** the SVG must be well-formed XML with a `viewBox` and a
   `<title>` element, and the `<img>` must carry useful `alt` text.
3. **Responsive:** keep the img `style` as `max-width:880px;width:100%;height:auto`.
   The SVG file itself keeps `width="1200" height="320"` + `viewBox="0 0 1200 320"`
   so the intrinsic aspect ratio drives scaling.
4. **Stat chips must stay truthful:** `31K+ TESTS` tracks the **Automated Tests**
   row and `42 PROJECTS` tracks the **Active Projects** row in the "Engineering by
   the Numbers" table — update the chips when those numbers change.
5. **Zero comments:** no HTML/XML comments in the SVG or header markup.
6. **Regeneration:** if the hero is ever re-illustrated (T2I or hand-drawn),
   re-export as `assets/readme/hero.svg` at 1200×320 with the same palette and
   keep the same img mount point.
7. **Glow dependency:** the hub uses `filter="url(#softGlow)"` (feGaussianBlur).
   Browsers render it, but rasterizing previewers may drop filters — keep the hub
   legible without the glow (high-contrast border + solid fill).
