---
name: tech-research-report
description: Generate a single self-contained HTML file for a long-form tech/industry research report (multi-section, data-viz heavy, "light tech dashboard" aesthetic — cool blue-white paper on a warm cream page, navy text, blue + orange-red accents). Use when the user wants a research note, quarterly industry watch, investment/market analysis report, or asks to turn a long analytical write-up (multiple sections, company profiles, stats, charts) into a polished report page. Sibling skill to insight-poster, which is for single-page concept posters instead — use this one whenever the content has 4+ sections or won't fit on one screen.
---

# Tech Research Report

A **long-form report**, not a poster. Where `insight-poster` compresses one idea onto one
screen, this skill lays out a full research note across many sections — numbered reasons,
company/entity profiles, comparison charts, stat tiles, an investment framework, a risk
callout, and a closing "manifesto" quote — while staying visually coherent end to end.

## Visual identity

**Light tech dashboard**, not dark-mode terminal and not warm editorial magazine. Two
light surfaces nested in each other (warm outer page, cool inner card) plus exactly two
accent hues (blue + orange-red) validated for color-vision safety.

```css
:root{
  --bg:#f5f0e8;        /* outer page — warm cream, "card floats on paper" */
  --paper:#eef3fa;      /* report card surface — cool light blue-white */
  --panel:#ffffff;      /* nested white panels: stat-tile, card, takeaways */
  --ink:#182648;        /* primary text — deep navy, never pure black */
  --muted:#57647a;
  --dim:#8794a8;
  --cyan:#1e6fd9;        /* primary accent: links, section labels, chart series 1 */
  --cyan-bright:#1e6fd9;
  --cyan-glow:#60a5fa;   /* brighter blue, ONLY for text inside the dark closing block */
  --indigo:#e35a2b;      /* secondary accent: warm orange-red "pop" color, chart series 2 */
  --risk:#9c2f34;        /* status red for the risk callout — muted, not alarm-red */
  --border:rgba(24,38,72,.10);
  --on-dark:#eef3fa;         /* text color for the one dark inverted block */
  --on-dark-muted:#93a3c0;
}
```

