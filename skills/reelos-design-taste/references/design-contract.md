# Design Contract

Use this when the output must travel across agents, future sessions, or implementation phases.

## Contract Structure

```text
Taste thesis
One sentence naming the design world.

Evidence map
| Source | Signal | Confidence | Reusable lesson |

Nine-section visual system
1. Visual Theme & Atmosphere
2. Color
3. Typography
4. Spacing & Grid
5. Layout & Composition
6. Components
7. Motion & Interaction
8. Voice & Brand
9. Anti-patterns

Semantic tokens
- canvas:
- surface:
- text-primary:
- text-muted:
- border:
- accent-primary:
- accent-secondary:
- success / warning / error:
- focus-ring:

Component states
- button:
- input:
- navigation:
- card / panel:
- table / list:

Implementation handoff
- files to read:
- constraints:
- assets:
- responsive checks:
- first-screen acceptance:
```

## Evidence Confidence

- **observed**: measured or read directly from code, DOM, screenshot, design file, or provided asset.
- **provided**: stated by the user or source material.
- **inferred**: reasoned from available signals; label the assumption.

## Contract Rules

- Prefer concrete constraints over adjectives.
- Keep one dominant aesthetic stance.
- Include anti-patterns so future agents know what not to generate.
- Define component states when the artifact is interactive.
- Include verification notes that can be checked visually or in browser.
