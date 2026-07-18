# ReelOS Skills

中文 | [English](README.md)

ReelOS Skills 是一组可复用的 Codex skills，用于中文内容生产、视觉设计、文章插图、阅读工作流和口播视频制作。

这个仓库本质上是一个 skill library。`skills/` 下的每个目录都是一个独立 skill，通常包含自己的 `SKILL.md`、agent 元数据、参考文件、示例、脚本或素材。

## 这个仓库适合做什么

当你希望 Codex 稳定复用一套 ReelOS 工作流，而不是每次都靠临时 prompt 时，可以使用这个仓库：

- 把中文文章、脚本或链接转成可口播的 Remotion 视频；
- 制作 SketchTalk 风格的竖屏观点海报和视频封面；
- 生成 ReelOS 风格中文文章配图；
- 评审或构建更有品味的视觉系统；
- 加速 PDF 阅读、拆书和知识提取；
- 把视频生产、视觉规则和动效规则沉淀成可复用 skills。

## 可用 Skills

| Skill | 适合什么时候用 | 主要输出 |
| --- | --- | --- |
| `koubo-shengao-yuan` | 你想把书面中文材料改成更自然、有能量的自媒体口播稿，再进入 TTS 或视频制作。 | 口播稿审稿、TTS 分段建议、视频工作流检查 |
| `reelos-video-production` | 你想制作中文口播 Remotion 视频，并完成 TTS、时间轴同步、视觉设计、动效、渲染和校验。 | MP4 视频、TTS 音频、时间轴文件、Remotion composition、关键帧审阅 |
| `slides-product-promo` | 你想研究真实网站，并制作一支由 TTS 驱动、动感但不闪眼的 Bolt Slides 产品宣传片。 | 官网研究、口播、TTS、时间轴、交互 Slides、音画同步 MP4 |
| `reelos-sketchtalk` | 你想制作 SketchTalk / 竖屏思想海报 / 强观点封面 / 黑红白极简视觉系统。 | 9:16 封面图、分镜页、隐喻插画 prompt |
| `reelos-design-taste` | 你需要设计品味评审、字体方向、文化视觉系统或参考提炼。 | 设计决策、风格系统、评审意见、UI/视觉指导 |
| `reelos-editorial-line-system` | 你想用一张图把文章、观点、产品想法或 AI/科技分析讲清楚，并使用 ReelOS 编辑线稿风格。 | 文章头图、解释型视觉、风格模式 prompt、text-safe 视觉系统 |
| `reelos-jinghuan-illustrations` | 你想生成 ReelOS 风格中文文章插图或品牌文章视觉。 | 插图 prompt、文章配图、封面/banner 方向 |
| `reelos-voice-cinema` | 你想使用独立的 voice-cinema 风格 Remotion 视频工作流。 | 口播视频、字幕效果、动效素材指导 |
| `reelos-creative-15s` | 你想基于一张图或创意 brief 生成 ReelOS 品牌化 15 秒创意视频脚本。 | 品牌向镜头脚本、旁白节奏、BGM 和声音设计建议 |
| `tech-research-report` | 你想把长篇科技或行业分析做成精致的自包含研究报告页面。 | HTML 研究报告、数据可视化章节、对比面板、导出/打印控件 |
| `pdf-book-accelerator` | 你想快速浏览、总结、学习或提取 PDF 书籍知识。 | 章节笔记、摘要、行动清单、复习卡片 |

## 推荐安装顺序

普通设计、插图或阅读任务，只安装你需要的 skill 即可。

如果要做视频生产，建议按这个顺序准备：

1. 系统工具：Node.js、pnpm/npm、FFmpeg，以及可运行的 Remotion 项目。
2. 基础视频 skills：Remotion 指导、TTS 相关 skill。
3. 可选动效参考：transitions.dev / GSAP skills，用于更丰富的动效表达。
4. 本仓库中的 ReelOS skills。
5. 安装后重启 Codex，让新 skills 被加载。

视频依赖的详细说明在：

```text
skills/reelos-video-production/references/setup-dependencies.md
```

## 安装单个 Skill

在任意本地目录运行 Codex skill installer：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production
```

安装 SketchTalk：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-sketchtalk
```

安装 Bolt Slides 产品宣传片 skill：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/slides-product-promo
```

安装口播审稿 skill：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/koubo-shengao-yuan
```

安装 ReelOS 15 秒创意脚本生成器：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-creative-15s
```

安装 ReelOS Editorial Line System：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-editorial-line-system
```

安装科技研究报告生成器：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/tech-research-report
```

## 一次安装多个 Skills

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path \
    skills/koubo-shengao-yuan \
    skills/reelos-video-production \
    skills/slides-product-promo \
    skills/reelos-sketchtalk \
    skills/reelos-design-taste \
    skills/reelos-editorial-line-system \
    skills/reelos-jinghuan-illustrations \
    skills/reelos-creative-15s \
    skills/tech-research-report
```

