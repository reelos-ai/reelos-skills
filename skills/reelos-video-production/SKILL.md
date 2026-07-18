---
name: reelos-video-production
description: Use when turning Chinese articles, pasted text, links, or long-form viewpoints into ReelOS-style narrated Remotion videos or Slide Story decks, especially for 口播视频, TTS, 音画同步, 视觉设计师, 自动动效导演, 语义动效评分, ReelOS SketchTalk, Slide Story, slides/deck mode, 演示型口播视频, 路演式视频, 互动演示, 演示稿与视频双交付, or a stable repeatable video production workflow.
---

# ReelOS 口播视频生产

## 核心定位

把中文文章、链接、粘贴文本或观点稿做成稳定可复用的 Remotion 口播视频。核心原则是：先把内容审成适合真人讲述的口播稿，再生成真实 TTS 音频，用真实音频时长反写 timing，然后由视觉设计师绑定设计上下文、色板和版式，再由动效导演定义全片运动骨架，最后让 Remotion 画面跟随 timing 文件。

## 模式路由

### 入口决策顺序

每次只选择一个主模式。按以下顺序判定，不要只凭单个关键词猜测：

1. **显式模式**：用户明确说 `Slide Story`、`SketchTalk` 或某个既有模板名时，优先采用该模式。
2. **交付物**：先确认用户要 `Web 演示`、`MP4 视频`，还是两者都要；交付物不明确但用户说“制作视频”时，默认 MP4。
3. **内容形态**：章节式商业讲解、产品宣传、路演、教学拆解优先 Slide Story；强观点、哲思、个人认知、黑红白大字优先 SketchTalk；其余进入标准口播视频。
4. **冲突消解**：显式模式高于内容风格；交付物高于视觉关键词；主题只决定视觉系统，不自动改变主模式。

| 用户意图 | 主模式 | 默认路由 |
| --- | --- | --- |
| “用 slide/Slide Story/演示页做” | Slide Story | `slides-video`；明确要演示链接时改为 `slides-web` |
| “同时给我演示稿和视频” | Slide Story | `slides-dual` |
| “空见心力/黑红白/强观点大字/beat 字幕” | SketchTalk | MP4 |
| “制作口播视频”，没有模式词 | 标准口播视频 | MP4 |
| 只说“整理成 PPT/大纲”，未要求可播放 Deck 或视频 | 不进入 Slide Story | 先完成内容整理 |

如果用户同时要求 Slide Story 和 SketchTalk，以显式交付物为准：需要演示页结构时用 Slide Story，并把黑红白作为主题 token；需要竖屏强观点口播时用 SketchTalk，不套演示页模板。

### Slide Story 演示叙事模式

当用户出现以下任一表达时，读取 `references/slide-story-mode.md`：

- `Slide Story`、`slide 模式`、`slides 模式`
- `演示型口播视频`、`幻灯片讲解模式`、`路演式视频`
- `生成互动演示`、`响应式幻灯片`
- `同时生成演示稿和视频`
- 要求使用 Cover、Split、Bento、Steps、Comparison、Timeline 等演示页语法讲述内容

不要仅因输入里出现 `PPT`、`页面`、`卡片`、`截图` 或“参考某个演示”就自动进入；必须同时存在演示式叙事、可播放 Deck、路演/讲解视频或明确的 Slide Story 交付意图。

先判断输出目标：

- `slides-web`：输出可交互的响应式 React 演示稿，适合现场演讲、屏幕分享和链接传播。
- `slides-video`：输出 Remotion 口播视频，使用 Slide Story 视觉语法，但动画必须由真实 TTS timing 和 Remotion 帧驱动。
- `slides-dual`：先生成共享内容规划，再同时输出 Web 演示和 MP4 视频。

再选择模板。读取 `references/slide-story-templates.md`，按时长、受众和叙事任务选择稳定模板 ID；不要从空白布局列表临时拼装整条片。

硬性边界：

