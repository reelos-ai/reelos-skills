---
name: reelos-video-production
description: Use when turning Chinese articles, pasted text, links, or long-form viewpoints into ReelOS-style narrated Remotion videos, especially when the user asks for 口播视频, TTS, 音画同步, 视觉设计师, 战略作战室风, 黑板推演风, or a stable repeatable video production workflow.
---

# ReelOS 口播视频生产

## 核心定位

把中文文章、链接、粘贴文本或观点稿做成稳定可复用的 Remotion 口播视频。核心原则是：先把内容审成适合真人讲述的口播稿，再生成真实 TTS 音频，用真实音频时长反写 timing，然后由视觉设计师绑定设计上下文、色板和版式，再由动效导演定义全片运动骨架，最后让 Remotion 画面跟随 timing 文件。

## 设计思想

- 内容先行：视频不是把文章搬上屏幕，而是把观点重构成镜头前能讲清楚的表达。
- 标题先定：口播稿确认后必须生成主标题、副标题和文件名短标题；标题要服务封面、文件检索和发布，不只服务对话回答。
- 声音定时：真实 TTS 音频是节奏基准，画面、字幕、转场都服从音频 timing。
- 一段一意：每个分镜只服务当前口播段落，避免一屏堆多个结论。
- 风格克制：默认做商业推演和教学拆解，不做空洞科技感、丑线框和模板卡片堆叠。
- 真实上下文优先：先学习项目已有视频、截图、配色、组件和用户明确喜欢的版本，再做新设计；既有成功风格是约束，不是参考图。
- 主题入场：讲儒释道、哲学、心理学、AI、投研、品牌时，先识别内容主题，再选择 AI 生成主题图层或可授权素材层，把画面带入对应场域。
- 视觉闭环：视觉设计不止选色，还要输出设计卡、关键帧、动效中间态和修正记录。
- 动效导演：写代码前先定义全片主运动骨架、2-4 个运动章节、每章主运动对象和 TTS 绑定点；动效必须解释内容关系，不做随机装饰。
- 工程可复用：每条视频都沉淀为脚本、音频、timing、组件和验收记录，方便迭代下一条。

## 先读这些参考

按任务需要读取，不要一次塞满上下文：

- `references/setup-dependencies.md`：首次搭建或环境不稳定时必须先读；包含程序、环境变量、基础 skills 和本 skill 的安装顺序。
- `references/video-production-workflow.md`：制作新视频时读取；包含设计思想、完整工作流、文件命名、命令、验收清单。
- `references/style-presets.md`：用户要求选风格、换风格、去 AI 味、优化视觉时读取。
- `references/visual-design-system.md`：每次开始 Remotion 合成前读取；包含视觉设计师职责、真实上下文扫描、视觉设计卡、受控配色、字体参考、外部视觉参考提炼、主题节奏和动效设计。
- `references/motion-director.md`：科普、系统模型、因果链路、长视频或用户要求“增强动效/图表动效”时读取；包含 motion brief、运动章节、图表动效语法和动效验收。
- `references/ai-image-layer-prompts.md`：儒释道、哲学、心理学、抽象方法论等主题需要 AI 图片模型生成背景层、金描线稿、主题插图时读取。
- `references/material-sourcing.md`：需要主题素材增强、背景视频、真实纹理或外部素材叠加时读取；包含 Pexels、Pixabay、Coverr 检索策略和启用判断。
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
3. 标题包装：生成主标题、副标题、文件名短标题；主标题抓住信号或核心判断，副标题解释收益或反差，文件名短标题便于查找。
4. 分段脚本：拆成 8-12 段 TTS，每段只讲一个意思；长视频可按内容逻辑扩展到 30-50 段。
5. TTS 生成：用 Giggle 生成源音频，按真实时长做慢速微调。
6. Timing 生成：写入 `{slug}Timings.ts`，作为音画同步唯一来源。
7. 视觉设计：先扫描既有视觉上下文，再产出视觉设计卡，确定风格、色板、主题图层方向、字体层级和场景节奏；AI 主题图层默认作为背景替代，并先离线优化为 1920x1080 JPG/WebP；儒释道、哲学、心理学等抽象主题优先读取 `references/ai-image-layer-prompts.md`，真实场景/产品/新闻素材再读取 `references/material-sourcing.md`。
8. 动效导演：读取 `references/motion-director.md`，产出 motion brief，定义全片主运动骨架、运动章节、每章主运动对象、镜头推进方式、图表动效和 TTS 绑定点。
9. 分镜设计：每段画面只承载当前口播核心信息，同时绑定视觉设计卡和 motion brief。
10. Remotion 合成：用 `Sequence`、`Html5Audio`、`staticFile`、`interpolate`；不用 CSS animation。
11. 视觉与动效审查：导出关键帧和动效中间态，检查文字、遮挡、线框感、AI 味、颜色单调、动效不可见、素材贴图感、信息拥挤和运动骨架是否清楚。
12. 导出验证：导出关键帧、跑 `tsc`、完整 render、用 `ffprobe` 验证音视频流。

## 默认决策

- 默认画幅：1920x1080。
- 默认帧率：30fps。
- 默认音色：使用用户指定或项目既有 voice id。
- 默认情绪：`neutral`。
- 默认推荐风格：战略作战室风。
- 默认推荐色板：墨水经典或靛蓝瓷；AI/科技信号内容可选瑞士克莱因蓝。
- 教学概念拆解可选：黑板推演风。
- 强观点商业内容优先：战略作战室风。

## 必须避免

- 不要直接朗读原文。
- 不要靠人工估算音频时长同步画面。
- 不要把 API key 写入脚本、README、文档或提交历史。
- 不要提交 `node_modules/`、`out/`、`tmp/`、`.env`。
- 不要使用 CSS transition / CSS animation / Tailwind animation。
- 不要做空洞科技感、丑线框、过度渐变、模板化卡片堆叠。
- 不要使用未授权 Pinterest/网页图片；外部图片必须来自免费/可授权素材站或公共版权来源，并在项目里记录来源、作者和许可。
- 不要为了“高级感”机械添加图层；只有内容抽象、文化/宗教/心理/哲学/自然/空间氛围明显，或用户明确要求视觉增强时才启用主题图层。
- 不要让用户随意给一个 hex 后直接混搭；先映射到受控色板，确需自定义时也必须保持一条视频一套主题。
- 不要在没有看旧稿、旧视频、截图或已有组件的情况下重做风格。

## 完成口径

完成视频任务时说明：

- 视频主标题、副标题和文件名短标题。
- 口播分成几段。
- TTS 是否生成。
- timing 是否来自真实音频。
- motion brief 是否完成，主运动骨架和运动章节是什么。
- Remotion 合成 ID。
- 导出 MP4 路径。
- 已跑哪些验证：`tsc`、关键帧、`ffprobe`、Studio 预览。
