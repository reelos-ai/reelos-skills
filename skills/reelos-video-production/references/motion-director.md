# 动效导演参考

## 目标

动效导演不是“给每屏加动画”，而是在写 Remotion 组件前定义一条能贯穿全片的运动骨架。它解决三个问题：

1. 这条视频的核心关系如何被看见。
2. 哪些图表、路径、状态或变量需要随口播发生变化。
3. 哪些运动只是装饰，应该删掉。

适用场景：

- 用户要求“增强动效”“图表动效”“科普类更易理解”。
- 视频讲系统、因果、流程、变量、策略、投资、AI Agent、产品机制。
- 长视频超过 6 分钟，需要章节化运动节奏。
- 旧版本被反馈“没有新动效”“动效不明显”。

## 核心原则

- 先做 motion brief，再写组件。
- 一条视频只设一条主运动骨架，不要每幕随机换动效语言。
- 每段最多一个主运动对象：路径、变量、卡片、图表、镜头或背景层。
- 动效必须解释关系变化，例如输入到输出、状态到干预、旧局到新局。
- 动效先绑定 TTS beat，再谈视觉丰富；字幕、图形、隐喻图和转场都应有同一个 cue 来源。
- 关键帧必须看得出差异；如果 15%、50%、85% 三帧几乎一样，动效太弱。
- 长视频用 4-6 个大章节复用同一套运动语法，不为每个小段发明新系统。
- 不用 CSS animation；Remotion 里用 frame、`interpolate()`、`spring()`、`Sequence`。
- 可以学习 transitions.dev 和 GSAP 的动效词典、时间线、easing 和 stagger，但不要直接搬 CSS transition 或 GSAP runtime 进 Remotion 合成。

## Motion Brief 模板

每次做科普或复杂结构视频，内部先写这张卡：

```text
内容任务：
目标观众：
视觉基调：
主运动骨架：
运动章节：
每章主运动对象：
镜头语言：
图表动效：
TTS timing 绑定：
关键帧检查：
禁用方向：
```

示例：

```text
内容任务：解释 Causal World Models 为什么是 Agent 下一层能力。
主运动骨架：观察 → 状态 → 机制 → 干预 → 验果 → 更新 的闭环。
运动章节：
  1. 信号出现：从普通 Agent 流程收束到因果闭环。
  2. 动作后果：从预测下一步转为推演动作影响。
  3. 传统映射：象/势/因/变/用/果 逐层对齐。
  4. Causal Skill：从流程步骤升级成因果任务模型。
  5. World Agent：闭环完成，显示判断系统。
每章主运动对象：环形链路、变量节点、力线、反馈回路、章节地图。
```

## Beat Motion Map

适用：SketchTalk、科普、系统模型、长视频、用户反馈“动画少”“画面切换不足”“字幕和画面不同步”。

在写组件前，为每个 TTS scene 建一张 beat 表：

```ts
{
  cue: "每天问自己",
  caption: ["每天问自己"],
  visualAction: "text-swap",
  metaphorState: "question-door-open",
  focus: "main-caption",
  transition: "stagger-reveal"
}
```

规则：

- `cue` 必须能在 TTS 原文里找到，优先用真实口播短句，不用概括句。
- `caption` 是屏幕主 beat 字幕，应短、狠、可读，不等于完整字幕。
- `visualAction` 只选一个主动作，不要同一 cue 同时触发多套运动。
- `metaphorState` 让底部插画、图表或隐喻对象跟着 cue 变化。
- `focus` 决定观众眼睛应该看哪里：主字幕、插画、节点、路径、数字或 footer。
- `transition` 只描述运动语法，具体代码转成 Remotion motion preset。
- 每个 scene 至少 2-3 个可见状态；长 scene 每 6-10 秒至少有一次画面状态变化。
- 用户改口播稿后必须重建 Beat Motion Map。任何新增、删改或重排的句子，都要同步更新 cue、caption、metaphorState 和 footer note，不允许旧 cue 继续驱动画面。

验收：

- 静音看视频，仍能看出当前口播讲到哪个概念。
- 字幕切换时，至少一个非字幕元素也有轻微变化。
- 画面动作不得早于对应 cue 太多；如有固定偏差，优先调局部 offset。

## 从 transitions.dev 学习的动效词典

只学习语法，不直接复制 CSS snippet。

| transitions.dev 概念 | Remotion 转译 | 视频用途 |
| --- | --- | --- |
| texts reveal | `textReveal(frame, start)` | 标题、主 beat 字幕进入 |
| text states swap | `textSwap(frame, start, end)` | beat 字幕换句 |
| page side-by-side | `pageSlide(frame, start)` | 分镜横向切换、对比页 |
| panel reveal | `panelReveal(frame, start)` | 图表、插画区展开 |
| tabs sliding | `footerKeywordSlide(frame, active)` | footer 关键词激活 |
| number pop-in | `numberPop(frame, start)` | 集数、步骤、指标数字 |
| success check / icon swap | `markResolve(frame, start)` | 答案出现、选择完成、结论落地 |
| skeleton / shimmer | `thinkingSweep(frame)` | 搜索、生成、脑内检索、AI 处理 |
| card resize | `layoutMorph(frame, start)` | 概念块从小到大、观点展开 |

