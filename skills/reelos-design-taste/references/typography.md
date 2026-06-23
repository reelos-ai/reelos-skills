# Typography Taste

Typography is the quiet narrator of design. It sets trust, rhythm, cultural register, and hierarchy before users read the words.

## Typography-First Decision Tree

1. **Language mix**: Chinese-only, English-only, CJK + Latin, or data-heavy mixed interface.
2. **Primary voice**: editorial, product, ceremonial, poetic, technical, meditative, literary, or signal/intelligence.
3. **Role map**: define display, body, UI, meta/data, and accent before choosing exact fonts.
4. **Optical match**: match CJK and Latin by visual weight, x-height impression, contrast, and emotional temperature.
5. **Reading mode**: choose line-height and line length based on prose, UI labels, dashboard density, or poetic fragments.
6. **Restraint pass**: remove one family or one weight if the system feels performative.

Recommended role order:

| Role | Purpose | Typical choices |
| --- | --- | --- |
| Display | Brand voice and first impression | Serif, compressed display, geometric display, or restrained CJK title |
| Body | Reading trust | Sans for product, serif for literary/cultural, high legibility always |
| UI | Buttons, forms, navigation | Clean sans, predictable weights, no expressive fonts |
| Meta/Data | Dates, IDs, issue numbers, coordinates | Mono or narrow sans |
| Accent | Seal, tagline, one emotional note | Brush, italic serif, symbolic display, never body |

## CJK + Latin Pairings

Use personality matching, not font-name matching.

| Direction | Chinese | Latin | Use |
| --- | --- | --- | --- |
| Classic editorial | Noto Serif SC / Source Han Serif SC | Playfair Display | Culture, luxury, editorial hero |
| Modern product | Noto Sans SC / Source Han Sans SC | Inter | Product UI, SaaS, clear interfaces |
| Poetic editorial | Noto Serif SC Light | Cormorant Garamond | Poetry, art, lifestyle, quiet pages |
| Tech rational | Noto Sans SC Bold | Space Grotesk | AI, data, sci-fi, startup product |
| Frontier intelligence | Bebas Neue | Manrope + Space Mono | Frontier tech, AI community, events, intelligence products |
| Chinese brush accent | Ma Shan Zheng / Zhi Mang Xing | Keep Latin simple | Taglines only; never body text |
| Brush humanity | Noto Serif SC | Ma Shan Zheng / Zhi Mang Xing accent | Poetry, calligraphy, literary culture, scholar pages |
| Deep space signal | Noto Serif SC | Syncopate + JetBrains Mono + Cormorant Garamond | Sci-fi narrative, decoded messages, telemetry |
| Fluid infrastructure | Noto Sans SC | Inter / Geist / system sans | Cloud infra, adaptive systems, liquid SaaS, observability |
| Sonic creator studio | Noto Sans SC | Manrope + Inter | AI music, creator tools, audio SaaS, track libraries |
| Performance creative agency | Noto Sans SC | DotGothic16 + mono | Ad creative agencies, growth studios, ecom performance teams |
| Western rational | Inter / Helvetica-like | Space Grotesk or Inter | Swiss, Bauhaus, technical clarity |
| Japanese calm | Noto Serif JP + Noto Sans JP | Cormorant Garamond or Inter | Craft, hospitality, subdued UI |

## Six Principles

1. **气质统一**: serif with serif, sans with sans, unless contrast is the concept.
2. **视觉平衡**: CJK characters sit visually higher; adjust Latin size/baseline optically.
3. **字重对应**: numeric weights do not match across scripts. Match visual weight by eye.
4. **间距克制**: avoid letter-spacing in Chinese body text. Use weight, spacing around blocks, or color for emphasis.
5. **标点规范**: use full-width punctuation for CJK and half-width punctuation for Latin; keep punctuation attached to its script.
6. **留白即信息**: line-height and paragraph spacing are part of the message.

## Optical Matching Checklist

- CJK 400 may feel like Latin 500; compare by eye before trusting numeric weights.
- If Latin has high contrast strokes, pair it with a CJK serif that has comparable elegance.
- If Latin is geometric and low contrast, pair with a CJK sans for clarity.
- If CJK title uses Song/serif, Latin display can use Playfair, Cormorant, or another editorial serif.
- If CJK title uses bold sans, Latin display can use Space Grotesk, Inter Tight, Manrope, or similar geometric sans.
- If the page includes Chinese paragraphs, do not let Latin display rules set the whole rhythm.

## Hierarchy Rules

