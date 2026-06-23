# Visual Systems

## Table of Contents

1. Taste-To-Token Workflow
2. Example: GuanShan-Inspired New Chinese System
3. Example: Aura Cloud-Inspired Fluid Infrastructure System
4. Example: NovaPulse-Inspired Sonic Creator Studio System
5. Example: Nexura-Inspired Performance Creative Agency System
6. Component Taste Rules
7. Image Direction Patterns
8. Anti-Generic Checklist

Use this when turning taste into tokens, components, or production UI.

## Taste-To-Token Workflow

1. Name 3-5 semantic color roles before choosing colors.
2. Define typography roles by usage, not just sizes: display, body, UI, meta, accent.
3. Pick one spacing base and enforce it.
4. Decide shape language: sharp, micro-radius, soft, circular, or irregular.
5. Define texture/material rules.
6. Define motion tempo and easing.
7. Build component states: default, hover, active, disabled, focus, error.

## Example: GuanShan-Inspired New Chinese System

Color tokens:

| Token | Value | Role |
| --- | --- | --- |
| Cinnabar | `#C9372C` | Primary button, links, emphasis |
| Cinnabar Hover | `#B03025` | Primary hover |
| Ochre | `#D4A574` | Decoration, subtle gold, dividers |
| Void | `#0A0A0A` | Main text, deep background |
| Ink | `#141414` | Secondary dark surface |
| Stone | `#333333` | Body text / secondary title |
| Mist | `#8A8A8A` | Metadata / placeholders |
| Ash | `#C4C4C4` | Borders / disabled |
| Rice | `#F0EDE8` | Page background |
| Teal | `#7BA7A6` | Auxiliary / status |
| Success | `#5A8A6A` | Positive status |
| Warning | `#C9A84C` | Warning |
| Info | `#4A7C8F` | Help / info |

Typography:

| Role | Family | Weight | Use |
| --- | --- | --- | --- |
| Display | Source Han Serif / Noto Serif SC | 800-900 | Brand, hero |
| H1-H3 | Source Han Serif / Noto Serif SC | 600-700 | Page and section titles |
| H4 / Label | Source Han Sans / Noto Sans SC | 500 | UI labels |
| Body | Source Han Sans / Noto Sans SC | 400 | Product text |
| Brush accent | Ma Shan Zheng / Zhi Mang Xing | regular | Tagline only |

Spacing:
- Use a 4px base for interface systems.
- `8px` inline gap, `16px` card padding, `24-32px` component spacing, `48-64px` module spacing, `96-128px` page rhythm.

Radius:
- `0px` for images and dividers.
- `2px` for buttons, tags, inputs.
- `4px` for cards, panels, popovers.
- Avoid large pill shapes unless the brand is explicitly soft or playful.

Shadow:
- Default to none.
- Small shadow for hover or tags.
- Medium shadow only for menus, popovers, dialogs.

Motion:
- Default transition: 0.3s for UI feedback.
- Cultural page reveal: 0.8-1.2s.
- Easing: `cubic-bezier(0.22, 0.61, 0.36, 1)`.

## Example: Aura Cloud-Inspired Fluid Infrastructure System

Use this for cloud infrastructure, deployment, observability, AI systems, and technical SaaS that should feel adaptive and alive.

Color tokens:

| Token | Value | Role |
| --- | --- | --- |
| Void | `#000000` | Root page background |
| Deep Graphite | `#050606`, `#070A0A` | Section depth and canvas fallback |
| Glass Black | `rgba(0,0,0,0.40-0.80)` | Header, cards, floating nodes |
| Glass White | `rgba(255,255,255,0.03-0.06)` | Subtle panel fill |
| Hairline | `rgba(255,255,255,0.05-0.15)` | Borders, dividers, navigation shell |
| Primary Cyan | `#06B6D4` | CTA border, live state, routing energy |
| Electric Cyan | `#22D3EE` | High-energy glow, hover signal |
| Teal | `#14B8A6` | Secondary system energy |
| Aqua | `#2DD4BF` | Soft highlights and gradient stops |
| Text | `#FFFFFF` | Main copy on dark |
| Muted Text | `rgba(255,255,255,0.55-0.76)` | Body, nav, supporting copy |

Typography:

| Role | Family | Weight | Use |
| --- | --- | --- | --- |
| Display | Inter / Geist / system sans | 500 | Hero and section titles |
| Body | Inter / Geist / system sans | 400 | Product prose |
| UI | Inter / Geist / system sans | 500 | Navigation, buttons |
| Meta/Data | Inter / Geist / system sans | 500 | Uppercase labels and stats |
| Chinese fallback | Noto Sans SC | 400-600 | Chinese headings and body |

Type scale notes:
- English hero can use line-height `0.95-1.05` and tracking around `-0.02em`.
- Uppercase metadata should use tracking around `0.08-0.12em`.
- Keep Chinese `letter-spacing: 0`; use weight, line-height, and spacing for hierarchy.

