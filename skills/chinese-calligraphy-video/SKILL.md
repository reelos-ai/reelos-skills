---
name: chinese-calligraphy-video
description: Analyze Chinese poems, prose, or short quotations, develop and score content-specific aesthetic directions, then turn the selected direction into polished calligraphy videos using Codex built-in GPT Image, chroma-key transparency, two-color Chinese palettes, synchronized TTS, brush-reveal animation, and ffmpeg. Use when the user asks to design, make, improve, or remake a Chinese poetry video, 狂草/行草/书法字幕视频, 水墨诗词短片, 双配色书法成片, 内容审美评估, or to reproduce a supplied calligraphy-video style with narration.
---

# Chinese Calligraphy Video

Build a reusable, source-traceable pipeline rather than a one-off rendered clip.

## Collect the brief

Confirm or infer:

- exact text split into one line per shot;
- title, dynasty/author, and bottom-left badge;
- calligraphy style and any reference image/video;
- two foreground colors and background mood;
- aspect ratio, resolution, and frame rate;
- TTS voice, emotion, and speed.

Default to 1920×1080, 24 fps, modern wild cursive, four-to-seven characters per shot, and badge `愿君全屏静赏`. Never guess uncertain Chinese characters; preserve the user's text verbatim.

If the user supplies only a poem title, present the proposed canonical text and obtain confirmation before image generation. If color names lack HEX values, use `references/palette-defaults.md` or ask when no reliable mapping exists.

## Evaluate content and design the direction

Complete this design gate before generating images or TTS. Read `references/content-aesthetics.md` and create `design_manifest.json` from `assets/design_manifest.example.json`.

1. Analyze genre, theme, imagery, time/space, emotional arc, cadence, light/material, and cultural logic. Mark evidence as `observed`, `provided`, or `inferred`.
2. Propose 2–3 genuinely distinct directions. Give each one dominant aesthetic, no more than two supporting signals, and define typography first.
3. For each direction, specify calligraphy and font roles, two-color semantic roles, composition and negative space, material and lighting, motion tempo, TTS performance, and explicit anti-patterns.
4. Score every direction using the weighted rubric. Select the direction that best serves the content, not the most decorative one.
5. Run the design audit. Do not proceed unless the selected direction scores at least 80/100, passes all critical dimensions, and meets foreground contrast thresholds.

```bash
"$PYTHON_BIN" <skill-dir>/scripts/calligraphy_video.py design-audit \
  --manifest design_manifest.json
```

If the gate fails, revise the direction rather than lowering the threshold. Carry `implementation_handoff` into the image and TTS prompts so implementation cannot drift from the approved aesthetic.

## Prepare the project

Use this layout:

```text
project/
├── design_manifest.json
├── assets/backgrounds/
├── assets/lines/<variant>/source/
├── assets/audio/
├── previews/
├── video_config.json
└── output.mp4
```

Initialize new projects with `scripts/init_project.py`; use one `--line` argument per shot. Keep variants in separate directories and filenames unless the user explicitly requests replacement.

```bash
"$PYTHON_BIN" <skill-dir>/scripts/init_project.py --project-dir <target> \
  --title '《诗名》' --author '朝代 · 作者' --variant <variant> \
  --line '<第一句>' --line '<第二句>'
```

Use a project virtual environment with Pillow 11.x. Do not assume the system Python has a compatible Pillow build. In the commands below, set `PYTHON_BIN` to the project's interpreter, for example `./.venv/bin/python` or `./venv/bin/python`.

Bootstrap a new project when no working environment exists:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r <skill-dir>/assets/requirements.txt
PYTHON_BIN=./.venv/bin/python
```

If the project already has `venv/bin/python`, reuse it and set `PYTHON_BIN=./venv/bin/python` instead of creating another environment. Require `ffmpeg` and `ffprobe` on `PATH`.

## Generate visual assets

Use the installed `imagegen` skill and Codex built-in GPT Image. Do not create a standalone OpenAI image API caller.

1. Inspect every supplied local reference with `view_image` before generation.
2. Reuse the approved direction's typography, palette roles, composition, material, lighting, and anti-patterns; do not redesign ad hoc during prompting.
3. Generate one text-free background with the specified negative space.
4. Generate or edit one complete calligraphy line per shot. Use exact text and explicitly prohibit extra glyphs, seals, signatures, and captions.
5. For a new style, use the generation contract in `references/prompt-contracts.md`.
6. To preserve an approved style, use each approved line as an edit target and change only palette/background.
7. Request a flat chroma-key background. Use `#FF00FF` when the foreground contains green; otherwise use `#00FF00`.
8. Copy every selected source from Codex's generated-image directory into the project before using it.
9. Remove the key with the `imagegen` helper. Use soft matte and despill; if a thin fringe remains, retry once with `--edge-contract 1`.
10. Inspect all transparent results and a four-line contact sheet. Reject misspelled, missing, duplicated, or reordered characters.

