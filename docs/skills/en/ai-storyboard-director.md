# ai-storyboard-director — script to shots and prompts

| Status | Current source 5.6; selected for daily use; v1.3.0 ZIP preserves 5.4.4 |
|---|---|
| Can deliver alone | A complete storyboard and copy-ready prompt package for an existing approved script. |
| Cannot claim alone | It does not rewrite the script, directly generate the video, or prove platform success. |

[Runtime `SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md) · [v1.3.0 historical ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/ai-storyboard-director.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

Historical v1.3.0 ZIP contains 5.4.4, not current source 5.6.

<!-- contract:purpose -->
## 1. Purpose

Turn an approved script into human-readable multi-shot design and production prompts while preserving causality, blocking, timing, and world-space continuity.

<!-- contract:principles -->
## 2. Design principles

- Story causality, character purpose, blocking, and spatial action come before shot terminology.
- Blocking and camera are designed as one event; a complex move needs a visible start, trigger, phases, and endpoint.
- World state stays fixed while each camera position recomputes the frame projection.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

A complete storyboard and copy-ready prompt package for an existing approved script.

**Cannot claim alone:** It does not rewrite the script, directly generate the video, or prove platform success.

<!-- contract:inputs -->
## 4. Inputs

- An approved script or passage with complete story facts, dialogue, and the user's locked shot decisions.
- Total duration, aspect ratio, platform when known, approved assets, and entering world state.
- Any unresolved director decision must be identified instead of hidden inside shot jargon.

<!-- contract:workflow -->
## 5. Workflow

1. Read causality, character goals, relationships, emotion, space, action, and continuity.
2. Fix the world state and design blocking before selecting camera projection.
3. In an explicitly identified project, read the actual design-memory context and required knowledge, save the selected intent/shots/states with revision and hash checks, and read back the result.
4. Build shot sentences, varied coverage, and phased camera events that visibly carry the beat.
5. Write the human-readable storyboard and compile Digital-10 information into the six visible prompt modules.
6. Run the current package completion gates and reverse-check that prompt formatting preserved the selected camera design; return the requested creative artifact and actual limits.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Story or director failures return upstream; spatial, blocking, camera, timing, or prompt-encoding failures return to their responsible design stage.
- Package maintenance is distinct from creative rework; the shared ZIP contains only the current self-contained runtime and no historical runtime dependency.
- A continuity failure is repaired from fixed world coordinates, never by moving the room to preserve screen-left labels.

<!-- contract:review -->
## 7. Review gates

- [ ] The shots preserve script facts, character purpose, action results, dialogue, and user-locked order.
- [ ] Camera, blocking, depth, focus, movement, and editing form shot sentences rather than rotate terminology.
- [ ] Duration closes exactly; dialogue timing, world projection, off-frame subjects, light direction, props, and end states remain continuous.

<!-- contract:pass -->
## 8. Pass standard and states

- The current package completion gates pass and the storyboard is readable without engineering-only fields.
- Prompt modules contain all ten information categories, but this still does not prove that a platform generated a successful video.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- A five-column storyboard: time, framing/angle, camera, visible action, and dialogue/sound.
- Copy-ready prompts using the required six-module outer structure and Digital-10 information core.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Do not rewrite locked story facts or dialogue and do not invent platform capability or generation success.
- Storyboard completion is not a finished video or user-approved visual result.
- The 5.6 helper checks recorded state, timing and explicit geometry; it does not judge aesthetics, prove image/video semantics, or force every chat entry to use it. A text-only question without a project does not invent persistence.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- Text storyboard work needs the complete folder. Project save/recovery additionally requires authorized file access and the bundled Python standard-library helper. Media execution needs separate model/tool permissions.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/ai-storyboard-director/agents/openai.yaml)
- [`SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md)

**References**

- [`references/cinematography-design-engine.md`](../../../skills/ai-storyboard-director/references/cinematography-design-engine.md)
- [`references/delivery-mode-guard.md`](../../../skills/ai-storyboard-director/references/delivery-mode-guard.md)
- [`references/design-memory-protocol.md`](../../../skills/ai-storyboard-director/references/design-memory-protocol.md)
- [`references/framing-and-axis.md`](../../../skills/ai-storyboard-director/references/framing-and-axis.md)
- [`references/production-contract.md`](../../../skills/ai-storyboard-director/references/production-contract.md)
- [`references/shot-design-engine.md`](../../../skills/ai-storyboard-director/references/shot-design-engine.md)

**Deterministic helpers**

- [`scripts/design_memory.py`](../../../skills/ai-storyboard-director/scripts/design_memory.py)

**Distribution notices in new ZIP builds**

New builds attach these files inside the Skill folder without editing its runtime source. Historical release archives are unchanged.

- [`LICENSE`](../../../LICENSE)
