# ReelOS Video Production 使用指南

`reelos-video-production` 用于把中文文章、确认后的口播稿或真实网站，制作成带 TTS、音画同步、内容动效和质量验证的 Remotion 视频。

它不是单纯套模板。Skill 会先理解内容和产品，再决定视频结构、视觉语言和动效方式。

## 最快开始

在 Codex 中直接发送：

```text
使用 $reelos-video-production，给 https://reelos.ai 制作一条产品宣传视频。
先研究网站，再写口播稿；确认产品事实和品牌配色后生成云熙 TTS。
画面使用 Slide Story 模式，自动选择最适合内容的图表、流程、打字和转场动效。
最后输出 1920x1080 MP4、第一帧封面和 Remotion Studio 地址。
```

如果只说“制作视频”，默认交付 MP4。明确要求演示网页或双交付时，Skill 才会额外生成 Web Deck。

## 三种视频模式

| 模式 | 适用内容 | 典型画面 | 推荐触发词 |
| --- | --- | --- | --- |
| 标准口播视频 | 文章、观点、商业讲解 | 主题画面、重点文字、解释型动画 | `制作口播视频` |
| Slide Story | 产品宣传、科普、路演、章节式讲解 | Cover、Split、Steps、Comparison、Timeline、图表 | `Slide Story 模式` |
| SketchTalk | 哲学、心理、认知、强观点内容 | 白底黑红、大字 Beat、极简隐喻图 | `SketchTalk 模式` |

每次只选择一个主模式。主题和配色属于视觉层，不会自动改变模式。

### 可选视觉系统：深空信号系统风

当内容是 AI 系统、Agent、Skill、基础设施、研究信号或方法论产品时，可以在 Slide Story 主模式下追加“深空信号系统风”。它不是第四种主模式，而是一套视觉与动效契约。

```text
使用 $reelos-video-production，研究 https://reelos.ai，制作 60 秒 Slide Story 产品宣传 MP4。
采用深空信号系统风，使用真实官网证据；
观点层、结构层、证据层分明，按语义自动选择汇聚、拓扑、矩阵、路径、闭环和动排；
相邻场景避免重复构图，全片只保留一个强度 5 的英雄时刻；
完成低清预览、静音审查和 VFX 终审后再输出。
```

## 常用提示词

### 1. 网站产品宣传片

```text
使用 $reelos-video-production。
研究 https://reelos.ai，并制作一条 60 秒产品宣传片。

要求：
- Slide Story 模式，交付 MP4；
- 使用网站当前真实文案、界面和品牌色；
- 先写口播稿，再生成 TTS；
- timing 必须来自最终音频；
- 自动动效导演根据语义选择增长曲线、流程、打字、界面推进和转场；
- 第一帧可以直接作为封面；
- 输出成片路径、封面路径和 Studio 地址。
```

### 2. 更强调动效的产品视频

```text
使用 $reelos-video-production，给 https://reelos.ai 制作 Slide Story 品宣视频。

希望视觉更有动感，但不要随机堆动效：
- 数据变化用曲线或计数动画；
- 工作流用节点、路径和状态推进；
- 产品名称和网址用打字动画；
- 关键判断使用短暂停顿和强标题；
- 相邻两幕不能重复同一种构图；
- 每个 beat 生成候选动效并评分，只采用合格方案。
```

### 3. 使用已经确认的口播稿

```text
使用 $reelos-video-production。
下面是已经确认的口播稿，请不要改写内容。

为 https://reelos.ai 制作 16:9 Slide Story 视频：
- 重新生成 TTS；
- 按最终音频重建 timing；
- 官网研究只用于核对产品事实、视觉和素材；
- 不加逐字字幕，只保留关键观点和图表动效；
- 完成关键帧审查后再渲染终版。

【在这里粘贴口播稿】
```

### 4. 同时输出演示稿和视频

```text
使用 $reelos-video-production。
把 https://reelos.ai 做成一套产品介绍 Slide Story。

使用 slides-dual：
1. 输出可点击播放的 Web Deck；
2. 使用同一份内容规划输出带云熙口播的 MP4；
3. Web 动效和视频动效分别实现，不能把浏览器点击状态直接搬进 Remotion；
4. 两个交付物保持相同的章节、事实和品牌视觉。
```

## Skill 会自动完成什么

完整流程如下：

```text
内容或网站研究
→ 口播稿与标题
→ TTS
→ 真实音频 timing
→ 视觉设计卡
→ Motion Brief
→ 自动动效评分与去重复
→ VFX 特效预算与英雄时刻
→ Beat Motion Map
→ Remotion 合成
→ 低清全片与四种观看模式
→ 100 分终审与定向返修
→ MP4 渲染与技术验证
```

其中有三条硬规则：

1. 修改口播稿后，必须重新生成 TTS 和 timing。
2. 动效必须解释当前内容关系，不能只为了让画面一直动。
3. 第一帧、场景中间态和最终成片都必须经过检查。

## 自动动效导演如何决策

Skill 会先判断当前段落的语义，再选择画面动作：

| 内容关系 | 优先动效 |
| --- | --- |
| 数量、速度、增长 | 曲线、计数、柱形变化 |
| 流程、因果、系统 | 节点、路径、分层架构、状态推进 |
| 前后差异、方案取舍 | Split、Comparison、过滤与收敛 |
| 产品界面、功能操作 | 真实截图、局部聚焦、扫描、界面推进 |
| 品牌名称、网址、命令 | 打字、光标、确认状态 |
| 强判断、结论 | 大标题、停顿、聚焦、弱化背景 |

每个 Beat 默认生成 2–3 个候选方案，并按语义匹配、可读性、节奏、品牌一致性和渲染稳定性评分。低分方案会被降级或替换，相邻镜头还会进行构图去重复。

## 输入越完整，结果越稳定

建议提供：

- 真实网址或完整内容；
- 视频目标，例如产品宣传、科普、融资路演；
- 目标时长和画幅；
- 明确的模式；
- 已确认的音色或 voice id；
- 希望保留或避免的视觉元素；
- 参考视频、截图或过去满意的版本。

信息不完整时，Skill 会基于内容和现有项目上下文做保守判断。

## 默认交付物

完成后应提供：

- 最终 MP4；
- 第一帧封面 PNG；
- 最终口播稿和 TTS；
- 真实音频 timing；
- Slide Story Plan 或分镜规划；
- Motion Decision Plan；
- VFX Enhancement Plan；
- Final Acceptance Report；
- Remotion composition 源码；
- Studio 预览地址；
- 类型检查、关键帧、解码、音视频流、黑帧和响度验证结果。

## 本地环境

需要：

- Node.js 和 npm；
- FFmpeg 与 ffprobe；
- 可运行的 Remotion 项目；
- TTS 所需的环境变量，例如 `GIGGLE_API_KEY`。

不要把 API key 写入提示词、源码、README 或 Git 提交。

## 查看与重新渲染

在生成的视频工程中运行：

```bash
npm install
npm run studio
npm run typecheck
npm run render
```

实际脚本名称以生成工程的 `package.json` 为准。

## 一句话记住

最稳定的调用方式是：

```text
使用 $reelos-video-production + 真实网址或定稿 + 明确模式 + 交付要求。
```

例如：

```text
使用 $reelos-video-production，研究 https://reelos.ai，采用 Slide Story 模式制作 60 秒产品宣传 MP4，并自动选择最适合内容的动效。
```