从指定分支或 tag 安装：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --ref main \
  --path skills/reelos-video-production
```

安装完成后，请重启 Codex。

## 更新 Skill

重新运行相同安装命令即可。安装器会用 GitHub 上的版本覆盖本地已安装版本。

示例：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production
```

如果 Codex 没有识别更新，请重启 Codex，并确认 skill 出现在可用 skills 列表里。

## 如何在 Codex 中调用 Skills

你可以显式指定 skill 名称：

```text
Use $koubo-shengao-yuan to rewrite this article into a natural Chinese narration script.
```

```text
Use $reelos-video-production to turn this script into a narrated video.
```

```text
使用 $slides-product-promo，研究 https://reelos.ai，先生成营销口播和 TTS，再制作一支音画同步、动感但不闪眼的产品宣传片。
```

```text
Use $reelos-video-production.
用 ReelOS SketchTalk｜黑红白强观点哲思风制作口播视频。
```

```text
Use $reelos-sketchtalk to create a vertical cover and storyboard for this episode.
```

```text
Use $reelos-editorial-line-system to turn this article into one image that makes the argument clear.
```

也可以自然描述任务，Codex 会在任务和 skill 描述匹配时自动选择：

```text
把这篇文章做成口播视频，TTS 和画面要同步。
```

```text
按深度进化 Theo 那种黑红白强观点风格，给我做一个竖屏封面。
```

如果你希望行为更稳定，仍然建议显式调用 skill。

## 视频生产工作流

使用 `reelos-video-production` 做完整口播视频。

推荐流程：

1. 如果输入像文章或过于书面，先用 `koubo-shengao-yuan` 审稿。
2. 确认口播脚本。
3. 确认标题包装和风格选择。
4. 执行 voiceover review。
5. 生成或更新 TTS。
6. 基于真实音频生成 timing。
7. 创建设计卡。
8. 创建动效 brief。
9. 创建 Beat Motion Map。
10. 构建或更新 Remotion composition。
11. 导出关键帧审阅。
12. 渲染 MP4。
13. 校验音视频流和可见输出。

重要规则：

- 如果用户改了口播稿，必须重新生成 TTS 和 timing，不能只改屏幕文字。
- 屏幕文字、节拍字幕、底部说明和隐喻图形，都必须跟最新脚本一致。
- 模板需要封面时，第一帧应该就是可用封面帧。
- 动效要解释内容关系，而不是随机装饰。
- SketchTalk 风格视频里，主节拍字幕、顶部红色 prompt、底部说明不要重复同一句话。

## 口播审稿工作流

当输入是长文章、正式 essay、粘贴的观点文本或粗稿时，先用 `koubo-shengao-yuan`。

它负责：

1. 理解原文并提取核心观点。
2. 判断目标受众、语气、情绪强度和观众应该记住的一句话。
3. 把书面语改写成自然口播中文。
4. 强化开头 hook、节奏、转场、例子和结尾问题。
5. 切分成适合 TTS 的分段。
6. 检查脚本是否可以进入 `reelos-video-production`。

默认风格：

```text
自媒体人口播风格，热情、接地气、有经验，像一个博主在镜头前自然表达。
```

只需要口播稿时，可以单独使用它。最终要做视频时，建议和 `reelos-video-production` 一起使用。

详细工作流：

```text
skills/reelos-video-production/references/video-production-workflow.md
```

动效方向：

```text
skills/reelos-video-production/references/motion-director.md
```

视觉设计系统：

```text
skills/reelos-video-production/references/visual-design-system.md
```

## SketchTalk 工作流

使用 `reelos-sketchtalk` 制作 9:16 竖屏思想海报、封面图和分镜页。

适合：

- 哲学 / 心理学 / 认知内容；
- 强观点封面；
- 黑红白极简布局；
- “一句话，一个视觉隐喻”的 storyboards；
- `reelos-video-production` 的视频封面帧。

默认视觉结构：

```text
[顶部系列 / episode metadata]

[红色前提句]

[大号黑色主观点]
[细 English subtitle]

[下三分之一的极简隐喻插画]
```

## Skill 编写约定

每个 skill 应放在：

```text
skills/<skill-name>/
```

最低要求是一个 `SKILL.md`。较长的规则、风格系统、工作流和检查清单应拆到 `references/`，不要全部塞进 `SKILL.md`。

更多说明：

```text
docs/skill-authoring.md
```

## 贡献建议

- 新 skill 的目录名应和 `SKILL.md` frontmatter 里的 `name` 一致。
- 触发描述要具体，让 Codex 能自然选择 skill。
- 长规则放进 `references/`。
- 命令、脚本、素材、示例尽量放在 skill 自己的目录内。
- 如果新增面向社区常用的 skill，请同步更新本 README 和 `README.zh-CN.md`。

## License

请以仓库根目录中的 license 信息为准。
