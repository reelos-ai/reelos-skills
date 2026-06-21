# Material Workflow

Use this reference when the video should prioritize external video/image backgrounds.

## Principle

Material-led videos should feel like edited footage with subtitles and light visual packaging. Do not replace the background with pure MG unless the content is abstract or the user explicitly asks for a product-film/diagram style.

## OpenMontage Lessons to Keep

The project learned these ideas from OpenMontage:

- source-led production
- scene slots
- multi-keyword search
- provider abstraction
- candidate scoring
- download validation
- manifest as the contract between material sourcing and composition
- quality gate before render

Do not copy OpenMontage source code because of AGPLv3. Keep the implementation self-authored.

## Local Pipeline

Use `scripts/material_pipeline.py` as the reusable layer. A material script should define:

- slug and output directory
- target orientation and resolution
- scene slots with `id`, `query`, `keywords`, and duration need
- providers such as Pexels, Pixabay, Coverr when credentials are available
- scoring preferences: orientation match, width/height, duration, quality, relevance

Outputs should include:

- downloaded media under `public/materials/{slug}/`
- `public/materials/{slug}/manifest.json`
- generated TS manifest such as `src/compositions/{slug}Materials.ts`

## Provider Rules

- Pexels: good for free video search by keyword and orientation.
- Pixabay: good fallback for videos and images with multiple size versions.
- Coverr: useful for horizontal video, often needs later resize/crop.

Always record enough provenance in the manifest to audit where a clip came from.

## Composition Rules

- Use `OffthreadVideo` for video material.
- Loop short background clips if they are shorter than the scene.
- Use `objectFit: 'cover'`.
- Add a dark overlay and gradient mask for text readability.
- Keep subtitles and keywords stable; avoid turning the video into a full-screen dashboard.
