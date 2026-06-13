# ReelOS Skills

Experimental Codex / OpenClaw skills for ReelOS workflows.

This repository collects reusable skills for Chinese article workflows, visual thinking, product operations, and ReelOS-specific creative systems.

## Skills

| Skill | Purpose | Status |
| --- | --- | --- |
| `reelos-jinghuan-illustrations` | Generate ReelOS-style Chinese article illustrations with the Jinghuan Worker IP. | active |
| `reelos-video-production` | Produce Chinese narrated Remotion videos with TTS, timing sync, visual style presets, render, and validation. | active |

## Install

Each folder under `skills/` is a self-contained skill. Skill-specific setup, workflow, and design documentation should live inside that skill, usually under `references/`.

Install a skill from this repository with the Codex skill installer:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/reelos-skills \
  --path skills/reelos-jinghuan-illustrations
```

Replace `<owner>` with the GitHub account or organization that hosts this repository.

For the video production skill, install system programs, Remotion project dependencies, TTS credentials, and base skills first. The detailed dependency map and install commands are documented in:

```text
skills/reelos-video-production/references/setup-dependencies.md
```

The design principles, full production workflow, generated artifacts, and validation checklist are documented in:

```text
skills/reelos-video-production/references/video-production-workflow.md
```

Then install:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo reelos-ai/reelos-skills \
  --path skills/reelos-video-production
```

After installing, restart Codex so the new skill is loaded.

## Repository Layout

```text
reelos-skills/
├── skills/
│   ├── reelos-jinghuan-illustrations/
│   │   ├── SKILL.md
│   │   ├── agents/
│   │   ├── assets/
│   │   └── references/
│   └── reelos-video-production/
│       ├── SKILL.md
│       ├── agents/
│       └── references/
├── docs/
│   └── skill-authoring.md
└── examples/
    └── README.md
```

## Naming

Use the `reelos-` prefix for all public skills.

Good examples:

- `reelos-jinghuan-illustrations`
- `reelos-article-refiner`
- `reelos-workflow-designer`
- `reelos-brand-auditor`

## License

Add a license before publishing if you want others to reuse these skills.
