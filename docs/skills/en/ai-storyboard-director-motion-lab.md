# ai-storyboard-director-motion-lab — 5.4.3 complex-motion test line

| Status | Testing; 5.4.3 experimental candidate; explicit invocation only |
|---|---|
| Can deliver alone | An explicitly requested 5.4.3 test storyboard, input-duty decision, and six-module prompt package for complex camera motion. |
| Cannot claim alone | It is not the default storyboard Skill and cannot claim formal promotion, stable model generation, finished-video quality, or user acceptance. |

[Runtime `SKILL.md`](../../../experimental/ai-storyboard-director-motion-lab/SKILL.md) · [Standalone ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-storyboard-director-motion-lab.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. Purpose

Test whether complex camera paths, visual transformations, motion-reference video, and 3D previs can add necessary visible information without replacing the formal 5.4.2 storyboard contract.

<!-- contract:principles -->
## 2. Design principles

- Story causality, character purpose, blocking, and spatial action come before shot terminology.
- Blocking and camera are designed as one event; a complex move needs a visible start, trigger, phases, and endpoint.
- World state stays fixed while each camera position recomputes the frame projection.
- Compare fixed, simple, and complex camera solutions; use the complex route only when it adds a visible story, spatial, temporal, or subjective result that the simpler routes cannot provide.
- Text, reference video, 3D previs, images, and keyframes each keep an explicit responsibility boundary and cannot silently overwrite story or asset truth.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

An explicitly requested 5.4.3 test storyboard, input-duty decision, and six-module prompt package for complex camera motion.

**Cannot claim alone:** It is not the default storyboard Skill and cannot claim formal promotion, stable model generation, finished-video quality, or user acceptance.

<!-- contract:inputs -->
## 4. Inputs

- An approved script or passage with complete story facts, dialogue, and the user's locked shot decisions.
- Total duration, aspect ratio, platform when known, approved assets, and entering world state.
- Any unresolved director decision must be identified instead of hidden inside shot jargon.
- An explicit request to test `$ai-storyboard-director-motion-lab`; the words 'complex camera movement' alone do not authorize the experimental route.
- Any motion-reference video or 3D previs must state what motion or topology it controls and what characters, locations, brands, materials, and story facts it does not contribute.

<!-- contract:workflow -->
## 5. Workflow

1. Read causality, character goals, relationships, emotion, space, action, and continuity.
2. Fix the world state and design blocking before selecting camera projection.
3. Build shot sentences, varied coverage, and phased camera events that visibly carry the beat.
4. Write the human-readable storyboard and compile Digital-10 information into the six visible prompt modules.
5. Run the twelve-item completion gate and return only the requested creative artifact plus genuine unresolved limits.
6. Label the output as a 5.4.3 test that does not change formal 5.4.2, decide input responsibilities, and split or request previs when the path cannot be described reliably.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Story or director failures return upstream; spatial, blocking, camera, timing, or prompt-encoding failures return to their responsible design stage.
- Version rollback is distinct from creative rework and exists only for the documented 5.4.1 hash-verified snapshot when explicitly requested.
- A continuity failure is repaired from fixed world coordinates, never by moving the room to preserve screen-left labels.
- If complex motion adds only spectacle, return to a fixed or simple camera plan; if topology or occlusion cannot be proven, return to 3D previs instead of inventing continuity.

<!-- contract:review -->
## 7. Review gates

- [ ] The shots preserve script facts, character purpose, action results, dialogue, and user-locked order.
- [ ] Camera, blocking, depth, focus, movement, and editing form shot sentences rather than rotate terminology.
- [ ] Duration closes exactly; dialogue timing, world projection, off-frame subjects, light direction, props, and end states remain continuous.
- [ ] Every motion phase has a visible trigger, path, focus or occlusion handoff, speed change, new information, endpoint, and a stated reason the simpler alternative is insufficient.

<!-- contract:pass -->
## 8. Pass standard and states

- All twelve completion checks pass and the storyboard is readable without engineering-only fields.
- Prompt modules contain all ten information categories, but this still does not prove that a platform generated a successful video.
- A structural or text-behavior pass keeps the module in Testing; only explicit later user approval can start a separate promotion decision.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- A human-readable multi-shot storyboard with time, shot/camera, visible action, dialogue, and sound.
- Copy-ready prompts using the required six-module outer structure and Digital-10 information core.
- The output begins with `5.4.3 experimental candidate | this test only | formal 5.4.2 unchanged` and includes the readable five-column storyboard plus complete six-module prompts.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Do not rewrite locked story facts or dialogue and do not invent platform capability or generation success.
- Storyboard completion is not a finished video or user-approved visual result.
- The package keeps `allow_implicit_invocation: false`, stays outside the complete-studio ZIP, and requires `--experimental` for local installation.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- The complete folder is usable for text storyboard design in any reading host; file access helps with references and hash-verified rollback, while actual generation requires separate media tools and permissions.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../experimental/ai-storyboard-director-motion-lab/agents/openai.yaml)
- [`SKILL.md`](../../../experimental/ai-storyboard-director-motion-lab/SKILL.md)

**References**

- [`references/advanced-motion-engine.md`](../../../experimental/ai-storyboard-director-motion-lab/references/advanced-motion-engine.md)
- [`references/formal-production-contract.md`](../../../experimental/ai-storyboard-director-motion-lab/references/formal-production-contract.md)
- [`references/input-duty-matrix.md`](../../../experimental/ai-storyboard-director-motion-lab/references/input-duty-matrix.md)
