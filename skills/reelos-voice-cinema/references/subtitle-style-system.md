# Subtitle Style System

Use this reference when the user asks for better Chinese subtitles, karaoke/typewriter effects, dynamic text, style options, or comparison samples.

## Principle

The voice and text carry the video. Background footage is atmosphere. Subtitles must be readable first, beautiful second, and animated only when it helps the spoken rhythm.

Default to a mixed strategy, not one fixed style for the whole video:

- base style for normal narration
- flash style for hooks and questions
- quote style for aphorisms and chapter turns
- impact style only for climax lines

## Seven Style Options

### A. Clear Karaoke

Use as the default whole-video subtitle.

- best for long narration
- high contrast white fill
- hard black stroke
- warm gold active words
- local dark backing strip
- steady word-by-word progress

### B. Kinetic Pulse

Use for hooks, rhetorical questions, and the first 3 seconds.

- fast word pulses
- short scale and opacity punches
- stronger tracking or stagger
- keep duration short
- do not use for every sentence

### C. Cinematic Quote

Use for chapter titles, core claims, and memorable lines.

- larger center title
- topic label above
- quiet rule line below
- one or two emphasized words only
- slower reveal than flash

### D. Zen Vertical

Use for philosophy, nature, water, forest, mountain, and calm material.

- vertical keyword columns
- restrained gold accent
- calm center/bottom narration
- generous negative space
- slower motion and lower density

### E. Magazine Editorial

Use for premium documentary, reflective essays, and serious viewpoints.

- lower-third or left-column text block
- editorial label such as `TOPIC`, `SIGNAL`, or `SELF TRAINING`
- thin vertical accent line
- layered dark glass backing
- useful when footage should remain visible

### F. Impact Poster

Use only for climax, final conclusion, or a very strong claim.

- oversized keyword
- short punch phrase under it
- strong scale-in or snap-in
- heavy stroke, minimal blur
- limit to one or two appearances per minute

### G. System Minimal

Use for AI, Agent, method, judgment, and system-thinking content.

- compact labels such as `SIGNAL`, `SYSTEM`, `PROMPT`
- thin gold/cold-white rules
- structured blocks
- less emotional, more precise
- good for ReelOS and AI-native topics

## Recommended Mix

For normal narrated vertical videos:

```text
70% A Clear Karaoke
10% B Kinetic Pulse
10% C Cinematic Quote
5% E Magazine Editorial
5% F Impact Poster
```

For calm philosophy or nature videos:

```text
65% A Clear Karaoke
15% D Zen Vertical
10% C Cinematic Quote
10% E Magazine Editorial
```

For AI/Agent/signal videos:

```text
55% A Clear Karaoke
20% G System Minimal
15% B Kinetic Pulse
10% C Cinematic Quote
```

## Rendering Rules

- Use Remotion frame math: `useCurrentFrame()`, `interpolate()`, `spring()`, `Sequence`.
- Do not use CSS animation or transition for subtitle motion.
- Keep Chinese text sharp: `paintOrder: 'stroke fill'`, hard stroke, and no large blur shadow.
- Put a translucent layer behind text only where needed; keep the background footage visible.
- Avoid fake 3D bevels, excessive glow, and stacked blurry shadows.
- Preserve safe areas for app header/footer controls in vertical preview.

## Comparison Samples

When the user asks to choose a style, generate a style board and short sample videos:

- one still board with all options
- one 6-10 second vertical MP4 per option
- same sentence, same background, same duration
- validate each sample with `ffprobe`

Recommended output names:

```text
out/stills/{slug}-subtitle-style-board.png
out/subtitle-styles/01-clear-karaoke.mp4
out/subtitle-styles/02-kinetic-pulse.mp4
out/subtitle-styles/03-cinematic-quote.mp4
out/subtitle-styles/04-zen-vertical.mp4
out/subtitle-styles/05-magazine-lower-third.mp4
out/subtitle-styles/06-impact-poster.mp4
out/subtitle-styles/07-system-minimal.mp4
```