Read `references/prompt-contracts.md` before generating or editing calligraphy assets.

Use the installed helper explicitly:

```bash
"$PYTHON_BIN" "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" \
  --input <source.png> --out <transparent.png> --auto-key border \
  --soft-matte --transparent-threshold 12 --opaque-threshold 220 --despill
```

## Generate TTS

Prefer one audio file per shot so timing remains deterministic.

- If the user selected an installed TTS skill, follow that skill completely. When the provider requires voice selection, list voices and obtain a choice before submission.
- Otherwise accept user-supplied WAV/MP3/M4A files.
- Use neutral or restrained emotion for classical poetry unless the user requests another delivery.
- Translate the approved direction's emotional arc and pause logic into the provider-specific voice instructions; do not select a voice independently of the visual direction.
- Do not store API keys in the project or configuration.

Set each line's `audio` field in the config. Omit all `audio` fields for a silent video.

Persist every generated voice set in `assets/audio/tts_manifest.json`. Record provider, exact `voice_id`, displayed name, gender/age metadata when available, emotion, speed, task ID, source text, and output path. A human-friendly label is not an identity key.

When the user asks to reuse a voice from an earlier video, reuse the exact provider + `voice_id` + emotion + speed from that video's TTS manifest. If the manifest is missing, recover the original generation command/task record or ask the user to reselect; never infer identity from a prose description such as “古风男声” or from a similar display name.

Descriptions such as “沉静男声” are selection criteria, not necessarily provider voice IDs. List matching available voices and obtain the required provider-specific choice before submitting TTS.

When no TTS provider is named:

1. Inspect the currently available TTS/speech skills.
2. If exactly one is available, announce it and follow its voice-selection flow.
3. If multiple are available, present the available providers and ask the user to choose before listing voices.
4. If none are available, ask for user-supplied audio or permission to install/configure a TTS capability. Do not silently choose an external service.

## Compose and validate

Use the unified CLI from the target project:

```bash
PYTHON_BIN=./.venv/bin/python  # adjust to the project's virtual environment
CLI=<skill-dir>/scripts/calligraphy_video.py
"$PYTHON_BIN" "$CLI" validate --config video_config.json
"$PYTHON_BIN" "$CLI" preview --config video_config.json --output previews/preview.png
"$PYTHON_BIN" "$CLI" contact --config video_config.json --output previews/contact-sheet.png
"$PYTHON_BIN" "$CLI" render --config video_config.json --output output.mp4
"$PYTHON_BIN" "$CLI" inspect --input output.mp4 --config video_config.json
```

Inspect the preview before the full render. Check all hold frames after rendering. Require H.264 video, `yuv420p`, expected dimensions/frame rate, and AAC when audio is configured.

After the first preview, re-review it against `design_manifest.json`: one focal point, typography dominance, palette roles, negative space, cultural coherence, motion restraint, and audio cadence. Contrast passing in the manifest is only a floor; rendered frames still require visual inspection.

The bundled reveal is a stylized left-to-right character-region mask, not true historical stroke-order animation. Do not describe it as real brush-stroke order; use specialized masks or animation tooling if the user requires authentic stroke order.

Use global `reveal_style` or per-line overrides: `character-wipe` for normal shots, `line-wipe` for continuous sweeps, and `fade` for title/end cards. Per-line timing, offsets, scale, reveal style, and TTS lead can override global defaults.

Read `references/configuration.md` when changing timing, layout, labels, or encoding. Read `references/quality-checklist.md` before final delivery. Read `references/extension-guide.md` before adding render strategies, providers, or schema fields.

Run `"$PYTHON_BIN" "$CLI" self-test` after changing bundled scripts.

## Deliver

Report:

- final video and preview paths;
- exact palette, calligraphy style, and prompt contract used;
- selected aesthetic direction, design score, and key content rationale;
- TTS voice/emotion or supplied-audio source;
- technical validation results;
- any variants retained for comparison.

Never claim the characters are correct without visually checking each completed line.
