# fantasy-design — fantasy world and magic parameters

| Status | Deployed |
|---|---|
| Can deliver alone | A fantasy `style_route`, world and magic prompt fields, negative constraints, and QC contract. |
| Cannot claim alone | It does not justify arbitrary glow, modern objects, or copied franchise creatures merely because the genre is fantasy. |

[Runtime `SKILL.md`](../../../skills/fantasy-design/SKILL.md) · [v1.3.0 historical ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/fantasy-design.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

Historical v1.3.0 snapshot; differs from current source where updated.

<!-- contract:purpose -->
## 1. Purpose

Translate fantasy into coherent world rules, magical cause and light, spatial behavior, materials, creatures, action, and continuity.

<!-- contract:principles -->
## 2. Design principles

- Translate genre feeling into observable camera, color, space, action, material, sound, and continuity parameters.
- Genre parameters support an approved story and assets; they do not rewrite either one.
- Director names and color values are sources or starting points, never imitation commands or universal laws.
- Golden hour, complementary colors, shallow focus, foreground people, exact lens values and worn surfaces are optional design choices, not universal quality requirements.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

A fantasy `style_route`, world and magic prompt fields, negative constraints, and QC contract.

**Cannot claim alone:** It does not justify arbitrary glow, modern objects, or copied franchise creatures merely because the genre is fantasy.

<!-- contract:inputs -->
## 4. Inputs

- Genre, intended medium, scene function, subjects, locked choices and relevant assets; duration and platform fields only when needed by the current deliverable.
- Existing director, blocking, lighting, continuity, and end-state decisions.
- Missing fields remain open; generic words such as 'cinematic' cannot fill them.

<!-- contract:workflow -->
## 5. Workflow

1. Read the package-local cinematic-image-direction reference, choose the imaging medium, and establish the visible proposition and attention hierarchy before presets.
2. Derive functional color, light sources, spatial structure, and scene parameters.
3. Add materials, contact and state continuity; include camera motion, timing and sound only for video, and preserve supplied approved assets.
4. Compile the ten information categories and platform translation without changing upstream decisions.
5. Run shared and genre-specific review; emit `ready_for_prompt` or a field-specific `rework` result.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Story, asset, or blocking failures return to their owning layer; style failures return to the camera, color, space, action, material, or continuity field that caused them.
- Review failure produces `rework` with the failed field; it cannot be bypassed by another generation attempt.
- These modules have design rework, not historical version rollback.

<!-- contract:review -->
## 7. Review gates

- [ ] All fields required by the current medium agree: framing, functional color, motivated light, space, subject/material relations and state; add motion and sound for video only.
- [ ] The shared anti-fake-cinema checks reject empty quality words, unmotivated camera moves, source-less light, decorative color, and unstable props or space.
- [ ] Genre-specific negative constraints target only likely failures and do not suppress story-authorized color, scale, stillness, or motion.
- [ ] Magic has a visible source, rule, cost, target, and environment response; wings, bodies, and materials avoid plastic or gravity-free behavior.

<!-- contract:pass -->
## 8. Pass standard and states

- All shared and genre-specific checks pass, approved assets remain unchanged, and the module can emit `ready_for_prompt`.
- `ready_for_prompt` means the visual parameter package is ready; it does not prove that an image, clip, or final film passed.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- A genre-specific `style_route`, `style_module`, and `qc_contract` that can stand alone as a visual parameter package.
- Scene-ready prompt fields, negative constraints, continuity state, and sound cues.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Do not write the screenplay, replace director judgment, or modify approved asset appearance.
- Do not claim universal genre color laws, living-artist imitation, or generation success.
- The new image-relationship reference is an authored synthesis of supplied-image analysis. The 14 accepted showcase results do not establish the source methods of another Skill, a stable success rate, or an old/new same-prompt A/B improvement.
- The user accepted this round's representative image, recorded in docs/showcase/manifest.json; that is an image-level result, not a universal success claim.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- The visual parameter and QC package is text-only and host-neutral. Actual image or video output requires the host's media tools, model access, permissions, and visual review.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/fantasy-design/agents/openai.yaml)
- [`SKILL.md`](../../../skills/fantasy-design/SKILL.md)

**References**

- [`references/cinematic-image-direction.md`](../../../skills/fantasy-design/references/cinematic-image-direction.md)
- [`references/COMMON-12-SECTION-PROTOCOL.md`](../../../skills/fantasy-design/references/COMMON-12-SECTION-PROTOCOL.md)
- [`references/NEGATIVE-CASE-BOOK.md`](../../../skills/fantasy-design/references/NEGATIVE-CASE-BOOK.md)
- [`references/SOURCE-LEDGER.md`](../../../skills/fantasy-design/references/SOURCE-LEDGER.md)

**Distribution notices in new ZIP builds**

New builds attach these files inside the Skill folder without editing its runtime source. Historical release archives are unchanged.

- [`LICENSE`](../../../LICENSE)
