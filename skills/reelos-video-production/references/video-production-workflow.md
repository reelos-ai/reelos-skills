# 视频生产 SOP

## 一句话原则

先用真实 TTS 音频确定时间，再让 Remotion 画面跟随 timing 文件。

## 内容处理

1. 读原文，提炼主旨、受众、核心概念和结尾追问。
2. 删除引用来源、重复论证、过长背景和表格细节。
3. 改成镜头前能讲的口播稿。
4. 拆成 8-12 段，每段只讲一个意思。

## 文件命名

假设合成名是 `ProductionControl`，slug 是 `production-control`：

| 类型 | 路径 |
| --- | --- |
| TTS 脚本 | `scripts/generate-production-control-voiceover.mjs` |
| TTS 输出 | `public/voiceover-production-control/` |
| Timing 文件 | `src/compositions/productionControlTimings.ts` |
| Remotion 组件 | `src/compositions/ProductionControl.tsx` |
| 关键帧 | `out/stills/production-control/` |
| 成片 | `out/production-control-war-room-tts.mp4` |

## 制作步骤

1. 写 TTS 脚本，包含 `scenes`、`voiceId`、`emotion`、`slow`。
2. 运行脚本生成音频、`manifest.json` 和 timing。
3. 写 Remotion 组件，导入 timing。
4. 在 `Root.tsx` 注册 Composition。
5. 跑 `npm exec tsc -- --noEmit`。
6. 导出 3-5 张关键帧并目检。
7. 完整 render。
8. 用 `ffprobe` 验证 MP4。
9. 打开 Studio 路径做最终确认。

## 常用命令

```bash
source ~/.zshrc >/dev/null 2>&1
node scripts/generate-production-control-voiceover.mjs
npm exec tsc -- --noEmit
```

```bash
mkdir -p out/stills/production-control
npx remotion still src/index.ts ProductionControl out/stills/production-control/cover.png --frame=120 --overwrite
npx remotion still src/index.ts ProductionControl out/stills/production-control/final.png --frame=5000 --overwrite
```

```bash
npx remotion render src/index.ts ProductionControl out/production-control-war-room-tts.mp4 --overwrite --crf=18
ffprobe -v error -show_entries format=duration,size -show_streams -of json out/production-control-war-room-tts.mp4
```

## 验收清单

内容：

- 不是文章朗读。
- 开头有钩子。
- 结尾有金句或追问。
- 专业词已经口语化。

音频：

- 第一段不过快。
- 每段没有截断。
- `manifest.json` 有真实时长。
- timing 文件来自脚本自动生成。

画面：

- 文字不重叠、不溢出。
- 每屏只服务当前口播重点。
- 没有丑线框、空洞科技感、模板味。
- 色彩不过度单一。

工程：

- `Root.tsx` 已注册。
- `tsc` 通过。
- 关键帧已目检。
- `ffprobe` 确认视频流和音频流。
- Studio 能打开 `/{CompositionId}`。