Surface and effects:
- Full-bleed background: canvas/WebGL liquid field or layered radial gradients behind content.
- Ambient blobs: cyan/teal at `8-14%` alpha with `120-160px` blur.
- Panels: black `40-60%` opacity, `backdrop-blur-md/xl`, 1px low-alpha borders.
- CTA: cyan/teal gradient border, black inner fill, soft glow that intensifies on hover.
- Data cards: transparent fills and crisp stat typography; let numbers prove the system.

Motion:
- Page scroll: smooth, calm, no snap unless the product needs a guided narrative.
- Floating nodes: 6-9s `ease-in-out` loops, staggered duration and delay.
- Hover: 150-500ms, opacity/color/scale only; keep movement under 4px.
- Reveal: 0.8s with blur-to-clear or slight vertical rise when content enters view.
- Shader/canvas: slow liquid flow, optional mouse reaction, never high-frequency flicker.

## Example: NovaPulse-Inspired Sonic Creator Studio System

Use this for AI music studios, audio generation tools, creator-safe track libraries, sample marketplaces, and production-suite landing pages.

Color tokens:

| Token | Value | Role |
| --- | --- | --- |
| Stage Black | `#000000` | Root background and hero stage |
| Deep Slate | `#020617`, `#030712` | Header, page depth, dark panels |
| Panel Slate | `#0F172A`, `#111827`, `#1E293B` | Player, cards, pricing surfaces |
| Primary Blue | `#3B82F6` | CTA, playback, active states |
| Electric Blue | `#60A5FA` | Gradient text, hover highlights |
| Deep Blue | `#1D4ED8`, `#2563EB` | CTA gradients and borders |
| Cyan Glow | `#22D3EE` | Audio halo, orbit glow, pulse states |
| Text | `#F8FAFC` | Main copy on black |
| Muted Text | `#CBD5E1`, `#94A3B8` | Body, metadata, nav |
| Hairline | `rgba(255,255,255,0.05-0.15)` | Borders, cards, controls |

Typography:

| Role | Family | Weight | Use |
| --- | --- | --- | --- |
| Display | Manrope | 500 | Hero and signature phrases |
| Body | Inter / system sans | 400 | Product copy and feature text |
| UI | Inter / system sans | 400-500 | Buttons, controls, nav |
| Meta | Inter / system sans | 400-500 | BPM, artist, license, processing state |
| Chinese fallback | Noto Sans SC | 400-600 | Chinese headings and copy |

Type scale notes:
- English hero can be very tight: line-height `0.95-1.05`, tracking around `-0.04em`.
- Use blue gradient on one phrase only; keep most headline text white.
- Body copy should stay relaxed around line-height `1.5-1.65`.
- Music metadata can stay human-readable; do not force mono unless showing code/API details.

Surface and effects:
- Header: sticky dark gradient, `backdrop-blur-md`, 1px low-alpha border.
- Hero player: slate-to-black gradient, 24-26px radius, blue border around `20-50%` alpha, cyan glow shadow.
- Record/orbit UI: circular product preview, rotating rings, centered track state, compact controls.
- Track cards: cover art first, gradient edge/overlay second, metadata third.
- CTA: dark pill with conic/blue border for the primary action; secondary action remains transparent.

Motion:
- Enter reveal: 0.6-0.8s rise from `translateY(20px)` with opacity fade.
- Orbit: 20s linear infinite for record rings or circular audio systems.
- Glow pulse: 3s box-shadow pulse from low cyan to brighter cyan.
- Scan line: 2.5s vertical scan when analyzing or processing audio.
- Audio bars: 1s `scaleY` bounce with stagger if multiple bars are present.
- Hover: image/card scale around `1.05`, button active scale around `0.95-0.98`, movement under 4px.

## Example: Nexura-Inspired Performance Creative Agency System

Use this for ad creative agencies, growth studios, e-commerce creative operations, UGC pipelines, and paid-social service pages.

Color tokens:

| Token | Value | Role |
| --- | --- | --- |
| Engine Black | `#000000` | Root background and hero overlay |
| Deep Navy | `#0B0F18`, `#111827` | Atmospheric depth |
| Panel Dark | `#14161C`, `#1C1F26` | Dashboard and kanban shells |
| Task Graphite | `#262A34` | Task cards, proof cards, testimonial cards |
| White | `#FFFFFF` | Hero, CTA, key metrics |
| Muted Gray | `#9CA3AF`, `#D1D5DB` | Nav, body, labels |
| Performance Blue | `#2563EB`, `#3B82F6` | Primary action, task button, proof accent |
| Light Blue | `#60A5FA` | Avatars and gradient stops |
| Purple Accent | `#A855F7`, `#C084FC` | Secondary creative energy |
| Cyan Accent | `#22D3EE`, `#2DD4BF` | Proof avatars, light trail highlights |
| Success | `#34D399` | Availability/live dot |
| Hairline | `rgba(255,255,255,0.05-0.20)` | Borders and dividers |

