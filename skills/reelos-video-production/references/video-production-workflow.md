# 视频生产工作流

## 一句话原则

先用真实 TTS 音频确定时间，再让 Remotion 画面跟随 timing 文件。内容、声音、视觉、动效、特效、工程、验收七层必须按顺序生产，不能先做画面再硬塞口播，也不能没做 motion brief 和 VFXEnhancementPlan 就随手堆动画。

## 设计思想

ReelOS 口播视频生产不是“文章转视频”的机械流程，而是一套内容产品化流程。它要解决三个问题：

1. 把长文章、链接或粘贴文本变成观众听得懂、愿意听完的口播。
2. 把口播节奏变成可计算、可复用、可验证的时间轴。
3. 把时间轴变成稳定、可维护、可迭代的 Remotion 工程。
4. 把复杂概念变成可见的运动关系，让观众通过图表动效理解内容。

核心设计取向：

- 内容先行：先判断观点和结构，再写口播，不照搬文章段落。
- 标题包装：口播稿确认后必须生成主标题、副标题和文件名短标题，用于封面、发布和本地检索。
- 声音定时：真实 TTS 音频是唯一节奏基准，画面服从声音。
- 一段一意：每个场景只讲一个核心意思，避免一屏多个结论。
- 视觉先定：写 Remotion 组件前先检查真实视觉上下文，再确定风格、主题色板、明暗节奏和动效主语。
- 动效导演：科普、系统模型和长视频必须先产出 motion brief，明确主运动骨架、运动章节、每章主运动对象和 TTS 绑定点。
- 特效师强化：自动择效后由 VFX Supervisor 定义英雄时刻、强度曲线、效果预算、镜头连续性和重特效 fallback，让“更酷”成为可审计方案而不是随机堆叠。
- 终审闭环：交付前用静帧、低清全片、四种观看模式、100 分评分和硬门槛验收；最多两轮定向返修，仍不稳定则降级。
- 设计绑定：用户认可过的旧风格、截图反馈、已有组件和受控色板是约束，不是可有可无的参考。
- 视觉克制：做商业推演、教学拆解和认知表达，不做空洞科技感。
- 工程沉淀：每条视频都留下脚本、音频、manifest、timing、组件和成片，方便下一条复用。

## 输入与输出

### 输入

支持三种输入：

| 输入类型 | 示例 | 处理方式 |
| --- | --- | --- |
| URL | 文章链接、博客链接 | 先读取内容，再提炼观点 |
| 粘贴文本 | 用户直接贴长文 | 先审稿，再重写口播 |
| 已写口播稿 | 用户给出完整口播 | 以用户稿为准，只做结构校正、分段、TTS 和 timing |

用户在成片后修改口播稿时，必须按完整链路重跑：更新 TTS scenes → 重新生成音频 → 重新生成 manifest/timing → 按新 timing 更新 beat cue、画面字幕和隐喻图 → 重新导出关键帧和 MP4。不能只改屏幕文字，也不能复用旧音频硬凑新稿。

### 输出

每次完整生产至少应输出：

| 产物 | 位置 | 说明 |
| --- | --- | --- |
| 口播稿 | 对话或项目文档 | 人能直接念的版本 |
| 标题包装 | 对话或项目文档 | 主标题、副标题、文件名短标题 |
| TTS 脚本 | `scripts/generate-{slug}-voiceover.mjs` | scenes、voiceId、slow、emotion |
| 音频文件 | `public/voiceover-{slug}/scene-xx.mp3` | 每段独立音频 |
| 音频 manifest | `public/voiceover-{slug}/manifest.json` | 真实时长、文件名、段落元数据 |
| timing 文件 | `src/compositions/{slug}Timings.ts` | Remotion 唯一时间来源 |
| 动效决策 | `MotionDecisionPlan` | 语义候选、评分、去重复与选中动作 |
| 特效强化 | `VFXEnhancementPlan` | 英雄时刻、特效预算、强度、连续性与 fallback |
| Remotion 组件 | `src/compositions/{CompositionId}.tsx` | 画面和动画 |
| Composition 注册 | `src/Root.tsx` 或项目实际入口 | 注册可渲染视频 |
| 关键帧 | `out/stills/{slug}/` | 视觉审查 |
| 低清预览 | `out/previews/{slug}-review.mp4` | 完整节奏与连续性审片 |
| MP4 成片 | `out/{slug}.mp4` | 最终交付 |
| 终审报告 | `FinalAcceptanceReport.md` | 评分、硬门槛、返修与技术验证记录 |