The single most important trick, lifted straight from the reference this palette was
built from: **cool blue dominates, one warm orange-red word or bar is the punctuation.**
Never make blue and orange-red both loud in the same view — pick one hero moment per
section (usually the headline's key phrase, or the second series in a 2-way comparison).

Fonts: `Noto Sans SC` (sans, not serif — this is what reads as "tech" rather than
"editorial") for all headings/body, `JetBrains Mono` for labels/data/section numbers,
`Playfair Display` weight 900 **only** for the giant faint background watermark glyph
(e.g. "Q2") — never for real text.

Full CSS (variables, every component class, responsive breakpoint) is in
[reference/components.md](reference/components.md) — copy it wholesale into a
`<style>` block rather than re-deriving it.

## Structure (in order)

1. **Controls** — fixed top-right: `导出 PNG` (html2canvas) + `打印 / PDF` (`window.print()`)
2. **Topbar** — dark tag-chip (category) left, mono source/date right
3. **Hero** — giant faint watermark glyph, small red/mono eyebrow, big navy `<h1>` with
   the ONE key phrase wrapped in `<em>` (orange-red, underlined), gray subhead paragraph
4. **TL;DR takeaway box** — white panel, blue left border, one bolded synthesis sentence
   (not a bullet list unless the source material genuinely gives you 3 discrete claims)
5. **Divider** (`◆` on a hairline) between hero and body, and again before the closing quote
6. **Numbered sections** — mono `"01 · 关键词"` label + **big, bold 27px `<h2>`** (section
   headers must be unmissable — users will tell you if they're too subtle; when in doubt,
   make the `<h2>` bigger, not the label)
7. **Closing quote block** — the one dark-inverted panel in the whole report (`#0d1420`
   background, `--on-dark`/`--cyan-glow` text) — reserve this for the single sharpest
   synthesis line, placed last before the footer
8. **Footer** — small disclaimer (sourcing + data-caveat) + mono brand line

## Component picker

Pick components by what the source content actually contains — don't force all of them.

| Content shape | Component | Class names |
|---|---|---|
| A single punchy definition/thesis | Takeaway box | `.takeaways` |
| "Here's why, in N reasons" | Numbered reason blocks | `.reason` / `.rn` / `.rc` |
| Per-company / per-entity analysis | Alternating profile blocks | `.company` / `.company.alt` |
| A short judgment worth pulling out | Pull-quote | `.pullquote` (border color follows `.alt` state) |
| "X owns this, Y owns that, Z owns the rest" (3 short parallel lines) | Structured triad | `.triad` |
| 2–3 entities compared on one metric | Horizontal comparison bars | `.chart-box` / `.cc-row` / `.cc-track` / `.cc-fill` |
| 2–4 standalone metrics | Stat tile grid | `.stat-grid` / `.stat-tile` (colored top border + dot per entity) |
| A 3-layer framework (e.g. infra / platform / application) | Card grid | `.grid` / `.card` (faint number watermark top-right) |
| Risks / caveats worth a callout | Alert bar | `.alert-bar` (uses `--risk`, never the chart accent colors) |

All code for these is in [reference/components.md](reference/components.md).

## Content strategy

1. **Extract the one-sentence thesis** for the takeaway box — if the source has an
   explicit "in one sentence..." claim, use it verbatim; don't synthesize a weaker one.
2. **Give every section a real `<h2>`**, not just the mono kicker label. If you're
   tempted to skip it because the mono label already says "03 · 模型公司格局", add it
   anyway — the label is navigation, the `<h2>` is the actual claim of that section.
3. **One pull-quote per section, max two.** Reserve them for the sentence the source
   itself frames as a verdict ("一句话判断", "所以...") — don't manufacture one from a
   sentence that was already fine as a plain paragraph.
4. **Charts only for numbers that are actually in the source.** Don't invent a
   comparison chart to fill a slot — if the source drops a stat between drafts, drop the
   chart with it rather than inventing a plausible-looking bar. Always caption exactly
   what's being compared and flag when methodologies/scopes differ (see the `Morgan
   Stanley vs JPMorgan` capex example in reference/components.md — different company
   sets AND different spending scope, both called out in the caption).
5. **The closing quote block is the manifesto, not a summary.** It should be the one
   line a reader screenshots. Write it last, after you know what the report actually
   argued.
6. **Alternate `.company`/`.company.alt`** strictly in source order (don't hand-pick
   which ones get the orange accent) — the alternation is a scanning aid, not emphasis.

## Before shipping a new chart color

This palette's blue/orange-red pair is already validated (CVD ΔE > 100, both clear the
light-surface contrast floor). If a report needs a **third** categorical color (a third
company in one chart, a fourth stat tile), don't eyeball a new hex — use the `dataviz`
skill's validator:

```
node <dataviz-skill-dir>/scripts/validate_palette.js "#1e6fd9,#e35a2b,#<new-hex>" --mode light --surface "#eef3fa"
```

Fix chroma/lightness until it passes before using it. Never reuse `--risk` (#9c2f34) as
a categorical color — it's reserved for the alert bar alone.

## Output requirements

- Single self-contained `.html` file (Google Fonts `<link>` + html2canvas CDN are the
  only externals — must still open and read fine offline once fonts are cached)
- PNG export via html2canvas at `scale:2` against `--paper`'s hex as `backgroundColor`
  (reports are long — this exports one full-length image, not a paginated capture);
  button text swaps to a "generating…" state during export
- Print support via `@media print` hiding `.controls`
- Mobile breakpoint at 640px: grids collapse to 1 column, hero font shrinks, section
  padding tightens

## Render-check before calling it done

Take a screenshot of the hero, at least one chart, the stat-tile grid, and the closing
quote block. Check specifically for: section `<h2>` actually reads as a big heading (not
just the small mono label), chart bars have visible direct-value labels (don't rely on
color alone at ~2:1 contrast), and the dark closing block's text isn't using the
light-surface `--ink` color by mistake (it needs `--on-dark`/`--cyan-glow`, a common bug
when copy-pasting text-color rules from the rest of the page).
