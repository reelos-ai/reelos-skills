# Prompt Recipes

Use these recipes when generating PNGs through `image_gen`.

## Text Rendering Strategy

Image models often render text as drawn shapes, which can make Chinese characters, small labels, chart text, and exact headings fuzzy or incorrect. Choose a strategy before writing the prompt:

- **Image-only**: ask for only 3-8 large words or labels. Use this for posters and loose mood images.
- **Text-safe**: ask the image model to leave clean blank text zones, simple unlabeled panels, or placeholder label boxes; then typeset exact text separately with HTML/SVG. Use this for explainers, diagrams, style boards, and article lead images.
- **Editable**: skip image text and create the full layout in HTML/SVG when crisp readable text is the primary requirement.

Prompt phrases for text-safe generation:

```text
Leave clear blank title and label areas for later typesetting. Use simple placeholder label boxes without detailed text. Do not render small body text, tiny labels, or dense captions inside the image. Keep diagram areas clean and readable for an external typography overlay.
```

## Master Image Prompt

```text
A modern editorial illustration system for [SUBJECT], featuring minimalist black-and-white line art characters across [APPLICATIONS]. The scene translates [CORE_IDEA] into everyday urban life moments: [SCENES]. Characters are clean, flat, geometric, with simple facial features, stylized proportions, and mostly monochrome bodies. The design emphasizes bold typography, large negative space, asymmetrical editorial hierarchy, and strong contrast blocks. Use soft pastel accents selectively for backgrounds, product surfaces, packaging, UI panels, and section dividers: [ACCENT_COLORS]. Include [SPECIFIC_ELEMENTS]. Straight-on multi-panel layout view, high-resolution vector-like lines, smooth edges, flat design, no realistic lighting.

Negative prompt: realistic lighting, 3D render, glossy effects, painterly texture, anime, childish mascot, excessive color, busy background, cluttered layout, heavy gradients, illegible typography.
```

## Vertical Poster

```text
Create a vertical PNG editorial poster for [SUBJECT/TEXT]. Minimalist black-and-white line art characters interact with the idea through everyday urban gestures: [ACTION]. Use a clean magazine grid, large headline typography, generous negative space, and a few pastel accent blocks in [ACCENT_COLORS]. Characters remain mostly monochrome, drawn in clean flat geometric line art with simple faces and stylized proportions. If visible text is needed, make it large, sparse, and editorial, preserving the essential wording: [TEXT]. Contemporary lifestyle branding aesthetic, high contrast, vector-like smooth edges, flat design, no realistic lighting.

Negative prompt: 3D, realistic shading, glossy gradients, stock-photo look, childish cartoon, clutter, illegible text, excessive colors.
```

## Horizontal Article Explainer

Use this when the user provides analysis, industry commentary, news interpretation, or a long argument.

```text
Create a horizontal PNG editorial explainer image, 1792x1024, in a minimalist black-and-white editorial line-art system with selective pastel accents.

Topic: [TOPIC]
Main thesis: [ONE_SENTENCE_THESIS]
Central conflict: [CONFLICT]
Viewer takeaway: [ONE_SENTENCE_THE_VIEWER_SHOULD_REMEMBER]

Structure the image as [FLOW_TYPE: cause-and-effect flow / three-crack explainer / market map / before-after split]. The image must explain the causal chain clearly, not just show symbols. It should work as "one image that makes the matter clear."

Panel 1: [CAUSE_OR_STARTING_POINT]
Visual: [EVERYDAY_OR_SYSTEM_METAPHOR]
Short label: [LABEL]

Panel 2: [CONFLICT_OR_TENSION]
Visual: [METAPHOR]
Short label: [LABEL]

Panel 3: [BOTTLENECK]
Visual: [METAPHOR]
Short label: [LABEL]

Panel 4: [CONSEQUENCE_OR_NEW_LOGIC]
Visual: [METAPHOR]
Short label: [LABEL]

Bottom conclusion strip: [SHORT_CONCLUSION]

Style: cream/off-white background, bold Chinese magazine headline, asymmetrical editorial hierarchy, generous negative space, clean flat geometric line art, mostly monochrome characters, soft yellow/muted purple/warm orange/muted pink accents used only as functional signals. Avoid real likenesses, real logos, 3D, glossy lighting, heavy gradients, clutter, and tiny illegible text.
```

If a ReelOS mode is chosen, replace the generic style sentence with the selected mode from `reelos-style-modes.md`. Keep the characters mostly monochrome even in dark, sonic, or performance modes.

For diagrams with many labels, use the Text-safe strategy: generate the visual system with blank label zones and later typeset the exact Chinese text outside the image model.

## One-Image Clarity Builder

Use this before writing an article explainer prompt.

```text
Central question: [WHAT_THE_IMAGE_MUST_ANSWER]
Old logic: [WHAT_USED_TO_BE_TRUE]
New logic: [WHAT_IS_NOW_TRUE]
Mechanism: [WHY_THE_SHIFT_HAPPENS]
Affected actors: [WHO_OR_WHAT_CHANGES]
Risk or caveat: [WHAT_CAN_GO_WRONG]
Takeaway sentence: [WHAT_VIEWER_REMEMBERS]

Best structure:
- Cause-and-effect flow when a process changed.
- Before/after split when the operating logic changed.
- Market map when actors and incentives matter.
- Three-crack explainer when one system is failing from multiple tensions.
- Orbit/loop diagram when the point is a repeatable production system.
```

## Brand System Board

```text
Create a horizontal PNG brand visual system board for [BRAND/PRODUCT]. Interpret the brand as [SOUL_INTERPRETATION]. Show minimalist black-and-white line art characters in everyday scenes: [SCENES]. Include application panels for [APPLICATIONS]. Use bold editorial typography, large negative space, asymmetrical layout, and selective pastel accents: [ACCENT_COLORS]. Characters are mostly monochrome, clean flat geometric, simple faces, stylized bodies. Include product or brand proof objects: [OBJECTS].

Negative prompt: realistic lighting, 3D render, glossy effects, anime, childish mascot, excessive color, busy background, cluttered layout, heavy gradients, illegible typography.
```

## Image-To-Illustration

Write the image prompt in English unless the user requests Chinese.

```text
Preserve the main subject, pose, composition, and recognizable objects from the reference image. Convert the scene into a minimalist black-and-white editorial line-art illustration with clean flat geometric forms, simple facial features, stylized proportions, and a strong magazine-like layout. Simplify background clutter into large negative space and selective pastel accent blocks in [ACCENT_COLORS]. Keep the subject mostly monochrome. Use high-contrast vector-like lines, smooth edges, flat design, no realistic lighting.

Negative prompt: realistic rendering, 3D, painterly texture, glossy lighting, anime style, childish cartoon mascot, excessive color, busy background.
```
