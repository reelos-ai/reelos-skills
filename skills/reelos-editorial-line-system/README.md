# ReelOS Editorial Line System

This Codex skill converts text, images, brands, products, UI concepts, campaigns, and analysis articles into a ReelOS-flavored editorial illustration system: black-and-white line-art characters, flat geometric scenes, strong typography, large negative space, and sparse pastel accents.

Its core claim: **one image should make the matter clear**. For articles and analysis, the image should compress the argument, conflict, mechanism, and conclusion into a visual explanation, not merely decorate the text.

Default representative style: **Base Editorial Line**. Use it when no other mode is specified. `ReelOS Lab Orbit` is the second mode and the representative ReelOS-branded style for personal AI OS, builder lab, orbit, signal, or system telemetry language.

For sharp text, use the text-safe workflow: let image generation create the illustration layer, then typeset exact Chinese titles, labels, and captions with HTML/SVG or another layout layer. Pure image generation is best for sparse large text, not dense diagrams.

## Structure

- `SKILL.md`: lightweight entry point, trigger rules, routing, and core operating principles.
- `references/visual-language.md`: visual DNA, accent palette, composition principles, and negative constraints.
- `references/output-routing.md`: input classification and output decision rules.
- `references/prompt-recipes.md`: PNG prompt recipes for posters, article explainers, brand boards, and image-to-illustration conversion.
- `references/reelos-style-modes.md`: ReelOS palette and aesthetic modes adapted from `reelos-design-taste`.
- `references/html-output.md`: guidance for exact editable HTML layouts.
- `references/quality-check.md`: final quality checklist.

## Attribution

This skill is an adapted and reorganized ReelOS version inspired by the original project:

[huxiang1126/editorial-line-system](https://github.com/huxiang1126/editorial-line-system)

Thanks to the original author for the editorial line-art visual system direction and prompt foundation.
