# whitebox-previs-executor — inspectable 3D camera and blocking previews

| Status | Experimental; implemented basic previs and individually qualified action gates |
|---|---|
| Can deliver alone | An MP4 preview and its compiled/validation contract when the host has the required runtime. |
| Cannot claim alone | It cannot promise arbitrary actors, complete untested fights, final-film quality or the pixels a separate AI-video model will generate. |

[Runtime `SKILL.md`](../../../experimental/whitebox-previs-executor/SKILL.md) · [Install current source](../../INSTALLATION.md#experimental-packages) · [Install](../../INSTALLATION.md) · [Compatibility](../../COMPATIBILITY.md) · [Design system](../../SKILL_DESIGN_SYSTEM.md)

New source package; no v1.3.0 release asset.

<!-- contract:purpose -->
## 1. Purpose

Compile an existing prompt or storyboard into a playable 3D preview of camera, spatial parallax, basic blocking, timing and cuts, with explicit action-capability limits.

<!-- contract:principles -->
## 2. Design principles

- Compile an existing prompt into a visible 3D interpretation without redirecting the story.
- A playable MP4 is the primary deliverable; screenshots, a project file or numeric checks alone do not prove a viewed result.
- Use only implemented proxies and action profiles. Dense combat needs a passed short action gate before a longer sequence.

<!-- contract:standalone -->
## 3. Standalone scope

Use this module by itself when the requested result stays inside the following boundary:

An MP4 preview and its compiled/validation contract when the host has the required runtime.

**Cannot claim alone:** It cannot promise arbitrary actors, complete untested fights, final-film quality or the pixels a separate AI-video model will generate.

<!-- contract:inputs -->
## 4. Inputs

- The original prompt, shot description or storyboard; explicit duration, aspect and camera decisions where supplied.
- Host Python/Blender and actual MP4 decoding; explicit source, output paths and permission for rendering.

<!-- contract:workflow -->
## 5. Workflow

1. Preserve the source and record explicit values, derived values, deterministic defaults and unresolved decisions.
2. Validate the compiled camera, actor and timing contract before rendering.
3. Render with the implemented basic or qualified rigged backend; do not silently substitute unsupported actors or root-only combat.
4. Decode the MP4 and inspect the visible camera, scale, movement and cuts; combat additionally needs an independent visual action gate.

<!-- contract:returns -->
## 6. Return, rework, and rollback

- Unresolved geometry or unsupported proxies return to the compiled interpretation or explicit capability gap.
- An unpassed action gate stops expansion; preserve diagnostic status instead of calling it a successful fight preview.

<!-- contract:review -->
## 7. Review gates

- [ ] Actual decoded duration, frame rate, frame count, resolution and shot boundaries match the contract.
- [ ] Requested camera movement produces observable 3D parallax, and actor/prop contact remains on final rendered geometry.
- [ ] Human-readable combat requires identifiable attacker, defender, weapon, contact and reaction; numeric contact alone is insufficient.

<!-- contract:pass -->
## 8. Pass standard and states

- A playable, inspected MP4 and compiled/validation records exist; defaults and unresolved limits are disclosed.
- Existing basic-previs and short-contact evidence does not validate arbitrary fight actions or a complete 30-second fight.

> A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states.

<!-- contract:outputs -->
## 9. Outputs

- Playable MP4, previs_compiled.json, previs_validation.json and optionally an editable Blender project.

<!-- contract:boundaries -->
## 10. Boundaries, dependencies, and permissions

- This is an experimental preview executor, not an AI-video model, final-film renderer or prediction of a generation model's pixels.
- Supported humanoid/basic proxies and qualified profiles are limited; do not claim quadrupeds, vehicles or new combat without implemented and verified support.

<!-- contract:agents -->
## 11. Cross-Agent use

- The canonical package is the complete Skill folder, not a copied prompt fragment.
- `agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.
- A complete readable package plus host Python, compatible Blender, media decoding and appropriate file/render permissions; Blender and models are not bundled.
- An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.

<!-- contract:sources -->
## 12. Source files and references

**Runtime and metadata**

- [`agents/openai.yaml`](../../../experimental/whitebox-previs-executor/agents/openai.yaml)
- [`SKILL.md`](../../../experimental/whitebox-previs-executor/SKILL.md)

**References**

- [`references/previs-spec.md`](../../../experimental/whitebox-previs-executor/references/previs-spec.md)
- [`references/prompt-to-previs.md`](../../../experimental/whitebox-previs-executor/references/prompt-to-previs.md)

**Deterministic helpers**

- [`scripts/blender_previs_adapter.py`](../../../experimental/whitebox-previs-executor/scripts/blender_previs_adapter.py)
- [`scripts/blender_rigged_fight_adapter.py`](../../../experimental/whitebox-previs-executor/scripts/blender_rigged_fight_adapter.py)
- [`scripts/render_previs.py`](../../../experimental/whitebox-previs-executor/scripts/render_previs.py)
- [`scripts/run_blender_previs.py`](../../../experimental/whitebox-previs-executor/scripts/run_blender_previs.py)
- [`scripts/run_blender_rigged_fight.py`](../../../experimental/whitebox-previs-executor/scripts/run_blender_rigged_fight.py)
- [`scripts/validate_compiled_previs.py`](../../../experimental/whitebox-previs-executor/scripts/validate_compiled_previs.py)
- [`scripts/validate_spec.py`](../../../experimental/whitebox-previs-executor/scripts/validate_spec.py)

**Other packaged files**

- [`assets/sample-previs.json`](../../../experimental/whitebox-previs-executor/assets/sample-previs.json)

**Distribution notices in new ZIP builds**

New builds attach these files inside the Skill folder without editing its runtime source. Historical release archives are unchanged.

- [`LICENSE`](../../../LICENSE)