Typography:

| Role | Family | Weight | Use |
| --- | --- | --- | --- |
| Display | DotGothic16 | 400 | Hero, section titles, metrics |
| Body | ui-monospace / SFMono / Menlo | 400 | Product copy and proof text |
| UI | ui-monospace / SFMono / Menlo | 500-600 | Nav, buttons, task controls |
| Meta | ui-monospace / SFMono / Menlo | 400-500 | Dates, statuses, labels, task counts |
| Chinese fallback | Noto Sans SC | 400-600 | Chinese copy and headings |

Type scale notes:
- English hero can use large pixel display at 64-72px with line-height around `1.0-1.1`.
- Keep pixel display out of long body text.
- Mono body copy should be short; use compact paragraphs and proof bullets.
- Chinese should use clean sans fallback; pixel style can be simulated with layout, not forced onto long CJK text.

Surface and effects:
- Hero: full-bleed light-trail, gravity-field, or high-speed abstract creative background with dark overlay.
- Availability chip: low-alpha white fill, 1px border, backdrop blur, small green pulsing dot.
- CTA: white pill on dark for primary conversion; glass pill for secondary action.
- Workflow preview: graphite kanban/dashboard with blue primary button, task rows, status columns, avatars, and date metadata.
- Cards: gradient border shell from white `20%` to transparent, graphite inner surface, low-alpha borders.

Motion:
- Reveal: 0.8s opacity + translate + blur-to-clear for hero, stats, cards, and sections.
- Availability: slow pulse on the green dot only.
- Hover: brighten border/fill, no large movement; this style should feel operational.
- Kanban: horizontal scroll is acceptable; avoid auto-moving tasks unless it communicates throughput.
- Background: light trails can imply motion in the asset itself; avoid adding unrelated particles.

## Component Taste Rules

Buttons:
- Primary button should be visibly actionable and materially consistent with the style.
- Use icon buttons for familiar actions when possible.
- Avoid ornate borders on every button; reserve ceremony for primary moments.

Cards:
- Use cards for repeated items or true framed tools, not every section.
- In refined designs, card borders often work better than heavy shadows.
- If a card contains an image, the image should reveal the actual subject.

Forms:
- Labels should be clear and quiet.
- Error states need semantic color plus text; do not rely on red alone.

Navigation:
- Western/product systems: clear active states, grid alignment, predictable placement.
- Chinese/garden systems: navigation can reveal progressively, but must remain usable.
- Zen systems: reduce navigation to essentials; avoid constant motion.

## Image Direction Patterns

Chinese:
- Ink mountains, mist, porcelain, paper fiber, restrained cinnabar seal.
- Avoid generic dragons, lantern overload, or fake ancient texture.

Japanese / Zen:
- Stone, paper, shadow, quiet rooms, imperfect ceramics, seasonal detail.
- Avoid cliché cherry-blossom wallpaper unless the brief is explicitly seasonal.

Nordic:
- Real interiors, wood, daylight, snow, forest, glass, textile warmth.

Dunhuang:
- Mineral pigment, cave darkness, flying ribbon, lotus/caisson structure, sacred glow.

Indian:
- Textile, mandala, saffron/indigo/gold, festival color, temple ornament.

African:
- Earth, rhythmic pattern, craft, body/gesture, beadwork, landscape.

Sci-fi:
- Signal panels, star maps, coordinates, waveform, sensor data, narrow typography.

Fluid infrastructure:
- Dark glass control rooms, living system maps, liquid shader backgrounds, observability stats, cyan/teal routing energy, adaptive cloud nodes.

Sonic creator studio:
- Black-stage hero, waveform icons, orbiting record/player modules, cover-art track cards, blue playback glow, BPM/license metadata, audio bars, DAW/export panels.

Performance creative agency:
- Light-trail growth-engine hero, pixel display headlines, mono CTAs, ROAS/turnaround proof metrics, kanban workflow previews, task cards, UGC/creative pipeline dashboards.

Frontier tech community:
- Real event/community/tech imagery, black overlays, compressed display headlines, mono metadata, acid-lime signal dots, issue-card editorial grids.

Brush humanity:
- Paper fiber, ink wash, poetry pages, calligraphy traces, brush pressure, cinnabar seal, quiet reading rooms.

Fantasy Zen:
- Dark void, floating dust, moonlit mist, abstract particles, sparse poetic text, muted blue/mauve/moss accents.

Deep space signal:
- Telemetry table, waveform, decoded message, chronology, RA/DEC coordinates, confidence metrics, cyan/amber signal accents.

## Anti-Generic Checklist

- Is the typography system defined before color and imagery?
- Does the style have a structural logic, or only color decoration?
- Are there too many accents competing?
- Is the spacing system visible and consistent?
- Can the design survive if one decorative motif is removed?
- Does the typography match the domain and culture?
- Are images specific enough to inspect, not just atmosphere?
- Does motion help comprehension or mood?
