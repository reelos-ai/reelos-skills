# 依赖与安装手册

这份文档用于在新机器、新项目或新 Codex 会话里稳定运行 ReelOS 口播视频生产流程。安装顺序必须是：

1. 机器级程序。
2. Remotion 视频项目依赖。
3. TTS 环境变量。
4. 基础 Codex skills。
5. `reelos-video-production` workflow skill。
6. 验证命令。

## 1. 依赖关系总览

| 层级 | 组件 | 用途 | 安装方式 |
| --- | --- | --- | --- |
| 系统程序 | Node.js / npm | 运行 Remotion、Next、脚本和 npm 依赖 | Homebrew、nvm 或官方安装包 |
| 系统程序 | ffmpeg / ffprobe | 音频处理、读取音视频真实时长、成片验收 | `brew install ffmpeg` |
| 系统程序 | Git | 克隆和推送 skill 仓库 | Xcode Command Line Tools 或 Homebrew |
| 系统程序 | GitHub CLI `gh` | 私有仓库鉴权、修复 HTTPS git 凭据 | `brew install gh` |
| 项目依赖 | Remotion | React 视频合成、Studio 预览、still/render 导出 | `npm install` |
| 项目依赖 | React / React DOM | Remotion 组件运行基础 | `npm install` |
| 项目依赖 | TypeScript / tsx | 类型检查、运行 TTS 生成脚本 | `npm install` |
| 项目依赖 | `@remotion/player` | Web app 内预览 Remotion composition | `npm install` |
| 项目依赖 | `ffmpeg-static` | 项目内 ffmpeg fallback | `npm install` |
| 外部服务 | Giggle TTS API | 生成中文口播音频 | 设置 `GIGGLE_API_KEY` |
| 外部服务 | Pexels API | 可选，搜索主题背景视频素材 | 设置 `PEXELS_API_KEY` |
| 外部服务 | Pixabay API | 可选，搜索主题背景视频素材 | 设置 `PIXABAY_API_KEY` |
| 外部服务 | Coverr API | 可选，搜索横屏背景视频素材 | 设置 `COVERR_API_KEY` |
| Codex skill | `koubo-shengao-yuan` | 内容理解、口播审稿、分段 | skill 安装 |
| Codex skill | `giggle-generation-speech` | Giggle TTS 调用能力 | skill 安装 |
| Codex skill | `remotion-best-practices` | Remotion 工程约束 | skill 安装 |
| Codex skill | `reelos-design` | ReelOS 视觉审美与风格审查 | skill 安装 |
| Codex skill | `reelos-jinghuan-illustrations` | 可选，ReelOS 插图和品牌视觉资产 | skill 安装 |
| Codex skill | `reelos-video-production` | 最终编排整个口播视频生产流程 | 本仓库安装 |

## 2. 安装系统程序

### 2.1 安装 Homebrew

如果 macOS 上还没有 Homebrew，先安装：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

检查：

```bash
brew -v
```

### 2.2 安装 Node.js 和 npm

推荐使用 LTS 版本。任选一种方式。

方式 A，Homebrew：

```bash
brew install node
node -v
npm -v
```

方式 B，nvm：

```bash
brew install nvm
mkdir -p ~/.nvm
nvm install --lts
nvm use --lts
node -v
npm -v
```

### 2.3 安装 ffmpeg 和 ffprobe

```bash
brew install ffmpeg
ffmpeg -version
ffprobe -version
```

`ffmpeg` 用于调整音频语速、拼接静音、转码。`ffprobe` 用于读取 MP3 和 MP4 的真实时长、码率、帧率和音视频流。

### 2.4 安装 GitHub CLI

私有仓库安装 skill、推送文档和修复 git HTTPS 凭据都建议使用 `gh`。

```bash
brew install gh
gh auth login
gh auth status
gh auth setup-git
```

如果 `git push` 报 `could not read Username for 'https://github.com'`，通常执行 `gh auth setup-git` 后再 push 即可。

## 3. 安装 Remotion 视频项目依赖

进入视频项目目录，例如：

```bash
cd "/Users/netseek/Documents/vibe remotion/vibe-motion"
```

安装项目依赖：

```bash
npm install
```

当前项目依赖里和视频生产直接相关的组件包括：