- Web Deck 可以使用点击 Build、Presenter、Annotation 和响应式重排。
- Remotion 不直接引入 Framer Motion、浏览器点击状态、`localStorage`、`BroadcastChannel` 或 CSS animation。
- 视频中的 `Build` 必须转译为 TTS cue，`Reveal` 必须转译为 `interpolate` / `spring`。
- 一页只讲一个判断；相邻两页不得重复同一种构图。
- 真实网站、品牌或产品必须使用可核验的文案、颜色和界面，不得把模板示例数据当成真实数据。

### SketchTalk 强观点口播视频模式

当用户出现以下任一表达时，直接启用 SketchTalk 视频模式：

- `ReelOS SketchTalk`
- `SketchTalk 强观点口播风`
- `黑红白强观点哲思风`
- `白底黑红`
- `强观点大字`
- `底部隐喻图`
- `beat 字幕`
- `空见心力`
- 要求参考“深度进化 Theo”这类白底、黑红、强观点、极简隐喻图的竖屏观点视频

执行路径：

1. 如果输入是长文章、书面稿或粗稿，先用 `koubo-shengao-yuan` 审成口播稿；如果用户已经给出确认稿，以用户稿为准。
2. 用 SketchTalk 视觉语法设计封面、字体层级、底部隐喻图和 footer 关键词；必要时读取 `reelos-sketchtalk` 的 layout/metaphor 规则。
3. 仍由 `reelos-video-production` 负责 TTS、真实音频 timing、Beat Motion Map、Remotion 合成、关键帧审查、MP4 导出和验证。

硬性要求：

- 第一帧必须是可直接当封面的完整画面，不要从空白或半入场开始。
- 默认画面语言是白底、黑、暖红、灰；不要引入额外高饱和色。
- 文案层级必须去重：顶部红色命题句负责场景/问题提示，中间主 beat 负责当前口播短句，底部辅助只做方法名、章节名或进度提示。
- 主 beat 字幕必须比封面主标题低一级，不能压住底部隐喻图。
- 底部隐喻图必须随口播 beat 发生轻微变化，例如路径显影、红点激活、节点状态变化、2%-4% 微缩放或轻微位移。
- 用户修改口播稿后，必须重跑 TTS、manifest/timing、Beat Motion Map、主字幕、footer 和隐喻图状态；不能复用旧音频硬凑新稿。
- beat 字幕和画面动作以真实音频 timing 校准；如果发现偏差，优先调整 cue offset，而不是靠视觉猜时长。

## 设计思想

- 内容先行：视频不是把文章搬上屏幕，而是把观点重构成镜头前能讲清楚的表达。
- 标题先定：口播稿确认后必须生成主标题、副标题和文件名短标题；标题要服务封面、文件检索和发布，不只服务对话回答。
- 声音定时：真实 TTS 音频是节奏基准，画面、字幕、转场都服从音频 timing。
- 一段一意：每个分镜只服务当前口播段落，避免一屏堆多个结论。
- 风格克制：默认做商业推演和教学拆解，不做空洞科技感、丑线框和模板卡片堆叠。
- 真实上下文优先：先学习项目已有视频、截图、配色、组件和用户明确喜欢的版本，再做新设计；既有成功风格是约束，不是参考图。
- 主题入场：讲儒释道、哲学、心理学、AI、投研、品牌时，先识别内容主题，再选择 AI 生成主题图层或可授权素材层，把画面带入对应场域。
- 视觉闭环：视觉设计不止选色，还要输出设计卡、关键帧、动效中间态和修正记录。
- 动效导演：写代码前先定义全片主运动骨架、2-4 个运动章节、每章主运动对象、TTS 绑定点和 Beat Motion Map；动效必须解释内容关系，不做随机装饰。
- 自动择效：复杂口播、科普、产品宣传、SketchTalk 和 `slides-video` 默认启用自动动效导演；每个 beat 先做语义分类，再生成候选、评分择优和去重复，不以“动得多”代替“讲得清”。
- 工程可复用：每条视频都沉淀为脚本、音频、timing、组件和验收记录，方便迭代下一条。

## 先读这些参考

按任务需要读取，不要一次塞满上下文：

