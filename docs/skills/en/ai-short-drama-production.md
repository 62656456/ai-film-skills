# ai-short-drama-production — short-drama control contracts

| Status | Packaged; not deployed |
|---|---|
| Can deliver alone | Production-control orchestration and gap auditing for existing decisions, including any one of its six control contracts. |
| Cannot claim alone | It does not require a companion package: its director, asset, genre, prompt, and QC rules are rewritten as local short-drama modules, while actual image/video generation still needs the host's media tools and permissions. |

[Runtime `SKILL.md`](../../../skills/ai-short-drama-production/SKILL.md) · [v1.3.0 historical ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/ai-short-drama-production.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

Historical v1.3.0 snapshot; differs from current source where updated.

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

**Cannot claim alone:** It does not require a companion package: its director, asset, genre, prompt, and QC rules are rewritten as local short-drama modules, while actual image/video generation still needs the host's media tools and permissions.

<!-- contract:inputs -->
## 4. Inputs

- Audience, duration, script form, character objective and obstacle, scenes, main genre, target platform, and existing assets or sketches.
- Approved director decisions and asset versions when available; missing values are `pending`, inferred values are `assumed`.
- The specific control gap: beat, asset registry, blocking, lighting, action, sketch translation, or pre-generation QC.

<!-- contract:workflow -->
## 5. Workflow

1. Obtain current director and beat decisions; do not recreate them with a generic formula.
2. Preserve approved assets; label unresolved assets as candidates for text design, and require the applicable asset review before actual generation.
3. Create blocking, lighting, action, and sketch-to-shot control contracts only where needed.
4. Compile a five-column storyboard and one six-module master prompt for the requested total duration; preserve locked formats, cuts, camera paths, dialogue and timing.
5. Distinguish coherent candidate text (`ready_for_prompt`) from approved assets and verified execution conditions (`ready_for_generation`); inspect actual media after generation.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Story, concept, beat, or dialogue returns to the directing/writing layer; asset drift returns to asset design.
- Space, axis, or action returns to storyboard control; field compilation returns to prompt engineering; actual-image mismatch returns to QC.
- The module routes the failure; it never substitutes 'generate again' for diagnosis.

<!-- contract:review -->
## 7. Review gates

- [ ] Hook, objective, obstacle, information gap, power turn, cost, and end hook are visible rather than adjective labels.
- [ ] Approved and candidate assets remain distinct; blocking explains world space and each camera projection; light has a physical source and action has start, path, end and reaction.
- [ ] Cuts or continuous takes are explicit, locked structure is preserved, dialogue fits its time window, and the final prompt retains selected camera design and end-state continuity.

<!-- contract:pass -->
## 8. Pass standard and states

- The requested artifact is complete; timing, actions, camera and user locks can be reconstructed from its final text, with ten information categories covered inside six modules.
- Text readiness, generation readiness, actual video review and user acceptance are separate states.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- A narrative beat contract, asset registry, blocking map, lighting plan, action ledger, or sketch-to-shot brief as needed.
- The requested control contract, five-column storyboard or complete six-module prompt; internal IDs stay in records and natural names appear in user-facing prompts.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- It can organize approved decisions or audit missing controls by itself; it does not copy every directing, asset, genre, generation, or QC capability into one module.
- This package includes a self-contained handoff aligned with the 5.6 storyboard format, without importing its persistence engine. Source alignment does not establish deployment or actual-video acceptance.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- Text design uses this package's own rules and handoff. Actual generation, playback review and editing require the host's media capabilities, applicable approvals and checked platform limits.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/ai-short-drama-production/agents/openai.yaml)
- [`SKILL.md`](../../../skills/ai-short-drama-production/SKILL.md)

**References**

- [`references/control-contracts.md`](../../../skills/ai-short-drama-production/references/control-contracts.md)
- [`references/independent-production-core.md`](../../../skills/ai-short-drama-production/references/independent-production-core.md)
- [`references/production-handoff.md`](../../../skills/ai-short-drama-production/references/production-handoff.md)
- [`references/SOURCE-LEDGER.md`](../../../skills/ai-short-drama-production/references/SOURCE-LEDGER.md)

**Distribution notices in new ZIP builds**

New builds attach these files inside the Skill folder without editing its runtime source. Historical release archives are unchanged.

- [`LICENSE`](../../../LICENSE)
