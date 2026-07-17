# Slide Story 模板目录

## 目录

1. 选择顺序
2. 路由与模板的边界
3. 共享 Plan 契约
4. 模板目录
5. 页面槽位规则
6. 触发与冲突样例
7. 反模式
8. 最小交付结构

## 选择顺序

进入 Slide Story 后，按以下顺序确定配置：

1. 选择输出路由：`slides-web`、`slides-video` 或 `slides-dual`。
2. 选择叙事模板：显式模板 ID 优先，否则按任务目标选择。
3. 绑定主题 token：品牌色、字体、密度、圆角、图表和截图风格。
4. 用真实内容填充固定槽位；不需要的槽位可以合并，但不得随意打乱论证顺序。
5. 视频路由在 TTS 完成后写入真实 timing；Web 路由保留 presenter notes。

默认选择：

| 任务 | 模板 ID | 典型长度 |
| --- | --- | --- |
| 网站、产品或功能宣传短片 | `promo-fast-8` | 20–90 秒 / 6–8 页 |
| 概念、方法、科普或文章讲解 | `explainer-core-10` | 3–9 分钟 / 8–12 页 |
| 路演、方案陈述、投资或管理决策 | `pitch-decision-12` | 5–15 分钟 / 10–14 页 |
| 研究报告、行业分析、数据复盘 | `report-evidence-12` | 6–18 分钟 / 10–16 页 |

没有显式模板时，优先按“宣传 → 讲清楚 → 促成决策 → 证据复盘”四种任务判断。仍无法判断时使用 `explainer-core-10`。

## 路由与模板的边界

路由和模板是两个正交字段：

- `slides-video + promo-fast-8`：网站宣传短片。
- `slides-web + pitch-decision-12`：现场路演 Deck。
- `slides-dual + report-evidence-12`：研究汇报的 Web Deck 与 MP4 双交付。
- `slides-dual + explainer-core-10`：课程讲解的演示链接与口播视频。

不要创建 `dual-template`。双交付是渲染路由，不是叙事骨架。

## 共享 Plan 契约

所有 Slide Story 任务先生成一个可由 Web 和视频共同消费的 plan：

```ts
type SlideStoryRoute = 'slides-web' | 'slides-video' | 'slides-dual';

type SlideStoryTemplateId =
  | 'promo-fast-8'
  | 'explainer-core-10'
  | 'pitch-decision-12'
  | 'report-evidence-12';

type SlideStoryLayout =
  | 'cover'
  | 'statement'
  | 'split'
  | 'bento'
  | 'stats'
  | 'steps'
  | 'comparison'
  | 'timeline'
  | 'table'
  | 'quote'
  | 'browser'
  | 'section'
  | 'custom';

type SlideStoryCue = {
  id: string;
  text: string;
  action: string;
  startMs?: number;
  endMs?: number;
};

type SlideStoryScene = {
  id: string;
  slot: string;
  purpose: 'cover' | 'problem' | 'proof' | 'method' | 'comparison' | 'section' | 'cta';
  layout: SlideStoryLayout;
  headline: string;
  body?: string;
  evidence?: string[];
  media?: {type: 'image' | 'video' | 'browser' | 'chart'; src: string; alt: string};
  source?: string;
  notes?: string;
  cues: SlideStoryCue[];
};

type SlideStoryPlan = {
  version: 1;
  mode: 'slide-story';
  route: SlideStoryRoute;
  templateId: SlideStoryTemplateId;
  title: string;
  audience: string;
  objective: string;
  format: {width: number; height: number; fps: number};
  theme: {palette: string; typography: string; density: 'airy' | 'balanced' | 'dense'};
  scenes: SlideStoryScene[];
};
```

约束：

- `slot` 使用模板定义的稳定槽位名，不使用 `page-1` 这类无语义名称。
- `headline` 是页面唯一主判断，不复述 body。
- `source` 用于数据、引语和真实产品信息；纯观点页可以省略。
- `cues` 在内容规划阶段先写动作意图；视频 TTS 完成后再补 `startMs/endMs`。
- `media.alt` 必填，便于 Web 可访问性、素材审查和视频制作记录。

## 模板目录

### `promo-fast-8`

目标：快速建立品牌认知并引导行动。默认 8 个槽位：

| 槽位 | 目的 | 推荐布局 |
| --- | --- | --- |
| `hook` | 第一帧说清品牌或产品是什么 | `cover` |
| `pain` | 呈现一个高相关问题 | `statement` |
| `shift` | 给出新判断或反差 | `comparison` |
| `product` | 展示真实产品界面 | `browser` / `split` |
| `capability` | 解释 2–4 个互补能力 | `bento` |
| `workflow` | 展示使用路径 | `steps` |
| `payoff` | 明确用户得到什么 | `statement` / `stats` |
| `cta` | URL、二维码或下一步 | `cover` |

硬规则：首帧品牌可识别；至少一页真实界面；结尾 CTA 保留足够阅读时间；不得用虚构数字制造效果。

### `explainer-core-10`

目标：把一个抽象概念讲清楚，并给出可执行方法。默认 10 个槽位：

| 槽位 | 目的 | 推荐布局 |
| --- | --- | --- |
| `question` | 提出观众正在困惑的问题 | `cover` |
| `thesis` | 给出全片核心判断 | `statement` |
| `definition` | 定义关键概念与边界 | `split` |
| `old-model` | 展示常见旧理解 | `comparison` |
| `mechanism` | 解释内部机制或因果链 | `steps` / `custom` |
| `evidence` | 给出事实、数据或来源 | `stats` / `quote` |
| `example` | 用具体案例降低理解成本 | `split` / `browser` |
| `method` | 提炼可执行方法 | `steps` |
| `boundary` | 说明何时不适用 | `comparison` |
| `conclusion` | 复述判断并给下一步 | `statement` / `cover` |

