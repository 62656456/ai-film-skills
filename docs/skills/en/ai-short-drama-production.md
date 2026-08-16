# ai-short-drama-production — short-drama control contracts

| Status | Packaged; not deployed |
|---|---|
| Can deliver alone | Production-control orchestration and gap auditing for existing decisions, including any one of its six control contracts. |
| Cannot claim alone | It does not duplicate all director, asset, genre, generation, and QC abilities in one folder. |

[Runtime `SKILL.md`](../../../skills/ai-short-drama-production/SKILL.md) · [Standalone ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-short-drama-production.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. Purpose

Turn approved creative decisions into traceable beat, asset, blocking, lighting, action, sketch, prompt, and QC control contracts for AI short-drama production.

<!-- contract:principles -->
## 2. Design principles

- This is a control-contract layer that connects approved directing, assets, visual language, shots, prompts, and QC without replacing their specialist modules.
- Every assumption, version, blocking map, lighting source, action state, and end frame remains traceable.
- Actual image QC decides readiness; another blind generation attempt does not.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

Production-control orchestration and gap auditing for existing decisions, including any one of its six control contracts.

**Cannot claim alone:** It does not duplicate all director, asset, genre, generation, and QC abilities in one folder.

<!-- contract:inputs -->
## 4. Inputs

- Audience, duration, script form, character objective and obstacle, scenes, main genre, target platform, and existing assets or sketches.
- Approved director decisions and asset versions when available; missing values are `pending`, inferred values are `assumed`.
- The specific control gap: beat, asset registry, blocking, lighting, action, sketch translation, or pre-generation QC.

<!-- contract:workflow -->
## 5. Workflow

1. Obtain current director and beat decisions; do not recreate them with a generic formula.
2. Build or reference human-approved Cxx/Sxx/Pxx assets and their versions.
3. Create blocking, lighting, action, and sketch-to-shot control contracts only where needed.
4. Compile contracts into one continuous-camera AG-CLIP with bounded action density and a usable end state.
5. Review actual images and emit `ready_for_prompt` only when all eight pre-generation gates pass.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Story, concept, beat, or dialogue returns to the directing/writing layer; asset drift returns to asset design.
- Space, axis, or action returns to storyboard control; field compilation returns to prompt engineering; actual-image mismatch returns to QC.
- The module routes the failure; it never substitutes 'generate again' for diagnosis.

<!-- contract:review -->
## 7. Review gates

- [ ] Hook, objective, obstacle, information gap, power turn, cost, and end hook are visible rather than adjective labels.
- [ ] Every asset version is human-reviewed; blocking explains people, props, camera and axis; lighting has visible sources; action has start, path, end and reaction.
- [ ] Each clip has no hidden hard cut, respects dialogue timing and action density, and ends in a continuous next-shot state.

<!-- contract:pass -->
## 8. Pass standard and states

- All eight `ready_for_prompt` conditions pass with traceable contract IDs and actual-image review where required.
- This state means the controlled task is ready for prompt production; it is not a finished clip or film.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- A narrative beat contract, asset registry, blocking map, lighting plan, action ledger, or sketch-to-shot brief as needed.
- A traceable `ready_for_prompt` package or a responsibility-specific rework record.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- It can organize approved decisions or audit missing controls by itself; it does not copy every directing, asset, genre, generation, or QC capability into one module.
- From-zero end-to-end production still needs the relevant specialist Skills and host tools.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- Contract design is text/file based. Full orchestration benefits from the companion specialist Skills, while actual image review and generation require media tools and permissions.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/ai-short-drama-production/agents/openai.yaml)
- [`SKILL.md`](../../../skills/ai-short-drama-production/SKILL.md)

**References**

- [`references/control-contracts.md`](../../../skills/ai-short-drama-production/references/control-contracts.md)
- [`references/SOURCE-LEDGER.md`](../../../skills/ai-short-drama-production/references/SOURCE-LEDGER.md)
