---
name: reelos-video-production
description: Use when turning Chinese articles, pasted text, links, or long-form viewpoints into ReelOS-style narrated Remotion videos, especially when the user asks for 口播视频, TTS, 音画同步, 战略作战室风, 黑板推演风, or a stable repeatable video production workflow.
---

# ReelOS 口播视频生产

## 核心定位

把中文文章、链接、粘贴文本或观点稿做成稳定可复用的 Remotion 口播视频。核心原则是：先把内容审成适合真人讲述的口播稿，再生成真实 TTS 音频，用真实音频时长反写 timing，最后让 Remotion 画面跟随 timing 文件。

## 先读这些参考

按任务需要读取，不要一次塞满上下文：

- `references/setup-dependencies.md`：首次搭建或环境不稳定时必须先读；包含程序、环境变量、基础 skills 和本 skill 的安装顺序。
- `references/video-production-workflow.md`：制作新视频时读取；包含完整 SOP、文件命名、命令、验收清单。
- `references/style-presets.md`：用户要求选风格、换风格、去 AI 味、优化视觉时读取。
- `references/tts-remotion-pattern.md`：新增 TTS 脚本、timing 文件或 Remotion 合成时读取。

## 使用前置条件

如果用户是在一个新机器、新项目或新 Codex 会话里第一次使用这个 skill，先检查依赖。必须确认：

- 本机有 Node.js、npm、ffmpeg、ffprobe。
- Remotion 项目能运行 `npm run studio` 或 `npx remotion studio`。
- 已设置 `GIGGLE_API_KEY`，不要把 key 写入代码或文档。
- 已安装并可用这些基础 skills：`koubo-shengao-yuan`、`giggle-generation-speech`、`remotion-best-practices`、`reelos-design`。
- 如需 ReelOS 品牌正文配图，再安装 `reelos-jinghuan-illustrations`。

如果缺依赖，先按 `references/setup-dependencies.md` 引导安装，再继续制作视频。

## 标准工作流

1. 内容理解：提炼主旨、目标观众、关键概念、逻辑骨架和结尾追问。
2. 口播审稿：把书面稿改成自然、短句、有停顿、有情绪的自媒体口播。
3. 分段脚本：拆成 8-12 段 TTS，每段只讲一个意思。
4. TTS 生成：用 Giggle 生成源音频，按真实时长做慢速微调。
5. Timing 生成：写入 `{slug}Timings.ts`，作为音画同步唯一来源。
6. 分镜设计：每段画面只承载当前口播核心信息。
7. Remotion 合成：用 `Sequence`、`Html5Audio`、`staticFile`、`interpolate`；不用 CSS animation。
8. 视觉审查：检查文字、遮挡、线框感、AI 味、颜色单调和信息拥挤。
9. 导出验证：导出关键帧、跑 `tsc`、完整 render、用 `ffprobe` 验证音视频流。

## 默认决策

- 默认画幅：1920x1080。
- 默认帧率：30fps。
- 默认音色：使用用户指定或项目既有 voice id。
- 默认情绪：`neutral`。
- 默认推荐风格：战略作战室风。
- 教学概念拆解可选：黑板推演风。
- 强观点商业内容优先：战略作战室风。

## 必须避免

- 不要直接朗读原文。
- 不要靠人工估算音频时长同步画面。
- 不要把 API key 写入脚本、README、文档或提交历史。
- 不要提交 `node_modules/`、`out/`、`tmp/`、`.env`。
- 不要使用 CSS transition / CSS animation / Tailwind animation。
- 不要做空洞科技感、丑线框、过度渐变、模板化卡片堆叠。

## 完成口径

完成视频任务时说明：

- 口播分成几段。
- TTS 是否生成。
- timing 是否来自真实音频。
- Remotion 合成 ID。
- 导出 MP4 路径。
- 已跑哪些验证：`tsc`、关键帧、`ffprobe`、Studio 预览。
