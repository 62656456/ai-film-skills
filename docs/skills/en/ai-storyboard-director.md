# ai-storyboard-director — script to shots and prompts

| Status | Deployed; 5.4.2 candidate over the 5.4.1 continuity contract |
|---|---|
| Can deliver alone | A complete storyboard and copy-ready prompt package for an existing approved script. |
| Cannot claim alone | It does not rewrite the script, directly generate the video, or prove platform success. |

[Runtime `SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md) · [Standalone ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-storyboard-director.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

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
3. Build shot sentences, varied coverage, and phased camera events that visibly carry the beat.
4. Write the human-readable storyboard and compile Digital-10 information into the six visible prompt modules.
5. Run the twelve-item completion gate and return only the requested creative artifact plus genuine unresolved limits.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Story or director failures return upstream; spatial, blocking, camera, timing, or prompt-encoding failures return to their responsible design stage.
- Version rollback is distinct from creative rework and exists only for the documented 5.4.1 hash-verified snapshot when explicitly requested.
- A continuity failure is repaired from fixed world coordinates, never by moving the room to preserve screen-left labels.

<!-- contract:review -->
## 7. Review gates

- [ ] The shots preserve script facts, character purpose, action results, dialogue, and user-locked order.
- [ ] Camera, blocking, depth, focus, movement, and editing form shot sentences rather than rotate terminology.
- [ ] Duration closes exactly; dialogue timing, world projection, off-frame subjects, light direction, props, and end states remain continuous.

<!-- contract:pass -->
## 8. Pass standard and states

- All twelve completion checks pass and the storyboard is readable without engineering-only fields.
- Prompt modules contain all ten information categories, but this still does not prove that a platform generated a successful video.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- A human-readable multi-shot storyboard with time, shot/camera, visible action, dialogue, and sound.
- Copy-ready prompts using the required six-module outer structure and Digital-10 information core.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Do not rewrite locked story facts or dialogue and do not invent platform capability or generation success.
- Storyboard completion is not a finished video or user-approved visual result.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- The complete folder is usable for text storyboard design in any reading host; file access helps with references and hash-verified rollback, while actual generation requires separate media tools and permissions.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/ai-storyboard-director/agents/openai.yaml)
- [`SKILL.md`](../../../skills/ai-storyboard-director/SKILL.md)

**References**

- [`references/production-contract.md`](../../../skills/ai-storyboard-director/references/production-contract.md)
- [`references/shot-design-engine.md`](../../../skills/ai-storyboard-director/references/shot-design-engine.md)

**Version and rollback evidence**

- [`versions/5.4.1/production-contract.snapshot.md`](../../../skills/ai-storyboard-director/versions/5.4.1/production-contract.snapshot.md)
- [`versions/5.4.1/rollback-manifest.json`](../../../skills/ai-storyboard-director/versions/5.4.1/rollback-manifest.json)
- [`versions/5.4.1/SKILL.snapshot.md`](../../../skills/ai-storyboard-director/versions/5.4.1/SKILL.snapshot.md)
