# TTS 与 Remotion 同步模式

## TTS 脚本结构

每条视频一个脚本：

```text
scripts/generate-{slug}-voiceover.mjs
```

脚本必须做这些事：

1. 定义 `voiceId`、`emotion`、`fps`。
2. 定义 `scenes`，每段包含 `id`、`text`、`slow`。
3. 调用 TTS API 生成源 MP3。
4. 用 `ffprobe` 读取源音频真实时长。
5. 用 `ffmpeg` 调整到目标时长。
6. 输出最终音频到 `public/voiceover-{slug}/scene-xx.mp3`。
7. 写 `public/voiceover-{slug}/manifest.json`。
8. 写 `src/compositions/{camelSlug}Timings.ts`。

## Timing 文件结构

```ts
export const productionControlTotalFrames = 5520;
export const productionControlTargets = [18, 20, 18];
export const productionControlSceneStarts = [0, 19, 40];
export const productionControlSceneDurations = [19, 21, 19];
```

规则：

- `Targets` 是真实 TTS 播放秒数。
- `SceneDurations` 通常比 target 多 1 秒。
- `TotalFrames = totalSeconds * 30`。
- Remotion 组件只读 timing，不手写时长。

## Remotion 组件结构

```tsx
const voiceoverScenes = targets.map((duration, index) => ({
  from: sceneStarts[index] + 0.45,
  duration,
  src: `voiceover-slug/scene-${String(index + 1).padStart(2, "0")}.mp3`,
}));
```

画面：

```tsx
<Sequence from={secondsToFrames(sceneStarts[index])} durationInFrames={secondsToFrames(sceneDurations[index])}>
  <Scene scene={scene} />
</Sequence>
```

音频：

```tsx
<Sequence from={secondsToFrames(audio.from)} durationInFrames={secondsToFrames(audio.duration)} layout="none">
  <Html5Audio src={staticFile(audio.src)} volume={1} />
</Sequence>
```

## Remotion 约束

- 用 `useCurrentFrame()` 和 `interpolate()` 做动画。
- 用 `Sequence` 控制时间。
- 用 `staticFile()` 引用 public 资产。
- 不使用 CSS transition。
- 不使用 CSS animation。
- 不使用 Tailwind animation。

## 语速调节

第一段默认更慢：

```js
slow: 1.05
```

如果第一段仍快，调到 `1.08`，或拆成两段。

重新用已有源音频调速：

```bash
node scripts/generate-{slug}-voiceover.mjs --refit-existing
```
