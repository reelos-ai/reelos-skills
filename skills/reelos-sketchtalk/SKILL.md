---
name: reelos-sketchtalk
description: 生成 ReelOS SketchTalk / 漫说 ReelOS 方法论风格的竖屏观点页、短视频封面、分镜页和极简哲思插画。用于用户要求“漫说 ReelOS”“ReelOS SketchTalk”“竖屏观点页”“短视频封面”“知识视频分镜”“强观点海报”“黑红白极简插画”“参考深度进化Theo这种版式但做成自己的内容模板”等任务；默认以用户输入的主题、标题、观点、作者或系列名为画面主体，ReelOS 只作为内部风格名或用户明确要求时的系列标识。
---

# 漫说 ReelOS / ReelOS SketchTalk

## 核心定位

生成 9:16 竖屏观点页、短视频封面和分镜页。目标不是正文配图、PPT 信息图或商业海报，而是把用户输入里的一个判断、一句口播、一段哲思或一个内容主题，压缩成“强文字 + 大留白 + 极简隐喻图”的可传播画面。

内容优先：不要默认把 `漫说 ReelOS`、`ReelOS` 或任何预设品牌放进画面。顶部署名、英文副标、右下角小字都应从用户输入推导；只有用户明确要求 ReelOS 系列、漫说 ReelOS 或没有提供任何署名/系列名且需要占位时，才使用 ReelOS 相关文字。

默认主视觉不是固定 IP 角色，而是普通人物剪影、半抽象人物、黑色山体、红色太阳、线条路径、洞口、桥、门、书、镜头环等极简物件。人物必须服务观点氛围，不能抢走文字中心。

## 先读这些参考

按任务需要读取，不要一次塞满上下文：

- `references/style-dna.md`：颜色、字体气质、留白、禁止项。
- `references/layout-template.md`：竖屏版式、区域比例、文字层级。
- `references/metaphor-system.md`：底部极简隐喻图的题材和构图方法。
- `references/prompt-template.md`：单张生成、改图和分镜提示词模板。
- `references/qa-checklist.md`：生成后检查和迭代规则。
- `assets/reference-style/`：用户给的参考图，仅用于低频校准版式密度、黑红白比例和插画克制程度。不要复刻原账号、圆章、署名、中文口号或具体构图。

## 工作流

### 1. 提炼观点

先读用户给的主题、文章、口播稿、视频脚本或单句观点。提炼：

- 这一页要让观众记住哪一句话
- 用户输入里有没有标题、作者、账号、栏目名或系列名
- 红色命题句是什么
- 黑色主观点是什么
- 底部隐喻图要承接哪种情绪：困住、远望、跨越、觉醒、沉淀、回家、出发、重构
- 是否需要做成一组连续分镜

不要平均拆内容。每一页只讲一个判断，不把整段文章做成说明书。

### 2. 先出页面策略

如果用户说“先设计 / 先规划 / 出模板 / 做 shot list”，不要生成图片，先输出页面方案。每页写清楚：

- 页名或镜头名
- 红色命题句
- 黑色主观点
- 英文副标
- 底部隐喻图
- 画面情绪

单个主题默认 1 张；长口播默认 4-8 张分镜页；超过 9 张时先建议精简。

### 3. 单张生成

如果用户明确要求“生成 / 做图 / 出图 / 输出封面 / 做分镜图”，用内置 `image_gen` 每张单独生成。不要把多页拼成一张。

生成提示词必须包含：

- 9:16 vertical Chinese short-video thought poster
- pure white background
- black / restrained warm red / soft gray only
- strong Chinese typography as the main visual anchor
- red long premise line near upper third
- bold black main statement in the center
- thin uppercase English subtitle derived from the user content
- minimal black-and-red metaphor illustration in lower third
- ordinary human silhouette or semi-abstract human figure, not recurring IP
- no forced ReelOS branding unless explicitly requested, no copied external logo, no watermark, no platform UI, no original reference account mark

### 4. 检查与迭代

生成后检查 `references/qa-checklist.md`。如果出现以下问题，优先重生成或局部编辑：

- 画幅不是 9:16
- 文字区域和插画区域互相挤压
- 太像 PPT、课程封面或营销海报
- 使用了外部账号标识、圆章“深”、原参考署名或水印
- 插画太复杂、太可爱、太商业
- 红色过多，破坏黑白克制感
- 中文错字严重或主观点不可读

### 5. 保存交付

如果用户在 workspace 内工作，把最终图保存到：

```text
assets/<topic-slug>-sketchtalk/
```

按顺序命名：

```text
01-topic-name.png
02-topic-name.png
```

保留原始生成文件，不要覆盖已有资产，除非用户明确要求替换。

## 输出口径

生成前的策略输出要短而准。生成后的交付包含：

- 生成了几张
- 每张图的主观点和用途
- 保存路径
- 哪些页适合做封面，哪些页适合做中段分镜

不要长篇解释风格理论；让画面和文字结构自己说话。
