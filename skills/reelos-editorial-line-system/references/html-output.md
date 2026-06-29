# HTML Output

Use HTML when the user explicitly asks for HTML, browser-rendered output, exact editable text layout, or long Chinese text that must remain precise. Also use HTML/SVG as a typography overlay when an image needs crisp readable Chinese labels.

## Text-Safe Overlay Workflow

Use this workflow for article explainers, style boards, diagrams, and "one image explains it" outputs when labels must be sharp:

1. Generate or design the illustration layer with little or no text.
2. Reserve blank zones for headline, panel labels, arrows, legends, and conclusion strips.
3. Typeset exact Chinese/English text in HTML/SVG using real fonts.
4. Export or screenshot the final layout if the user needs a PNG.
5. Keep font sizes large enough for social sharing: main title 56-96px on a 1792px canvas; panel labels 24-40px; small metadata at least 18-22px.

## HTML Rules

- Make a complete standalone HTML file if the user wants a file. Otherwise return the HTML code.
- Preserve user text exactly when it is meant to appear on the visual. Ask before rewriting.
- Use responsive layout. Width adapts to content.
- For long text, use a vertical editorial page.
- For short slogans, use a poster/card canvas.
- For brand systems, use a horizontal multi-panel board with a 1792x1024 feel.
- Use CSS and minimal inline SVG for black line-art people and objects.
- Keep the first screen useful; do not make a marketing landing page unless asked.
- Typography carries the layout: large headline, smaller support text, clear grid, strict spacing.
- Use real text for all important Chinese titles, labels, captions, legends, and conclusion strips.
- Use no more than two pastel accent colors in one HTML composition unless it is a brand system board.
- Characters are small-to-medium editorial actors, not mascot stickers.

## Recommended Formats

- Short quote or slogan: 1080x1440 or 1080x1920 poster-like canvas.
- Article or long text: 900-1100px wide adaptive editorial long page.
- Brand system: horizontal multi-panel board, 1792x1024 feel.
- Product or app concept: hero plus UI screens plus character set section.

## Avoid

Avoid AI-demo tropes: purple-blue gradients, floating blobs, glass cards, fake dashboards, decorative clutter, oversized hero type inside compact panels, and text overlap.
