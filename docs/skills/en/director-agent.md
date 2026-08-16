# director-agent — script and directing design

| Status | Deployed; long-term practice evidence remains separate |
|---|---|
| Can deliver alone | A script, replacement passage, diagnosis, director treatment, workbench, or pre-storyboard directing draft. |
| Cannot claim alone | It does not by itself produce a full production storyboard, generated media, or proof of user acceptance. |

[Runtime `SKILL.md`](../../../skills/director-agent/SKILL.md) · [Standalone ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/director-agent.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. Purpose

Create, revise, or diagnose scripts and make the directing decisions that must exist before full storyboard production.

<!-- contract:principles -->
## 2. Design principles

- Tell a clear story through character action and causality before using state engines, checklists, or visual polish.
- Attach every directing decision to audience effect, story function, actor action, or a physical image.
- An independent cold read tests the actual screenplay; it does not replace writing or guarantee taste.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

A script, replacement passage, diagnosis, director treatment, workbench, or pre-storyboard directing draft.

**Cannot claim alone:** It does not by itself produce a full production storyboard, generated media, or proof of user acceptance.

<!-- contract:inputs -->
## 4. Inputs

- A screenplay, story, outline, dialogue-only passage, novel passage, or abstract material plus the requested mode.
- Locked facts, format, length, audience, production constraints, and any approved or forbidden decisions.
- Unknown story facts remain marked as assumptions instead of being silently invented.

<!-- contract:workflow -->
## 5. Workflow

1. Load only the relevant writing and directing references.
2. Read the material in story, character, and directing layers; verify stimulus, objective, strategy, state change, and dialogue response.
3. Choose creation, diagnosis, treatment, workbench, or pre-storyboard mode.
4. Build the visual idea, actor actions, sound, time, editing, theme, and subtext from the causal reading.
5. Cold-read the actual output, repair the earliest upstream failure, and deliver the requested readable artifact first.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- If causality, character knowledge, or scene purpose fails, return to the earliest broken scene before polishing dialogue or visuals.
- If the request actually needs production storyboard detail, hand the approved directing decisions to `ai-storyboard-director` instead of stretching this module beyond its contract.
- Cold-read PASS is a screenplay review state, not proof that the user likes the work.

<!-- contract:review -->
## 7. Review gates

- [ ] Every consequential action and line has a prior stimulus, an objective, a tactic, a listener effect, and a state change.
- [ ] The protagonist does not ignore an obvious safer or easier option without a demonstrated cost or blockage.
- [ ] Scenes hand a changed state to the next scene; setup and payoff change meaning, power, possibility, choice, or result.

<!-- contract:pass -->
## 8. Pass standard and states

- The requested script, diagnosis, treatment, workbench, or pre-storyboard draft is complete enough to use without hidden rationale.
- The earliest blocking story failures are repaired or explicitly left as unresolved boundaries.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- A readable screenplay or replacement passage, not merely an outline when full writing was requested.
- Director treatment, workbench package, diagnosis, or pre-storyboard directing draft when that mode is requested.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Do not invent film history, citations, director methods, or missing story facts.
- Do not describe director analysis as full storyboard production or a cold read as user acceptance.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- Text-only creation and diagnosis work in any host that can read the complete folder; current or source-sensitive claims require web access and citation capability.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/director-agent/agents/openai.yaml)
- [`SKILL.md`](../../../skills/director-agent/SKILL.md)

**References**

- [`references/anti-laziness-contract.md`](../../../skills/director-agent/references/anti-laziness-contract.md)
- [`references/director-thinking-spine.md`](../../../skills/director-agent/references/director-thinking-spine.md)
- [`references/director-workbench-protocol.md`](../../../skills/director-agent/references/director-workbench-protocol.md)
- [`references/github-project-watchlist.md`](../../../skills/director-agent/references/github-project-watchlist.md)
- [`references/local-knowledge-map.md`](../../../skills/director-agent/references/local-knowledge-map.md)
- [`references/research-update-protocol.md`](../../../skills/director-agent/references/research-update-protocol.md)
- [`references/screenplay-cold-read-protocol.md`](../../../skills/director-agent/references/screenplay-cold-read-protocol.md)
- [`references/screenplay-exemplar-benchmarks.md`](../../../skills/director-agent/references/screenplay-exemplar-benchmarks.md)
- [`references/screenplay-state-engine.md`](../../../skills/director-agent/references/screenplay-state-engine.md)
- [`references/screenplay-writing-core.md`](../../../skills/director-agent/references/screenplay-writing-core.md)
- [`references/verified-director-logic.md`](../../../skills/director-agent/references/verified-director-logic.md)