推荐 tokens：

- 微动效：4-8px 位移，150-250ms。
- 文字显影：12px 位移，2-3px blur，350-500ms。
- 面板展开：24-40px 位移，350-500ms。
- 强调瞬间：轻微 overshoot，scale 0.96 → 1 或 1 → 1.04 → 1。
- 常用 easing：`Easing.bezier(0.22, 1, 0.36, 1)` 用于开合；`Easing.bezier(0.16, 1, 0.3, 1)` 用于 ReelOS 稳定推进。

## 从 GSAP 学习的时间线方法

只学习 timeline 编排，不直接引入 GSAP runtime。

Remotion 里用 `frame`、`sceneStart`、`caption.ranges`、`Sequence` 替代 `gsap.timeline()`：

```ts
const labels = {
  intro: 0,
  beat1: caption.ranges[0].start,
  beat2: caption.ranges[1].start,
  outro: durationFrames - 24,
};
```

转译规则：

- GSAP `timeline label` → Remotion `labels` 或 `caption.ranges`。
- GSAP `stagger` → `start + index * 4` 这类帧偏移。
- GSAP `to/from/fromTo` → `interpolate(frame, [start, end], [from, to])`。
- GSAP nested timeline → 一个 scene 内的局部 helper 函数。
- GSAP easing → Remotion `Easing.bezier()` 或 `spring()`。

设计要求：

- 用 label 命名关键动作：`intro`、`question`、`turn`、`answer`、`outro`。
- 不用大量 `delay` 魔法数；优先从 cue range 推导动作时间。
- 同一 scene 的字幕、插画和 footer 要共享 beat label，避免各自动。

## Remotion Motion Preset 建议

如果同类动画出现 2 次以上，抽成项目本地 helper，不要每个组件重写：

```ts
textReveal(frame, start, options)
textSwap(frame, start, end, options)
panelReveal(frame, start, options)
pathDraw(frame, start, end)
nodePulse(frame, start)
numberPop(frame, start)
footerKeywordSlide(frame, activeStart)
beatProgress(frame, range)
sceneOutro(frame, durationFrames)
```

约束：

- helper 返回 `opacity`、`transform`、`filter`、`clipPath`、`strokeDashoffset` 等可直接用于 style/SVG 的值。
- helper 必须可由 frame 完全决定，不读取 DOM，不依赖浏览器时间。
- 重图层和实时 blur 谨慎使用；可预烘焙就预烘焙。

## 抖动治理规则

当用户反馈“动画抖”“画面晃”“字在闪”时，优先检查这些点：

- 不要把 `beatPunch`、`Math.sin()` 这类先升后降的脉冲混入主 `progress`；主进度必须单调递增，否则路径、节点和插画状态会前进后退。
- 不要在同一个大容器上同时叠加持续横移、上下浮动、beat 位移和 beat 缩放；整块插画最多保留一个慢速主运动，其余变化放到局部线条、红点或节点。
- 大号中文主字幕避免持续 `scale()`、高强度 `blur()` 和小数像素位移；进入后应稳定在整数像素位置。
- beat 字幕可以轻微反馈，但位移建议控制在 0-2px，不要每个短句都上下弹跳。
- 底部背景线、纹理层、装饰点不要持续正弦漂移；如要动，优先做低透明局部描边或进度线。
- 对相邻帧导出 still 检查：同一稳定 beat 内，主体轮廓不应大范围位置变化。

## 可复用动效语法

### 1. 路径追踪

用于解释流程、因果链、Agent loop、用户旅程。

- 线条沿路径生长。
- 当前节点点亮，已讲节点降为低透明。
- 节点之间出现方向箭头或光点。
- 适合：观象 → 察势 → 明因 → 知变 → 取用 → 验果。

### 2. 状态转化

用于解释旧模型到新模型、前后对比、认知升级。

- 左侧旧状态压缩、变灰或后退。
- 中间变量被激活。
- 右侧新状态展开、变亮或锁定。
- 适合：Prediction Model → Causal World Model。

### 3. 变量激活

用于解释系统变量、五行生克、物理抓取、投资因子。

- 一个中心对象保持稳定。
- 周边变量按口播逐个点亮。
- 变量之间用生长线或抑制线连接。
- 适合：重量、摩擦力、接触点、支撑关系、力的方向。

### 4. 反馈闭环

用于解释学习、验证、修正、Skill 迭代。

- 输出不是终点，而是回到输入或模型更新。
- 用回流箭头、环形进度、版本层叠表达。
- 适合：Goal → Observation → State → Intervention → Feedback → Update。

### 5. 镜头推进

用于章节转场、重要结论、封面和收束。

- 微推近：进入深层机制。
- 侧移：从现象移动到结构。
- 拉远：从单点回到系统。
- 锁定：关键判断落地。

### 6. 章节背景层

用于长视频分章，不让 15 分钟看起来一屏到底。

- 每个大章节可以有不同背景层次、网格密度或主题纹理。
- 色板不随意换，但可改变明暗比例和强调色占比。
- 章节切换用同一运动骨架过渡，避免断裂。