- `references/setup-dependencies.md`：首次搭建或环境不稳定时必须先读；包含程序、环境变量、基础 skills 和本 skill 的安装顺序。
- `references/video-production-workflow.md`：制作新视频时读取；包含设计思想、完整工作流、文件命名、命令、验收清单。
- `references/style-presets.md`：用户要求选风格、换风格、去 AI 味、优化视觉时读取。
- `references/visual-design-system.md`：每次开始 Remotion 合成前读取；包含视觉设计师职责、真实上下文扫描、视觉设计卡、受控配色、字体参考、外部视觉参考提炼、主题节奏和动效设计。
- `references/motion-director.md`：科普、系统模型、因果链路、长视频、SketchTalk 模板或用户要求“增强动效/图表动效”时读取；包含 motion brief、Beat Motion Map、transitions.dev/GSAP 转译规则、图表动效语法和动效验收。
- `references/auto-motion-director.md`：制作科普、产品宣传、SketchTalk、`slides-video`，或用户要求“自动选择最佳动效/多一些可视化”时必须读取；包含语义分类、候选效果、100 分评分、去重复、硬约束和自动返修门槛。
- `references/slide-story-mode.md`：用户要求 Slide Story、互动演示、演示型口播视频、路演式视频或演示稿与视频双目标输出时读取。
- `references/slide-story-templates.md`：进入 Slide Story 后必须读取；包含模板 ID、选择规则、页面槽位、共享 plan 契约和触发示例。
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
9. 自动择效：读取 `references/auto-motion-director.md`，为每个 beat 标注语义类型，生成 2-3 个候选效果并按 100 分制评分；只采用总分不低于 75 的候选，平分时选择更简单、渲染更稳定的方案。
10. Beat Motion Map：把每个 TTS scene 拆成 beat cue，给每个 cue 绑定主字幕、选中的画面动作、候选评分、隐喻图状态和转场方式；SketchTalk、科普和长视频必须做这一步。
11. 分镜设计：每段画面只承载当前口播核心信息，同时绑定视觉设计卡、motion brief 和 Beat Motion Map。
12. Remotion 合成：用 `Sequence`、`Html5Audio`、`staticFile`、`interpolate`、`spring` 和本地 motion preset；不用 CSS animation/transition，不直接引入 GSAP runtime。
13. 自动返修：导出场景边界及 15%/50%/85% 中间帧，检查语义覆盖、连续重复、信息拥挤、空白、首帧和 cue 偏差；按自动动效导演规则降级、替换或重排不合格镜头。
14. 导出验证：跑 `tsc`、完整 render、用 `ffprobe` 验证音视频流，并检查首秒黑帧、全片解码和响度。

## 默认决策

- 默认画幅：1920x1080。
- 默认帧率：30fps。
- 默认音色：使用用户指定或项目既有 voice id。
- 默认情绪：`neutral`。
- 默认推荐风格：战略作战室风。
- 默认开启自动动效导演：适用于 `slides-video`、SketchTalk、科普、产品机制和商业讲解；纯静态 Web Deck 或用户明确要求极简静态时关闭。
- 默认推荐色板：墨水经典或靛蓝瓷；AI/科技信号内容可选瑞士克莱因蓝。
- 教学概念拆解可选：黑板推演风。
- 强观点商业内容优先：战略作战室风。

## 必须避免

- 不要直接朗读原文。
- 不要靠人工估算音频时长同步画面。
- 不要把 API key 写入脚本、README、文档或提交历史。
- 不要提交 `node_modules/`、`out/`、`tmp/`、`.env`。
- 不要使用 CSS transition / CSS animation / Tailwind animation。
- 不要把 transitions.dev 的 CSS snippet 或 GSAP runtime 直接搬进 Remotion 合成；只学习其动效词典、时间线和 easing，再转译为帧驱动 motion preset。
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
- Beat Motion Map 是否完成，字幕 cue、画面动作和隐喻图状态是否绑定到 TTS。
- 自动择效是否完成，采用了哪些语义类型、候选评分和去重复策略；低于 75 分的候选是否已降级或替换。
- Remotion 合成 ID。
- 导出 MP4 路径。
- 已跑哪些验证：`tsc`、关键帧、`ffprobe`、Studio 预览。
