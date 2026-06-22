---
name: reelos-voice-cinema
description: Independent ReelOS voice cinema production skill. Use when the user asks to turn Chinese scripts, articles, AI/Agent signals, philosophy/knowledge content, brand copy, pasted text, or TTS audio into a narrated Remotion video with real TTS timing, optional free external materials, subtitle and typography effects, motion graphics, keyframe review, and MP4 export.
---

# ReelOS Voice Cinema

Use this skill as an independent production lane that can be installed into any Remotion-capable project: script -> TTS -> timing -> optional materials -> Remotion composition -> keyframes -> render -> ffprobe validation.

## Core Rules

- Use real audio duration as the timing source. Never estimate scene timing from text length for final video.
- Keep Remotion responsible for text, subtitle effects, light motion graphics, diagrams, and final composition.
- Prefer free external videos/images as background material when the user asks for素材感、画面不单一、低成本, or scene-based narration.
- Use pure Remotion motion graphics when the content is abstract, technical, brand, AI Agent, causal systems, diagrams, or product-film style.
- Use Lottie for reusable deterministic micro-animations such as icons, seals, strokes, signal pulses, loading cores, and decorative overlays.
- Use GSAP knowledge for motion design, timeline planning, easing, stagger, and prototypes; translate final Remotion output back to frame-driven math unless a host project explicitly supports a deterministic GSAP render path.
- Do not copy OpenMontage code. Only reuse the source-led idea: slots, providers, candidate scoring, manifest, and quality gates.
- Do not save API keys in code or docs. Read TTS/API credentials from environment variables.
- Do not use CSS animation or transition for video motion. Use `useCurrentFrame()`, `interpolate()`, `spring()`, and `Sequence`.
- Keep generated outputs under the active project root, normally `public/voiceover-*`, `public/materials/*`, `src/compositions/*Timings.ts`, `out/stills/*`, and `out/*.mp4`.

## Project Independence

- Treat the current working directory as the project root unless the user gives another path.
- Discover the host project before editing: inspect `package.json`, Remotion entry files, `src/Root.tsx` or equivalent composition registry, `public/`, `scripts/`, and any local docs.
- Do not depend on `/Users/netseek/Documents/Voice2Video`, MoneyPrinterTurbo, or any other fixed local path.
- If expected helper scripts do not exist, create small project-local equivalents instead of assuming a specific repository layout.
- If the host project is not a Remotion project, first add or ask for the minimum Remotion scaffold needed for rendering.
- Keep reusable workflow knowledge inside this skill; keep generated video assets, scripts, timings, and outputs inside the host project.

## Workflow

1. **Read context**
   - Inspect `package.json`, Remotion entry files, existing compositions, and relevant local docs such as `helloagents/wiki/*` when present.
   - If making a material-driven vertical video, read `references/material-workflow.md`.
   - If making a TTS-driven narrated video, read `references/tts-timing.md`.
   - If building or modifying Remotion components, read `references/remotion-patterns.md`.
   - If visual quality matters, read `references/visual-motion.md`.
   - If choosing subtitle typography, caption layout, karaoke/flash modes, or style samples, read `references/subtitle-style-system.md`.
   - If adding Lottie assets, GSAP-inspired sequencing, animated icons, signal pulses, or advanced motion systems, read `references/motion-assets-lottie-gsap.md`.

2. **Package the content**
   - Convert long text into short spoken scenes. One scene should carry one idea.
   - Create a title, subtitle, slug, and `CompositionId`.
   - Choose the lane:
     - `material-led`: free videos/images are the main background; Remotion adds subtitles and light overlays.
     - `mg-led`: Remotion diagrams, charts, particles, product-film motion, or causal/system graphics are the main visual.
     - `hybrid`: external material plus diagrams/subtitles.

3. **Generate TTS and timing**
   - Create or update `scripts/generate-{slug}-voiceover.py`.
   - Use the user-specified voice when provided; otherwise use the host project's default voice if appropriate.
   - Generate per-scene MP3 files and `manifest.json`.
   - Write `src/compositions/{camelSlug}Timings.ts` from `ffprobe` durations.

4. **Source materials when needed**
   - Define scene slots and keyword queries.
   - Reuse a host project material pipeline when present. If none exists, create a small project-local script with providers, scoring, download validation, and manifest output.
   - Record source URL, provider, dimensions, duration, and selected path.

5. **Build Remotion composition**
   - Register the composition in `src/Root.tsx`.
   - Add npm scripts for TTS/render/still when useful.
   - Load local fonts through `@font-face` and wait for `document.fonts.ready` with `delayRender`.
   - Use clear Chinese text rendering: hard stroke, `paintOrder: 'stroke fill'`, dark backing layer, no blurry 3D shadow.
   - For narrated Chinese videos, choose a subtitle style strategy before rendering: default to clear karaoke, then mix in flash, quote, editorial, or impact styles only where the script needs emphasis.
   - For Lottie/GSAP-enhanced videos, keep the output hierarchy clear: footage first for atmosphere, subtitles first for comprehension, Lottie/GSAP-style motion only as an accent or structured information layer.

6. **Review and render**
   - Run `npm run check`.
   - Export representative stills: cover, mid-scene, dense information frame, final frame.
   - Visually inspect stills for readability, overlap, fake HUD clutter, and timing logic.
   - Render MP4.
   - Validate with `ffprobe` for duration, video stream, audio stream, dimensions, and fps.

## Project Conventions

- Default FPS: `30`.
- Default horizontal size: `1920x1080`.
- Default vertical size: `1080x1920`.
- Recommended ReelOS TTS voice when the user does not specify another voice: `clone_20260518_060330_483432`.
- Recommended subtitle strategy: use clear karaoke/typewriter as the base, then selectively add kinetic flash, cinematic quote, editorial, or impact modes. See `references/subtitle-style-system.md`.
- Recommended material principle: background videos/images carry the picture; MG should not replace real material unless the subject is abstract or brand/diagram-heavy.
- Recommended Lottie/GSAP principle: use Lottie JSON for portable loopable assets, and use GSAP timelines as design blueprints that are converted into Remotion frame math for final rendering.

## Completion Contract

When finished, report:

- title, subtitle, slug, and composition id
- number of TTS scenes and whether timing came from real audio
- material lane used, and whether external/free assets were used
- subtitle strategy used, especially if multiple modes are mixed
- Lottie or GSAP-derived motion assets used, if any
- motion brief in one sentence
- MP4 path and key still paths
- verification commands run and result
