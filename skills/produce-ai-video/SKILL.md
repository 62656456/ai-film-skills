---
name: produce-ai-video
description: Produce or revise an actual playable AI video when the user explicitly requests video generation, an actual video test, or a finished film. Interpret the story, preserve locked directing and storyboard decisions, then generate, edit, add authorized sound, review playback, and repair within scope. Creative shot ideas, workflow or Skill testing, storyboards, prompts, and requests for results within those text stages do not activate video production.
---

# Produce AI Video

## Outcome

Deliver the actual video artifact the user requested. A finished-film request needs an assembled film; an explicitly requested single-shot video or video test stays within that scope. Storyboards, prompts and QC reports are supporting artifacts, not proof of video delivery.

## Entry and handoff

Read the latest request in its current stage. “Test”, “show the result”, or a film example does not by itself authorize media generation. Creative shot ideas stay as optional text describing the intended image, story purpose, camera or edit, and tradeoffs. They do not require an account, credits, reference upload or a playable sample. Adopting an idea authorizes only the adoption named by the user, not a subsequent generation step.

Start this workflow only for an actual video request or an already authorized video task. Use its current director plan, storyboard, approved assets and entry/exit states as the handoff. Complete only missing decisions needed for execution; do not rerun every upstream Skill or redesign locked shots. New creative alternatives remain separate suggestions until specifically adopted; do not add them to the production queue.

This package contains its own production storyboard and six-module prompt compiler in `references/storyboard-prompt-compiler.md`. Use it only after the director judgment is complete.

## Choose the execution mode

### Autonomous production mode

Use this mode when the user asks for an actual video or film and delegates the necessary directing and production decisions. A test of Skill instructions or creative thinking alone is not this mode.

- Read the project knowledge, current script, approved assets, visual rules, decisions, and checkpoints.
- Make the director decisions independently.
- Design the shot groups, prompts, production route, generation, selection, edit, sound, review, and repairs.
- Do not push ordinary directing decisions back to the user.
- Ask only when a missing choice materially changes story meaning, spend, permissions, publication, or an already locked structure.

### User-directed execution mode

Use this mode when the user supplies or has repeatedly adjusted a storyboard, timing, shot order, staging, dialogue, or prompt structure.

- Treat the user-locked structure as authoritative.
- Change only the requested scope.
- Do not add shots, remove shots, reorder beats, rewrite dialogue, or replace staging in the name of optimization.
- If a requested result conflicts with the locked structure, identify the exact conflict and its visible consequence before proposing a change.

## Run the autonomous workflow

1. **Lock sources and acceptance.** Identify the unique project, current script version, approved assets, fixed decisions, requested video scope, permissions, cost boundary, and relevant acceptance checks. Reuse verified, unchanged context; a local correction reads the affected material and required continuity, not the whole project again. Separate verified facts, unknowns, assumptions, and conventions.
2. **Interpret the script.** Determine the dramatic event, character objective, power relation, information reveal, physical action, emotional turn, sound cue, entry state, and exit state. Read [autonomous-production-workflow.md](references/autonomous-production-workflow.md) for the auditable decision framework.
3. **Direct before prompting.** Decide what the audience must see and in what order. Build a world-state model for space, subjects, props, light sources, movement axes, and continuity.
4. **Design segments and shots.** Treat a segment as a dramatic sequence and a shot as one uninterrupted viewpoint. Choose continuous staging, cuts or a mixed structure from performance, viewing order and spatial relations; there is no minimum shot count or fixed duration grid. Every cut must change what the audience can understand or experience. A deliberate long take needs no special exemption.
5. **Create and compile the director package.** Produce a `DIRECTOR_SHOT_PACKAGE` containing the segment objective, entry and exit states, world-state lock, shot order, timing, framing, camera, visible action, sound, cut motivation, and continuity handoff. Only after this package is coherent may `references/storyboard-prompt-compiler.md` convert it into the approved five-column storyboard and six-module video prompt.
6. **Choose the production route.** Preserve the director timing and shot design. If one model call cannot reliably render the required internal shots, generate individual shots or smaller clusters and edit them into the designed segment. Never let a model's maximum duration redefine the dramatic timing.
7. **Generate real motion.** Produce actual video material. Reject static-frame motion, keyframe slideshows, or technical previews when the requested deliverable is a finished video.
8. **Select and assemble.** Judge takes by performance, identity, action, continuity, composition, and editability. Cut on motivated action, gaze, occlusion, object, sound, or information change. Add handles where the tool permits; do not concatenate fixed clip durations blindly.
9. **Build sound.** Integrate dialogue, performance breaths, environment, effects, transitions, silence, and music only when authorized. Make sound carry space, action, rhythm, and continuity rather than feeling pasted on.
10. **Watch, repair, and rewatch.** Review the entire film at normal speed for story and rhythm, then inspect continuity, artifacts and sound. Keep the last checked assembly before changing it. Fix the earliest responsible defect within the authorized generation/cost boundary, recheck the affected material and watch the final assembly. If a repair fails, restore the previous checked assembly; service failure, exhausted budget or missing evidence stops the loop with an honest incomplete result. Use [qualified-video-acceptance.md](references/qualified-video-acceptance.md).
11. **Deliver honestly.** Return the playable final video, its duration and format, the validation state, and any visible residual risk. If full-playback review or a hard gate is unavailable, report `未完成/待验证`; never call the result qualified.

## Enforce hard rules

- Do not start from prompt formatting. Start from what the audience must see.
- Do not equate a script paragraph, generation segment, and shot.
- Do not equate continuity with a fixed camera. Keep the world state fixed while recalculating screen projection after every camera change.
- Carry the selected audience information, environment activity and sound through compilation. Places keep operating during protagonist action; deliberate quiet and stable light remain valid. Do not add weather, crowds or plot sounds during compilation to fill fields.
- Do not count repeated crops, cosmetic zooms, or unchanged viewpoints as new effective shots.
- Do not declare success because files exist, durations match, prompts are complete, or individual clips pass technical checks.
- Do not deliver autonomous work that resembles independent single-shot demonstrations joined together.
- Do not claim a qualified final video without actually viewing the complete rendered file.

## Output Contract

Keep internal work concise and production-facing. The user-facing completion must lead with the playable video and one of these states:

- `合格成片`: every hard gate passed after full playback.
- `候选成片`: playable, but one or more visible quality judgments still await user review.
- `未完成/待验证`: generation, assembly, full playback, or a hard gate is incomplete.

Never substitute text, stills or a QC checklist for a requested video. A test clip fulfills an explicitly requested video-test scope; it does not prove an entire film or Skill has passed user acceptance. Explain the verified scope, and preserve user approval as a separate decision.