## 七层工作流

### 1. 内容层

目标：把原文变成口播。

步骤：

1. 读懂原文，提炼主旨、受众、核心概念、情绪和结尾追问。
2. 删除原文里的引用来源、重复论证、过长背景和表格细节。
3. 把书面语改成口语化表达：短句、停顿、设问、反问、感叹和转折。
4. 按“开头钩子 → 关键问题 → 分点讲解 → 总结金句 → 互动追问”重排结构。
5. 拆成 8-12 段，每段只表达一个核心意思。
6. 生成标题包装：主标题抓住核心判断，副标题解释观众收益或内容反差，文件名短标题用 2-6 个英文或拼音词便于检索。

判断标准：

- 开头 10 秒内能让人知道为什么要听。
- 每段能单独概括成一句话。
- 专业概念有生活化解释。
- 不是原文朗读。

### 2. 声音层

目标：把口播变成真实时间。

步骤：

1. 写 TTS 生成脚本，定义 `scenes`。
2. 配置 `voiceId`、`emotion`、`slow` 和输出目录。
3. 调用 Giggle TTS 生成每段独立 MP3。
4. 用 `ffprobe` 读取每段真实时长。
5. 写入 `manifest.json`。
6. 根据真实时长生成 `{slug}Timings.ts`。

注意：

- 第一段通常需要稍慢，因为开头信息密度最高。
- 不要用字数估算时长。
- 不要手动硬改 `durationInFrames` 去凑画面。
- 如果某段被截断，优先重生成音频或增加缓冲。

### 3. 视觉层

目标：先由视觉设计师环节绑定视觉系统，再为动效导演提供稳定画面约束。

步骤：

1. 读取 `references/visual-design-system.md`。
2. 扫描真实视觉上下文：用户反馈、旧截图、旧 Composition、旧关键帧、已有组件。
3. 产出视觉设计卡：上下文结论、视觉基调、推荐色板、字体层级、主题节奏、禁用方向。
4. 为每段口播设计一个画面任务，例如提出问题、展示结构、强调关键词、画出关系。
5. 把视觉设计卡交给动效导演，不在视觉层直接发明随机动画。

SketchTalk 类竖屏观点视频的额外要求：

- 必须单独设计封面 Composition 或封面帧，不直接截视频中间帧当封面。
- 第一帧必须是可直接当封面的静态封面，不要让视频从空白或半入场状态开始。
- 封面采用“红色命题句 + 粗黑主观点 + 英文副标 + 底部极简隐喻图”的结构；主观点可以比视频内 beat 字幕更大。
- 视频内 beat 字幕不是封面标题，字号要降一级，保留冲击力但不能压住底部隐喻图。
- 视频内信息三层必须去重：上方红色命题句只做场景/问题提示，中间主 beat 承担当前口播强观点，底部辅助字幕只做方法提示和 beat 进度。不要让三层同时重复同一句话。
- 底部隐喻图必须跟随口播短句有轻微变化，例如位移、线条显影、红点激活、微缩放；不要只做静态摆件。
- 底部隐喻图必须跟当前口播语义一致。用户改稿后如果概念从“云雨伞”变成“事实、原因、行动”，必须同步换图形状态和关键词，不能残留旧隐喻。
- 这类模板默认白底黑红灰，使用暖红作为命题句和视觉锚点，不引入额外高饱和色。

### 4. 动效层

目标：由动效导演把口播逻辑转成可见的运动关系。

步骤：

1. 读取 `references/motion-director.md`。
2. 先写 motion brief：主运动骨架、运动章节、主运动对象、镜头语言、图表动效、TTS timing 绑定。
3. 科普和系统模型优先使用路径追踪、状态转化、变量激活、反馈闭环和分层架构。
4. 长视频拆成 4-6 个运动章节，复用同一套运动语法，不每段换一套规则。
5. 把 scroll/scrub 思想转译成 Remotion scene progress 和 global progress；不用网页滚动状态。
6. 如果使用背景视频或重图层，先确认可预烘焙、可降级、不会明显拖慢 render。
7. 导出 15% / 50% / 85% 中间帧，检查动效是否能看出变化。

