# 依赖安装顺序

这份文档用于让 ReelOS 口播视频生产流程在新机器、新项目或新 Codex 会话里稳定运行。安装顺序很重要：先装系统程序和环境变量，再装基础 skills，最后安装 `reelos-video-production`。

## 1. 系统程序

### Node.js 和 npm

Remotion 依赖 Node.js。建议使用当前 LTS 版本。

检查：

```bash
node -v
npm -v
```

### ffmpeg 和 ffprobe

TTS 分段和成片验收都依赖 ffmpeg：

- `ffmpeg`：调整音频语速、补齐静音、转 MP3。
- `ffprobe`：读取音频和 MP4 的真实时长、帧率、音视频流。

macOS 安装：

```bash
brew install ffmpeg
```

检查：

```bash
ffmpeg -version
ffprobe -version
```

### GitHub CLI

如果需要创建、推送或安装私有仓库里的 skill，建议安装 `gh` 并登录。

```bash
brew install gh
gh auth login
gh auth status
```

## 2. Remotion 项目依赖

在视频项目目录里安装依赖：

```bash
npm install
```

启动 Studio：

```bash
npm run studio -- --port=3002
```

如果项目没有 `studio` script，也可以使用：

```bash
npx remotion studio --port=3002
```

## 3. Giggle TTS 环境变量

必须设置 `GIGGLE_API_KEY`。不要把 key 写入代码、文档、`.env` 或提交历史。

临时设置：

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

## 4. 先安装基础 skills

`reelos-video-production` 依赖这些基础能力。建议先安装或确认已经存在。

### 口播审稿

用途：内容理解、口播稿改写、分段、口播视频流程约束。

```bash
npx skills add remotion-dev/skills
```

如果团队使用私有版本，确保本地有 `koubo-shengao-yuan`。

### Giggle TTS

用途：调用 Giggle TTS 生成口播音频。

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo giggle-official/skills \
  --path skills/giggle-generation-speech
```

### Remotion 最佳实践

用途：约束 Remotion 写法，避免 CSS animation、错误资产引用和不同步。

```bash
npx skills add remotion-dev/skills
```

### ReelOS 视觉审美

用途：风格选择、去 AI 味、战略作战室风、黑板推演风、排版和视觉审查。

如果在 ReelOS 私有 skill 仓库里：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-jinghuan-illustrations
```

说明：`reelos-jinghuan-illustrations` 主要负责正文配图和品牌插图，不是 Remotion 视频核心依赖；但如果视频需要 ReelOS IP 插图素材，建议安装。

## 5. 最后安装本 skill

基础程序、环境变量和基础 skills 都准备好以后，再安装本 skill：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production
```

安装后重启 Codex，让新 skill 进入可发现列表。

## 6. 推荐验证顺序

安装完成后，在 Remotion 视频项目里执行：

```bash
npm exec tsc -- --noEmit
npm run studio -- --port=3002
```

生成 TTS 的项目还要验证：

```bash
test -n "$GIGGLE_API_KEY" && echo "GIGGLE_API_KEY is set"
ffprobe -version
```

如果有现成合成，例如 `ProductionControl`：

```bash
npx remotion still src/index.ts ProductionControl out/stills/check.png --frame=120 --overwrite
npx remotion render src/index.ts ProductionControl out/check.mp4 --overwrite --crf=18
ffprobe -v error -show_entries format=duration,size -show_streams -of json out/check.mp4
```

## 7. 常见安装问题

### Python 安装器证书校验失败

如果出现 `CERTIFICATE_VERIFY_FAILED`，可以改用 git 方式：

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
```

或确认 git 可以访问：

```bash
git ls-remote https://github.com/reelos-ai/reelos-skills.git
```

### Studio 能开但没声音

检查：

- `public/voiceover-{slug}/scene-xx.mp3` 是否存在。
- Remotion 组件是否使用 `Html5Audio` 和 `staticFile()`。
- `voiceoverScenes` 的路径是否和 public 目录一致。
- render 命令是否完整执行成功。

### 画面和声音不同步

不要手调画面。先检查：

- `manifest.json` 的真实音频时长。
- `{slug}Timings.ts` 是否由 TTS 脚本反写。
- `Sequence from` 是否用 timing 文件。
- 每段 `sceneDuration` 是否比 TTS target 多 1 秒转场缓冲。
