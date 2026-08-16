# web-design-director — product-native interface direction

| Status | Deployed |
|---|---|
| Can deliver alone | A complete interface direction or review; with code and browser access, a verified implementation slice. |
| Cannot claim alone | Without actual rendering and interaction review, it cannot claim visual implementation or user acceptance passed. |

[Runtime `SKILL.md`](../../../skills/web-design-director/SKILL.md) · [Standalone ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/web-design-director.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. Purpose

Direct, review, or build a distinctive production-grade web interface from product truth through rendered verification.

<!-- contract:principles -->
## 2. Design principles

- Make product and design decisions before implementation; the interface direction must come from the product's real subject, audience, and job.
- Spend visual boldness in one justified signature element and keep the surrounding system disciplined.
- Source inspection and implementation tests do not replace rendered visual, state, responsive, and accessibility review.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

A complete interface direction or review; with code and browser access, a verified implementation slice.

**Cannot claim alone:** Without actual rendering and interaction review, it cannot claim visual implementation or user acceptance passed.

<!-- contract:inputs -->
## 4. Inputs

- Product type, audience, the page's single job, primary journey, real content, brand/design system, and technical stack.
- Existing interface, screenshots or repository when reviewing or modifying an existing product.
- Required states, devices, accessibility constraints, performance limits, and authorization to change code.

<!-- contract:workflow -->
## 5. Workflow

1. Ground the product, audience, single job, and vocabulary.
2. Inspect the actual interface and system before inventing a direction.
3. Choose a product-native color, type, layout, and one signature element; reject generic defaults.
4. Design the user journey, empty/loading/error/success states, responsive behavior, and engineering contract.
5. Implement one coherent slice, render it, and verify visual quality, interaction, keyboard use, mobile layout, and regressions.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- If product truth or the journey is unclear, return to grounding; do not solve it with decoration.
- If the direction could belong to any product, return to subject-native direction and signature.
- Missing states return to workflow design; implementation or rendering blockers return to the engineering contract and are re-verified in the actual interface.

<!-- contract:review -->
## 7. Review gates

- [ ] Product truth, information architecture, distinctiveness, visual system, interaction, accessibility, responsive behavior, and engineering quality all pass.
- [ ] All required states are visible and direct the user; errors explain recovery and controls use consistent action names.
- [ ] The actual rendered result is inspected at desktop and mobile widths with keyboard focus and reduced-motion behavior.

<!-- contract:pass -->
## 8. Pass standard and states

- Direction mode passes when the decision system and workflow are specific and implementable; build mode additionally requires rendered evidence.
- Without rendered and interaction evidence, report a design or source review—not visual implementation acceptance.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- A product-native design direction and engineering contract, an evidence-backed review, or a verified implemented slice.
- Concrete decisions, blocker-ranked findings, exact changed files when building, and remaining verification limits.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Do not migrate frameworks, add dependencies, or redesign unrelated surfaces merely for aesthetic uniformity.
- Do not call source inspection, tests, or a static mockup proof of user-accepted visual quality.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- Direction and review can be text-based; build and visual-pass claims require repository/file access, the project's runtime, browser rendering or screenshots, and interaction checks.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/web-design-director/agents/openai.yaml)
- [`SKILL.md`](../../../skills/web-design-director/SKILL.md)

**References**

- [`references/creative-direction.md`](../../../skills/web-design-director/references/creative-direction.md)
- [`references/design-rubric.md`](../../../skills/web-design-director/references/design-rubric.md)
- [`references/web-quality-checklist.md`](../../../skills/web-design-director/references/web-quality-checklist.md)