动效原则：

- 主运动骨架必须服务理解，例如“观察 → 状态 → 机制 → 干预 → 验果 → 更新”。
- 每段最多一个主运动对象，避免一屏多个动效抢注意力。
- 动效要表达关系变化，不是为了热闹。
- 旧风格被用户确认好时，保留有效动效，只增强运动清晰度、节奏和图表表达。

### 5. 特效层

目标：由特效师把已经选中的语义动作强化成有吸引力、有连续性且可稳定渲染的镜头。

步骤：

1. 读取 `references/vfx-supervisor.md`。
2. 基于 MotionDecisionPlan 生成 VFXEnhancementPlan。
3. 为全片定义强度曲线和效果预算，不允许所有 scene 同时高强度。
4. 每个运动章节选择至多 1 个英雄时刻，明确它服务的内容重音。
5. 为相邻 scene 定义 `continuityIn` / `continuityOut`，至少继承位置、方向、对象、形状、颜色或语义之一。
6. 重特效标记性能等级并准备 fallback；视觉强化不得遮挡真实产品证据。

默认支持文字、数据、界面、镜头和氛围五类特效，包括卡拉 OK、Sheen、翻牌数字、Kinetic Typography、K 线绘制、雷达扫描、仪表盘、热力矩阵、流向粒子、幽灵鼠标、爆炸拆解、聚光灯、分屏擦除、截图拼装、Zoom-through、Whip Pan、单帧闪白和 Blur-through。

特效原则：

- 每幕最多 1 个主特效和 2 个低强度辅助特效。
- 高信息密度 scene 以阅读为主，镜头运动降级。
- 英雄时刻必须有语义，不用粒子、模糊或闪白制造假高潮。
- 纯炫技无语义的运动和超过约 3% 的整片变速不采用。

### 6. 工程层

目标：把视觉设计卡和 motion brief 落到 Remotion 工程。

步骤：

1. 用 `Sequence` 对齐每段 `startFrame` 和 `durationInFrames`。
2. 用 `Html5Audio` 加载真实 TTS 音频。
3. 用 `staticFile()` 引用 `public/` 里的音频和图片。
4. 用 `interpolate()`、`spring()` 和 frame 计算做动画。
5. 导出 3-5 张关键帧和至少 1 张动效中间态做目检。
6. 修正视觉和动效问题后完整 render 成 MP4。
7. 用 `ffprobe` 验证音视频流。

画面原则：

- 每屏只出现当前段落需要理解的信息。
- 字体大小、行高和容器宽度必须保证不溢出。
- 封面标题、视频内 beat 字幕、底部辅助字幕必须是三个层级：封面最大，视频内主字幕次之，底部辅助字幕最弱。
- 视频内不要出现“红色命题句、主 beat、底部辅助字幕”三处重复同一句。推荐职责：红色命题句=场景提示，主 beat=当前原文短句，底部辅助=方法名 + `01-05` 这类进度。
- 如果主字幕像封面标题一样压迫画面，优先缩小 10%-15%，并增加左右安全边距。
- 一条视频只用一套受控色板，不临时混搭多个高饱和色；但每一屏都必须通过构图、明暗比例、信息结构、图形主语或动效主语形成变化。
- 不使用丑线框、空洞科技感、纯渐变背景和模板卡片堆叠。
- 动效要表达关系变化，不是为了热闹；复杂科普必须能看到图表、变量或路径随口播变化。
- 旧风格被用户确认好时，后续只能迭代色调、层次、动效和节奏，不能推翻成另一套视觉语言。

### 7. 验收层

目标：确认成片不只可播放，而且清晰、吸引、有记忆点并能稳定交付。

步骤：

1. 读取 `references/final-acceptance.md`。
2. 导出首帧、边界帧、每幕 15%/50%/85% 中间帧和 contact sheet。
3. 生成低清全片预览，分别静音看、只听音频、正常完整看、暂停逐帧看。
4. 按钩子、语义、同步、层级、连续性、酷感、多样性和技术稳定做 100 分评分。
5. 总分低于 85 或命中硬门槛时返修；最多两轮，仍不稳定则降级为清晰可靠方案。
6. 终版执行类型检查、完整渲染、`ffprobe`、全片解码、黑帧和响度验证。
7. 写入 FinalAcceptanceReport 后交付。

