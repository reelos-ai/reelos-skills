# 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse red/orange/blue handwritten Chinese annotations. Clean absurd product-sketch feeling. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI.

Recurring IP character required:
Always include ReelOS.ai's default recurring article-illustration IP character, even when the user does not mention a character name. The internal character name is 镜环小工. It is a small serious deadpan system-operator creature with a deep navy / near-black slightly uneven rounded body, one concentric lens-ring face inspired by the ReelOS logo, ivory outer ring, black ring, warm orange inner ring, tiny dark center, thin legs, tiny thin arms, and at most very subtle white dot eyes. 镜环小工 must perform the core conceptual action, not decorate the scene. Make it calm, strange, functional, and slightly bizarre, not cute, not a robot mascot.

Hard character lock:
The character must not be a plain black blob, generic robot, camera icon, cute mascot, or old 小黑-style creature. The lens-ring face is the identity anchor and must be visible in the final image.

Theme:
{正文配图主题}

Structure type:
{结构类型：Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小漫画分镜}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：ReelOS 固定 IP 在哪里、正在做什么、主要物件是什么、信息如何流动；默认使用镜环小工，不要因为用户没写角色名而省略角色}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Chinese handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Color use:
Black for main line art. Deep navy / near-black for 镜环小工's body. Ivory and warm orange for the lens-ring face accents. Orange for main flow/path/arrows. Red only for key warnings/problems/results. Blue only for secondary notes or feedback/system state.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short handwritten Chinese labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. It should be clear but not instructional, interesting but not childish, strange but clean.
```

## 图像编辑提示

去掉左上角标题：

```text
Edit the provided image. Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

增强怪诞感：

```text
Regenerate this illustration with the same core meaning and simple layout, but make 镜环小工 more central to the conceptual action. 镜环小工 should be doing the strange work that explains the idea, not standing beside the diagram. Preserve the ReelOS lens-ring face: ivory outer ring, black ring, warm orange inner ring. Keep it clean, sparse, hand-drawn, and not cute.
```
