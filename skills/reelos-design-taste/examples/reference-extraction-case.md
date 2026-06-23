# Reference Extraction Case

## User input

研究这个 HTML / 网站的配色和字体，把可复用的品味规则学习进 skill。

## Expected behavior

The skill should:
- Extract title, font roles, CSS variables, colors, section structure, imagery, and motion signals.
- Convert the source into reusable principles rather than copying brand assets.
- Decide which reference file should be updated.
- Preserve typography-first analysis.

## Expected output

```text
Extracted pattern
Frontier Tech / Intelligence Aesthetics.

Reusable rules
- Typography: compressed display for urgency, geometric sans for body/UI, mono for metadata, CJK sans fallback.
- Palette: near-black background, warm off-white text, one acidic signal accent, low-alpha card surfaces.
- Layout: editorial issue cards, manifesto badge, section numbers, stack/timeline structures.
- Material / imagery: real community or tech imagery with black overlays.
- Motion: short precise transitions, subtle glow on status only.
- Taste guardrails: avoid cyberpunk overload, terminal cosplay, and large lime surfaces.

Skill placement
- Typography roles belong in `references/typography.md`.
- Palette and cultural logic belong in `references/cultural-aesthetics.md`.
- Card/image/motion usage belongs in `references/visual-systems.md`.
```
