# 生图提示词模板

每张图单独生成。根据主题替换变量，不要把多页拼在一起。

```text
Generate one standalone 9:16 vertical Chinese short-video thought poster in the ReelOS SketchTalk layout method, but make the user's input content the primary identity.

Visual DNA:
Pure white background. Minimal black, restrained warm red, and soft gray palette. Strong typography is the main visual anchor. Large empty white space. Minimal philosophical line illustration in the lower third. Calm, restrained, high-contrast, modern Chinese knowledge-video cover feeling. No gradients, no paper texture, no shadows, no platform UI, no watermark, no copied external account mark.

Top identity area:
Use the user's provided author name, account name, column name, series name, or title-derived label near the top center. If the user provides no identity and no brand requirement, keep the top area minimal or blank. Do not force "ReelOS", "漫说 ReelOS", or "@ReelOS" into the image unless the user explicitly asks for ReelOS branding. Do not use the reference account name, the circular "深" stamp, "SHEN DU JIN HUA LUN", or any external logo.

Text hierarchy:
Red premise line near the upper third:
{红色命题句}

Large bold black main statement in the center, 2 lines maximum:
{黑色主观点}

Thin uppercase English subtitle below, derived from the user's topic:
{英文副标}

Lower-third metaphor illustration:
{底部隐喻图：普通人物剪影在哪里、正在做什么、周围有什么极简物件}

Character / figure:
Use an ordinary human silhouette or semi-abstract human figure, small and quiet. Not a recurring IP character, not 镜环小工, not a cute mascot, not a robot. The figure should support the mood and metaphor, not dominate the page.

Color use:
Black for main statement and silhouette. Warm red for the premise line and one small visual anchor such as sun, moon, ring, apple, dots, or accent strokes. Soft gray only for weak secondary text or very light terrain. Keep red restrained.

Layout constraints:
9:16 vertical. Top brand area 0-10%. Red premise line around 12-24%. Main black statement around 30-45%. English subtitle around 47-54%. Large blank space before the lower illustration. Lower illustration around 66-88%. Preserve clean margins. Text must be readable and not overlap. The final image should feel like a serious short-video thought page, not a PPT slide, not a marketing poster, not a course cover.
```

## 分镜页策略模板

```text
For this script, create a vertical storyboard plan using the ReelOS SketchTalk layout method while prioritizing the user's own content identity.
For each page, output:
1. Page name
2. Red premise line
3. Bold black main statement
4. English subtitle
5. Top identity label from the user's input, or blank
6. Lower-third metaphor illustration
7. Mood

Keep each page to one idea. Use a pure white, black/red/gray, typography-led vertical thought poster style.
```

## 改图提示

去掉外部标识：

```text
Edit the provided image. Remove the external account mark, watermark, platform UI, copied reference branding, and any forced ReelOS branding that was not requested by the user. Replace the top identity area with the user's provided author, account, column, series, or title-derived label; if none was provided, keep it blank. Preserve the white background, black/red restrained style, text hierarchy, and lower minimal metaphor illustration. Do not add extra decorative elements.
```

增强 ReelOS SketchTalk 感：

```text
Regenerate this page with the same core idea, but make it more like a content-first vertical thought poster: stronger central Chinese typography, more white space, less illustration detail, ordinary human silhouette, black/red/gray only, no platform UI, no copied reference branding, and no forced ReelOS branding unless explicitly requested.
```
