# 视频生产工作流

## 一句话原则

先用真实 TTS 音频确定时间，再让 Remotion 画面跟随 timing 文件。内容、声音、画面三层必须按顺序生产，不能先做画面再硬塞口播。

## 设计思想

ReelOS 口播视频生产不是“文章转视频”的机械流程，而是一套内容产品化流程。它要解决三个问题：

1. 把长文章、链接或粘贴文本变成观众听得懂、愿意听完的口播。
2. 把口播节奏变成可计算、可复用、可验证的时间轴。
3. 把时间轴变成稳定、可维护、可迭代的 Remotion 工程。

核心设计取向：

- 内容先行：先判断观点和结构，再写口播，不照搬文章段落。
- 声音定时：真实 TTS 音频是唯一节奏基准，画面服从声音。
- 一段一意：每个场景只讲一个核心意思，避免一屏多个结论。
- 视觉克制：做商业推演、教学拆解和认知表达，不做空洞科技感。
- 工程沉淀：每条视频都留下脚本、音频、manifest、timing、组件和成片，方便下一条复用。

## 输入与输出

### 输入

支持三种输入：

| 输入类型 | 示例 | 处理方式 |
| --- | --- | --- |
| URL | 文章链接、博客链接 | 先读取内容，再提炼观点 |
| 粘贴文本 | 用户直接贴长文 | 先审稿，再重写口播 |
| 已写口播稿 | 用户给出完整口播 | 只做结构校正、分段和 TTS |

### 输出

每次完整生产至少应输出：

| 产物 | 位置 | 说明 |
| --- | --- | --- |
| 口播稿 | 对话或项目文档 | 人能直接念的版本 |
| TTS 脚本 | `scripts/generate-{slug}-voiceover.mjs` | scenes、voiceId、slow、emotion |
| 音频文件 | `public/voiceover-{slug}/scene-xx.mp3` | 每段独立音频 |
| 音频 manifest | `public/voiceover-{slug}/manifest.json` | 真实时长、文件名、段落元数据 |
| timing 文件 | `src/compositions/{slug}Timings.ts` | Remotion 唯一时间来源 |
| Remotion 组件 | `src/compositions/{CompositionId}.tsx` | 画面和动画 |
| Composition 注册 | `src/Root.tsx` 或项目实际入口 | 注册可渲染视频 |
| 关键帧 | `out/stills/{slug}/` | 视觉审查 |
| MP4 成片 | `out/{slug}.mp4` | 最终交付 |

## 三层工作流

### 1. 内容层

目标：把原文变成口播。

步骤：

1. 读懂原文，提炼主旨、受众、核心概念、情绪和结尾追问。
2. 删除原文里的引用来源、重复论证、过长背景和表格细节。
3. 把书面语改成口语化表达：短句、停顿、设问、反问、感叹和转折。
4. 按“开头钩子 → 关键问题 → 分点讲解 → 总结金句 → 互动追问”重排结构。
5. 拆成 8-12 段，每段只表达一个核心意思。

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

### 3. 画面层

目标：让画面跟着 timing 服务理解。

步骤：

1. 为每段口播设计一个画面任务，例如提出问题、展示结构、强调关键词、画出关系。
2. 用 `Sequence` 对齐每段 `startFrame` 和 `durationInFrames`。
3. 用 `Html5Audio` 加载真实 TTS 音频。
4. 用 `staticFile()` 引用 `public/` 里的音频和图片。
5. 用 `interpolate()`、`spring()` 和 frame 计算做动画。
6. 导出 3-5 张关键帧做目检。
7. 完整 render 成 MP4。
8. 用 `ffprobe` 验证音视频流。

画面原则：

- 每屏只出现当前段落需要理解的信息。
- 字体大小、行高和容器宽度必须保证不溢出。
- 不使用丑线框、空洞科技感、纯渐变背景和模板卡片堆叠。
- 动效要表达关系变化，不是为了热闹。

## 详细生产步骤

### Step 1：确认任务

确认三件事：

- 视频主题是什么。
- 目标观众是谁。
- 默认风格是否使用“战略作战室风”。

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

命名规则：

| 类型 | 规则 | 示例 |
| --- | --- | --- |
| `slug` | 小写短横线 | `production-control` |
| `CompositionId` | PascalCase | `ProductionControl` |
| TTS 脚本 | `generate-{slug}-voiceover.mjs` | `generate-production-control-voiceover.mjs` |
| timing 文件 | `{camelSlug}Timings.ts` | `productionControlTimings.ts` |
| 组件文件 | `{CompositionId}.tsx` | `ProductionControl.tsx` |

### Step 4：生成 TTS

脚本职责：

- 保存每段口播文本。
- 调用 Giggle TTS。
- 输出 MP3。
- 读取真实时长。
- 生成 `manifest.json`。
- 生成 `{slug}Timings.ts`。

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

### Step 5：生成 timing

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

### Step 6：写 Remotion 组件

组件职责：

- 读取 timing。
- 渲染背景、标题、关键词、结构图和字幕。
- 对每段使用 `Sequence`。
- 用 `Html5Audio` 播放对应音频。
- 用 frame 计算做动效。

禁止：

- CSS animation。
- Tailwind animation。
- 组件里手写音频秒数。
- 动态引用不存在的 public 文件。

### Step 7：注册 Composition

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

### Step 8：关键帧目检

至少导出：

- 封面或开头帧。
- 中段结构帧。
- 高信息密度帧。
- 结尾帧。

示例：

```bash
mkdir -p out/stills/production-control
npx remotion still src/index.ts ProductionControl out/stills/production-control/cover.png --frame=120 --overwrite
npx remotion still src/index.ts ProductionControl out/stills/production-control/mid.png --frame=1800 --overwrite
npx remotion still src/index.ts ProductionControl out/stills/production-control/final.png --frame=5000 --overwrite
```

### Step 9：完整渲染

```bash
npx remotion render src/index.ts ProductionControl out/production-control-war-room-tts.mp4 --overwrite --crf=18
```

### Step 10：成片验收

```bash
ffprobe -v error -show_entries format=duration,size -show_streams -of json out/production-control-war-room-tts.mp4
```

必须确认：

- 有视频流。
- 有音频流。
- duration 合理。
- 文件大小不是异常小。

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

工程：

- `Root.tsx` 或实际入口已注册 composition。
- `tsc` 通过。
- 关键帧已目检。
- `ffprobe` 确认视频流和音频流。
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