## 详细生产步骤

### Step 1：确认任务

确认三件事：

- 视频主题是什么。
- 目标观众是谁。
- 默认风格是否使用“战略作战室风”。
- 口播稿内容是否确认。
- 风格选择是否确认；默认推荐“战略作战室风”。

如果用户没有指定风格，默认推荐“战略作战室风”。如果是入门教学，可推荐“黑板推演风”。

### Step 2：口播审稿

把内容改成口播稿时，使用这个口径：

- 语气像经验丰富的自媒体博主。
- 多用短句。
- 可以加入“兄弟们”“哎呀”“我的天”等口语表达，但不要滥用。
- 观点要有推进感。
- 每段开头能承接上一段。
- 结尾要有总结或追问。

### Step 3：确定 slug 和 CompositionId

先完成标题包装，再确定 slug 和 CompositionId。

标题包装规则：

- 主标题：优先使用“对象 + 核心判断”结构，例如 `Aether AI：Agent 的下一层，是因果世界模型`。
- 副标题：补充反差、收益或方法论，例如 `不是更多工具，而是更懂动作后果`。
- 文件名短标题：用稳定、短、可检索的英文或拼音，不用整句中文标题。
- 系列视频：文件名必须带集数或主题序号，例如 `yinfu-18.mp4`、`causal-world-models-33-director.mp4`。
- 不要为了标题党牺牲准确性；技术、投研、哲学类标题必须保留核心概念。

命名规则：

| 类型 | 规则 | 示例 |
| --- | --- | --- |
| `slug` | 小写短横线 | `production-control` |
| `CompositionId` | PascalCase | `ProductionControl` |
| TTS 脚本 | `generate-{slug}-voiceover.mjs` | `generate-production-control-voiceover.mjs` |
| timing 文件 | `{camelSlug}Timings.ts` | `productionControlTimings.ts` |
| 组件文件 | `{CompositionId}.tsx` | `ProductionControl.tsx` |

### Step 4：视觉设计师环节

在生成 Remotion 组件前，先读取 `references/visual-design-system.md`，并完成四件事：

1. 上下文扫描：看旧视频、截图、用户反馈、已有 Composition 和关键帧。
2. 约束绑定：确认保留什么、避免什么、这次强化什么。
3. 视觉设计卡：基于口播内容确定风格、色板、字体层级、明暗节奏和禁用方向。
4. 关键帧验收：导出封面帧、中间态帧、高密度信息帧和结尾帧，发现问题立即回改。

外部参考边界：

- html-video 只作为配色、字体、版式气质参考。
- 不安装、不接入、不复制它的 HTML 模板、播放器、CLI、Studio、渲染引擎和交互流程。
- 如借鉴某个模板，只把它转译成“色板 + 字体气质 + 信息密度 + 动效主语”。

视觉设计卡至少包含：

- 推荐风格。
- 推荐色板。
- 上下文结论。
- 明暗主题节奏。
- 每段主视觉任务。
- 可交给动效导演的画面主语。
- 禁用方向。

默认策略：

- AI/技术信号：靛蓝瓷或瑞士克莱因蓝。
- 商业战略：墨水经典或沙丘。
- 教学拆解：黑板推演风，可保留墨水经典的红/琥珀强调。
- 风险验证：深色幕 + 红/安全橙强调。

当用户要求“更好看”“更高级”“去 AI 味”，不要只换颜色。优先从这些维度改：

- 信息密度：少放装饰，多放能帮助理解的结构。
- 构图：让标题、字幕、图形和编号有稳定位置。
- 色调：从受控色板里选一套，减少随机渐变。
- 动效：交给 motion brief 定义；视觉设计卡只约束动效不能破坏风格、可读性和旧版成功经验。

### Step 4.5：动效导演环节

在生成 Remotion 组件前，必须先读取 `references/motion-director.md`，并完成 motion brief。

适用判断：

- 普通 3 分钟观点视频：可以只写简版 motion brief，定义 2-3 个主运动。
- 科普、系统模型、AI Agent、投资、工程机制、10 分钟以上视频：必须写完整 motion brief。

motion brief 至少包含：

