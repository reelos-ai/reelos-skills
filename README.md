# ReelOS Skills

[中文](README.zh-CN.md) | English

ReelOS Skills is a collection of reusable Codex skills for Chinese content production, visual design, illustration, reading workflows, and narrated video creation.

The repository is organized as a skill library. Each folder under `skills/` is an independent skill with its own `SKILL.md`, agent metadata, references, examples, scripts, or assets.

## What This Repo Is For

Use this repo when you want Codex to handle repeatable ReelOS workflows with stable quality:

- turn Chinese articles, pasted scripts, or links into narrated Remotion videos;
- create SketchTalk-style vertical thought posters and video cover systems;
- generate ReelOS-style Chinese article illustrations;
- review or build refined visual taste systems;
- accelerate PDF reading and knowledge extraction;
- keep production workflows, visual rules, and motion rules as reusable skills instead of one-off prompts.

## Available Skills

| Skill | Use when | Main output |
| --- | --- | --- |
| `koubo-shengao-yuan` | You want to turn written Chinese material into an energetic self-media narration script before TTS or video production. | Reviewed narration script, TTS segmentation guidance, video workflow checks |
| `reelos-video-production` | You want a Chinese narrated Remotion video with TTS, timing sync, visual design, motion direction, render, and validation. | MP4 video, TTS assets, timing files, Remotion composition, review frames |
| `reelos-sketchtalk` | You want a SketchTalk / vertical thought poster / strong viewpoint cover / black-red-white minimalist visual system. | 9:16 cover images, storyboard pages, metaphor illustration prompts |
| `reelos-design-taste` | You want design taste review, typography direction, cultural visual systems, or reference extraction. | Design decisions, style systems, review notes, UI/visual guidance |
| `reelos-editorial-line-system` | You want one image to make an article, argument, product idea, or AI/tech analysis clear in a ReelOS editorial line-art style. | Article lead images, explainer visuals, style-mode prompts, text-safe visual systems |
| `reelos-jinghuan-illustrations` | You want ReelOS-style Chinese article illustrations or brand article visuals. | Illustration prompts, article figures, cover/banner guidance |
| `reelos-voice-cinema` | You want an independent voice-cinema style Remotion video workflow. | Narrated video, subtitle effects, motion material guidance |
| `reelos-creative-15s` | You want a ReelOS-branded 15-second creative video script from one image or creative brief. | Brand-forward shot script, voiceover beats, BGM and sound design guidance |
| `pdf-book-accelerator` | You want to skim, summarize, study, or extract knowledge from a PDF book. | Chapter notes, summaries, action lists, review cards |

## Recommended Install Order

For ordinary design or illustration work, install only the skill you need.

For video production, install dependencies in this order:

1. System tools: Node.js, pnpm/npm, FFmpeg, and a working Remotion project.
2. Base video skills: Remotion guidance and any TTS skill used in your Codex environment.
3. Optional motion references: transitions.dev / GSAP skills if you want richer motion vocabulary.
4. ReelOS skills from this repository.
5. Restart Codex after installation so new skills are loaded.

The detailed video dependency map lives in:

```text
skills/reelos-video-production/references/setup-dependencies.md
```

## Install A Skill

From any local directory, run the Codex skill installer:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production
```

Install SketchTalk:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-sketchtalk
```

Install the narration reviewer:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/koubo-shengao-yuan
```

Install the ReelOS 15-second creative script generator:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-creative-15s
```

Install the ReelOS editorial line system:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-editorial-line-system
```

Install multiple skills at once:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path \
    skills/koubo-shengao-yuan \
    skills/reelos-video-production \
    skills/reelos-sketchtalk \
    skills/reelos-design-taste \
    skills/reelos-editorial-line-system \
    skills/reelos-jinghuan-illustrations \
    skills/reelos-creative-15s
```

Install from a specific branch or tag:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --ref main \
  --path skills/reelos-video-production
```

After installing, restart Codex.

## Update A Skill

Re-run the same install command. The installer will overwrite the local installed copy with the version from GitHub.

Example:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production
```

