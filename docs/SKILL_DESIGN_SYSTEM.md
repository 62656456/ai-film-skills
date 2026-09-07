# How every Skill is designed

A Skill owns a bounded result and the evidence needed to judge it. The [20 module guides](skills/INDEX.md) explain the current source in English and Simplified Chinese; each links its exact runtime files. The [full workflow](WORKFLOW.md) explains how those results can be handed to the next stage without loading every Skill at once.

## The design contract

| Field | Required answer |
|---|---|
| Purpose | What visible problem is being solved? |
| Inputs | Which facts, materials, constraints and approvals are actually available? |
| Workflow | What causal order produces the result? |
| Return path | Which earlier decision changes if the result fails? |
| Review | What must be read, viewed, heard or run? |
| Pass evidence | What observable output supports the stated completion level? |
| Handoff | What can the next person or Skill use without hidden context? |
| Boundary | What remains unknown, unsupported or outside the request? |

Start from the actual requested outcome and available evidence. Existing examples, templates and named methods are candidate inputs, not automatic conclusions. Preserve user-locked facts and differentiate a creative proposal from an approved decision.

## Shared operating loop

<img src="assets/review-loop.svg" width="100%" alt="Input, visible design, review, directed return and evidence-backed handoff" />

```text
current request and material
  -> one primary Skill for the requested result
  -> establish facts, open decisions and constraints
  -> produce the visible artifact at the requested scope
  -> inspect the applicable module gates
       fail -> repair the earliest responsible decision
       pass -> record evidence and deliver the named handoff
  -> use another Skill only for a different necessary outcome
```

## Image relationships before presets

The visual and asset packages now carry their own `cinematic-image-direction.md`. It derives the viewing proposition, attention, subject/background separation, source-based light and reflection, scale, material differences and detail hierarchy together. This is an authored synthesis of supplied-image analysis, not a reconstruction of another creator's hidden Skill or exact camera settings.

- Choose photographic, 3D-animation or 2D/illustration imaging before selecting negative constraints.
- Derive lens, light, color, scale and focus from the current image; do not require golden hour, complementary colors, foreground people or shallow focus everywhere.
- Keep requested new surfaces, real plastic and designed emission. Wear must follow use rather than a blanket quality filter.
- Match delivery scope: a single prompt or image does not automatically become a multi-view sheet, a video timeline or a complete film.
- Read actual pixels for an image verdict and actual motion for video; text consistency remains text evidence.

The [14-image showcase](showcase/manifest.json) records accepted outcomes. It is not a same-prompt comparison against the old rules and does not prove a general success rate.

## Storyboard 5.6: persistence without replacing judgment

In a supplied project directory, 5.6 saves the source identity, director intent, selected shots and scene entry/exit states, then restores the current context and required knowledge. It uses revision/hash checks and protects accepted facts from silent replacement. The records live with the work and do not replace the work's overall project state.

The helper checks recorded fields, timing, inheritance and explicit geometry. It does not decide whether a shot is powerful, verify arbitrary 3D geometry or make the native chat route impossible to bypass. Prompt formatting must preserve the selected camera design; a valid JSON record cannot compensate for a weak or changed shot.

Without a supplied project directory, a simple shot consultation can still deliver text. It must not claim that it saved or restored a project.

## Directed return

| Visible failure | Return to | Preserve |
|---|---|---|
| Missing decisive input | Scope and source interpretation | Unaffected known facts |
| Causality, knowledge or dialogue fails | Earliest broken story decision | Approved scope and unaffected scenes |
| Camera, blocking or continuity fails | Responsible shot and world-state decision | Story event and character purpose |
| Image feels generic or unreadable | Attention, framing, light, material or detail relationship | Locked identity and intended function |
| Model cannot execute the plan | Actual production route | Approved dramatic intent and required state |
| Whitebox action is unsupported | Capability boundary and short action gate | Already verified basic preview |
| Rights or permission is absent | Applicable source/publication boundary | Private material and existing approved output |
| Final result cannot be inspected | Delivery path or playable export | The work itself |

A return names the failed relationship and a concrete correction. It does not use a new generation attempt as a substitute for diagnosis or restart unrelated stages.

## Evidence states

1. **Structurally valid:** the package and its local resources are present.
2. **Loaded or executed:** the actual host read the instructions or ran the helper.
3. **Task evidence:** a script, image, preview, report or other result was produced and inspected.
4. **User-accepted result:** the user explicitly accepted the named visible output.
5. **Practice-validated Skill:** the maintainer has accepted evidence across three different real tasks.

These states attach to their exact scope. A user-accepted image is not a complete-film acceptance; several examples from one run do not automatically prove three independent tasks. An experimental package may have accepted examples while remaining opt-in. Current source, Git push, local builds and published Release assets are also separate states.

## Maintaining the documentation

`docs/skill-contracts.json` contains the reviewed bilingual explanations and distribution links. `scripts/generate_skill_guides.py` generates 40 guides and an index from that registry plus the actual packaged resources. Edit the registry or runtime truth, regenerate, and validate; do not hand-edit derived pages.

A useful maintenance change keeps the runtime and guide in agreement, keeps dependencies inside the standalone package, preserves approved behavior, and identifies a concrete rollback or repair route. Read [Publication scope](../PUBLICATION_SCOPE.md), [Architecture](ARCHITECTURE.md) and [Contributing](../CONTRIBUTING.md).