- 主运动骨架。
- 运动章节。
- 每章主运动对象。
- 图表动效。
- TTS timing 绑定。
- 关键帧检查。
- 禁用方向。

从 Higgsfield Motion Website 流程中只吸收方法，不接入其闭源服务：

- 先 intake，再写代码。
- 少量章节先跑通，不一上来堆太多 pinned section。
- scroll progress 转为 Remotion scene progress。
- scrub video 转为可由 frame 控制的章节背景层或图表进度。
- dev hooks 转为导出 15% / 50% / 85% 帧目检。
- 质感：减少假科技 HUD、细线框、玻璃卡片和模板阴影。

### Step 5：生成 TTS

脚本职责：

- 保存每段口播文本。
- 调用 Giggle TTS。
- 输出 MP3。
- 读取真实时长。
- 生成 `manifest.json`。
- 生成 `{slug}Timings.ts`。

如果用户修改了已确认口播稿：

- 必须用新稿替换 TTS scenes 的 `text`。
- 必须重新调用 TTS 生成所有受影响段落；段落边界变化时优先重跑整条。
- 必须重新生成 `manifest.json` 和 timing 文件。
- 必须检查新旧段落时长变化，特别是某段变长后是否需要增加 beat cue 和画面状态。
- 必须导出至少 1 张变更段落中段帧，确认字幕、隐喻图和 footer 没有旧稿残留。

推荐输出目录：

```text
public/voiceover-{slug}/
```

推荐文件结构：

```text
public/voiceover-production-control/
├── manifest.json
├── scene-01.mp3
├── scene-02.mp3
└── scene-03.mp3
```

### Step 6：生成 timing

Timing 文件应包含：

- `fps`
- `totalFrames`
- `voiceoverScenes`
- 每段的 `id`
- 每段的 `audio`
- 每段的 `text`
- 每段的 `startFrame`
- 每段的 `durationInFrames`
- 每段的 `audioDuration`

Remotion 组件只能读 timing，不要在组件里重新估算时间。

### Step 6.5：自动择效与特效师强化

真实 timing 生成后，按固定顺序执行：

1. 读取 `references/auto-motion-director.md`，为每个 beat 生成候选、硬约束过滤、评分和去重复，写入 MotionDecisionPlan。
2. 读取 `references/vfx-supervisor.md`，在不改变选中语义动作的前提下，设计特效处理、英雄时刻、强度曲线、连续性和 fallback。
3. 把 VFXEnhancementPlan 的 `audioCue` 绑定到真实 timing；卡拉 OK 必须使用词级时间戳或强制对齐。
4. 检查前 3 秒视觉钩子、章节高潮和 CTA 是否形成完整强弱曲线。
5. 未通过特效师预审时不进入 Remotion 实现。

### Step 7：写 Remotion 组件

组件职责：

- 读取 timing。
- 实现视觉设计卡里的色板、明暗节奏和主运动。
- 渲染背景、标题、关键词、结构图和字幕。
- 对每段使用 `Sequence`。
- 用 `Html5Audio` 播放对应音频。
- 用 frame 计算做动效。

禁止：

- CSS animation。
- Tailwind animation。
- 组件里手写音频秒数。
- 动态引用不存在的 public 文件。
- 随机新增与视觉设计卡无关的颜色。

### Step 8：注册 Composition

在项目 Remotion 入口注册：

```tsx
<Composition
  id="ProductionControl"
  component={ProductionControl}
  durationInFrames={productionControlTimings.totalFrames}
  fps={30}
  width={1920}
  height={1080}
/>
```

实际文件名以项目入口为准，常见是 `src/Root.tsx` 或 `src/index.ts`。

### Step 9：关键帧目检

至少导出：

- 封面或开头帧。
- 至少 1 张动效中间态帧。
- 中段结构帧。
- 高信息密度帧。
- 结尾帧。

目检时按视觉设计师标准判断：

- 是否延续了用户认可过的视觉语言。
- 是否一眼能看出内容类型和当前段落重点。
- 是否有文字溢出、字幕遮挡、线框感、模板感。
- 是否出现随机色、过度蓝紫、过度渐变或无意义装饰。
- 动效中间态是否能看出变化。
- 前 3 秒是否已经建立视觉钩子，没有空白或半入场。
- 英雄时刻是否真正突出，其他 scene 是否为其留出强度空间。
- 相邻 scene 是否继承对象、方向、位置或语义，而不是无意义淡入淡出。
- 高密度图表、产品界面和字幕是否被特效遮挡。