| npm 包 | 用途 |
| --- | --- |
| `remotion` | 核心视频合成、`Sequence`、`Html5Audio`、`staticFile`、`interpolate` |
| `@remotion/player` | Web 页面内预览 composition |
| `react` / `react-dom` | Remotion 组件运行基础 |
| `typescript` | 类型检查，避免 render 前才发现接口错误 |
| `tsx` | 运行 `.mjs` / TypeScript 辅助脚本 |
| `ffmpeg-static` | 项目内 ffmpeg fallback |
| `sharp` | 图片处理和部分构建场景依赖 |
| `lucide-react` | UI 图标 |
| `next` | 项目应用外壳和路由 |

启动项目应用：

```bash
npm run dev
```

如果项目使用独立 Remotion Studio，也可以运行：

```bash
npx remotion studio src/index.ts --port=3002
```

如果项目没有独立 `src/index.ts`，以实际 Remotion entry 文件为准。

## 4. 配置 Giggle TTS

必须设置 `GIGGLE_API_KEY`。不要把真实 key 写入代码、文档、`.env` 或提交历史。

临时设置，只对当前终端有效：

```bash
export GIGGLE_API_KEY="你的 key"
```

写入 zsh：

```bash
echo 'export GIGGLE_API_KEY="你的 key"' >> ~/.zshrc
source ~/.zshrc
```

检查是否存在，不要打印完整 key：

```bash
test -n "$GIGGLE_API_KEY" && echo "GIGGLE_API_KEY is set"
```

默认使用用户指定 voice id。当前流程里常用 voice id 示例：

```text
clone_20260518_060330_483432
```

voice id 可以写在生成脚本配置里，API key 不可以写进脚本。

## 4.1 可选：配置主题素材 API

只有需要主题素材增强、背景视频或真实纹理叠加时才需要这些 API key。不要把 key 写入代码、文档、`.env` 或提交历史。

```bash
export PEXELS_API_KEY="你的 pexels key"
export PIXABAY_API_KEY="你的 pixabay key"
export COVERR_API_KEY="你的 coverr key"
```

检查是否存在，不要打印完整 key：

```bash
test -n "$PEXELS_API_KEY" && echo "PEXELS_API_KEY is set"
test -n "$PIXABAY_API_KEY" && echo "PIXABAY_API_KEY is set"
test -n "$COVERR_API_KEY" && echo "COVERR_API_KEY is set"
```

如果没有这些 key，流程仍可运行；视觉设计师应跳过 API 检索，改用已有项目素材、公共版权网页手动下载素材，或不加外部素材层。

## 5. 安装基础 Codex skills

`reelos-video-production` 是编排 skill，它依赖下面这些基础能力。先装基础 skills，再装本 skill。

### 5.1 口播审稿 skill

用途：

- 深入理解文章。
- 把书面语改成自媒体口播。
- 控制节奏、停顿、情绪和互动感。
- 输出可进入 TTS 的分段稿。

安装方式取决于团队维护位置。如果使用当前团队私有仓库，可以从 `reelos-ai/reelos-skills` 安装未来公开版本；如果本地已有 `koubo-shengao-yuan`，检查即可：

```bash
test -f ~/.codex/skills/koubo-shengao-yuan/SKILL.md && echo "koubo-shengao-yuan installed"
```

如果团队通过 `remotion-dev/skills` 分发口播和 Remotion 相关 skills：

```bash
npx skills add remotion-dev/skills
```

### 5.2 Giggle TTS skill

用途：调用 Giggle TTS，提交文本转语音任务，获取音频。

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo giggle-official/skills \
  --path skills/giggle-generation-speech
```

如果 Python 证书报错，改用 git mode：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo giggle-official/skills \
  --path skills/giggle-generation-speech \
  --method git
```

检查：

```bash
test -f ~/.codex/skills/giggle-generation-speech/SKILL.md && echo "giggle-generation-speech installed"
```

### 5.3 Remotion 最佳实践 skill

用途：

- 避免 CSS animation、错误资产路径和不可复现的 render 行为。
- 使用 `Sequence`、`Html5Audio`、`staticFile`、`interpolate` 等 Remotion 原生模式。
- 约束 still、render、ffprobe 验收方式。

安装：

```bash
npx skills add remotion-dev/skills
```

检查：

```bash
test -f ~/.codex/skills/remotion-best-practices/SKILL.md && echo "remotion-best-practices installed"
```

