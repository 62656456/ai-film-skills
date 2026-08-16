# Visual continuity for multi-image and multi-shot work

Load this reference whenever two or more images belong to the same scene, sequence, location, asset family, or story state; when deriving from an approved image; or when the deliverable includes a scene bible or CONTACT-SHEET.

Continuity means every frame is a recorded state of the same physical world. It does not freeze camera position, performance, or every deployable part.

## Contents

1. Authority and versioning
2. Minimum scene bible
3. Invariant and variable contract
4. Shot state card
5. Color and material continuity
6. Spatial direction
7. Equipment-family continuity
8. CONTACT-SHEET bridge
9. Workflow and gates

## Authority and versioning

Use this order:

1. current explicit user locks and corrections;
2. named current screenplay/version and selected scene/beat;
3. approved project and scene bibles within their declared scope;
4. approved anchor frames and state cards;
5. generated candidates;
6. CONTACT-SHEET overview.

A candidate cannot silently rewrite the screenplay or bible. Promote a deviation only after explicit approval, record its scope, increment the affected version, and propagate it forward. A CONTACT-SHEET is an audit artifact, never a replacement for full-resolution frames or state records.

## Minimum scene bible

Record only fields applicable to the current source, production route, asset set, and requested continuity scope; mark intentionally absent states instead of inventing people, costume, props, wear, damage, pollution, or a camera:

- `scene_bible_id` and `version`;
- story time, elapsed-time assumption, and operating state;
- gravity, pressure, medium, temperature, weather, reference frame, and motion rules;
- spatial topology, axes, landmarks, entrances, exits, and fixed interfaces;
- scale anchors and stable proportions;
- environmental light, practical sources, exposure logic, and functional color semantics;
- principal bodies/agents, costume or surface state, carried/attached objects, and equipment identity when present;
- asset/equipment-family grammar;
- applicable material history and any persistent wear, repair, contamination, growth, or damage;
- `invariant_set`, `allowed_variables`, and the event that may change each variable.

Generated text, logos, and serial numbers are unreliable identity anchors. Prefer geometry, interface placement, patch shape, material region, functional color block, or occupied scale relationship.

## Invariant and variable contract

### Normally invariant

Apply only to elements declared present in the approved bible; do not invent a door, interface, manufacture, damage, character, costume, light, or material state merely to fill the list.

- physical environment and reference frame;
- architecture topology and landmark order;
- vehicle or habitat proportions;
- handedness and location of doors, hatches, windows, radiators, thrusters, controls, and service interfaces;
- declared equipment/asset-family interface or relationship grammar and origin/manufacturing/growth generation when present;
- base materials and source-motivated color relationships;
- any existing persistent damage, repair/healing, contamination, and wear;
- character identity, base costume, essential objects, and unit assignment;
- dominant light geometry unless the story changes time, weather, orientation, or power state.

### Normally variable

- camera, lens, crop, focus, and foreground occlusion;
- pose, gaze, gesture, task phase, and emotion;
- deployable mechanism and interface state;
- heat, power, fault, coolant, consumable, or authorization state;
- local dust, condensation, wetness, ice, debris, or biological response when caused by the event;
- background work and traffic;
- practical lights whose devices change state.

Every variable change needs a trigger. Every invariant change needs a declared bible revision or visible transition.

## Shot state card

Create one per frame:

- `shot_id`, beat, and time gap;
- `scene_bible_id/version` and approved anchor-frame IDs;
- viewer/camera/sensor anchor, projection or lens where applicable, view direction, and relevant spatial/action-relation side;
- `continuity_in`: positions, orientations, tasks, props, damage, power, heat, light, and background motion;
- `beat/change`: the selected function-specific beat and any intentional state change; an establishing, relationship, discovery, aftermath, or asset frame need not invent an action event;
- `continuity_out`: resulting state inherited by the next frame;
- persistent anchors, intentional changes, and unresolved drift.

Do not write only `same as previous`. Restate the few invariants and entering states that must be visible.

## Color and material continuity

For each story beat record dominant source/direction, practical-light state, exposure/contrast, environmental neutral, material colors, functional accents, and the cause of any transition.

Keep color changes source-motivated. A grade cannot substitute for a changed light, atmosphere, material, power state, or event. Preserve relative skin, material, light, and shadow relationships unless the color script records a cause.

