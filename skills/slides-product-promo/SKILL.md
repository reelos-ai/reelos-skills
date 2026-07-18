---
name: slides-product-promo
description: Research a real product or website, write a marketing voiceover, generate or ingest TTS, derive a timed storyboard from the actual audio, build a Bolt Slides product-promo deck, and render a synchronized MP4. Use for 产品宣传片、网站宣传视频、TTS 配画面、Slides 宣传短片、产品发布视频、域名输入动画, or when a user wants visuals and motion to follow narration without uncomfortable flashing.
---

# Slides Product Promo

Create product-promo videos in this order: research → voiceover → TTS → timeline → slides → motion → render → sync QA. Treat actual TTS timing as the source of truth.

## Required companion skills

- Use `slides` for the Bolt Slides engine and layout constraints. Never modify `src/deck/`.
- Use the requested TTS skill when available. For `giggle-generation-speech`, complete its voice and emotion selection before submission.
- Use `koubo-shengao-yuan` when available for spoken-Chinese review; otherwise apply the voiceover rules below directly.

## 1. Research before writing

Read the supplied website, About page, product documentation, and visible UI. Capture:

- One-sentence positioning
- Audience and use moments
- Three to five verified capabilities
- Product mechanism or workflow
- Evidence, limitations, and compliance language
- Brand colors, typography, logo, domain, and real UI assets

Do not invent metrics, customer quotes, guarantees, or capabilities. Save source-backed facts separately from marketing interpretation.

## 2. Write the voiceover first

Draft the spoken script before final slide authoring. Use short, speakable sentences and one idea per breath group.

Use this default arc unless the product requires another:

1. Hook or user tension
2. Product reveal
3. What it brings together
4. How it works or why it is different
5. User outcome
6. Domain or action CTA
7. Required disclaimer

Target about 3–4 Chinese characters per second for a clear marketing read, then let the selected voice determine the final duration. Do not force a fixed video duration by accelerating a finished voice track.

Use `assets/product-promo-template/voiceover-brief.md` as the drafting skeleton. Read `references/story-arcs.md` when choosing a narrative variant.

## 3. Generate TTS before final slides

Confirm script, voice, emotion, and speed. Generate a fresh TTS task and wait until the actual audio file is ready.

Record:

- Audio path and codec
- Exact duration
- Voice, emotion, and speed
- Word or phrase timestamps when available

If word timestamps are unavailable, detect pauses with:

```bash
bash scripts/detect-pauses.sh voiceover.mp3
```

Never reuse an old task ID for a new narration.

## 4. Build the sync timeline

Create `timeline.json` from the real audio. Map every phrase to a visual beat and every high-value word to a visible action.

Prefer one main scene per semantic beat. Use short inserts only when they clarify the narration. Do not cut on every pause.

Mark explicit sync anchors for:

- Product name reveal
- Feature names
- Contrast words such as “风险” or “反证”
- Domain spoken or CTA phrase
- Disclaimer start

Use `assets/product-promo-template/timeline.json` as the schema starter. Read `references/sync-contract.md` for timing tolerances.

Validate before rendering:

```bash
python3 scripts/validate_timeline.py timeline.json --audio voiceover.mp3
```

## 5. Author slides from the timeline

Only now finalize slide count and content. Keep the live deck useful as a presentation while adding a clean export mode that hides deck controls.

For each timed scene define:

- Spoken phrase
- Visual purpose
- Slide or crop source
- Entrance action
- Continuous motion while held
- Exit or cut type
- Sync anchor and tolerance

Use real product screenshots at or above delivery resolution. Prefer full-bleed crops, UI focus boxes, diagrams, large typography, and real workflow states over repeated text-only slides.

For a spoken domain, show a domain input animation. Type at 7–10 characters per second and hold the completed domain for at least 0.6 seconds.

## 6. Keep motion active but comfortable

Change scenes when the narration changes idea. Add motion inside held scenes instead of adding unrelated cuts.

Default motion budget:

- Main scene: 1.4–3.2 seconds
- Complex product UI: 2.0–4.0 seconds
- Punch insert: 0.7–1.1 seconds, never more than two consecutively
- Slow push: 2–5% across the full scene
- Horizontal drift: 1–3% of frame width
- Transition: 4–10 frames; prefer hard semantic cuts, soft wipes, or matched motion

Avoid whole-video time stretching. Keep video retiming within 3%. When mismatch is larger, revise scene durations, rewrite the script, or regenerate TTS.

Read `references/pacing-and-motion.md` before implementing the compositor or export script.

## 7. Render cleanly

Capture at delivery resolution or higher. Keep product screenshots at least as large as their final displayed area.

Recommended delivery defaults:

- 1920×1080 or 1080×1920
- 30 fps
- H.264 CRF 14–18, `yuv420p`
- BT.709 color metadata
- AAC 48 kHz, normalized near -16 LUFS with true peak below -1.5 dB

Do not use low bitrate as a proxy for quality. Use quality-based encoding and inspect small UI text after export.

## 8. Verify before delivery

Require all checks:

1. `npm run build` passes.
2. Timeline validation passes with no gaps or overlaps beyond one frame.
3. Product reveal, feature anchors, domain typing, and disclaimer align with TTS.
4. No more than three hard cuts occur inside any two-second window unless intentionally approved.
5. Held scenes retain subtle motion without cropping key content.
6. Full MP4 decode completes with no errors.
7. Final stream is correct resolution, frame rate, color space, and contains audio.
8. Review a contact sheet plus CTA typing start/middle/end frames.

Deliver the research notes, approved voiceover, TTS audio, timeline, Slides project, final MP4, and poster when requested.