示例：

```bash
mkdir -p out/stills/production-control
npx remotion still src/index.ts ProductionControl out/stills/production-control/cover.png --frame=120 --overwrite
npx remotion still src/index.ts ProductionControl out/stills/production-control/mid.png --frame=1800 --overwrite
npx remotion still src/index.ts ProductionControl out/stills/production-control/final.png --frame=5000 --overwrite
```

### Step 10：完整渲染

```bash
npx remotion render src/index.ts ProductionControl out/production-control-war-room-tts.mp4 --overwrite --crf=18
```

### Step 11：成片验收

先按 `references/final-acceptance.md` 生成低清预览并完成四种观看模式，再渲染或确认终版。

终审合格要求：

- 总分不低于 85。
- 钩子与留存、语义清晰、音画同步、层级与可读性均达到各自权重的 70%。
- 不命中任何硬门槛。
- 有明确英雄时刻，但没有连续高强度轰炸。
- 返修不超过两轮；仍不稳定时采用 fallback。

```bash
ffprobe -v error -show_entries format=duration,size -show_streams -of json out/production-control-war-room-tts.mp4
ffmpeg -v error -i out/production-control-war-room-tts.mp4 -f null -
```

必须确认：

- 有视频流。
- 有音频流。
- duration 合理。
- 文件大小不是异常小。
- 全片解码无错误。
- 没有非预期连续黑帧。
- 网络视频响度接近 -16 LUFS，除非用户或平台另有要求。
- FinalAcceptanceReport 已记录评分、硬门槛、返修和交付结论。

## 文件命名示例

假设合成名是 `ProductionControl`，slug 是 `production-control`：

| 类型 | 路径 |
| --- | --- |
| TTS 脚本 | `scripts/generate-production-control-voiceover.mjs` |
| TTS 输出 | `public/voiceover-production-control/` |
| Timing 文件 | `src/compositions/productionControlTimings.ts` |
| Remotion 组件 | `src/compositions/ProductionControl.tsx` |
| 关键帧 | `out/stills/production-control/` |
| 成片 | `out/production-control-war-room-tts.mp4` |

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
- 每段只有一个主要观点。

音频：

- 第一段不过快。
- 每段没有截断。
- `manifest.json` 有真实时长。
- timing 文件来自脚本自动生成。
- MP4 有音频流。

画面：

- 文字不重叠、不溢出。
- 每屏只服务当前口播重点。
- 没有丑线框、空洞科技感、模板味。
- 色彩不过度单一。
- 动画和口播节奏一致。
- 前 3 秒有完整视觉钩子。
- 相邻 scene 不连续重复同一构图和同一主动作。
- 至少有一个有语义的英雄时刻。
- 特效强弱有起伏，没有持续高强度轰炸。

特效与验收：

- MotionDecisionPlan 已完成。
- VFXEnhancementPlan 已完成，重特效有 fallback。
- 低清全片已按四种观看模式审查。
- 终审总分不低于 85，且未命中硬门槛。
- FinalAcceptanceReport 已保存。

工程：

- `Root.tsx` 或实际入口已注册 composition。
- `tsc` 通过。
- 关键帧已目检。
- `ffprobe` 确认视频流和音频流。
- 全片解码、黑帧和响度检查通过。
- Studio 能打开 `/{CompositionId}`。

## 常见返工原因

| 问题 | 原因 | 处理 |
| --- | --- | --- |
| 第一段太快 | 开头信息密度过高，TTS 默认语速偏快 | 拆短第一段，降低 `slow` 或重生成 |
| 画面落后声音 | 使用手写 duration，没有读真实音频 | 重新生成 manifest 和 timing |
| 画面像 PPT | 每段只是摆文字，没有视觉动作 | 用关系、路径、对比、状态变化表达 |
| 线框感太重 | 使用大边框、硬直线和空白容器 | 减少边框，改用色块、标签、层级和动效 |
| 文字溢出 | 没有限制容器宽度和字号 | 使用固定布局、换行、压缩文案 |
| render 后没声音 | 音频路径或 `Html5Audio` 引用错误 | 检查 `public/` 路径和 `staticFile()` |
