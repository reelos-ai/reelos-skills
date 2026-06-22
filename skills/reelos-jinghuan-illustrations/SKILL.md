---
name: reelos-jinghuan-illustrations
description: 生成 ReelOS 风格的中文正文配图、文章封面 banner 和品牌插图。用于用户要求“ReelOS 风格”“这个风格”“品牌正文配图”“logo 色调”“手绘配图”“文章插图”“配图建议”“shot list”“去标题/改图”“封面图”“banner”，或为 ReelOS.ai 站内文章、帖子、博客、Notion 文档、工作流文档、方法论、流程、结构、状态、隐喻、观点生成怪诞清爽的图；默认自动注入 ReelOS 固定 IP 角色镜环小工，用户不需要显式提到角色名。给 ReelOS.ai 仓库文章配图时，要同时考虑正文 figure、列表/社交 heroImage、站内资产路径、构建验证和线上加载。
---

# ReelOS 镜环小工怪诞正文配图

## 核心定位

为中文文章设计和生成 16:9 横版正文配图，也为 ReelOS.ai 站内列表卡片与社交分享生成统一封面 banner。正文配图的目标不是做商业插画、PPT 信息图或可爱卡通，而是把文章里的关键判断、流程、结构、状态或隐喻，变成一张清爽、怪诞、有创意、可读但不说明书的手绘解释图。

默认视觉 IP 是“镜环小工”：深蓝近黑的小圆柱/豆形身体，一个来自 ReelOS logo 的同心镜头环脸，米白外环、黑色环、橙色内芯、细手细腿、表情冷静。镜环小工必须参与画面的核心动作，不能只是站在旁边当装饰。

角色名是内部规则，不是用户触发条件。只要用户说“ReelOS 风格”“这个风格”“品牌配图”“logo 色调配图”或类似表达，就默认使用镜环小工；不要要求用户额外确认角色，也不要在回复里提醒用户必须说出角色名。

## 先读这些参考

按任务需要读取，不要一次塞满上下文：

- `references/style-dna.md`：风格 DNA、颜色、文字、禁忌。
- `references/jinghuan-worker-ip.md`：镜环小工 IP 的形象、性格、动作库和禁忌。
- `references/composition-patterns.md`：结构类型、原创隐喻方法和反复刻规则。
- `references/prompt-template.md`：单张生图提示词模板。
- `references/qa-checklist.md`：生成后检查和迭代规则。
- `assets/reelos/jinghuan-worker-character-sheet.png`：镜环小工角色设定草图，用于低频校准角色形象。
- `assets/examples/`：只作低频视觉校准，不进入默认生成路径。不要照抄这些案例的构图、物件或标注。

## 工作流

### 1. 消化正文

先读用户给的正文、链接、Notion 页面、Markdown 文件或截图内容。提炼：

- 核心观点是什么
- 哪些段落承担认知转折
- 哪些内容适合用图解释
- 哪些地方只适合文字，不需要图

不要平均配图。优先选择“认知锚点”，例如：核心判断、两个断点、输入输出闭环、分流、前后对比、一鱼多吃、承接路径、常见坑、角色状态变化。

### 1.1 正文排版微标注

当任务涉及 ReelOS.ai 文章正文排版、标题层级或“事实 / 原则 / 步骤 / 模块”这类子分类小标题时，可以使用轻微下划线增强层次，但它应该是阅读辅助，不是视觉主角。

推荐规则：

- 只作用在正文三级标题或短子标题上，例如 `事实 1：...`、`原则一：...`、`步骤 2：...`。
- 线条要细、淡、克制：约 2px 高，透明度低，两端淡，中间略实。
- 使用 ReelOS logo 的橙色系或当前 `article-accent`，不要使用高饱和荧光黄、粗实线或大面积背景高亮。
- 线条宽度跟随标题文字自适应，不要铺满整行。
- 不要影响正文段落阅读，不要让读者先看到线再看到字。
- 移动端保持同样克制，避免标题换行后线条造成杂乱。

CSS 思路示例：

```css
.article-body h3 {
  position: relative;
  display: table;
  max-width: 100%;
  padding-bottom: 0.18em;
}

.article-body h3::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -0.04em;
  height: 2px;
  border-radius: 999px;
  background: linear-gradient(
    90deg,
    transparent 0,
    rgba(249, 115, 22, 0.08) 8%,
    var(--article-accent-soft) 44%,
    rgba(249, 115, 22, 0.26) 52%,
    var(--article-accent-soft) 60%,
    rgba(249, 115, 22, 0.08) 92%,
    transparent 100%
  );
  opacity: 0.46;
}
```

