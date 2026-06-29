---
name: reelos-editorial-line-system
description: Convert text, images, brands, product ideas, UI concepts, campaigns, or analysis articles into a ReelOS-flavored modern editorial black-and-white line-art visual system whose core claim is "one image should make the matter clear." Use this skill whenever the user asks for ReelOS editorial illustrations, minimalist line-art PNG posters, article lead images, explainers, brand visual boards, magazine spreads, website hero visuals, mobile UI mockups, packaging visuals, or "make this into a picture" in a monochrome line-art style with sparse pastel accents. Default to image generation for visual requests and prioritize clarity of argument over decoration.
user_invocable: true
version: "1.5.1"
---

# ReelOS Editorial Line System

Turn the user's input into a modern editorial visual system: black-and-white line-art characters, flat geometric forms, strong typography, large negative space, and selective pastel accent blocks.

The core thesis of this skill is: **one image should make the matter clear**. The image is not decoration for an article. It is a compressed explanation of the article's argument, conflict, mechanism, and conclusion.

Default visual identity: **ReelOS Lab Orbit**. Unless the user names another mode or the task clearly calls for a specialized style, use ReelOS Lab Orbit as the first-choice representative ReelOS style.

## Operating Rule

Default to a PNG image through `image_gen` when the user asks for a picture, poster, illustration, visual board, article image, campaign image, brand system, or provides text and asks to turn it into an image.

Use HTML/SVG or a text-safe two-pass workflow when the output needs crisp Chinese text, many labels, exact titles, or readable diagrams. AI-generated PNG text is acceptable only for sparse, large, non-critical labels.

## First Pass: Classify The Input

- **Text or article**: extract the thesis, central conflict, causal chain, turning point, conclusion, emotional temperature, and 3-5 visual scenes. For complex analysis, make the logic readable before making it beautiful.
- **Image**: preserve the main subject, pose, composition, and recognizable objects while converting the image into this editorial line-art system.
- **Brand, product, app, or campaign**: infer the everyday behavior it owns, the people who appear, and the applications that best show the system.
- **Mixed input**: preserve explicit constraints, then use the context to choose scene, layout, typography, and accent colors.
- **Ambiguous input**: ask one concise question or offer PNG poster, PNG brand board, image-to-illustration conversion, or HTML editorial page.

## Core Visual DNA

Read `references/visual-language.md` when building any output. If the user asks for a ReelOS mode, taste direction, palette, or a more specific aesthetic such as modern tech, paper, whitepaper, blueprint, data newspaper, product memo, frontier, infra, sonic, or performance style, also read `references/reelos-style-modes.md`. In short:

- Use minimalist black-and-white line art characters with simple faces and stylized geometric bodies.
- Let ordinary urban behavior express abstract ideas: reading, commuting, coding, shopping, working, waiting, presenting, deploying, reviewing, walking, resting.
- Use editorial hierarchy: bold headline, asymmetrical grid, generous white space, section blocks, and a few strong labels.
- Keep characters mostly monochrome. Use pastel accents only for backgrounds, UI panels, product surfaces, labels, dividers, or signal states.
- Avoid realistic rendering, 3D, glossy lighting, heavy gradients, anime, childish mascots, decorative clutter, and tiny illegible text.

## Route To The Right Reference

- For output selection and input classification details, read `references/output-routing.md`.
- For ReelOS palette modes and typography-first aesthetic choices, read `references/reelos-style-modes.md`. If no mode is specified, choose `ReelOS Lab Orbit`.
- For PNG prompt structures, article lead images, brand boards, campaign boards, and image-to-illustration prompts, read `references/prompt-recipes.md`.
- For exact editable layouts, long Chinese text, or browser-rendered output, read `references/html-output.md`.
- Before finalizing, check against `references/quality-check.md`.

## Article And Analysis Rule

For news analysis, business commentary, policy writing, or technical arguments, do not make a collage of keywords. Build the image around the argument and make the reader understand the matter before reading the article.

1. Name the central conflict.
2. Extract the causal chain.
3. Convert each step into a simple visual panel or repeated metaphor.
4. Put the conclusion in a short, readable bottom strip or headline.
5. Use labels sparingly; the scene should carry the reasoning.

### Default Explainer Structure

When the user asks for an article/signals/playbook visual, says "一张图说清楚", "一张图把事情说清楚", "帮助读者理解", "架构解析", or provides a long analytical article, default to an **editorial explainer board**, not a simple flowchart.

The preferred default structure is:

1. **Before / after split**: left side shows the old operating logic and its failure modes; right side shows the new operating logic and its working mechanism.
2. **Central transition**: place the turning point, migration arrow, or "from X to Y" claim between the two worlds.
3. **Mechanism core**: show the new system as a visible engine, orbit, loop, map, control panel, or operating layer.
4. **Component rail**: list only the key production components, actors, constraints, or resources that make the new system real.
5. **Bottom formula**: end with a short, memorable equation or conclusion strip that compresses the article's judgment.

Do not stop at a clean diagram if the article contains a thesis, conflict, and judgment. A good result should feel like a magazine-grade analytical spread: the reader should understand the old logic, the new logic, the mechanism, and the conclusion in one glance.

Use **HTML/SVG / text-safe** output for this default structure when the visual needs crisp Chinese, many labels, exact article terminology, or a reusable website asset. Use PNG generation only when text is sparse or the user explicitly prefers a raster poster.

Before generating, internally answer:

- What changed?
- Why did it happen?
- Who or what is affected?
- What is the new operating logic?
- What sentence should the viewer remember?

Good structures for complex text:

- **Editorial explainer board**: before/after split + central mechanism + component rail + bottom formula.
- **Cause-and-effect flow**: `thesis -> conflict -> bottleneck -> consequence`.
- **Three-crack explainer**: three tensions around one central system.
- **Before/after split**: old operating logic versus new operating logic.
- **Market map**: actors, incentives, gates, and bypass paths.

## Text Fidelity

Image generation draws text as pixels rather than typesetting it. Small Chinese labels, table text, dense captions, and exact headings may look fuzzy or malformed. Choose one text strategy before generating:

- **Image-only**: use only a few large, sparse words in the PNG. Best for mood posters.
- **Text-safe**: generate a mostly text-free illustration/background, then typeset exact title, labels, arrows, and captions with HTML/SVG or another layout layer.
- **Editable**: use HTML/SVG as the primary output when exact text, many labels, or downstream editing matters.

For "one image explains it" outputs with many labels, prefer **Text-safe** unless the user explicitly wants pure image generation.

## Default Dimensions

- Poster, quote, or social visual: vertical PNG, 1024x1792 or 1080x1920 equivalent.
- Brand system, campaign board, article explainer, or multi-panel analysis: horizontal PNG, 1792x1024 equivalent.
- Square social card: 1024x1024.
