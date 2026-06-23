# Typography Case

## User input

用 reelos-design-taste 给一个 AI 投研社区做字体系统，参考 Rewired 的感觉，但不要照抄。

## Expected behavior

The skill should:
- Treat typography as the first design layer.
- Define display, body, UI, meta/data, accent, and CJK fallback roles.
- Use the Frontier Tech / Intelligence pattern as a reference, not a copy.
- Explain line-height, tracking, and what not to do.

## Expected output

```text
Typography direction
Sharp frontier-intelligence voice: poster-like display headlines, readable modern product copy, and monospaced metadata for signal.

Font roles
- Display: Bebas Neue alternative such as Oswald / Archivo Narrow / DIN Condensed for large English headlines.
- Body: Manrope / Inter / Geist Sans for readable paragraphs and CTAs.
- UI: Manrope / Inter, 500 for buttons and labels.
- Meta / data: Space Mono / IBM Plex Mono for dates, issue numbers, tickers, confidence, and tags.
- Accent: one small acid-lime signal dot or arrow; no decorative font needed.
- Fallbacks: Noto Sans SC for Chinese; do not force compressed uppercase logic onto Chinese headings.

Rules
- Display line-height: 0.9-1.0 for English hero titles.
- Body line-height: 1.55-1.7.
- Meta tracking: 0.06-0.16em uppercase.
- Avoid terminal cosplay, random neon, and mono long-form prose.
```