### 2. 先出配图策略

如果用户只是说“分析怎么配图 / 思考哪些地方需要配图”，先给 shot list。每张图写清楚：

- 放在哪个段落后
- 图的主题
- 核心意思
- 结构类型
- 固定 IP 在图里做什么（默认镜环小工；用户未提角色名也要使用）
- 建议元素
- 建议中文标注词

默认 4-8 张。文章很短时 1-3 张；长文也不要轻易超过 9 张。够用就好，避免把正文做成画册。

### 3. 单张生成

如果用户明确要求“生成 / 输出 / 做图 / 帮我生成”，不要停下来等确认；用内置 `image_gen` 每张单独生成。不要把多张图拼在一张里。

每张图只讲一个核心结构。提示词必须包含：

- 16:9 横版中文正文配图
- 纯白背景
- 黑色手绘线稿
- 少量红色/橙色/蓝色中文手写批注
- 大量留白
- ReelOS 固定 IP 作为核心动作主体；即使用户未提“镜环小工”，也写清角色物理特征：深蓝近黑身体、同心镜头环脸、米白外环、橙色内芯、细手细腿、冷静表情
- 禁止 PPT、商业插画、幼稚可爱、复杂架构、左上角类型标题

优先使用 `assets/reelos/jinghuan-worker-character-sheet.png` 校准角色。`assets/examples/` 是旧版 legacy 风格案例，只能参考线条密度、留白和颜色克制，不要参考旧角色外形。不要复刻过往案例，不能直接复用“传送带断点 / 角色拉线 / 素材鱼 / 盖章工具箱 / 常见坑路径”等已有构图，除非用户明确要求复刻某张图。每次都要从当前文章重新发明一个奇怪但成立的隐喻。

### 4. ReelOS.ai 站内文章落地

当用户在 ReelOS.ai 网站仓库里说“给文章配插图 / 要配插图 / 更新正文配图 / 早期文章插图不够详细”等，默认不只生成图片，还要把图片接入文章页面。

优先按这个流程执行：

1. 读取目标 Markdown / MDX 正文，先找 3-6 个认知锚点，不要平均配图。
2. 区分两种图：`heroImage` 是站内列表卡片 / 分享封面，正文 `<figure>` 是阅读解释图。不要默认把白底正文解释图直接当列表封面。
3. 如果文章没有 `heroImage`，优先生成一张统一暗色 ReelOS banner 封面补到 frontmatter；正文解释图仍按认知锚点插入正文。
4. 只有当用户明确要求“白底手绘图也做封面”，或当前栏目已有一致白底封面系统时，才把正文解释图用作 `heroImage`。
5. 图片保存到站内公开资产目录，路径优先使用：

```text
public/assets/articles/<article-slug>-illustrations/
public/assets/signals/<signal-slug>-illustrations/
public/assets/playbooks/<playbook-slug>-illustrations/
```

6. 命名使用稳定序号和主题：

```text
01-router-control-plane.svg
02-goal-routing.svg
article-slug-cover.svg
```

7. 正文用 `<figure class="article-illustration">` 插入，图片要有 `alt`、`loading="lazy"`、`decoding="async"`，并配一句短 `figcaption`。不要只把图片塞在段落之间。

示例：

```html
<figure class="article-illustration">
  <img src="/assets/articles/article-slug-illustrations/01-topic.svg" alt="一句清楚描述图片含义的中文 alt" loading="lazy" decoding="async" />
  <figcaption>这张图帮助读者理解的关键判断。</figcaption>
</figure>
```

8. 如果站点需要更快加载、可版本管理、可微调，优先使用轻量 SVG 手绘图；如果用户明确要求真实生成图或 raster bitmap，再用 `image_gen` 生成 PNG。
9. 正文 SVG 要遵守风格 DNA：白底、黑线、少量橙/蓝/红标注、大量留白、镜环小工承担核心动作。不要因为是 SVG 就变成正式 PPT 架构图。
10. 插图完成后运行站点构建或至少验证页面 HTML 中图片路径存在。线上发布后用 `curl` 或浏览器确认图片 URL 返回 200。

### 4.1 站内列表封面 / heroImage 规则