硬规则：机制页必须有关系变化；方法页必须可执行；引用与数据必须可追溯。

### `pitch-decision-12`

目标：让特定受众理解机会并作出资源、合作或投资决定。默认 12 个槽位：

| 槽位 | 目的 | 推荐布局 |
| --- | --- | --- |
| `cover` | 项目名与一句话价值 | `cover` |
| `problem` | 目标用户的真实问题 | `statement` |
| `stakes` | 不解决的成本 | `stats` / `comparison` |
| `insight` | 团队看见的结构变化 | `statement` |
| `solution` | 解决方案全貌 | `split` |
| `product` | 产品如何工作 | `browser` / `steps` |
| `proof` | 用户、收入、实验或技术证据 | `stats` / `quote` |
| `market` | 市场与时机 | `stats` / `timeline` |
| `moat` | 难以复制的能力 | `bento` |
| `model` | 商业或落地模型 | `steps` / `table` |
| `roadmap` | 里程碑与资源使用 | `timeline` |
| `ask` | 明确希望对方作出的决定 | `cover` |

硬规则：每个数字有来源；产品页不以功能清单代替价值；最后一页必须有明确 ask。

### `report-evidence-12`

目标：用证据建立判断，适合行业报告、投研、复盘和正式汇报。默认 12 个槽位：

| 槽位 | 目的 | 推荐布局 |
| --- | --- | --- |
| `cover` | 报告主题、范围和日期 | `cover` |
| `executive-summary` | 先给 1–3 个结论 | `statement` |
| `scope` | 数据口径与研究边界 | `split` |
| `signal` | 最重要的变化信号 | `stats` |
| `drivers` | 变化由什么驱动 | `steps` / `custom` |
| `segments` | 分组或结构差异 | `table` / `bento` |
| `trend` | 时间变化 | `timeline` / `custom` |
| `comparison` | 基准、竞品或前后对照 | `comparison` |
| `case` | 代表性案例 | `split` |
| `implication` | 对受众意味着什么 | `statement` |
| `recommendation` | 建议与优先级 | `steps` |
| `sources` | 来源、限制与下一步 | `table` / `cover` |

硬规则：结论先行；事实与推断分开；图表必须标单位、时间和来源；限制条件不能藏在制作备注里。

## 页面槽位规则

- 可合并相邻槽位，但短片不得删除 `hook/cover`、核心证据和 `cta/ask/conclusion`。
- 长内容需要扩展时，在对应槽位后添加语义后缀，例如 `proof-2`、`case-2`，不要改变主顺序。
- 同一布局最多连续使用两次；连续两页大字必须至少一页加入图表、截图或结构变化。
- 每页默认一个主标题、一个证据区、一个动作焦点；不是每页都需要卡片。
- Web 与视频共享槽位和事实，允许因媒介不同更换布局。

## 触发与冲突样例

| 用户输入 | 主模式 | 路由 | 模板 | 理由 |
| --- | --- | --- | --- | --- |
| “给这个网站做 45 秒宣传短片，使用 slide 模式” | Slide Story | `slides-video` | `promo-fast-8` | 显式 slide + 宣传短片 |
| “把研究报告做成可演讲的网页，也导出视频” | Slide Story | `slides-dual` | `report-evidence-12` | 双交付 + 证据型内容 |
| “把这篇 AI 科普做成 6 分钟演示型口播” | Slide Story | `slides-video` | `explainer-core-10` | 概念讲解 + 视频 |
| “做投资人路演链接，现场翻页” | Slide Story | `slides-web` | `pitch-decision-12` | 决策型受众 + Web Deck |
| “空见心力，白底黑红，大字和底部隐喻图” | SketchTalk | MP4 | 不选 Slide Story 模板 | 明确竖屏强观点语法 |
| “整理成 10 页 PPT 大纲，先不做演示和视频” | 内容整理 | 无 | 无 | 没有可播放交付物 |
| “用 Slide Story，但要黑红白配色” | Slide Story | 按交付物 | 按任务 | 黑红白只是主题 token |
| “参考这个演示网站，制作普通纪录片口播” | 标准口播视频 | MP4 | 无 | 参考媒介不改变主模式 |

## 反模式

- 看到 `slide` 就默认 `slides-web`，忽略用户实际要 MP4。
- 把 `slides-dual` 写成模板名，导致 Web 与视频各自重新编一套内容。
- 先堆 Cover、Bento、Stats，再反推内容；模板槽位必须服务论证。
- 每页都做卡片墙，或者连续三页居中大字，没有证据和节奏变化。
- 把 SketchTalk 的顶部命题、主 beat、footer 全部塞进 Slide Story 页面，产生三层重复标题。
- Web 直接录屏当成视频；视频必须依据 TTS timing 在 Remotion 中重新编排。
- 用模板里的假数字、公司名或占位截图替换真实研究和产品证据。

## 最小交付结构

每次进入 Slide Story，制作记录至少写明：

```text
mode: slide-story
route: slides-video
template: explainer-core-10
theme: <palette / typography / density>
scenes: <count>
audio: <voice id / duration / timing source>
outputs: <web path and/or mp4 path>
```

如果用户没有指定模板，最终回复中必须说明自动选择了哪个模板及原因。
