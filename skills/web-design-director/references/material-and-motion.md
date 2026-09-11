# Material, movement, and rendering

Use for glass, optical distortion, dynamic visual fields, scroll narrative, Canvas, and 3D. Source mechanisms are linked at fixed versions in [research-to-design.md](research-to-design.md). Choose effects for the content and task; these are distinct capabilities, not a package to apply to every screen.

## Separate three kinds of glass

| Material | Mechanism | Useful test |
| --- | --- | --- |
| Frosted glass | Translucency, backdrop blur/saturation, restrained tint and boundary/elevation cues. | Against both quiet and detailed backgrounds, does the panel read as a surface and keep content legible? |
| Refractive liquid glass | A displacement field bends sampled background, often concentrating distortion near the contour; highlight, thickness, and restrained channel offset may strengthen the optical impression. | Do background features actually shift at the edge? Is the center controlled? A rounded blur with a white border alone does not establish refraction. |
| 3D transmissive material | Geometry, surface normals, lighting/environment, and a transmission/refraction model within a rendering scene. | Does shape respond coherently to light/view and remain affordable? A scene material does not automatically refract arbitrary DOM behind its canvas. |

First establish the layer relationship: background that can supply visible optical detail, material layer that samples/distorts it, and clear content/interaction above. A completely flat backdrop can make refraction invisible; noisy media can destroy label contrast. Select background detail, edge displacement, tint, and text support together rather than continually increasing blur.

Keep text, icons, hit targets, and focus rings out of the distorted layer unless distortion of content is explicitly the purpose. The decorative layer must not intercept controls. On both light and dark backgrounds, inspect composite contrast, border visibility, corners, clipping, and halos. Preserve a stable opaque or tinted surface when an optical layer cannot guarantee readable text.

In the studied implementations, JavaScript and Canvas 2D generate maps consumed by SVG filters; this is not necessarily a WebGL shader. Generate maps for actual bounds, cache/reuse when suitable, update on meaningful size/parameter changes, and avoid regenerating them every pointer event. Inspect resize and scale changes for stretched contours or stale bounds.

Treat SVG-filtered backdrop support as a target-browser question. A feature-support declaration is useful routing, not proof of correct compositing. Test the actual effect over real content. Provide an intentional frosted/tinted or opaque alternative for unsupported or too-expensive paths; interaction and identity must survive. Do not assert cross-browser compatibility from a Chrome demo.

## Design motion as a response

For consequential movement, define the initiating event, state change, perceptual purpose, interruptibility, and resting state. New input should update the current animation from its present value and, where appropriate, velocity. Do not reset from the old endpoint, queue obsolete transitions, or let completion callbacks commit stale state.

Animate a coherent relationship: an expanding inspector should preserve the selected object, a shared image transition should preserve its identity and crop, and a changing field should retain readable foreground controls. Hover embellishment is an enhancement; touch and keyboard need complete access without it. Rapid reversal, repeated activation, and changing target mid-flight are practical checks of continuity.

Separate geometry measurement from changes that cause layout. Batch reads before writes within a frame and keep pointer handlers primarily updating intent. Prefer compositor-suitable properties when they express the effect; avoid adding permanent layer promotion to every element. Use elapsed time for custom integration/damping, with bounded steps after long pauses, so motion does not depend on display refresh rate or leap when a tab resumes.

Decorative perpetual animation needs a clear purpose, restrained foreground relationship, and a rest/reduced-motion strategy. For reduced motion, present a well-composed static frame or a simple non-spatial state change; essential meaning and controls remain available. Never conceal content until an entrance animation completes.

## Keep scrolling under user control

Use native scrolling unless research shows that additional smoothing or choreography benefits the product. Adding a smooth-scroll library changes input-to-position behavior, not the quality of content sequencing. Preserve anchors, keyboard scrolling, browser restoration, touch, nested scroll containers, and focus visibility.

For a scroll narrative, map sections to changes in meaning and provide a readable linear route. Avoid long dead zones, hidden scroll locks, or animation progress that makes controls unreachable. If custom scroll integration is chosen, coordinate its clock with rendering and verify actual scroll completion; two independent loops can fight each other. Reduced motion should reveal a coherent sequence without forced travel.

## Bound the cost of dynamic rendering

Choose drawing work from the visual mechanism. CSS/SVG may suffice for a controlled material; Canvas 2D can generate maps or a lightweight scene; a fragment shader can create a continuous visual field; physical fluid simulation can require multiple buffers and repeated passes. Similar-looking motion can have very different costs. Use a richer simulation only when its visible behavior justifies it.

Share a frame clock where feasible. Draw on invalidation for a resting scene; after pointer release, animate only until settling when that fits the design. An intentionally continuous background needs bounded work, visibility handling, and a static option. Stop offscreen/hidden work when useful, reset elapsed-time baselines on resume, and remove loops, observers, listeners, and GPU resources when the surface is destroyed.

Set pixel resolution from the required appearance and device budget rather than blindly multiplying full-screen dimensions by devicePixelRatio. Bound render-target sizes and expensive sampling/passes. Reuse geometry, materials, textures, and buffers when their identity is shared. Render quality can step down with an observable device/performance signal; keep text and controls in crisp semantic DOM.

Do not infer efficiency from using React Three Fiber, a shader, transform, or requestAnimationFrame. Measure the affected interaction and actual device conditions. A source-level optimization is a hypothesis until measured; a visually successful desktop frame is not a mobile performance result.

## Verify the material and its transitions

Match checks to the chosen effect: inspect the main frame and a changed state; reverse or interrupt motion; resize with the material active; exercise touch/keyboard control; inspect light/dark or detailed/quiet backgrounds where applicable; check reduced motion and the unavailable-renderer fallback. For a dynamic claim, observe more than a screenshot and verify that the visible movement corresponds to the intended interaction.

Record appearance, behavior, compatibility, and measured performance separately. A fallback that merely removes all visual hierarchy is unfinished. A working optical demo is not yet a complete product; evaluate it with actual typography, content, action placement, and layout.
