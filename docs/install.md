# Install ReelOS Skills

## Install One Skill

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/reelos-skills \
  --path skills/reelos-jinghuan-illustrations
```

Then restart Codex.

## Install From a Branch

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/reelos-skills \
  --ref main \
  --path skills/reelos-jinghuan-illustrations
```

## Local Development

During development, edit the skill in this repository first. To test it globally, copy it into your Codex skills directory:

```bash
rm -rf ~/.codex/skills/reelos-jinghuan-illustrations
cp -R skills/reelos-jinghuan-illustrations ~/.codex/skills/reelos-jinghuan-illustrations
```

Restart Codex after copying.
