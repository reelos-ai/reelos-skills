# Product Promo Acceptance Evaluation

Use this evaluation after the final audio, timeline, slides, and rendered MP4 are available. Score the exported artifact, not only the live browser preview.

## Critical gates

Reject the film immediately if any condition is true:

- A product claim, metric, quote, or capability is invented or misleading.
- The final audio differs from the script or timing source used for the visuals.
- The timeline has a gap or overlap larger than one frame.
- Product-name reveal, primary CTA, or disclaimer misses its allowed sync tolerance.
- The CTA, compliance text, or essential UI is unreadable at delivery resolution.
- Audio is missing, clipped, broken, or significantly out of sync.
- The video contains decode errors, unintended black frames, frozen sequences, or missing assets.
- Repeated harsh flashes, extreme camera motion, or global retiming above 3% is present.

## Scored rubric

| Dimension | Weight | Full-score standard |
|---|---:|---|
| Narrative and marketing clarity | 15 | Hook, reveal, mechanism, outcome, and CTA form one understandable argument |
| Audio–visual synchronization | 20 | Product, feature, contrast, data, and CTA actions land on the intended spoken anchors |
| Hero-effect impact | 15 | Three to five memorable moments feel earned, distinct, and product-specific |
| Motion craftsmanship | 15 | Timing, easing, hierarchy, transitions, and recovery feel intentional and polished |
| Product evidence and UI clarity | 10 | Real product states remain legible and support the spoken claims |
| Brand coherence | 10 | Color, type, shape, imagery, and motion grammar feel like one brand system |
| Readability and viewing comfort | 10 | Text remains readable; motion guides attention without fatigue or flashing |
| Technical delivery | 5 | Resolution, frame rate, color, audio, codec, loudness, and full decode are correct |

## Release thresholds

- **90–100**: release Cinematic FX Mode.
- **85–89**: conditionally release standard mode after listed fixes; do not label it cinematic.
- **75–84**: return to motion direction or scene implementation.
- **Below 75**: return to narrative structure and rebuild the weak section.

Additional minimums:

- Audio–visual synchronization: at least 17/20
- Motion craftsmanship: at least 13/15
- Readability and viewing comfort: at least 9/10
- Technical delivery: 5/5

## Four-pass review

### 1. Fact and narrative pass

- Compare every spoken and visible claim with research notes.
- Watch once with effects mentally ignored. Confirm the argument still works.
- Check that the CTA is concrete and supported by the product experience.

### 2. Silent visual pass

- Watch without audio to judge visual hierarchy and pacing.
- Confirm every Hero Moment has setup, impact, hold, and recovery.
- Check that atmosphere never competes with text or UI.
- Inspect whether adjacent scenes repeat the same composition.

### 3. Audio–visual pass

- Watch once without pausing for overall rhythm.
- Review product reveal, feature anchors, contrast words, data changes, and CTA frame by frame.
- Verify karaoke against word timestamps, not perceived sentence timing.
- Confirm domain typing starts and finishes within its specified tolerance.

### 4. Technical pass

- Run build and timeline validation.
- Decode the entire MP4 with FFmpeg.
- Inspect resolution, frame rate, codec, color metadata, duration, and audio stream.
- Run black-frame and repeated-frame checks.
- Measure integrated loudness and true peak.
- Review a contact sheet and 100% crops of dense UI.
- Export CTA typing start, middle, completion, and hold frames.

## Effect-specific acceptance

- Karaoke: no skipped, doubled, or early highlighted words.
- Sheen: title remains readable and the sweep does not clip glyphs.
- Odometer: final number is correct and held long enough to read.
- Data draw: animation direction matches data logic and final chart state.
- Radar: points illuminate when the sweep crosses them.
- Gauge: needle lands on the correct value without excessive oscillation.
- Path particles: direction and destination match the narrated relationship.
- Ghost cursor: path is plausible and clicks land on real controls.
- Exploded UI: layers preserve spatial logic and reassemble cleanly.
- Spotlight: the focus region never hides the item being explained.
- Zoom-through: entry and exit share a convincing visual anchor.
- Whip pan: blur resolves to a sharp next frame within ten frames.
- Flash: exactly one frame unless explicitly approved otherwise.

## Rework loop

1. List defects by dimension and timestamp.
2. Fix critical gates before score improvements.
3. Fix the lowest-scoring high-weight dimension next.
4. Re-render affected scenes and regenerate the contact sheet.
5. Re-score from the exported MP4.
6. Repeat until the release threshold and minimum category scores pass.