ReelOS.ai 的列表卡片需要一致的封面识别。给文章、Signals、Playbooks、Skills 新增或更新 `heroImage` 时，优先使用“暗色品牌 banner”，不要把正文白底解释图直接放到列表第一屏，除非已有同栏目明确采用白底封面。

封面 banner 的推荐形态：

- 16:9 / 1200x630 SVG。
- 深蓝黑背景：接近 `#0b121d`、`#111a31`、`#1a2142`。
- 可叠加克制网格和一条橙蓝光带，与 ReelOS.ai 现有深色封面保持一致。
- 左上角使用橙色描边胶囊标签，例如 `Skill Review`、`Provider Selection`、`Trust & Safety Gateway`。
- 主标题使用短中文，不要把完整长标题全塞进封面；2-3 行以内。
- 副标题只保留一句判断，帮助读者理解主题。
- 右侧可以放 1 个简化结构、面板、路线、路由盘、控制台或小角色动作。
- 使用 ReelOS logo 色调：橙色路径 / 重点，蓝紫做系统状态或光带。
- 可以出现镜环小工，但不要在画面文字里写“镜环小工”四个字；让形象出现即可。

封面 banner 的禁忌：

- 不要使用正文白底解释图作为列表卡片封面，导致前后卡片色调断裂。
- 不要做成 PPT 信息图或复杂架构图。
- 不要堆太多节点、箭头和文字。
- 不要让卡片封面和正文第一张图完全重复；封面负责“识别与点击”，正文图负责“解释与理解”。

当一篇文章需要两类图时，建议路径：

```text
public/assets/articles/<slug>-cover.svg
public/assets/articles/<slug>-illustrations/01-topic.svg
public/assets/articles/<slug>-illustrations/02-topic.svg
```

frontmatter 示例：

```yaml
heroImage: "/assets/articles/<slug>-cover.svg"
```

### 4.2 正文 SVG 解释图显示规则

ReelOS.ai 的正文解释图通常已经在 SVG 内部自带白底、浅网格、卡片或手绘框。如果页面容器再额外挂边框、白底和阴影，容易出现“框里套框”、图片变小、留白过重的问题。

落地正文 SVG 时，优先采用轻容器：

- `<figure class="article-illustration">` 仍然保留，用于统一宽度、间距和图注。
- `.article-illustration img[src$=".svg"]` 不要额外加重边框、白底和阴影；让 SVG 自己的画面结构承担承托。
- 正文 SVG 宽度应略大于普通正文列宽，推荐约 `min(100%, 820px)`，避免解释图信息太挤或看起来像缩略图。
- 图注保持低调，字号小、颜色淡、间距紧一些；图注解释“这张图帮助理解什么”，不要重复标题。
- PNG/JPG/WebP 等真实图片或位图仍可保留轻边框和阴影，避免直接贴在网格背景上显得散。
- 如果某张 SVG 内部已经有多层白底卡片，优先改 SVG 内部留白和构图；不要再靠页面外框补救。

CSS 思路示例：

```css
.article-illustration {
  width: min(100%, 820px);
  margin: 30px auto 32px;
}

.article-illustration img {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: contain;
}

.article-illustration img[src$=".svg"] {
  border: 0;
  background: transparent;
  box-shadow: none;
}
```

### 5. 检查与迭代

生成后检查 `references/qa-checklist.md`。如果出现以下问题，优先重生成或局部编辑：

- 镜环小工只是装饰
- 画面太满
- 太像流程图/PPT
- 中文太多或错字严重
- 左上角出现“常见坑/流程图/系统架构图”等标题
- 画风太可爱、幼稚、死板
- 背景不是干净白底

### 6. 保存交付

如果用户在 workspace 内工作，把最终图复制到：

```text
assets/<article-slug>-illustrations/
```

按顺序命名：

```text
01-topic-name.png
02-topic-name.png
```

保留原始生成文件，不要覆盖已有资产，除非用户明确要求替换。

如果是在 ReelOS.ai 网站仓库内落地，优先使用上一节的 `public/assets/...` 公开路径，而不是裸 `assets/...`，这样静态站点可以直接访问。

## 输出口径

生成前的策略输出要短而准。生成后的交付要包含：

- 生成了几张
- 每张图的用途
- 保存路径
- 是否已接入正文和 `heroImage`
- 是否已构建 / 验证图片路径
- 哪些图最稳，哪些图是可选

不要长篇解释风格理论；让图自己说话。