### 5.4 ReelOS 视觉审美 skill

用途：

- 选择“战略作战室风”“黑板推演风”等视觉方向。
- 去掉 AI 味、模板味、丑线框和单调配色。
- 审查画面层级、字体、色彩、动效和信息密度。

检查：

```bash
test -f ~/.codex/skills/reelos-design/SKILL.md && echo "reelos-design installed"
```

如果团队将其放入私有 skill 仓库，按该仓库路径安装。安装后必须重启 Codex。

### 5.5 ReelOS 插图 skill，可选

用途：生成 ReelOS 品牌正文配图或镜环小工 IP 插图。口播视频核心流程不强依赖它，但需要品牌插图时建议安装。

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-jinghuan-illustrations \
  --method git
```

## 6. 安装本 workflow skill

基础程序、项目依赖、环境变量和基础 skills 都准备好以后，再安装本 skill：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production \
  --method git
```

检查：

```bash
test -f ~/.codex/skills/reelos-video-production/SKILL.md && echo "reelos-video-production installed"
```

安装后重启 Codex，让新 skill 进入可发现列表。

## 7. 从零安装推荐命令

下面是 macOS 上的一组最小命令。真实 API key 用你自己的，不要粘贴到仓库里。

```bash
brew install node ffmpeg gh
gh auth login
gh auth setup-git
```

```bash
cd "/Users/netseek/Documents/vibe remotion/vibe-motion"
npm install
test -n "$GIGGLE_API_KEY" && echo "GIGGLE_API_KEY is set"
```

```bash
npx skills add remotion-dev/skills
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo giggle-official/skills \
  --path skills/giggle-generation-speech \
  --method git
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-jinghuan-illustrations \
  --method git
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production \
  --method git
```

## 8. 验证安装

### 8.1 验证系统和项目

```bash
node -v
npm -v
ffmpeg -version
ffprobe -version
```

```bash
cd "/Users/netseek/Documents/vibe remotion/vibe-motion"
npm exec tsc -- --noEmit
npm run dev
```

### 8.2 验证 skill 存在

```bash
for skill in koubo-shengao-yuan giggle-generation-speech remotion-best-practices reelos-design reelos-video-production; do
  test -f "$HOME/.codex/skills/$skill/SKILL.md" && echo "$skill ok" || echo "$skill missing"
done
```

### 8.3 验证已有视频合成

如果项目里已有 `ProductionControl` 这类 composition：

```bash
npx remotion still src/index.ts ProductionControl out/stills/check.png --frame=120 --overwrite
npx remotion render src/index.ts ProductionControl out/check.mp4 --overwrite --crf=18
ffprobe -v error -show_entries format=duration,size -show_streams -of json out/check.mp4
```

验证重点：

- `ffprobe` 能读到视频流。
- `ffprobe` 能读到音频流。
- MP4 duration 接近 timing 总时长。
- Studio 里打开 composition 有声音、有画面、不报错。

## 9. 常见安装问题

### Python 安装器证书校验失败

如果出现 `CERTIFICATE_VERIFY_FAILED`，使用 git mode：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production \
  --method git
```

### 私有仓库无权限

先确认 GitHub CLI 登录：

```bash
gh auth status
gh auth setup-git
```

再确认 git 可以访问：

```bash
git ls-remote https://github.com/reelos-ai/reelos-skills.git
```

### Studio 能开但没声音

检查：

- `public/voiceover-{slug}/scene-xx.mp3` 是否存在。
- Remotion 组件是否使用 `Html5Audio` 和 `staticFile()`。
- `voiceoverScenes` 的路径是否和 `public/` 目录一致。
- render 命令是否完整执行成功。
- 浏览器预览是否被静音，render 后 MP4 是否有音频流。

### 画面和声音不同步

不要手调画面。先检查：

- `manifest.json` 的真实音频时长。
- `{slug}Timings.ts` 是否由 TTS 脚本反写。
- `Sequence from` 和 `durationInFrames` 是否来自 timing 文件。
- 每段 `sceneDuration` 是否比 TTS target 多出转场缓冲。

### npm install 失败

优先处理 Node 版本和原生依赖：

```bash
node -v
npm -v
npm install
```

如果涉及 `sharp`、`node-pty`、`ffmpeg-static` 等原生依赖，先确认 Xcode Command Line Tools：

```bash
xcode-select --install
```
