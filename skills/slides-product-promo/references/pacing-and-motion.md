# Pacing and motion

## Scene changes

- Cut on a new idea, product state, or spoken anchor—not on every comma.
- Keep ordinary scenes between 1.4 and 3.2 seconds.
- Give dense UI 2–4 seconds with a focus box or crop.
- Use 0.7–1.1 second inserts for emphasis only.
- Avoid more than three hard cuts in any two-second window.
- Avoid repeating the same layout in adjacent scenes.

## Motion inside held scenes

Use one primary and at most one secondary motion idea:

- Slow centered push of 2–5%
- Horizontal or vertical drift of 1–3%
- Scan line lasting 1.5–3 seconds
- Focus box draw or glow pulse
- Counter, ticker, path draw, or low-contrast particles
- Domain typing at 7–10 characters per second

Keep text stable while backgrounds move. Do not pan far enough to crop headlines, logos, CTA buttons, or compliance text.

## Transitions

- Prefer direct semantic cuts when narration changes topic.
- Use matched pan, short blur-through, or 4–10 frame wipe between related UI views.
- Use flashes only for deliberate signal shocks, at most one frame, and never repeatedly.
- Do not add movement merely because a scene is long; motion must preserve readability.

## Clarity

- Capture text and UI at native output size or higher.
- Never enlarge a screenshot beyond its useful source resolution without accepting softness.
- Use CRF-based output, BT.709 metadata, and inspect real exported frames at 100%.
- Keep body text large enough to survive H.264 chroma subsampling.

## Repairing duration mismatch

1. Reassign held-scene duration within natural phrase boundaries.
2. Add meaningful internal motion.
3. Add a source-backed visual beat.
4. Rewrite or shorten the voiceover.
5. Regenerate TTS.

Do not globally slow the video by more than 3% to fit narration.