### 7. SketchTalk beat 联动

用于白底黑红、强观点、底部极简隐喻图的竖屏口播。

- 主字幕使用 TTS 原文短句，按 cue 在 TTS 原文里的位置计算开始时间；没有 cue 时才退回短句权重分配。
- 每个短句触发一次可见但克制的变化：主字幕显影、底部进度线推进、隐喻图轻微横移或缩放、红点激活、路径线描边。
- 封面标题、视频内主 beat 字幕和底部辅助字幕必须分层；视频内主字幕不要像封面标题一样大。
- 三层文本不能重复同一句：顶部红色命题句写“场景/问题/方法提示”，中间主 beat 写当前口播短句，底部辅助写方法名、章节名或 `02-05` 进度。
- 底部辅助字幕建议用 `page.note / 当前beat-总beat`，字号为主 beat 的 25%-35%，低透明度，不承担第二标题功能。
- 底部隐喻图不是装饰摆件，至少要有一个随 beat 变化的对象，但不引入新的场景系统。
- 隐喻图必须表达当前段落的概念关系。比如口播讲“事实、原因、行动”时，用三节点/路径/激活状态；不要沿用旧稿里的“云雨伞”或其他不相干隐喻。
- 同一场景内 2 个关键帧应该能看出底部图位置、线条或红点发生变化；如果只看截图完全一样，动效不足。
- 画面动作优先从 Beat Motion Map 读取，避免字幕已切换但底部图仍按整段 progress 慢慢播放。

## 从滚动网站动效转译到 Remotion

可学习 scroll-driven website 的流程思想，但不要照搬网页实现。

| 网站动效概念 | Remotion 转译 |
| --- | --- |
| scroll progress | scene progress / global progress |
| pinned section | TTS 分段章节 |
| scrub video | 按 timing 驱动的视频/图形进度 |
| background video chapter | 章节背景层或预渲染素材段 |
| dev hooks | 导出 15% / 50% / 85% 关键帧目检 |
| preloader | render 前检查素材和音频存在 |
| mobile fallback poster | 重素材场景准备静态帧降级 |

启发规则：

- 第一阶段不要写代码，先收集内容 brief、视觉 brief 和 motion brief。
- 运动章节不要太多；先用少量章节跑通，避免 timing 难控。
- 背景视频或重图层必须可寻址、可降级，不让渲染速度被素材拖垮。
- 动效应能被进度控制，而不是依赖浏览器滚动状态。

## 图表动效建议

科普视频优先使用这些图表，而不是装饰卡片：

- 因果闭环图：解释 Agent 如何观察、干预、反馈、更新。
- 变量关系图：解释因果变量如何相互推动或抑制。
- 对比矩阵：解释普通预测模型和因果世界模型的差异。
- 时间轴：解释 Agent 从 Prompt 到 Tool、Memory、Causal World 的演进。
- 分层架构：解释 workflow skill 到 causal skill 的升级。
- 物理场景剖面：解释机器人抓杯子不是识别物体，而是理解支撑、接触和力。

动效绑定：

- 口播讲“观察”时，只点亮观察层。
- 口播讲“变量”时，才激活变量节点，不提前全亮。
- 口播讲“反馈”时，必须让输出回流到模型。
- 口播讲“失败修正”时，显示错误路径被剪掉，新路径被重算。

## 长视频策略

10-15 分钟视频不要做成几十个完全不同的小动画。推荐：

1. 先定义 4-6 个大章节。
2. 每章只切换主运动对象或镜头角度。
3. 固定一个全片进度骨架，帮助观众知道自己听到哪里。
4. 每 2-3 分钟给一次视觉重置：章节名、地图、核心问题或大图表。
5. 高密度段落用图表承载关系，低密度段落用大标题和背景层给呼吸。

## 动效验收清单

导出关键帧后检查：

- 不看口播，只看画面，能否识别这条片子的主运动骨架。
- 每个大章节是否有一个明确主运动对象。
- 15%、50%、85% 中间帧是否明显不同。
- 动效是否解释了关系变化，而不是只让元素进出场。
- 文字是否始终可读，没有被线条、光效、图层遮挡。
- 图表是否按口播逐步显影，而不是一开始全部堆上屏。
- SketchTalk 类视频是否在不破坏留白的前提下，让底部隐喻图随口播短句发生轻微变化。
- SketchTalk 类视频的主 beat 字幕是否比封面标题低一级，底部辅助字幕是否没有抢主字幕。
- 背景视频、主题图层、粒子和大面积 blur 是否拖慢渲染；能静态预烘焙就不要实时重算。
- 旧版用户认可的有效动效是否被保留，而不是被新风格推翻。

## 禁用方向

- 每一屏随机飞入飞出。
- 只做装饰性粒子、扫光、抖动，不解释内容。
- 为了“高级感”叠加重背景视频、重 PNG、实时滤镜和多层 blur。
- 让图表线条细到看不见，或动效弱到截图看不出变化。
- 科普类只放金句大字，不画出概念关系。
- 长视频每段都换一套视觉规则，导致观众无法建立认知地图。
