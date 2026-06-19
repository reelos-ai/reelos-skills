# AI 主题图层生成提示词

用于儒释道、哲学、心理学、抽象原则、心法和方法论视频。目标不是生成“插画主画面”，而是生成可叠加到 Remotion 里的背景层、金描线稿和主题隐喻图层。

## 通用规则

- 默认画幅：16:9，1920x1080。
- 不要文字、不要字幕、不要 logo、不要水印、不要 UI。
- 画面要给标题和口播关键词留安全区，通常左侧 45% 更暗、更干净。
- 生成图层要低对比、可叠加，不能像海报主视觉一样抢戏。
- 人物只做背影、侧影或线描轮廓，不要写实脸，不要强表情。
- 文化主题避免廉价国潮、仙侠、玄幻游戏、过度金光、符咒堆叠。
- 每条视频优先生成三张：`cover` 强氛围、`body` 轻纹理、`final` 收束图。

通用负面约束：

```text
no text, no subtitles, no logo, no watermark, no modern UI, no neon cyberpunk, no fantasy game style, no cheap stock illustration, no exaggerated glow, no clutter, no photorealistic face close-up
```

## 道家 / 阴符经 / 观天道

### 背景层

```text
16:9 cinematic background for a Chinese Taoist philosophy video, dark Dunhuang mineral mural texture, cave wall, distant mountain mist, ancient paper fibers, subtle star chart arcs, old gold and mineral teal accents, deep umber and cinnabar palette, calm mysterious atmosphere, left side kept dark and clean for Chinese title text, no text, no symbols in focus, no logo, no watermark
```

### 金描线稿层

```text
minimal abstract gold line drawing on transparent-feeling dark background, back view of a Taoist sage in wide robe standing before mountain mist and a faint star map, Dunhuang mural line art, Song dynasty figure silhouette, old gold ink line, no face, no detailed features, no fantasy weapon, no text, no logo, elegant and restrained, lots of empty space
```

### 结尾收束层

```text
dark cave wall and ancient scroll texture, one quiet Taoist sage silhouette far away under a faint circular star chart, old gold linework, cinnabar seal-like block without characters, deep brown mineral palette, solemn and minimal, no readable text, no logo, no watermark
```

## 佛学 / 禅修 / 心性

### 背景层

```text
16:9 quiet Buddhist philosophy background, dark stone grotto wall, soft lotus shadow, faint circular halo, subtle sutra paper texture, warm old gold and muted stone gray, calm meditative atmosphere, left side dark clean space for title, no text, no logo, no watermark, not overly bright
```

### 金描线稿层

```text
minimal old gold line drawing, abstract seated meditation silhouette, faint Buddha halo outline behind, lotus geometry very subtle, no face, no deity details, no religious excess, dark transparent-feeling background, elegant restrained Buddhist mural line style, no text
```

## 儒学 / 人文 / 经典

### 背景层

```text
16:9 Chinese classical humanities background, warm dark study room light, ancient books, bamboo slips, paper fibers, subtle red editorial marks, ink and old gold palette, quiet scholarly atmosphere, left side clean for title, no readable text, no logo, no watermark
```

### 金描线稿层

```text
minimal old gold line drawing of a Confucian scholar silhouette reading beside a low desk, bamboo slips and book pages suggested with simple lines, no face, no detailed costume pattern, restrained Chinese literati style, empty space, no text
```

## 哲学 / 原则 / 思辨

### 背景层

```text
16:9 abstract philosophy background, dark paper texture, stone steps fading into mist, a quiet doorway, subtle geometric arcs and balance lines, restrained editorial composition, warm ink black, bone white, old gold accent, left side clean for title, no text, no logo
```

### 线稿层

```text
minimal old gold line drawing of a solitary thinker silhouette facing a doorway and layered paths, abstract not literal, no face, no modern clothing details, restrained editorial line art, dark transparent-feeling background, no text
```

## 心理学 / 心智 / 情绪

### 背景层

```text
16:9 psychology and inner world background, dark warm paper texture, abstract inner room, soft ripples, faint human silhouette reflection, gentle neural map lines, calm and mature, not medical, not cartoon, muted ink, warm gray, old gold, deep teal accents, clean area for text, no text, no logo
```

### 线稿层

```text
minimal old gold line drawing of an abstract human silhouette facing a mirror-like inner room, subtle emotion waves and relationship lines, no face, no medical brain diagram, no cartoon, restrained mature psychology editorial style, no text
```

## AI / Agent / 工程信号

### 背景层

```text
16:9 AI engineering signal background, dark editorial workspace, subtle server racks, abstract model layers, faint logs and node topology without readable text, indigo ink, off-white, muted teal and cinnabar accents, serious research atmosphere, clean space for Chinese title, no logo, no readable words
```

### 线稿层

```text
minimal technical line drawing, abstract agent workflow nodes and execution paths, old gold and muted teal lines on dark transparent-feeling background, no fake HUD, no cyberpunk glow, no readable text, restrained engineering diagram aesthetic
```

## 使用方式

1. 先按内容选择主题模式。
2. 每个视频生成 2-3 张图层：`cover`、`body`、`final`。
3. 保存到 `public/generated/{slug}/`。
4. 默认先离线优化：转成 1920x1080 JPG/WebP，把裁切、亮度、对比度、饱和度、暗角和遮罩尽量预烘焙，保存到 `public/generated/{slug}-optimized/`。
5. 在设计卡记录：生成提示词、生成日期、本地路径、优化路径、用途、处理方式和渲染耗时。
6. Remotion 默认只用 `Img + staticFile` 做低透明度静态显影和少量遮罩，不在每帧对图片做 `filter`、`scale()`、`mixBlendMode` 或大幅漂移。
7. 只有最终宣传片、强视觉版本或用户明确要求“动效更强”时，才启用慢推拉、光扫、颗粒和更复杂的图层混合。