Track important surfaces by component or zone:

`base material/function → exposure/age → contact/heat/load/fluid/radiation/biology cause → localized wear → repair/retrofit → current state → event required to change it`

Damage does not disappear. Dust, fluid, frost, residue, and debris follow gravity, flow, shielding, temperature, and contact. A repair leaves a new persistent trace.

## Spatial direction

Choose one coordinate convention before the first shot.

- Surface scene: world direction, action axis, main travel vector, entry/exit, camera side, and landmark order.
- Microgravity or rotation: vehicle/habitat axes and named anchor surfaces; never invent one global down in free fall.

For each frame record the applicable viewer/camera/sensor location or projection, subject travel/attention, landmark ordering, depth relation, and spatial/action-relation side. For photographic or continuity-edited narrative shots, motivate or bridge a camera crossing when screen direction matters. For illustration, animation, diagrams, sensor views, or asset turnarounds, use the declared projection/view sequence instead of forcing cinematic over-axis grammar. Reject only unexplained reversals of facts, handedness when relevant, landmarks, interfaces, or travel.

## Equipment-family continuity

A family is shared operating logic, not identical shells. Choose and keep stable only the invariants that define the source's family; a biological, passive, continuous, bespoke, disposable, self-growing, or non-serviceable family need not acquire modular industrial hardware:

- interface, attachment, sensing, or relationship grammar when present;
- applicable power/data/material/biological distribution;
- joining, growth, access, replacement, or sealed-boundary logic;
- compatible modules or role/body variants when modularity exists;
- applicable handling, service, regeneration, disposal, or lifecycle method;
- protection logic, functional color semantics, origin/manufacturing/growth generation, and repair/healing/replacement culture when relevant.

Allow the role-, body-, or function-specific differences the source needs. Use family/unit IDs only when the project has such a registry. Carry forward only the deployment, thermal, consumable, governance, damage, growth, healing, and replacement states that exist. Avoid cloned condition and preserve the non-actionable weapon boundary.

## CONTACT-SHEET bridge

1. Arrange sequence frames in story order, not quality ranking.
2. Put alternate routes in separate labeled lanes; do not present mutually exclusive variants as consecutive time.
3. Preserve aspect ratio and composition. Fit or letterbox; never stretch or hide continuity evidence with inconsistent crops.
4. Put IDs and status in the margin, never inside the image.
5. For each adjacent pair record persistent anchor, elapsed time, declared change, axis/screen direction, light/color state, material/damage state, family/scale consistency, and unexplained drift.
6. Review the sheet at thumbnail scale for silhouette, geography, color, scale, and rhythm.
7. Review originals for interfaces, handedness, material history, damage, costume, and optical integration.
8. Use only approved frames and cards as references for the next generation. The sheet guides overview, not fine-detail inheritance.

Preserve existing project batch and shot IDs. Append the next unused IDs according to the current project's declared namespace; never renumber, overwrite, or silently replace prior assets.

If adjacent frames share no spatial, identity, material, equipment, light, or state anchor, declare a new scene or insert a bridge.

## Continuity workflow

1. Freeze a bible version and invariant set.
2. Select approved anchor frames; keep candidates separate.
3. Plan each frame as `continuity_in → selected beat or intentional change → continuity_out`.
4. Generate from the same bible version and incoming state.
5. Inspect the full-resolution result; reject drift before propagation.
6. Record accepted outgoing state.
7. Assemble the CONTACT-SHEET in story order and audit adjacent pairs.
8. If approval changes an invariant, increment the version and update only downstream frames.

## Continuity gates

Reject or revise if:

- a narrative shot lacks bible version, ID, or applicable incoming/outgoing state; an asset/view/state alternative instead lacks its declared variant identity and invariant set;
- physics, topology, scale, handedness, landmark order, or interface placement changes without cause;
- travel direction or axis crossing is unexplained;
- light/color changes through arbitrary grading;
- an existing damage, wear, contamination, deployment, power, heat, biological, or consumable state resets without an event;
- a family loses its declared shared interface/relationship/lifecycle grammar when one exists, or becomes a line of clones;
- a candidate silently becomes authority;
- a CONTACT-SHEET hides drift at thumbnail size;
- individual originals were not inspected after sheet review.
