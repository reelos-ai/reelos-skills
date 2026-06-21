# Remotion Patterns

Use this reference when adding or changing Remotion compositions.

## Composition Registration

Add a component in `src/compositions/{CompositionId}.tsx`, export total frames, then register in `src/Root.tsx`:

```tsx
<Composition
  id="CompositionId"
  component={CompositionId}
  durationInFrames={compositionTotalFrames}
  fps={30}
  width={1920}
  height={1080}
/>
```

Add npm scripts when useful:

```json
"render:slug": "remotion render src/index.ts CompositionId out/slug.mp4 --codec h264 --pixel-format yuv420p --crf 18"
```

## Font Loading

Use local fonts from `public/fonts`. For Chinese text, prefer local Noto Sans SC or Microsoft YaHei. Wait for fonts:

```tsx
const [handle] = React.useState(() => delayRender('Waiting for fonts'));
React.useEffect(() => {
  document.fonts.ready.then(() => continueRender(handle));
}, [handle]);
```

Use `@font-face` in the composition:

```tsx
<style>{`
  @font-face {
    font-family: "Noto Sans SC Local";
    src: url("${staticFile('fonts/NotoSansSC-VariableFont_wght.ttf')}") format("truetype");
    font-weight: 100 900;
  }
`}</style>
```

## Text Rendering

For readable Chinese over video:

- use high contrast fill
- use hard black stroke
- set `paintOrder: 'stroke fill'`
- avoid large blurred shadows
- add a dark backing strip for karaoke subtitles
- keep line height around `1.25-1.45`

## Animation

Use Remotion frame math:

- `useCurrentFrame()`
- `useVideoConfig()`
- `interpolate()`
- `spring()`
- `Sequence`
- `Loop`

Do not use CSS animation or transition. They are not reliable for deterministic video rendering.

## Still Review

Export stills before full render:

```bash
npx remotion still src/index.ts CompositionId out/stills/slug-0120.png --frame=120
```

Pick frames that show:

- cover/title
- high information density
- middle scene
- final frame
