# Skill Authoring Guide

## Standard Structure

Each skill should live under `skills/<skill-name>/`.

```text
skills/<skill-name>/
├── SKILL.md
├── agents/
├── assets/
└── references/
```

Only `SKILL.md` is required. Use `references/` for supporting instructions, `assets/` for examples or visual references, and `agents/` for host-specific metadata.

## Frontmatter

Every `SKILL.md` should start with:

```yaml
---
name: reelos-example-skill
description: A concise trigger-focused description of when to use this skill.
---
```

The `name` must match the directory name.

## Writing Rules

- Make the trigger description specific enough that Codex can choose the skill naturally.
- Put long reusable guidance in `references/` instead of overloading `SKILL.md`.
- Keep examples useful but avoid making the model copy them by default.
- Prefer concrete workflows, checklists, and output rules over abstract taste notes.
- Include safety limits when a skill can create, edit, publish, or install something.

## Versioning

For now, version by Git commits and release tags. If a skill becomes widely used, add a small changelog inside that skill directory.