- Display Chinese can use serif or calligraphic flavor, but body text should remain readable.
- For Chinese editorial or cultural design, line-height 1.8-2.2 often feels refined.
- For product UI, body line-height 1.55-1.75 is usually clearer.
- For poetic or high-end sparse pages, line-height around 2.0-2.4 can create ceremony.
- For dense dashboards, use smaller scale jumps and stricter grid alignment.
- Avoid huge display type inside compact panels. Match type scale to container size.

## Pairing Diagnostics

Good pairings:
- Serif + serif when both carry history, culture, or editorial elegance.
- Sans + sans when the goal is speed, clarity, product trust, or technical neutrality.
- Display + sans + mono when the brand needs a strong poster voice, readable body copy, and metadata rigor.
- Brush accent + sober serif/sans when the handwritten layer is a signature, not the whole system.

Poor pairings:
- Classical Chinese serif with aggressive sci-fi Latin unless the whole concept is a deliberate collision.
- Very thin Chinese with very heavy Latin; it creates unequal gravity.
- Brush fonts for body, navigation, forms, or dense UI.
- Mono for long prose; it turns reading into decoding.
- Latin display logic forced onto Chinese headings. Chinese needs weight, spacing, and composition, not all-caps imitation.

## Font Weight Notes

- Chinese Regular can look heavier than Latin Regular.
- Pair CJK 400 with Latin 450-500 or CJK 500 with Latin 600 only after optical checking.
- Use bold Chinese sparingly in refined cultural designs; weight contrast can feel blunt.
- Use mono type for telemetry, code, coordinates, IDs, and sci-fi metrics, not long prose.

## Letter Spacing

- Chinese: generally keep `letter-spacing: 0`; for ceremonial titles, small positive tracking can work if tested.
- Latin uppercase labels can use slight tracking.
- Do not use negative letter spacing as a default.
- CJK body text with tracking usually looks amateur; use line-height, paragraph spacing, or weight instead.
- Mono metadata can use tracking, but keep numbers readable.

## Line-Height Rules

- `1.2-1.35`: display titles, compact hero lines, short labels.
- `1.45-1.65`: product UI, dashboard copy, cards, short descriptions.
- `1.65-1.85`: comfortable mixed-language editorial/product text.
- `1.8-2.2`: Chinese cultural, literary, Zen, and long-form reading.
- `2.2-2.4`: poetic fragments, luxury editorial, ritualized reading moments.

## Practical CSS Defaults

Chinese cultural/editorial:

```css
font-family: "Noto Serif SC", "Source Han Serif SC", Songti SC, serif;
line-height: 1.9;
letter-spacing: 0;
```

Modern product:

```css
font-family: Inter, "Noto Sans SC", "Source Han Sans SC", system-ui, sans-serif;
line-height: 1.65;
letter-spacing: 0;
```

Fluid infrastructure:

```css
--font-display: Inter, Geist, "Noto Sans SC", system-ui, sans-serif;
--font-body: Inter, Geist, "Noto Sans SC", system-ui, sans-serif;
--font-meta: Inter, Geist, "Noto Sans SC", system-ui, sans-serif;
/* English display can use slight negative tracking; keep Chinese at 0. */
```

Sonic creator studio:

```css
--font-display: Manrope, "Noto Sans SC", system-ui, sans-serif;
--font-body: Inter, "Noto Sans SC", system-ui, sans-serif;
--font-ui: Inter, "Noto Sans SC", system-ui, sans-serif;
/* Use tight English display type, but keep creator/product copy relaxed. */
```

Performance creative agency:

```css
--font-display: "DotGothic16", "Noto Sans SC", system-ui, sans-serif;
--font-ui: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
--font-body: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
/* Use pixel/terminal display only for short English headlines; Chinese needs a cleaner fallback. */
```

Sci-fi telemetry:

```css
font-family: "JetBrains Mono", "IBM Plex Mono", ui-monospace, monospace;
letter-spacing: 0.02em;
```

Deep space narrative:

```css
--font-display: "Syncopate", sans-serif;
--font-mono: "JetBrains Mono", ui-monospace, monospace;
--font-serif: "Cormorant Garamond", Georgia, serif;
--font-cn: "Noto Serif SC", serif;
```

Brush humanity:

```css
--font-serif: "Noto Serif SC", "Songti SC", serif;
--font-brush: "Ma Shan Zheng", "Zhi Mang Xing", cursive;
line-height: 2;
```

Zen / wabi-sabi:

```css
font-family: "Noto Serif SC", "Songti SC", Georgia, serif;
line-height: 1.8;
letter-spacing: 0.05em; /* titles/poetic fragments only */
```

## Frontier Tech / Intelligence Pattern

Use this pattern for AI, chips, frontier tech, research communities, investment intelligence, and event brands that need to feel sharp, current, and slightly underground.

Typography roles:

