# TTS and Timing

Use this reference when generating voiceover, splitting scenes, or writing timing files.

## Scene Packaging

- Split long scripts into 8-20 scenes for typical short/medium videos.
- One scene should express one idea: hook, contrast, definition, example, framework, implication, conclusion.
- Keep scene text speakable. Remove citation clutter, long nested lists, and repeated transitions.
- Store scene metadata near the composition, for example `src/compositions/{slug}Script.ts`.

## TTS Script Pattern

Create `scripts/generate-{slug}-voiceover.py` with:

- `SLUG`
- `VOICE_ID`
- `EMOTION`
- `SPEED`
- `FPS`
- `SCENES`
- `OUT_DIR = public/voiceover-{slug}`
- `TIMING_FILE = src/compositions/{camelSlug}Timings.ts`

The script should:

1. Reuse existing `scene-xx.mp3` when present.
2. Submit missing scenes to Giggle TTS.
3. Poll until completed.
4. Download each MP3.
5. Run `ffprobe` to get exact duration.
6. Write `manifest.json`.
7. Write `{camelSlug}Timings.ts`.

## Timing File Shape

```ts
export type VoiceoverTiming = {
  id: string;
  audio: string;
  text: string;
  startFrame: number;
  durationInFrames: number;
  audioDurationInFrames: number;
  duration: number;
};

export const exampleFps = 30;
export const exampleTotalFrames = 0;
export const exampleTimings: VoiceoverTiming[] = [] as const;
```

Rules:

- `audioDurationInFrames = round(duration * FPS)`.
- `durationInFrames = audioDurationInFrames + FPS` unless the scene needs a longer visual hold.
- `startFrame` is cumulative.
- Remotion scenes should read timing; do not hardcode final timing in components.

## Audio in Remotion

Use a separate `Sequence` per audio scene:

```tsx
<Sequence from={timing.startFrame} durationInFrames={timing.audioDurationInFrames} layout="none">
  <Audio src={staticFile(timing.audio)} volume={1} />
</Sequence>
```

Use low background music volume for narration videos, normally `0.10-0.22`.
