# produce-ai-video — qualified final video production

| Status | Deployed |
|---|---|
| Can deliver alone | A full production and validation contract; with the required host tools and permissions, an actual reviewed final video. |
| Cannot claim alone | Installing the Skill alone does not supply models, credits, rights, editing tools, or a qualified video. |

[Runtime `SKILL.md`](../../../skills/produce-ai-video/SKILL.md) · [Standalone ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/produce-ai-video.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. Purpose

Turn an approved script or passage into a qualified, watchable AI-generated final video through directing, shots, generation, edit, sound, full playback, and repair.

<!-- contract:principles -->
## 2. Design principles

- The final, watchable video is the outcome; prompts, clips, edit projects, and QC reports are intermediate artifacts.
- Preserve locked source facts and review the whole final render, not isolated attractive frames.
- Repair the earliest point where the audience loses trust and distinguish candidate from qualified delivery.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

A full production and validation contract; with the required host tools and permissions, an actual reviewed final video.

**Cannot claim alone:** Installing the Skill alone does not supply models, credits, rights, editing tools, or a qualified video.

<!-- contract:inputs -->
## 4. Inputs

- Current approved script, assets, visual rules, decisions, checkpoints, delivery format, and qualification definition.
- Explicit authority for paid generation, external services, music, voices, publishing, or other consequential actions.
- A choice between autonomous production and user-directed execution when existing storyboards or structures are locked.

<!-- contract:workflow -->
## 5. Workflow

1. Lock source, acceptance, permissions, and mode; interpret the script and make director decisions.
2. Design shot groups and use `ai-storyboard-director` for the downstream shot and prompt contract.
3. Choose a generation route, create genuine motion, edit, build sound, and render the real final file.
4. Watch the whole render at least twice: once for story/emotion, once for technical and continuity defects.
5. Repair blocking failures and deliver with the honest status `qualified`, `candidate`, or `unfinished/needs validation`.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Return to the earliest wrong layer: script/directing, shot design, prompt, source clip, edit, sound, or final render.
- A platform task success, valid duration, or good still frame cannot bypass full-playback review.
- User-locked storyboards remain locked unless revision authority is explicit.

<!-- contract:review -->
## 7. Review gates

- [ ] Story, shot design, spatial and asset continuity, generation quality, edit, sound, and delivery all pass their applicable hard gates.
- [ ] The actual final file opens and has been watched from beginning to end; no hidden replacement file is reviewed instead.
- [ ] Rights, costs, permissions, and unresolved limitations are explicit.

<!-- contract:pass -->
## 8. Pass standard and states

- Only a fully watched render that passes every applicable hard gate may be called a qualified final video.
- Anything missing a key gate remains candidate or unfinished even when files and project artifacts exist.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- An actual playable final video plus its exact status and delivery path.
- Only the necessary supporting artifacts and a concise record of review, repairs, rights, and remaining limits.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Installing this method does not grant video models, paid credits, music rights, voice rights, or publishing authority.
- Never describe a storyboard, prompt, generated clip, edit timeline, or unreviewed render as the finished film.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- Real production requires media-generation tools, editing and audio capabilities, file access, sufficient permissions or budget, and full-playback review. A text-only host can inspect the method but cannot claim a finished video.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/produce-ai-video/agents/openai.yaml)
- [`SKILL.md`](../../../skills/produce-ai-video/SKILL.md)

**References**

- [`references/autonomous-production-workflow.md`](../../../skills/produce-ai-video/references/autonomous-production-workflow.md)
- [`references/qualified-video-acceptance.md`](../../../skills/produce-ai-video/references/qualified-video-acceptance.md)
