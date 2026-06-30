# User Guide

Use this guide when the user asks how to use the skill or seems unsure how to describe a design request.

## Minimal Prompt Formula

```text
Use $reelos-design-taste for [artifact type], typography first.
Project: [what it is]
Audience: [who uses/views it]
Language: [Chinese / English / mixed]
Desired feeling: [3-5 adjectives]
Style candidates: [optional]
Reference: [optional URL / screenshot / HTML / brand]
Avoid: [optional]
Output: [direction / typography only / implement / review / image prompt / reference extraction]
Verification: [optional browser screenshot / responsive / contrast / console]
```

For stronger results, replace vague adjective clusters with a concrete reference situation:

```text
Instead of: premium, modern, trustworthy
Try: like a founder memo from a frontier AI lab, translated into a public product landing page
```

## Quick Starters

Typography only:

```text
Use $reelos-design-taste to create a typography system first.
Project: AI investment community
Language: mostly English, some Chinese
Feeling: sharp, trustworthy, frontier, not cyberpunk
Output: typography only
```

Full visual direction:

```text
Use $reelos-design-taste to create a full visual direction.
Project: premium tea brand landing page
Language: Chinese first, English secondary
Feeling: new Chinese, quiet luxury, ceremonial, modern
Avoid: dragons, lantern cliches, overused gold
Output: direction
```

Review:

```text
Use $reelos-design-taste to review this page, typography first.
Focus: what makes it feel generic or not refined
Output: review with P0-P3 findings and suggested fixes
```

Implementation:

```text
Use $reelos-design-taste to implement this UI direction in the app.
Style: Deep Space Signal
Priority: typography, then palette, then layout
Verify: browser screenshot and responsive fit
```

Reference extraction:

```text
Use $reelos-design-taste to study this URL/HTML.
Extract reusable typography, palette, layout, material, and motion rules.
Do not copy the brand; convert it into a reusable pattern.
```

Portable taste spec:

```text
Use $reelos-design-taste to create a portable taste spec.
Project: mixed Chinese/English AI research product
Audience: technical founders and investors
Reference world: research-lab briefing meets premium product interface
Priority: typography first, then semantic tokens and component states
Output: portable taste spec with do/do-not constraints
```

Professional implementation brief:

```text
Use $reelos-design-taste to implement a polished landing page direction.
Project: high-conversion creative agency for ecom brands
Language: English
Style: Performance Creative Agency
Priority: typography first, then proof metrics, workflow preview, CTA clarity
Avoid: generic agency portfolio, vague gradients, pixel font in paragraphs
Verification: browser screenshot, responsive fit, contrast, console
```

## Choosing A Scheme

If the user does not know which aesthetic to choose, offer 3 options:

1. **Safe / Productive**: clearer, more usable, less expressive.
2. **Signature / Branded**: stronger personality and cultural signal.
3. **Experimental / Immersive**: more atmospheric, more risk, suitable for concept pages.

Example:

```text
I can take this in three directions:
1. Swiss Product Clarity - best for SaaS trust and usability.
2. Frontier Intelligence - best for AI/investor/community energy.
3. Deep Space Signal - best for immersive narrative and data mystery.
```

## Input Quality Ladder

Good:
- "Make it premium."

Better:
- "Make it premium, Chinese-first, for a tea brand."

Best:
- "Make it premium and Chinese-first for a tea brand landing page. Typography should feel Song-style and modern. Avoid dragons/lanterns. Output a full direction plus CSS token suggestions."

Professional:
- "Use $reelos-design-taste for a mixed Chinese/English AI product homepage. Audience: technical founders. Reference: Aura Cloud for motion restraint, Rewired for typography energy, but do not copy either. Output: typography system, visual tokens, motion rules, and implementation guardrails."

## Default Assumptions

When the user provides little context:
- Treat language as mixed CJK/Latin if the user writes Chinese and references English UI.
- Use typography-first direction before palette.
- Choose one dominant style and name assumptions.
- Provide 2-3 style options only when the dominant direction is unclear.

## Better Prompts By Task

Direction:
- State product type, audience, language mix, desired feeling, and forbidden cliches.

Review:
- Provide URL, screenshot, or files; name what feels wrong if known; ask for P0-P3 findings.

Implementation:
- Name stack/files if relevant; ask for visual verification; define whether to preserve existing design system.

Reference extraction:
- Provide source URL/HTML; ask for reusable rules; explicitly say not to copy brand, assets, text, or proprietary structure.

Portable taste spec:
- Ask for a taste thesis, design rationale, semantic tokens, component states, and do/do-not constraints.
- Use this when the design direction will be handed to another coding agent or reused across pages.
