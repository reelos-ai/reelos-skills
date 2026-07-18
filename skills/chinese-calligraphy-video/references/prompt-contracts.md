# GPT Image 提示词契约

## 新建书法母版

每句单独调用一次 Codex 内置 GPT Image，并替换尖括号内容：

```text
Use case: stylized-concept
Asset type: Chinese calligraphy video foreground asset
Primary request: Write exactly five Chinese characters in one horizontal line.
Text (verbatim): "<逐字原文>"
Style/medium: modern Chinese wild cursive, powerful heavy starts, exaggerated long sweeping tails, visible dry-brush flying-white gaps, sparse ink splatters, readable individual glyphs
Composition/framing: one centered horizontal line, dynamic size variation, generous padding, no cropping
Color palette: natural expressive transition between <颜色一与HEX> and <颜色二与HEX>, both colors clearly visible
Scene/backdrop: perfectly flat uniform solid <色键HEX> chroma-key background
Constraints: exactly the supplied characters in the same order; no extra strokes that resemble another glyph; preserve readable character structure
Avoid: no seal, signature, caption, border, shadow, paper texture, background gradient, watermark, or additional text
```

## 高保真风格改色

把已批准的同一句书法图作为 `edit target`：

```text
Use case: precise-object-edit
Asset type: Chinese calligraphy video foreground asset
Input image: edit target; approved calligraphy style and glyph structure
Primary request: recolor the existing calligraphy while preserving exact glyph shapes, brush trajectories, long tails, dry-brush gaps, ink splatters, spacing, scale, and composition
Text (verbatim): "<逐字原文>"
Color palette: replace brushwork colors only with <颜色一与HEX> and <颜色二与HEX>
Scene/backdrop: replace the entire background with perfectly flat uniform solid <色键HEX>
Constraints: change only brush colors and background; retain every original character and stroke relationship
Avoid: no new or missing glyphs, no seal, signature, caption, border, shadow, texture, or watermark
```

## 无文字山水背景

```text
Use case: stylized-concept
Asset type: 16:9 video background
Primary request: a cinematic Chinese ink-wash mountain landscape supporting a poetry calligraphy video
Style/medium: contemporary Chinese ink painting, restrained mineral pigments, subtle paper texture
Composition/framing: 16:9, large calm dark negative space across the center for calligraphy, visual weight at corners and lower edge
Color palette: <双色方案> on a deep ink-black base
Constraints: no text, no calligraphy, no seal, no people, no prominent object behind the center text area
Avoid: busy center, photorealism, neon colors, frames, logos, watermark
```

## 色键规则

- 前景包含绿色、青色或石绿时，使用 `#FF00FF`。
- 前景不含绿色时，优先使用 `#00FF00`。
- 背景必须纯色、无阴影、无渐变、无纹理。
- 抠图后检查四角 alpha 为 0、笔画非空、飞白和墨点没有被误删。