If Codex does not pick up the update, restart Codex and confirm the skill appears in the available skills list.

## How To Invoke Skills In Codex

You can call a skill explicitly by name:

```text
Use $koubo-shengao-yuan to rewrite this article into a natural Chinese narration script.
```

```text
Use $reelos-video-production to turn this script into a narrated video.
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

You can also describe the task naturally. Codex can select the skill when the request matches the skill description:

```text
把这篇文章做成口播视频，TTS 和画面要同步。
```

```text
按深度进化 Theo 那种黑红白强观点风格，给我做一个竖屏封面。
```

Explicit invocation is still recommended when you want deterministic behavior.

## Video Production Workflow

Use `reelos-video-production` for full narrated videos.

The intended workflow is:

1. Review the source with `koubo-shengao-yuan` when the input is article-like or too written.
2. Confirm the voiceover script.
3. Confirm title packaging and style selection.
4. Run the voiceover review step.
5. Generate or update TTS.
6. Generate timing from real audio.
7. Create the visual design card.
8. Create the motion brief.
9. Create the Beat Motion Map.
10. Build or update the Remotion composition.
11. Export keyframes for review.
12. Render MP4.
13. Validate audio/video streams and visible output.

Older workflow summaries may start from script confirmation. In practice, if the user gives raw article text, run the narration reviewer first.

Important rules:

- If the user changes the voiceover script, regenerate TTS and timing. Do not only change on-screen text.
- Screen text, beat captions, footer notes, and metaphor graphics must all follow the latest script.
- The first frame should be a usable cover frame when the template requires it.
- Motion should explain content relationships, not add random decoration.
- For SketchTalk-style videos, the main beat caption, top red prompt, and footer note must not repeat the same sentence.

## Narration Review Workflow

Use `koubo-shengao-yuan` before video production when the source is a long article, formal essay, pasted viewpoint text, or rough draft.

It is responsible for:

1. Understanding the source content and extracting the core point.
2. Identifying the target audience, tone, emotional intensity, and one sentence the audience should remember.
3. Rewriting written language into natural spoken Chinese.
4. Strengthening the hook, rhythm, transitions, examples, and final question.
5. Splitting the script into TTS-friendly segments.
6. Checking whether the script is ready for `reelos-video-production`.

Default style:

```text
自媒体人口播风格，热情、接地气、有经验，像一个博主在镜头前自然表达。
```

Use it alone when the user only asks for a polished narration script. Use it together with `reelos-video-production` when the final deliverable is a video.

Detailed workflow:

```text
skills/reelos-video-production/references/video-production-workflow.md
```

Motion direction:

```text
skills/reelos-video-production/references/motion-director.md
```

Visual design system:

```text
skills/reelos-video-production/references/visual-design-system.md
```

## SketchTalk Workflow

Use `reelos-sketchtalk` for 9:16 vertical thought posters, cover images, and storyboard pages.

Best suited for:

- philosophy / psychology / cognition content;
- strong viewpoint covers;
- black-red-white minimalist layouts;
- “one sentence, one visual metaphor” storyboards;
- video cover frames for `reelos-video-production`.

Default visual structure:

```text
[top series / episode metadata]

[red premise sentence]

[large black main statement]
[thin English subtitle]

[minimal metaphor illustration in lower third]

