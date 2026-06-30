# Taste Review

Use this reference to critique and refine design taste.

## Taste Axioms

- Taste is selection power: not more assets, but fewer stronger choices.
- Taste knows when to stop; stopping is an active design move.
- Taste ages better than fashion. Prefer durable structure over trend effects.
- Taste is the sum of invisible details: baseline, line-height, edge contrast, opacity, easing, and spacing.
- Restraint is confidence: when you can add more but choose not to.
- Specificity beats adjective clusters: a precise design world carries more taste than "modern, clean, premium."
- Negative constraints define character: what the system refuses to use is as important as what it permits.

## Taste Scorecard

Score each axis from 1-5:

1. **Typography**: Are scripts paired optically and emotionally, with appropriate hierarchy, line-height, and weight?
2. **Choice / Restraint**: Does the design know what to omit?
3. **Hierarchy**: Can the viewer immediately tell what matters?
4. **Cultural Coherence**: Do color, type, layout, material, imagery, and motion come from the same logic?
5. **Spacing Rhythm**: Is whitespace intentional and consistent?
6. **Material Honesty**: Do texture, shadow, and surfaces feel purposeful?
7. **Color Discipline**: Does every accent have a role?
8. **Interaction Tempo**: Does motion fit the aesthetic and task?
9. **Specificity**: Could this design only belong to this brief?
10. **Durability**: Will it still feel good after the trend passes?
11. **Execution Readiness**: Are tokens, components, states, and responsive behavior concrete enough to implement?
12. **Reference Integrity**: If a reference was used, has it been transformed into a reusable pattern rather than copied?
13. **Spec Portability**: Can another agent implement this from prose rationale, semantic tokens, states, and do-not-use rules without guessing?

Interpretation:
- 59-65: refined, durable, and implementation-ready.
- 48-58: strong direction with detail issues.
- 35-47: concept exists, taste needs tightening.
- Below 32: likely generic, overloaded, incoherent, or not shippable.

## Severity Guide

- **P0 Blocking**: unreadable text, broken responsive layout, inaccessible contrast, or cultural misuse that makes the design unsafe to ship.
- **P1 Major**: typography mismatch, no hierarchy, conflicting aesthetic systems, or decorative motifs replacing structure.
- **P2 Moderate**: palette overuse, weak spacing rhythm, unclear material logic, generic imagery, or motion mismatch.
- **P3 Polish**: microcopy, hover nuance, tiny opacity/radius/easing improvements.

## Fix Priority

1. Typography legibility and role clarity.
2. Information hierarchy and first-viewport focus.
3. Cultural/aesthetic coherence.
4. Palette role discipline.
5. Layout rhythm and responsive fit.
6. Material, imagery, texture, and motion polish.
7. Implementation readiness: tokens, states, constraints, verification.

## Common Taste Failures

- **Motif dumping**: adding cultural symbols instead of using cultural structure.
- **Over-accenting**: cinnabar, gold, teal, gradients, shadows, and texture all competing.
- **Generic premium**: beige background plus serif type but no real hierarchy.
- **Fake minimalism**: too little information hierarchy, not enough intent.
- **Unmatched scripts**: elegant Chinese paired with aggressive Latin, or vice versa.
- **Trend residue**: glassmorphism, blobs, bokeh, gradient orbs, oversized cards without domain reason.
- **Motion mismatch**: fast bouncy effects in Zen pages, slow ceremonial motion in dense SaaS workflows.
- **Image vagueness**: atmospheric stock image where the user needs product/place specificity.
- **Decorative cards everywhere**: page sections treated as floating cards, flattening the hierarchy.
- **Font theater**: display fonts doing body-text work, brush fonts used as UI, or mono type making prose hard to read.
- **Color-first design**: choosing palettes before defining type voice and hierarchy.
- **Adjective soup**: relying on "clean, premium, modern" without a specific product world, reference situation, or cultural logic.
- **Token theater**: listing colors, type sizes, and radii without rationale, component states, or negative constraints.
- **False luxury**: beige, serif, large whitespace, and gold accents without precise hierarchy or content specificity.
- **Fake tech**: terminal/scanline/neon effects with no data logic.
- **Overlocalized cliché**: dragons, lanterns, cherry blossoms, mandalas, or tribal patterns used as stickers.
- **Motion vanity**: animations that show off but do not clarify sequence, mood, or state.

## Refinement Moves

If overloaded:
- Remove one accent color.
- Remove one decorative motif.
- Reduce shadows and borders.
- Increase whitespace around the true focal point.
- Make the primary action visually calmer but clearer.

If bland:
- Add one culturally meaningful material signal.
- Add one precise accent color with a role.
- Increase type contrast between title and body.
- Introduce a stronger layout rhythm: grid, garden reveal, radial mandala, or signal panel.

If incoherent:
- Choose the dominant aesthetic and demote all others.
- Re-map tokens to semantic roles.
- Replace mismatched typography.
- Make imagery and motion follow the same metaphor.

If illegible:
- Improve contrast before adding style.
- Reduce texture under text.
- Use stronger body type.
- Tighten line length and line-height.

If typography is weak:
- Define display/body/meta roles before changing colors.
- Remove one font family or one unnecessary weight.
- Match CJK and Latin by optical weight.
- Increase line-height before increasing decoration.
- Use mono only for data, labels, and metadata.

If cultural signal is superficial:
- Replace motifs with structural logic: grid, garden reveal, ma, mandala radiality, telemetry, or brush rhythm.
- Reduce symbols to one or two moments.
- Add material specificity instead of more ornament.
- State which cultural idea drives layout, not just palette.

## Review Output Format

For a design review, lead with the highest-impact findings:

```text
Findings
1. [Severity] Issue - where it appears and why it weakens taste/usability.
2. [Severity] Issue - concrete fix.

Taste Direction
One sentence on the intended aesthetic and what needs to become stricter.

Suggested Fixes
- Type:
- Palette:
- Layout:
- Material:
- Motion:

Verification Needed
- What must be checked in rendered output:
```

Do not praise vaguely. Name what works only when it explains how to preserve it.

## Professional Review Checklist

Use this for serious UI, landing page, brand system, or reference-extraction work:

- Is the first viewport specific to the product, not a generic hero?
- Are CTA, proof, and audience fit visible without reading every paragraph?
- Are type roles mapped before choosing colors?
- Do cards, borders, shadows, gradients, and glows have semantic roles?
- Are hover, focus, active, disabled, and mobile states considered when implementing?
- If a portable spec is needed, does it include prose rationale plus semantic tokens rather than token values alone?
- Does the design use real subject matter or inspectable product/place/object imagery when needed?
- If a reference inspired the design, can the result survive without copying its exact layout or brand assets?
- Is there a clear "do not use" list to prevent taste drift?

## Generation Guardrails

Before finalizing generated design, ask:

- What did I intentionally not include?
- Did I confirm or infer the product context, audience, and artifact type?
- If using a reference, did I extract decisions rather than transplant its structure?
- Is the typography direction strong enough before color and imagery are considered?
- Is the first viewport instantly legible?
- Does every major element have a role?
- Is the cultural signal structural?
- Are the details quiet enough to feel confident?
- Would this still work in grayscale?
- Would this still work with real content, not placeholder copy?
- If implemented, did I verify rendered typography, spacing, responsive fit, and console/browser errors?
