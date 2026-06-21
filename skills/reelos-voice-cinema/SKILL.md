---
name: reelos-voice-cinema
description: ReelOS voice cinema production inside the Voice2Video project. Use when the user asks to turn Chinese scripts, articles, AI/Agent signals, philosophy/knowledge content, brand copy, pasted text, or TTS audio into a narrated Remotion video with real TTS timing, optional free external materials, subtitle and typography effects, motion graphics, keyframe review, and MP4 export.
---

# ReelOS Voice Cinema

Use this skill to produce videos in the `/Users/netseek/Documents/Voice2Video` project. Treat it as a project-scoped production lane: script → TTS → timing → optional materials → Remotion composition → keyframes → render → ffprobe validation.

## Core Rules

- Use real audio duration as the timing source. Never estimate scene timing from text length for final video.
- Keep Remotion responsible for text, subtitle effects, light motion graphics, diagrams, and final composition.
- Prefer free external videos/images as background material when the user asks for素材感、画面不单一、低成本, or scene-based narration.
- Use pure Remotion motion graphics when the content is abstract, technical, brand, AI Agent, causal systems, diagrams, or product-film style.
- Do not copy OpenMontage code. Only reuse the source-led idea: slots, providers, candidate scoring, manifest, and quality gates.
- Do not save API keys in code or docs. Read TTS/API credentials from environment variables.
- Do not use CSS animation or transition for video motion. Use `useCurrentFrame()`, `interpolate()`, `spring()`, and `Sequence`.
- Keep generated outputs in `public/voiceover-*`, `public/materials/*`, `src/compositions/*Timings.ts`, `out/stills/*`, and `out/*.mp4`.

## Workflow

1. **Read context**
   - Inspect `package.json`, `src/Root.tsx`, existing compositions, and relevant `helloagents/wiki/*` files.
   - If making a material-driven vertical video, read `references/material-workflow.md`.
   - If making a TTS-driven narrated video, read `references/tts-timing.md`.
   - If building or modifying Remotion components, read `references/remotion-patterns.md`.
   - If visual quality matters, read `references/visual-motion.md`.

2. **Package the content**
   - Convert long text into short spoken scenes. One scene should carry one idea.
   - Create a title, subtitle, slug, and `CompositionId`.
   - Choose the lane:
     - `material-led`: free videos/images are the main background; Remotion adds subtitles and light overlays.
     - `mg-led`: Remotion diagrams, charts, particles, product-film motion, or causal/system graphics are the main visual.
     - `hybrid`: external material plus diagrams/subtitles.

3. **Generate TTS and timing**
   - Create or update `scripts/generate-{slug}-voiceover.py`.
   - Use the user-specified voice when provided; otherwise use project default voice if appropriate.
   - Generate per-scene MP3 files and `manifest.json`.
   - Write `src/compositions/{camelSlug}Timings.ts` from `ffprobe` durations.

4. **Source materials when needed**
   - Define scene slots and keyword queries.
   - Use `scripts/material_pipeline.py` patterns for providers, scoring, download validation, and manifest output.
   - Record source URL, provider, dimensions, duration, and selected path.

5. **Build Remotion composition**
   - Register the composition in `src/Root.tsx`.
   - Add npm scripts for TTS/render/still when useful.
   - Load local fonts through `@font-face` and wait for `document.fonts.ready` with `delayRender`.
   - Use clear Chinese text rendering: hard stroke, `paintOrder: 'stroke fill'`, dark backing layer, no blurry 3D shadow.

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
- Existing TTS voice often used by this project: `clone_20260518_060330_483432`.
- Existing successful subtitle style: karaoke/typewriter text with high-contrast fill, hard black stroke, and a dark background strip.
- Existing material principle: background videos/images carry the picture; MG should not replace real material unless the subject is abstract or brand/diagram-heavy.

## Completion Contract

When finished, report:

- title, subtitle, slug, and composition id
- number of TTS scenes and whether timing came from real audio
- material lane used, and whether external/free assets were used
- motion brief in one sentence
- MP4 path and key still paths
- verification commands run and result