- **Display**: `Bebas Neue` or another compressed uppercase display face. Use for hero headlines and section titles. Keep line-height tight around `0.9-1.0`; slight positive tracking around `0.01-0.02em`.
- **Body/UI**: `Manrope` or another modern geometric sans. Use for paragraphs, CTAs, forms, and product copy. It keeps the display face from becoming theatrical.
- **Meta/Navigation**: `Space Mono` or a clean monospaced face. Use for nav, issue numbers, dates, labels, coordinates, and status chips. Uppercase with tracking around `0.06-0.2em`.
- **Chinese fallback**: `Noto Sans SC`. For Chinese pages, reduce display theatrics: avoid all-caps logic, set letter-spacing to `0`, and let Noto Sans SC carry headings with weight rather than compression.

Why it works:

- The compressed display font creates urgency and poster energy.
- The sans body font keeps long content readable and trustworthy.
- The mono layer turns ordinary metadata into intelligence/interface signals.
- The system feels "frontier" without relying on random neon or fake terminal styling.

## Fluid Infrastructure Pattern

Use this pattern for cloud platforms, deployment engines, observability tools, adaptive systems, and AI infrastructure that should feel alive without becoming cyberpunk.

Typography roles:

- **Display**: `Inter`, `Geist`, or another neutral product sans. Use medium weight around `500`; line-height near `1.0`; English display can use slight negative tracking around `-0.02em`.
- **Body/UI**: same sans family at regular or medium weights. Keep paragraphs calm so WebGL, blur, and depth effects can carry the atmosphere.
- **Meta/Data**: uppercase sans labels with positive tracking around `0.08-0.12em`. Use for live layers, latency, regions, uptime, deploys, and similar system states.
- **Numbers**: medium-weight sans, slightly tight tracking for large metrics. Avoid mono unless the product explicitly needs terminal or code credibility.
- **Chinese fallback**: `Noto Sans SC`. Keep Chinese headings at `letter-spacing: 0`; use weight and spacing instead of English-style compression.

Why it works:

- A neutral sans keeps the interface trustworthy while the background moves.
- Tight display type gives cloud infrastructure a premium product voice.
- Wide uppercase metadata creates a control-room signal without fake terminal styling.
- Using one family across display, body, UI, and data prevents the motion system from feeling noisy.

## Sonic Creator Studio Pattern

Use this pattern for AI music tools, creator-safe audio platforms, track libraries, sample packs, streaming assets, and music production SaaS.

Typography roles:

- **Display**: `Manrope` or another rounded geometric sans. Use medium weight around `500`, tight line-height around `1.0`, and English tracking around `-0.04em` for large hero copy.
- **Body/UI**: `Inter` or system sans for navigation, buttons, controls, pricing, and longer product copy.
- **Accent text**: gradient-filled words can carry the audio energy, but keep the rest of the headline white for legibility.
- **Metadata**: small sans labels for BPM, track type, license, artist, and processing state. Avoid making every label uppercase; music UI benefits from human readability.
- **Chinese fallback**: `Noto Sans SC`; keep Chinese display less tight than English, with `letter-spacing: 0` and line-height around `1.1-1.2`.

Why it works:

- Manrope gives the hero a smooth studio/product voice without becoming playful.
- Inter keeps controls and pricing predictable.
- Blue gradient emphasis suggests waveform energy while preserving a premium black-stage mood.
- Tight type pairs well with compact audio controls, waveform modules, and album/track cards.

## Performance Creative Agency Pattern

Use this pattern for ad creative agencies, growth studios, e-commerce performance teams, UGC production shops, and landing pages that sell speed, ROAS lift, and creative throughput.

Typography roles:

- **Display**: `DotGothic16` or another controlled pixel/grotesque display face. Use only for hero headlines, stats, and key section titles. Keep weight regular; let the grid shape create character.
- **Body/UI**: monospace or mono-like sans for navigation, labels, buttons, dashboard copy, dates, tasks, and performance metadata.
- **Proof/Data**: display numbers can use the same pixel face; labels should stay mono and small so ROAS, turnaround, and volume claims feel operational.
- **CTA**: mono, small, high contrast. White pill on black works because it feels like a decisive conversion control.
- **Chinese fallback**: `Noto Sans SC` or `Source Han Sans SC`. Avoid pixel fonts for long Chinese copy; use the pixel voice only for short titles if tested.

Why it works:

- Pixel display type turns the agency into a machine-like creative engine rather than a soft portfolio.
- Mono UI copy makes tasks, dates, boards, and performance proof feel operational.
- The contrast between huge pixel display and tiny mono controls creates authority without needing many colors.
- The system feels sharper when typography stays sparse; overusing the pixel font makes it gimmicky.
