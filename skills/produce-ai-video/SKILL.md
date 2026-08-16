---
name: produce-ai-video
description: Turn an approved script, scene, or story passage into a qualified, watchable AI-generated final video through autonomous script interpretation, directing, multi-shot storyboard design, prompt production, generation, editing, sound, full-playback review, and repair. Use when the user asks Codex to autonomously make, automatically produce, test its ability with, or directly deliver an actual video or finished film rather than only a storyboard or prompt. Preserve user-locked storyboards and structures when the user is directly directing or requests a scoped revision.
---

# Produce AI Video

## Outcome

Deliver an actual qualified video. Treat storyboards, prompts, generated clips, edit projects, and QC reports as intermediate artifacts, never as the final result.

Use `ai-storyboard-director` only after the director judgment is complete. Its six-module prompt structure and Digital-10 information core are the downstream encoding contract; do not modify or replace that Skill.

## Choose the execution mode

### Autonomous production mode

Use this mode when the user asks Codex to create autonomously, automatically make the video, test its ability, or deliver a finished film from a script.

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

1. **Lock sources and acceptance.** Identify the unique project, current script version, approved assets, fixed decisions, delivery format, permissions, cost boundary, and definition of a qualified video. Separate verified facts, unknowns, assumptions, and conventions.
2. **Interpret the script.** Determine the dramatic event, character objective, power relation, information reveal, physical action, emotional turn, sound cue, entry state, and exit state. Read [autonomous-production-workflow.md](references/autonomous-production-workflow.md) for the auditable decision framework.
3. **Direct before prompting.** Decide what the audience must see and in what order. Build a world-state model for space, subjects, props, light sources, movement axes, and continuity.
4. **Design segments and shots.** Treat a segment as a short dramatic sequence and a shot as one uninterrupted viewpoint. In autonomous mode, design at least 7–8 effective, non-equally timed shots per segment unless the user explicitly requests a long take. Every cut must add information, change power, clarify action, reveal a reaction, or hand off the next beat.
5. **Create the director handoff.** Produce a `DIRECTOR_SHOT_PACKAGE` containing the segment objective, entry and exit states, world-state lock, shot order, timing, framing, camera, visible action, sound, cut motivation, and continuity handoff. Only after this package is coherent may `ai-storyboard-director` convert it into the approved human-readable storyboard and six-module video prompt.
6. **Choose the production route.** Preserve the director timing and shot design. If one model call cannot reliably render the required internal shots, generate individual shots or smaller clusters and edit them into the designed segment. Never let a model's maximum duration redefine the dramatic timing.
7. **Generate real motion.** Produce actual video material. Reject static-frame motion, keyframe slideshows, or technical previews when the requested deliverable is a finished video.
8. **Select and assemble.** Judge takes by performance, identity, action, continuity, composition, and editability. Cut on motivated action, gaze, occlusion, object, sound, or information change. Add handles where the tool permits; do not concatenate fixed clip durations blindly.
9. **Build sound.** Integrate dialogue, performance breaths, environment, effects, transitions, silence, and music only when authorized. Make sound carry space, action, rhythm, and continuity rather than feeling pasted on.
10. **Watch, repair, and rewatch.** Review the entire film at normal speed for story and rhythm, then again for continuity, artifacts, and sound. Fix the first audience-rejecting defect and repeat until all hard gates in [qualified-video-acceptance.md](references/qualified-video-acceptance.md) pass.
11. **Deliver honestly.** Return the playable final video, its duration and format, the validation state, and any visible residual risk. If full-playback review or a hard gate is unavailable, report `未完成/待验证`; never call the result qualified.

## Enforce hard rules

- Do not start from prompt formatting. Start from what the audience must see.
- Do not equate a script paragraph, generation segment, and shot.
- Do not equate continuity with a fixed camera. Keep the world state fixed while recalculating screen projection after every camera change.
- Do not count repeated crops, cosmetic zooms, or unchanged viewpoints as new effective shots.
- Do not declare success because files exist, durations match, prompts are complete, or individual clips pass technical checks.
- Do not deliver autonomous work that resembles independent single-shot demonstrations joined together.
- Do not claim a qualified final video without actually viewing the complete rendered file.

## Output Contract

Keep internal work concise and production-facing. The user-facing completion must lead with the playable video and one of these states:

- `合格成片`: every hard gate passed after full playback.
- `候选成片`: playable, but one or more visible quality judgments still await user review.
- `未完成/待验证`: generation, assembly, full playback, or a hard gate is incomplete.

Never substitute a storyboard, prompt document, still gallery, test clip, or QC checklist for the final video.
