# guofeng-visual-director — Chinese period visual direction

| Status | Candidate 0.1.1; opt-in experiment; image review pending |
|---|---|
| Can deliver alone | A complete visual brief, image prompt, controlled variant or diagnosis. |
| Cannot claim alone | It does not certify historical accuracy, user acceptance or finished video. |

[Runtime `SKILL.md`](../../../experimental/guofeng-visual-director/SKILL.md) · [Install current source](../../INSTALLATION.md#experimental-packages) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

Candidate source; no historical v1.3.0 ZIP.

<!-- contract:purpose -->
## 1. Purpose

Design coherent Chinese period imagery across people, clothing, architecture, objects, color and light.

<!-- contract:principles -->
## 2. Design principles

- Ground culture, lived space and image design in the brief; separate history, invented worlds and stylization.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

A complete visual brief, image prompt, controlled variant or diagnosis.

**Cannot claim alone:** It does not certify historical accuracy, user acceptance or finished video.

<!-- contract:inputs -->
## 4. Inputs

- Story, portrait, environment, object brief or a visual reference, with any locked facts.

<!-- contract:workflow -->
## 5. Workflow

1. Identify evidence and open choices; choose culture and medium; design people, space, light and material; compile and review the actual result.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Repair the earliest factual, spatial or pictorial mismatch while preserving accepted choices.

<!-- contract:review -->
## 7. Review gates

- [ ] Compare the actual image with the brief; text checks do not imply image acceptance.

<!-- contract:pass -->
## 8. Pass standard and states

- A reviewed result fits the requested medium and explicit evidence; user taste remains a separate decision.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- Visual direction, complete image prompts, controlled variants or image diagnosis as requested.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- No automatic xianxia, wuxia, fixed dynasty, image generation or full-film expansion.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- The visual parameter and QC package is text-only and host-neutral. Actual image or video output requires the host's media tools, model access, permissions, and visual review.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../experimental/guofeng-visual-director/agents/openai.yaml)
- [`SKILL.md`](../../../experimental/guofeng-visual-director/SKILL.md)

**References**

- [`references/cultural-grounding.md`](../../../experimental/guofeng-visual-director/references/cultural-grounding.md)
- [`references/image-direction.md`](../../../experimental/guofeng-visual-director/references/image-direction.md)
- [`references/people-and-objects.md`](../../../experimental/guofeng-visual-director/references/people-and-objects.md)
- [`references/prompt-and-review.md`](../../../experimental/guofeng-visual-director/references/prompt-and-review.md)
- [`references/world-and-space.md`](../../../experimental/guofeng-visual-director/references/world-and-space.md)

**Distribution notices in new ZIP builds**

New builds attach these files inside the Skill folder without editing its runtime source. Historical release archives are unchanged.

- [`LICENSE`](../../../LICENSE)
