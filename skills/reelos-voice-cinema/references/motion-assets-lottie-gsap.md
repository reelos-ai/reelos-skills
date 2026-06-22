# Lottie and GSAP Motion Assets

Use this reference when ReelOS Voice Cinema needs animated icons, signal pulses, system cores, kinetic typography planning, reusable motion assets, or a more advanced motion language.

## Role in Voice Cinema

Voice Cinema videos should remain audio/subtitle-led. Lottie and GSAP-derived motion are supporting layers:

- Lottie: portable deterministic JSON assets loaded into Remotion or used as reusable overlays.
- GSAP: motion design grammar for sequencing, easing, stagger, and prototypes.
- Remotion: final renderer and timing source for MP4 export.

Do not let decorative motion compete with narration readability.

## Lottie Integration

Use Lottie for:

- signal pulses
- icon loops
- seal/stamp animations
- brush strokes
- loading/system cores
- subtle particles or HUD accents
- reusable transition marks

Good Lottie asset rules:

- keep assets short, usually 1-4 seconds
- expose useful slots when authoring raw JSON: background color, accent color, opacity, scale, or text
- avoid huge image-heavy JSON for long backgrounds
- keep alpha-friendly overlays when possible
- verify the JSON in a Lottie/Skottie viewer before relying on it in Remotion

Recommended project locations:

```text
public/lottie/{slug}/{asset-name}.json
public/lottie/{slug}/preview/
src/compositions/{CompositionId}.tsx
```

When using the `text-to-lottie` skill directly, follow its player layout:

```text
public/projects/{project-slug}/scene-{N}/lottie.json
public/projects/{project-slug}/scene-{N}/controls.json
```

For final Voice Cinema projects, copy verified `lottie.json` files into `public/lottie/...` and load them from Remotion.

## GSAP Integration

Use GSAP knowledge for:

- timeline choreography
- staggered text entrances
- easing selection
- interactive or browser prototype previews
- transforming a loose motion idea into exact beats

For final Remotion rendering, prefer converting GSAP concepts into frame math:

```text
gsap.timeline label     -> scene beat / frame offset
duration seconds        -> durationInFrames
ease power3.out         -> interpolate easing or spring config
stagger 0.08            -> per-word/per-item frame offset
x/y/scale/rotation      -> transform values from interpolate()
autoAlpha               -> opacity + optional display logic
```

Do not rely on GSAP's runtime clock for final MP4 rendering unless the host project has a proven deterministic setup. The safe default is: prototype with GSAP, render with Remotion.

## Motion Recipes

### Signal Pulse

- Use Lottie for a loopable ring or waveform.
- Bind opacity/scale to the scene beat in Remotion.
- Keep it behind subtitles or near the keyword, not across the whole screen.

### Kinetic Word Burst

- Use GSAP-style stagger planning.
- In Remotion, compute each word's local frame offset.
- Animate only transform and opacity.
- Keep hard text stroke and backing layer for Chinese readability.

### System Core Activation

- Use a Lottie core loop for the center object.
- Add Remotion labels, data lines, or module cards around it.
- Use GSAP timeline concepts for reveal order: core -> orbit labels -> final lockup.

### Editorial Transition Mark

- Use a short Lottie stroke, seal, or line draw.
- Place it between scenes or above a chapter title.
- Keep duration under 45 frames at 30fps unless it carries meaning.

## Performance and Quality Gates

- Prefer transform and opacity over layout-heavy motion.
- Avoid animating hundreds of DOM nodes at once.
- Keep Lottie file sizes modest; inspect heavy image assets.
- Export stills at dense text frames and motion peaks.
- Validate final MP4 with `ffprobe`.

## When Not to Use

- Do not add Lottie/GSAP motion to every line of a narration video.
- Do not replace clear karaoke captions with decorative animated text for long-form content.
- Do not use fake HUD clutter just because the subject is AI.
- Do not use CSS animation or transition for final Remotion output.
