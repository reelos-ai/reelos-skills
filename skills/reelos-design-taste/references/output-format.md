# Output Format

Use the smallest format that satisfies the task. Do not force every section into short answers.

## Design Direction

```text
Aesthetic direction
One precise sentence naming the dominant visual logic.

Assumptions
- Product / audience:
- Language:
- Dominant style:

Typography system
- Display:
- Body:
- UI:
- Meta / data:
- Accent:
- CJK/Latin matching rule:
- Line-height / tracking rule:

Design constraints
- Palette:
- Layout:
- Spacing:
- Shape:
- Material / imagery:
- Motion:

Taste guardrails
- What to avoid:
- What to preserve:

Implementation notes
- Concrete CSS, component, asset, or prompt decisions.

Verification notes
- What should be checked visually or in browser before delivery.
```

## Typography-Only Direction

```text
Typography direction
One sentence describing the type voice.

Font roles
- Display:
- Body:
- UI:
- Meta / data:
- Accent:
- Fallbacks:

Hierarchy
- H1:
- H2/H3:
- Body:
- Caption/label:
- Data/metadata:

Rules
- CJK/Latin optical matching:
- Line-height:
- Letter-spacing:
- Weight usage:
- What to avoid:
```

## Portable Taste Spec

Use this when the design direction must be reused by another agent, teammate, codebase, or future session. The goal is not to create a giant design system; it is to make taste executable without flattening it into tokens only.

```text
Taste thesis
One specific sentence naming the world this design belongs to. Prefer a concrete reference situation over adjective clusters.

Example pattern
- Better: "A graduate-level AI research lab briefing translated into a premium product interface."
- Weaker: "modern, clean, premium, trustworthy."

Design rationale
- Typography:
- Palette:
- Layout:
- Material / depth:
- Motion:
- Why these choices fit the product and audience:

Semantic tokens
- Color roles:
  - canvas:
  - surface:
  - text-primary:
  - text-muted:
  - accent-primary:
  - accent-secondary:
  - border:
  - state-success / warning / error:
- Type roles:
  - display:
  - heading:
  - body:
  - UI:
  - meta / data:
  - CJK / Latin pairing:
- Spacing:
  - base unit:
  - component padding:
  - section rhythm:
- Shape:
  - radius scale:
  - icon stroke:
- Depth / material:
  - surface stack:
  - border / shadow / blur rules:
- Motion:
  - reveal:
  - hover:
  - active / focus:
  - background:

Component states
- Primary button: default / hover / active / focus / disabled.
- Secondary button: default / hover / active / focus / disabled.
- Card or panel: default / hover / selected.
- Input: default / focus / error / disabled.
- Navigation item: default / active / hover.

Do / Do not
- Do:
- Do not:

Verification notes
- Contrast:
- Responsive fit:
- Typography rendering:
- Motion performance:
- Browser or screenshot checks:
```

## UI / Brand System Implementation

```text
Implemented
- Files or components changed.
- Visual system choices applied.

Typography applied
- Font roles:
- Scale / weights:
- CJK/Latin handling:

Design rationale
- One short paragraph connecting choices to the aesthetic.

Verification
- Typography, layout, responsive fit, contrast, console, screenshots, or tests.

Residual risk
- Any unchecked browser/device/source limitation.
```

## Design Review

```text
Findings
1. [Severity] Issue - where it appears and why it weakens taste/usability.
2. [Severity] Issue - concrete fix.

Taste direction
One sentence on the intended aesthetic and what must become stricter.

Suggested fixes
- Typography:
- Palette:
- Layout:
- Material / imagery:
- Motion:
```

## Image Prompt Direction

```text
Prompt
Specific subject, composition, material, lighting, color, and cultural logic.

Negative direction
Motifs, cliches, and generic stock-like signals to avoid.

Use case notes
Aspect ratio, placement, inspection needs, and text-safe areas if relevant.
```

## Reference Extraction

```text
Extracted pattern
Name the reusable pattern.

Source read
- URL/file/source type:
- Evidence used: CSS/HTML/computed style/screenshot:

Reusable rules
- Typography:
- Palette:
- Layout:
- Material / imagery:
- Motion:
- Taste guardrails:

Source treatment
- What was treated as reusable pattern, not copied content:

Skill placement
- Which reference file should be updated and why.
```

## Professional Brief Audit

Use this when the user's brief is vague and the next step should be to tighten the design problem.

```text
Brief diagnosis
- What is known:
- What is missing:
- What is risky:

Recommended next move
- Proceed with assumptions / ask one question / offer three directions:

Typography-first assumption
- Proposed type voice:

Style options
1. Safe / Productive:
2. Signature / Branded:
3. Experimental / Immersive:
```
