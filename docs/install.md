# Install ReelOS Skills

## Dependency Order

For stable video production, install in this order:

1. System programs: Node.js, npm, ffmpeg, ffprobe, Git, and optionally GitHub CLI.
2. Project dependencies: run `npm install` in the Remotion video project.
3. Environment variable: set `GIGGLE_API_KEY` in the shell, never in committed files.
4. Base skills: `koubo-shengao-yuan`, `giggle-generation-speech`, `remotion-best-practices`, `reelos-design`.
5. Optional visual asset skill: `reelos-jinghuan-illustrations`.
6. Final workflow skill: `reelos-video-production`.
7. Verification: run TypeScript, Studio/still render, full MP4 render, and `ffprobe`.

Detailed dependency map, third-party components, and install commands are in:

```text
skills/reelos-video-production/references/setup-dependencies.md
```

After installation, read the design principles, production workflow, generated artifacts, and validation checklist in:

```text
skills/reelos-video-production/references/video-production-workflow.md
```

## Install One Skill

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/reelos-skills \
  --path skills/reelos-jinghuan-illustrations
```

Then restart Codex.

## Install Video Production Skill

After completing the dependency order above:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production
```

If Python certificate validation fails, use git mode:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production \
  --method git
```

## Install From a Branch

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/reelos-skills \
  --ref main \
  --path skills/reelos-video-production
```

## Local Development

During development, edit the skill in this repository first. To test it globally, copy it into your Codex skills directory:

```bash
rm -rf ~/.codex/skills/reelos-jinghuan-illustrations
cp -R skills/reelos-jinghuan-illustrations ~/.codex/skills/reelos-jinghuan-illustrations
```

For video production:

```bash
rm -rf ~/.codex/skills/reelos-video-production
cp -R skills/reelos-video-production ~/.codex/skills/reelos-video-production
```

Restart Codex after copying.
