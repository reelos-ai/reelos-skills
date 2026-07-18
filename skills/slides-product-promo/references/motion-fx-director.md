# Motion FX Director

## Contents

- Mission and inputs
- Cinematic FX Mode
- Scene roles and effect stack
- Effect library
- FX Beat Map workflow
- Beat design and selection test
- Comfort and safety

## Mission

Turn the locked narration timeline into a deliberate motion system. Make the film feel premium and memorable while preserving product truth, readability, brand coherence, and deterministic export.

The Motion FX Director owns effect selection and timing. This role does not rewrite unsupported product claims or use motion to hide weak storytelling.

## Required inputs

- Final voiceover and TTS audio
- Phrase timestamps and word timestamps when available
- Semantic `timeline.json`
- Product facts and required disclaimer
- Brand colors, typography, logo, screenshots, video, and UI states
- Delivery size, frame rate, duration, and channel

If a requested effect depends on missing inputs, mark the asset requirement before implementation. Do not pretend a flattened screenshot is a layered UI explosion.

## Cinematic FX Mode

Enable Cinematic FX Mode when the user asks for the strongest effects, launch-film energy, high-impact motion, or a premium product reveal.

Use contrast as the source of impact:

- Select three to five Hero Moments in a 45–60 second film.
- Surround Hero Moments with calmer setup and recovery beats.
- Give each scene at most one hero effect, one supporting motion, and one atmosphere layer.
- Reuse motion grammar, color, and easing so the film feels directed rather than assembled.
- Reserve the strongest visual transformation for product reveal, mechanism proof, or CTA.

## Scene roles

Classify every scene before selecting effects:

| Role | Purpose | Preferred effects |
|---|---|---|
| Hook | Create tension or curiosity | kinetic typography, radar sweep, one-frame signal flash |
| Reveal | Introduce the product or decisive idea | title sheen, zoom-through, screenshot assembly |
| Mechanism | Explain how the system works | path particles, live line draw, exploded UI, ghost cursor |
| Proof | Make evidence or state change visible | gauge, heat grid, before/after wipe, spotlight |
| Transition | Change context without losing orientation | matched motion, whip pan, blur-through |
| CTA | Convert attention into action | domain typing, cursor focus, completion pulse |

## Effect stack

Build every scene with three possible levels:

1. **Hero effect**: the semantic event viewers should remember.
2. **Supporting motion**: guides the eye or explains sequence.
3. **Atmosphere layer**: low-attention texture such as grain, glow, grid, or particles.

Remove an effect when it repeats the same message, competes with spoken content, or has no precise trigger.

## Effect library

### Typography

- Word-level karaoke: highlight the currently spoken word. Require word timestamps or reviewed forced alignment.
- Title sheen: sweep a controlled highlight across the product name or key claim.
- Odometer or split-flap: animate prices, scores, ranks, or milestones into their final value.
- Kinetic typography: let one keyword grow, displace surrounding words, then restore hierarchy.

### Data visualization

- Live line or candlestick draw: reveal the chart left to right with a glowing head point.
- Radar sweep: rotate a sector and illuminate event points when crossed.
- Gauge needle: move to the target with a small overshoot and settle.
- Heat grid: reveal matrix cells by strength, cluster, or spoken sequence.
- Path particles: move points along SVG paths to explain cause, transmission, or flow.

### UI narrative

- Ghost cursor: move, hover, click, drag, select, or type along a real task path.
- Exploded UI: separate prepared interface layers in 2.5D perspective, then reassemble.
- Spotlight: dim the frame and move a circular or rectangular focus region with the explanation.
- Before/after wipe: move a divider across two aligned states.
- Screenshot assembly: fly prepared fragments into a browser or device frame.

### Camera and transition

- Zoom-through: push into a shared region that becomes the next scene.
- Whip pan: use directional displacement and short motion blur over 6–10 frames.
- Signal flash: use one white or brand-color frame at most once or twice per film.
- Blur-through: coordinate blur, scale, and opacity between related views.

### Atmosphere

- Film grain
- Perspective floor grid
- Breathing brand glow
- Map-point pulse
- Low-contrast dust or particles

Atmosphere must remain behind text and product evidence. Keep it low contrast and slow.

## FX Beat Map workflow

1. Mark product name, feature words, contrast words, proof moments, and CTA in the audio timeline.
2. Classify each scene role.
3. Select Hero Moments across the full film before assigning local effects.
4. Choose the lowest-complexity effect that makes each semantic relationship visible.
5. Define exact frames, easing, layers, asset requirements, and fallback in `fx-beat-map.json`.
6. Create a low-resolution animatic or keyframe strip before polishing.
7. Review pacing around every Hero Moment: setup, impact, hold, and recovery.
8. Implement only after the beat map is coherent and feasible.

## Beat design

Every hero effect needs four phases:

- **Setup**: establish the object and viewing direction.
- **Impact**: trigger on the spoken anchor.
- **Hold**: keep the result readable long enough to understand.
- **Recovery**: settle or transition without abrupt visual residue.

Record frame numbers rather than relying only on CSS delay values. Use deterministic time-based animation so browser capture can seek to any frame.

## Selection test

Approve an effect only when all answers are yes:

- Does it clarify the spoken meaning?
- Does it have a precise audio trigger?
- Does it fit the product and brand?
- Can the required assets be prepared at delivery resolution?
- Can it be rendered deterministically?
- Can viewers still read the headline, UI, and disclaimer?

## Comfort and safety

- Keep ordinary scenes between 1.4 and 3.2 seconds.
- Do not exceed three hard cuts in any two-second window.
- Limit signal flashes to one frame and at most two per film.
- Keep important text stable while backgrounds move.
- Avoid simultaneous large-scale zoom, kinetic text, and fast particle motion.
- Do not globally retime video or audio beyond 3%.
- Provide a calmer fallback for expensive or unstable effects.