[small footer keywords]
```

Read the layout reference when changing the template:

```text
skills/reelos-sketchtalk/references/layout-template.md
```

Read the metaphor system when designing lower-third illustrations:

```text
skills/reelos-sketchtalk/references/metaphor-system.md
```

## How `reelos-video-production` And `reelos-sketchtalk` Work Together

Use them together when producing the current SketchTalk-style narrated videos.

Recommended division:

- `reelos-sketchtalk` defines the cover, typography hierarchy, lower-third metaphor, and black-red-white visual grammar.
- `reelos-video-production` turns the script into TTS-synced Remotion video, applies timing, motion, beat captions, render, and validation.

Practical flow:

1. Use `reelos-sketchtalk` to define the cover and visual metaphor system.
2. Use `reelos-video-production` to generate TTS, timing, Beat Motion Map, and MP4.
3. If the video looks repetitive, update the Beat Motion Map and lower-third metaphor states.
4. If the script changes, rerun TTS/timing before rendering again.

## Example Prompts

Full narrated video:

```text
Use $koubo-shengao-yuan and then $reelos-video-production.
把下面这篇稿子做成 3 分钟口播视频。
要求：TTS 同步、画面不要重复、底部隐喻图要跟随口播变化、导出 MP4。
```

SketchTalk narrated video:

```text
Use $reelos-video-production.
用 ReelOS SketchTalk｜黑红白强观点哲思风制作口播视频。
要求：第一帧就是封面，白底黑红灰，主 beat 字幕跟随真实音频，底部隐喻图随每个 beat 变化。
```

Narration review only:

```text
Use $koubo-shengao-yuan.
把这篇文章改成 3 分钟以内的自媒体口播稿，语言要口语化、有停顿、有互动感。
```

SketchTalk cover:

```text
Use $reelos-sketchtalk.
给《空见心力》第5集做一个竖屏封面。
主题：每天，问自己一个更好的问题。
风格：白底、黑红、强观点、底部极简隐喻图。
```

Visual review:

```text
Use $reelos-design-taste.
Review this video frame and tell me whether typography, spacing, and color hierarchy are working.
```

Article illustration:

```text
Use $reelos-jinghuan-illustrations.
为这篇 ReelOS 文章生成 3 张正文配图建议和 heroImage 方案。
```

PDF reading:

```text
Use $pdf-book-accelerator.
帮我把这本 PDF 拆成章节摘要、关键问题、行动清单和复习卡片。
```

## Repository Layout

```text
reelos-skills/
├── README.md
├── skills/
│   ├── koubo-shengao-yuan/
│   ├── pdf-book-accelerator/
│   ├── reelos-design-taste/
│   ├── reelos-jinghuan-illustrations/
│   ├── reelos-sketchtalk/
│   ├── reelos-video-production/
│   └── reelos-voice-cinema/
└── .gitignore
```

Common skill structure:

```text
skill-name/
├── SKILL.md              # Required skill entry point
├── agents/openai.yaml    # Optional display metadata
├── references/           # Detailed instructions and reusable rules
├── examples/             # Optional usage examples
├── scripts/              # Optional helper scripts
└── assets/               # Optional reference assets
```

## Authoring Rules

When adding or updating a skill:

- Keep each skill self-contained.
- Put the entry behavior in `SKILL.md`.
- Put long guidance in `references/`.
- Put examples in `examples/`.
- Put helper scripts in `scripts/`.
- Avoid machine-specific paths in committed files.
- Do not commit local install artifacts such as `.agents/` or `skills-lock.json`.
- Do not commit secrets, API keys, generated videos, `node_modules/`, or temporary render output.

## Git Workflow

Recommended workflow for updates:

```bash
git switch main
git pull origin main
git switch -c codex/update-skill-name
# edit skill files
git diff --check
git add skills/<skill-name> README.md
git commit -m "Update <skill-name> skill"
git push -u origin codex/update-skill-name
```

Then open a pull request.

For small README or ignore-file updates, direct commits to `main` are acceptable if the repository owner allows it.

## Troubleshooting

### The skill does not appear in Codex

Reinstall the skill, then restart Codex.

### The wrong version is being used

Re-run the installer from `main`, then restart Codex:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --ref main \
  --path skills/reelos-video-production
```

### Local generated files appear in `git status`

They should be ignored by `.gitignore`.

If they still appear, check whether they were already tracked:

```bash
git status --short
git check-ignore -v .agents skills-lock.json
```

### Video output is not synchronized

For `reelos-video-production`, regenerate TTS and timing from the latest script. Do not reuse old timing after rewriting the voiceover.

### SketchTalk frames feel repetitive

Update the Beat Motion Map and lower-third metaphor states. Each beat should change at least one visible element such as text, path, red point, node state, or illustration position.

## License

Add a license before publishing this repository for broad external reuse.
