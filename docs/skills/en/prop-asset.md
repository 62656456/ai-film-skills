# prop-asset — prop identity and state contract

| Status | Deployed |
|---|---|
| Can deliver alone | A prop reference task, interaction/state views, locked handling rules, negative constraints, and JSON contract. |
| Cannot claim alone | It does not choreograph the full scene or prove correct handling until actual reference and shot images are reviewed. |

[Runtime `SKILL.md`](../../../skills/prop-asset/SKILL.md) · [Standalone ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/prop-asset.zip) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

<!-- contract:purpose -->
## 1. Purpose

Define a prop's identity, scale, materials, usable faces, interfaces, holder, orientation, wear, operation, and state transitions.

<!-- contract:principles -->
## 2. Design principles

- Establish an auditable, versioned asset identity before storyboard or video production.
- Platform adaptation may change syntax, never approved `locked_features` or state history.
- A static asset contract separates identity, allowed state changes, materials, geometry, lighting, and downstream references.
- A prop is tracked by usable faces, holder, orientation, open/closed or damaged state, and physical contact—not by name alone.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

A prop reference task, interaction/state views, locked handling rules, negative constraints, and JSON contract.

**Cannot claim alone:** It does not choreograph the full scene or prove correct handling until actual reference and shot images are reviewed.

<!-- contract:inputs -->
## 4. Inputs

- A unique asset ID, version, purpose, known source facts, and fields that remain unknown.
- Required views, states, scale references, target platform, and any approved reference images.
- Downstream continuity needs such as locked features, variable states, orientation, handling, or spatial anchors.

<!-- contract:workflow -->
## 5. Workflow

1. Extract required dimensions and mark missing facts instead of inventing them.
2. Lock identity, geometry, materials, physical behavior, lighting, and state rules.
3. Choose the necessary views or state plates and compile a platform-aware generation task.
4. Run the module checklist and create the machine-readable asset contract.
5. Mark failures `rework`; only human-reviewed assets may enter `assets_approved` and downstream shots.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Missing identity or state facts return to intake; geometry, material, lighting, or interaction failures return to the responsible contract field.
- Cross-view drift returns to locked features and the primary reference; it is not repaired by adding unrelated style words.
- A failed review remains `rework`; structural completion cannot auto-promote it.

<!-- contract:review -->
## 7. Review gates

- [ ] ID, version, purpose, required dimensions, locked features, and unknowns are explicit.
- [ ] Proportion, perspective, geometry, materials, contact, weight, shadows, and readable key faces are physically coherent.
- [ ] No extra limbs, objects, text, watermark, drift, or background competition compromises the reference.
- [ ] A/B faces, dimensions, holder, orientation, interfaces, open/closed condition, materials, wear, and state changes are unambiguous.

<!-- contract:pass -->
## 8. Pass standard and states

- The asset task and JSON contract pass the module checklist with no unresolved blocking field.
- `assets_approved` requires inspection of the actual reference images; a text contract alone remains pending review.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- A primary reference-image task plus only the necessary alternate views or state plates.
- A versioned JSON asset contract for storyboard, prompts, and QC.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- Do not invent missing source facts, overwrite approved features, or put video action and dialogue into a static asset identity.
- Without an image tool and visual review, this module delivers a generation task and contract, not finished reference images.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- Text contracts work in any host that can read the folder. Producing and approving actual reference images additionally requires an image tool, file access, and human visual review.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../skills/prop-asset/agents/openai.yaml)
- [`SKILL.md`](../../../skills/prop-asset/SKILL.md)

**References**

- [`references/NEGATIVE-CASE-BOOK.md`](../../../skills/prop-asset/references/NEGATIVE-CASE-BOOK.md)
