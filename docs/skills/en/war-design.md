# war-design — unified war and military film visual advisor

| Status | Deployed |
|---|---|
| Can deliver alone | Genre parameters, military visual advice, complete image prompts, actual images, and war-visual/sound supplements for approved shots. |
| Cannot claim alone | Merging and installation do not replace new image/video or user-aesthetic evaluation, or certify real tactics and equipment performance. |

[Runtime `SKILL.md`](../../../skills/war-design/SKILL.md) · [v1.3.0 historical ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/war-design.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

Historical v1.3.0 snapshot; differs from current source where updated.

<!-- contract:purpose -->
## 1. Purpose

Unify war-genre light and space, military clothing and equipment, environments and props, story/combat imagery, squad cinematography and actual-image review under war-design.

<!-- contract:principles -->
## 2. Design principles

- Select the requested mode before loading rules: style parameters, assets, story images, or shot supplements. Empty environments remain empty.
- Preserve user locks, treat presets as optional designs, and separate observations, source claims, and authored choices.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

Genre parameters, military visual advice, complete image prompts, actual images, and war-visual/sound supplements for approved shots.

**Cannot claim alone:** Merging and installation do not replace new image/video or user-aesthetic evaluation, or certify real tactics and equipment performance.

<!-- contract:inputs -->
## 4. Inputs

- The target medium, story or object, locked people/space/style, and relevant references.
- Use duration, platform and existing sound only when needed; do not invent unverified models or dates.

<!-- contract:workflow -->
## 5. Workflow

1. Choose parameters, character, environment, prop, story, combat, or squad mode.
2. Establish attention, spatial and material relationships; use genre presets when useful.
3. Add goals, obstacles and visible evidence for story tasks; preserve the scope of asset-only tasks.
4. Check actual prompt payloads for people, equipment, directions and reference roles; use natural names in copyable prompts.
5. Deliver prompts or use available image tools as requested, inspect actual results, and repair specific issues.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Identify location, visible defect and task impact; do not conceal problems with fog, cropping or wording.
- Preserve accepted states and rollback material; merging does not duplicate image acceptance counts.

<!-- contract:review -->
## 7. Review gates

- [ ] Verify medium, subject count, user locks, form/loadout, space, direction, light and materials.
- [ ] Keep necessary people and equipment readable in low light; shared gear does not prove actor identity.
- [ ] Do not invent temporal proof from stills; check timing, end state and sound only for video supplements.
- [ ] Terrain, cover, weapon direction, action cause and reaction, debris, smoke, injuries, and movement routes agree; slow motion has a dramatic reason.

<!-- contract:pass -->
## 8. Pass standard and states

- Report structure/prompt readiness, generation, review and user acceptance separately; ready_for_prompt only means prepared.
- Preserve sourced historical acceptance of the war example and five advisor images; merge checks are not new image acceptance.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- Task-specific visual designs, natural-language prompts, actual images, or visual supplements for approved shots.
- Keep style_module, style_route and qc_contract when needed; ten information categories are internal, not mandatory ten-section output.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Do not rewrite locked stories, take over full screenplay/shot-list production, or override approved assets and directing.
- Do not provide real weapon construction or attack-operation tutorials; still images do not certify engineering, tactics or motion.
- The standalone package contains its runtime knowledge; model tools, accounts and extra permissions are not provided by the Skill.
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

- [`agents/openai.yaml`](../../../skills/war-design/agents/openai.yaml)
- [`SKILL.md`](../../../skills/war-design/SKILL.md)

**References**

- [`references/cinematic-image-direction.md`](../../../skills/war-design/references/cinematic-image-direction.md)
- [`references/combat-visual.md`](../../../skills/war-design/references/combat-visual.md)
- [`references/COMMON-12-SECTION-PROTOCOL.md`](../../../skills/war-design/references/COMMON-12-SECTION-PROTOCOL.md)
- [`references/NEGATIVE-CASE-BOOK.md`](../../../skills/war-design/references/NEGATIVE-CASE-BOOK.md)
- [`references/SOURCE-LEDGER.md`](../../../skills/war-design/references/SOURCE-LEDGER.md)
- [`references/sources.md`](../../../skills/war-design/references/sources.md)
- [`references/squad-cinematography.md`](../../../skills/war-design/references/squad-cinematography.md)
- [`references/story-visual.md`](../../../skills/war-design/references/story-visual.md)
- [`references/visual-design.md`](../../../skills/war-design/references/visual-design.md)
- [`references/visual-review.md`](../../../skills/war-design/references/visual-review.md)
- [`references/war-visual-presets.md`](../../../skills/war-design/references/war-visual-presets.md)

**Distribution notices in new ZIP builds**

New builds attach these files inside the Skill folder without editing its runtime source. Historical release archives are unchanged.

- [`LICENSE`](../../../LICENSE)
