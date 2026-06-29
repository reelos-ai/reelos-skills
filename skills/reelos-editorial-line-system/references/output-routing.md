# Output Routing

Use this reference to decide what to produce.

## Default Decision

- Text without requested format -> create a PNG editorial image through `image_gen`.
- Text plus "图片", "海报", "PNG", "做成图", "头图", or "配图" -> create the PNG directly.
- Image input -> use image generation or editing directly, preserving subject and composition.
- Brand only -> infer the brand soul and create a PNG visual system board unless the user asks only for a prompt.
- Campaign, product, or app -> create a multi-application system board: magazine spread, product card, website hero, mobile UI, packaging, and character sheet as relevant.
- Exact long text, editable typography, or browser output -> use HTML only when the user asks for it.

## Text Input

Extract:

1. The thesis or message.
2. The emotional temperature.
3. The audience or use context.
4. The main visual metaphor.
5. The best layout type.

For long analysis, also extract:

1. Central conflict.
2. Causal chain.
3. Key actors.
4. Bottlenecks or turning points.
5. Consequence or conclusion.

## Brand Or Product Input

Build:

1. **Soul interpretation**: one or two sentences naming the everyday-life scene and emotional temperature.
2. **Character world**: who appears, what they do, and which objects prove the brand/product.
3. **Layout system**: the strongest applications, such as magazine spread, website hero, app screens, packaging, poster, social card, or character sheet.
4. **Color accent**: choose 1-3 pastel accents and assign roles.
5. **Ready prompt**: produce the prompt or generate the PNG if the user asked for an image.

## Image Input

Preserve:

- Main subject.
- Pose and composition.
- Recognizable objects.
- Important scene relationships.

Convert:

- Realistic forms into black-and-white line art.
- Background clutter into editorial negative space.
- Color complexity into sparse pastel accent blocks.
