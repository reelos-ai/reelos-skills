# 视频生产 SOP

## 一句话原则

先用真实 TTS 音频确定时间，再让 Remotion 画面跟随 timing 文件。

## 设计思想

ReelOS 口播视频生产不是“文章转视频”的机械流程，而是一套内容产品化流程。它要解决三个问题：

1. 把长文章变成观众听得懂、愿意听完的口播。
2. 把口播节奏变成可计算的时间轴。
3. 把时间轴变成稳定、可复用、可验收的 Remotion 工程。

核心设计取向：

- 先审稿，再生成声音，再做画面。不要先画页面再硬塞文案。
- 口播是主线，画面是辅助理解，不抢话、不堆信息。
- 真实音频时长是唯一时间依据，禁止手感估算同步。
- 风格服务内容类型，战略内容默认“战略作战室风”，教学拆解可用“黑板推演风”。
- 每条视频都要留下可复用资产：口播稿、分段脚本、音频、manifest、timing、Remotion 组件、成片。

## 工作流说明

整个流程分成三层：内容层、声音层、画面层。

内容层负责判断“讲什么”和“怎么讲”：

- 读懂原文，不照搬原文。
- 提炼主线、反常识点、关键概念和结尾追问。
- 用口播审稿员风格改写成短句、强节奏、有人味的口播稿。
- 将口播稿拆成 8-12 段，每段只表达一个核心意思。

声音层负责把口播变成真实时间：

- 每段生成独立 TTS 音频。
- 第一段和信息密度高的段落优先放慢，避免开头压迫感。
- 用 `ffprobe` 读取真实音频时长。
- 写入 `manifest.json` 和 `{slug}Timings.ts`。

画面层负责按 timing 做同步表达：

- 每个 `Sequence` 对应一段口播。
- 字幕、标题、图形和转场都从 timing 推导。
- 每屏只突出当前段落的关键词、结构或关系。
- 先导出关键帧目检，再完整 render。

最终验收不看“能不能播放”，而看四件事：

- 内容是否像人在讲，而不是在念文章。
- 声音是否自然，段落是否没有截断。
- 画面是否跟口播同步，重点是否清楚。
- 工程是否可复用，下一条视频能不能沿用同一模式。

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
