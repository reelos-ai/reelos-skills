# Slide Story 演示叙事模式

## 目录

1. 模式目标
2. 输出路由
3. 共享内容规划
4. 布局语法
5. Web 与视频转译
6. 动效纪律
7. 验收清单

## 模式目标

Slide Story 用演示页的高信息效率组织内容：一页一个判断、标题先行、视觉证据跟随、逐步揭示。它不是把文章切成 PPT，也不是把网站截图连续滚动，而是把叙事压缩成可讲、可看、可验证的页面序列。

设计思想参考 StackBlitz `bolt-slides` 的响应式 React 演示语法。其源码采用 MIT License；如复制 substantial portions 到 Web 模板，必须保留 StackBlitz 版权和 MIT 许可。Remotion 视频只转译能力，不复制其 Deck runtime。

## 输出路由

### slides-web

适合现场演讲、路演、教学演示和链接传播。

- 使用响应式 React 页面。
- 支持键盘翻页、点击 Build、缩略图、网格视图、Presenter 和 Annotation。
- 动效可使用 Web runtime，但必须支持 `prefers-reduced-motion`。
- 如果基于 Bolt Slides 模板，保持 `src/deck/` 引擎稳定，只改主题 token、内容和新增业务组件。

### slides-video

适合口播宣传片、知识讲解和商业汇报视频。

- 默认 1920×1080、30fps。
- TTS 音频是唯一时间基准。
- 所有动画使用 Remotion `Sequence`、`interpolate`、`spring` 和 `useCurrentFrame`。
- Web 的点击 Build 转成句级 cue；Presenter、Annotation、Dock 和 Rail 不进入成片。

### slides-dual

适合既要演讲链接又要视频传播的任务。

1. 先生成共享 `SlideStoryPlan`。
2. Web 端将 plan 作者化为 React slides。
3. 视频端将同一 plan 映射到 TTS scenes 和 Remotion sequences。
4. 两端共享标题、关键事实、章节顺序和主题 token，但不强求像素一致。

## 共享内容规划

每一页至少包含：

```ts
type SlideStoryScene = {
  id: string;
  purpose: 'cover' | 'problem' | 'proof' | 'method' | 'comparison' | 'section' | 'cta';
  layout: 'cover' | 'statement' | 'split' | 'bento' | 'stats' | 'steps' | 'comparison' | 'timeline' | 'table' | 'quote' | 'browser' | 'custom';
  headline: string;
  body?: string;
  evidence?: string[];
  media?: string;
  notes?: string;
  cues?: Array<{text: string; action: string}>;
};
```

规划规则：

- 8–16 页适合演示稿；15–45 秒宣传片通常 5–10 页。
- 开头用 Cover 或强 Statement，结尾用 CTA。
- 一页只证明一个判断；正文最多 1–3 个短句。
- 数据必须真实且注明来源；真实品牌不得使用模板虚构数据。
- 相邻页面切换布局，避免连续三页都是居中大字或卡片网格。

## 布局语法

- `Cover`：品牌、主张和行动入口；第一帧必须完整。
- `Statement`：一句强判断，适合问题、转折和结论。
- `Split`：一侧观点、一侧产品截图或真实视觉证据。
- `Bento`：多个互补能力组成一个系统时使用，不作为通用卡片墙。
- `Stats`：仅承载可核验数字；一页最多一个英雄数字。
- `Steps`：流程、方法和因果链。
- `Comparison`：真实的前后变化、两种模式或产品边界。
- `Timeline`：存在明确时间顺序时使用。
- `Table`：真实数据对比，最多 5 列、7 行。
- `Browser`：展示真实产品或网页；截图必须清晰，并聚焦当前卖点。
- `Section`：长演示的章节呼吸页，短片慎用。

没有侧视觉的纯文字页必须居中；左对齐或非对称构图必须有截图、图表或结构图平衡画面。

## Web 与视频转译

| Web 能力 | slides-video 转译 |
| --- | --- |
| `Build at={n}` | 绑定第 n 个 TTS cue，在对应帧显影 |
| `Reveal` | scene 入场后的 `spring` / `interpolate` |
| 点击下一页 | scene timing 结束自动进入下一幕 |
| 响应式重排 | 固定画幅下使用安全区和稳定网格 |
| Presenter notes | 进入口播稿或制作备注，不进入画面 |
| Annotation | 转成预先编排的圈选、划线、聚焦框 |
| Dock / Rail / Grid | 仅 Web 模式保留，视频中删除 |
| Framer Motion | 转成 Remotion 帧动画 |

## 动效纪律

- 快闪宣传片每页 1–2 个主动作，切换可用硬切、遮罩推入、局部放大和规则线扫描。
- 教学演示优先逐步显影、路径描边和图表生长，不做随机飞入。
- 文字动画只使用 opacity、transform、clip-path 等可控属性，避免抖动和布局重排。
- 网站截图以局部推进解释功能，不做无目的滚屏。
- 第一帧完整；结尾 URL 至少保留 1.5 秒。

## 验收清单

- [ ] 内容来自真实输入，没有残留模板公司、假数字或占位文案。
- [ ] 每页只有一个主判断，相邻页面版式不同。
- [ ] 纯文字页居中，非对称页有视觉平衡。
- [ ] Web 端检查桌面与窄屏；Build 前进和后退都正常。
- [ ] 视频端 timing 来自真实音频，所有动画可按帧复现。
- [ ] 第一帧完整，文字不溢出，截图清晰。
- [ ] 真实品牌色和字体来源已记录。
- [ ] `tsc`、关键帧、完整渲染与 ffprobe 均通过。
