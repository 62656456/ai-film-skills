# female-image-aesthetics — aesthetics-led portrait photography

| Status | Current v0.3.0 source; published examples are task-specific evidence, not a reliability guarantee. |
|---|---|
| Can deliver alone | Photographic concepts, complete actual prompts, authorized generated images and optional sharing copy. |
| Cannot claim alone | The folder does not include a model or account and does not itself authorize image generation or publication. |

[Runtime `SKILL.md`](../../../skills/female-image-aesthetics/SKILL.md) · [Install current source](../../INSTALLATION.md) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

Install the complete current source folder. Existing release ZIPs do not contain this newly published module.

<!-- contract:purpose -->
## 1. Purpose

Create compelling adult female photographic imagery by coordinating expression, action cause, styling, physical response, composition, lighting and rendering.

<!-- contract:principles -->
## 2. Design principles

- Design the entire image through expression, purposeful action, styling, setting, props, light and photographic rendering.
- Turn emotion into visible gaze, facial tension, body lines and material response; keep each still image to one moment.
- Choose optical softness, bokeh, motion traces or contrast for a visible purpose; a camera name alone is not an effect.
- Keep approved identity and design decisions; distinguish independent themes, identity variants and images in one story.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

Photographic concepts, complete actual prompts, authorized generated images and optional sharing copy.

**Cannot claim alone:** The folder does not include a model or account and does not itself authorize image generation or publication.

<!-- contract:inputs -->
## 4. Inputs

- The requested deliverable, subject or theme, intended use and existing generation or publication authorization.
- Any approved references and the exact roles they play in identity, wardrobe, composition, light or mood.

<!-- contract:workflow -->
## 5. Workflow

1. Recover existing design decisions and decide whether the request needs discussion, prompts, actual images or sharing copy.
2. State one concrete visual proposition and coordinate silhouette, color areas, depth, materials and exposure around it.
3. Write a complete prompt with expression, action cause, physical effects, composition and lighting; use references only for their stated roles.
4. Generate only within the active authorization, inspect the actual result and repair concrete failures from an eligible original basis.
5. Deliver the requested images or text with the complete actual prompts and an accurate account of reference use.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- For weak beauty or tension, revise the few dominant causes in expression, lines, light, styling or spatial design.
- A failed image is diagnostic only; return to an approved original reference or complete text rather than a chain of failed edits.

<!-- contract:review -->
## 7. Review gates

- [ ] The whole image has a coherent attraction, visual hierarchy and deliberate photographic expression.
- [ ] Shoulder, elbow, forearm, wrist, hand, contact and held objects form a credible chain.
- [ ] Wind, rain, fabric weight, shadows, reflections and depth of field support the intended moment.
- [ ] Prompts, actual reference inputs, generated results and user decisions are accurately distinguished.

<!-- contract:pass -->
## 8. Pass standard and states

- Text delivery is complete and executable; image delivery includes actual generated images that were inspected.
- Structural checks, a published example and explicit aesthetic acceptance remain different evidence states.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- Complete photographic design and image prompts; actual images when authorized tools are available.
- Optional image-plus-prompt sharing copy with AI disclosure and precise reference-use notes.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Subjects in this module are adults. A portrait request does not become a mandatory multi-view character-asset task.
- Writing, image generation and external publication retain their own active authorization; existing authorization is reused.
- Do not claim real-world shooting, unperformed retouching, exact optical reproduction or universal stable output.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- A host that can read the complete folder can use the design method. Actual images require its image tool and visual inspection; platform publication additionally requires an authorized account workflow.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/female-image-aesthetics/agents/openai.yaml)
- [`SKILL.md`](../../../skills/female-image-aesthetics/SKILL.md)

**References**

- [`references/body-and-prop.md`](../../../skills/female-image-aesthetics/references/body-and-prop.md)
- [`references/photographic-expression.md`](../../../skills/female-image-aesthetics/references/photographic-expression.md)
- [`references/photographic-prompt-design.md`](../../../skills/female-image-aesthetics/references/photographic-prompt-design.md)
- [`references/reference-to-live-action.md`](../../../skills/female-image-aesthetics/references/reference-to-live-action.md)
- [`references/style-integration.md`](../../../skills/female-image-aesthetics/references/style-integration.md)
- [`references/x-content-handoff.md`](../../../skills/female-image-aesthetics/references/x-content-handoff.md)

**Distribution notices in new ZIP builds**

New builds attach these files inside the Skill folder without editing its runtime source. Historical release archives are unchanged.

- [`LICENSE`](../../../LICENSE)
