# Creative direction and visual correction

Use for a new identity, significant layout change, or visible quality problem. For a locked brand or local correction, use only the relevant lens.

## From content to composition

Start with actual content and the next decision. Identify what must be noticed first, what supports that choice, and what can wait. Group content because it shares a task, meaning, or interaction; a rounded container is not a default unit of information.

Choose layout relationships that reveal these priorities. Compare genuinely different structures when direction is open: reading sequence versus exploration, image-led recognition versus text-led comparison, spatial editing versus ordered operations. These are examples of tradeoffs, not industry templates.

Determine what the user must see together at the moment of choice. Comparison-critical attributes should not require repeatedly closing one detail view to remember its values in another. Associate actions with a clearly identified object and expose the information needed before commitment. Keep overview, comparison, detail, and editing connected where the task needs them; do not require a particular table, card, sidebar, or split view.

Use frequency and consequence to distribute space. Repeated work may need a stable, compact tool area and contextual properties; occasional explanation can be progressively disclosed. Keep contextual changes predictable so that relevant controls appear without moving the whole workspace. On narrow screens, preserve the same decision and its essential context rather than merely shrink everything or hide important attributes.

Derive expression from the product's artifacts, material, pace, vocabulary, and culture, then check that the metaphor helps use. A film workbench may need a large inspection area and stable shot context; it does not automatically need black backgrounds, film perforations, or cinematic transitions. A financial table can be distinctive through exceptional typography and density.

Write a short causal statement: **because these users need to see/do X, organize Y this way; it should produce observable Z.** Replace “premium,” “modern,” and “cinematic” with specific type, scale, crop, spacing, contrast, and behavior choices.

## Use references to resolve a choice

Inspect supplied references before interpreting them. Distinguish a locked design from an illustrative example. Infer the relevant property of an example without making every feature a requirement.

Before a new direction or substantial implementation, follow [research-to-design.md](research-to-design.md): study complete interfaces for composition and sequence, and relevant source code for behavior and execution. Compare the property that matters rather than assembling a moodboard of unrelated attractive screenshots. Do not copy a site's brand, text, assets, or whole composition, or treat an appealing screenshot as evidence that its workflow works.

Do not research merely to decorate a proposal with links. If access fails, state that the reference was not inspected. Verify changing platform or font behavior in current primary documentation when a decision depends on it.

## Typography does structural work

Assign display, reading, and utility roles according to the surface. Choose actual available fonts and explicit fallbacks; naming a font in CSS does not prove it loaded. Avoid new font dependencies for a small fix when the existing family can carry the hierarchy.

Check real Chinese and mixed-language strings. Break Chinese headings at meaningful phrases where feasible; do not impose Latin uppercase styling or wide letter spacing on Chinese body copy. Inspect punctuation, numerals, units, dates, and Latin terms together. Tabular numerals help column comparison when the font supports them.

Use bounded fluid type where it improves hierarchy; minimum, preferred growth, and maximum must preserve hierarchy across widths rather than scale everything together. Pair type size with content measure, line height, and spacing. Verify Chinese line breaks with actual words instead of borrowing a Latin specimen's proportions. Dense tools may need compact labels and generous control targets; reading pages need sustained line rhythm. No single type scale or section spacing fits both.

Check clipping, widows, button wrapping, truncation, and font fallback shifts. Essential titles, status, amounts, and errors need an accessible way to read their full meaning; an ellipsis alone is insufficient.

## Images, color, and space

Choose images for information or emotion, not simply to fill a hero. Know each important asset's source, subject, focal point, aspect ratio, narrow-width crop, and missing-image fallback. Start with approved assets; preserve user-specified identity and images. Generated and external imagery follows task authorization and attribution requirements.

Inspect whether cropping preserves the face, object, or contextual relationship that makes an image useful. Avoid stretching, incidental low-resolution enlargement, illegible text baked into imagery, and decorative photos that compete with the main action. Related images need a coherent treatment that preserves meaningful differences.

Define semantic color roles: canvas, surface, text, muted text, border, action, selection, and applicable status colors. Distinguish selected from hovered or focused. Check contrast on actual composite backgrounds, including gradients and overlays. Necessary distinctions cannot depend on color alone.

Design light and dark role values separately; mechanically inverting a palette does not preserve perceived hierarchy. Evaluate a color with the backgrounds and neighboring roles it will occupy. Retain an sRGB baseline if adding wide-gamut values, and verify the feature/gamut path. Over moving imagery, contrast depends on the changing composite: use a stable text treatment when a glass layer alone cannot maintain readability.

Set spatial rhythm from content and interaction density. Use alignment and shared baselines before adding borders or cards. Contrast large/small, dense/open, and quiet/emphatic areas deliberately. Expressive devices may be absent or multiple if the whole composition remains coherent.

Beauty and ease of use are joint outcomes. When a design is hard to operate, first repair hierarchy, relationships, legibility, and control placement rather than indiscriminately stripping away identity or shrinking text. When a utilitarian layout is visually weak, refine its type, rhythm, assets, and material without concealing the user's work. A beautiful task surface can be dense; a simple task surface can still be distinctive.

## Motion explains change

Use motion to clarify where an item went, what changed, how panels relate, or whether work is pending. Specify trigger, changing property, timing/easing, interruption, and reduced-motion alternative for meaningful transitions. For expressive materials and rendering behavior, read [material-and-motion.md](material-and-motion.md). Do not make essential content wait for an entrance animation or repeated tasks sit through a brand performance.

No-motion is a valid direction. Scroll hijacking, cursor replacement, perpetual glow, and ubiquitous entrance effects require strong product justification. Preserve platform expectations and user control.

## Inspect, diagnose, correct

Resolve a representative screen with real text and assets before replicating its pattern. At sketch fidelity, inspect hierarchy and relationships; do not demand final imagery or implementation before the user can judge a rough sketch.

Inspect the page without relying on your explanation:

- Does the initial frame make product, priority, and next action legible?
- Can the intended decision be made with the needed context in view, and are its actions clearly associated with the right object?
- Do grouping and hierarchy survive long titles, values, missing images, and narrow widths?
- Are visual weight, alignment, reading rhythm, crop, and contrast coherent?
- Does the composition still belong to this product when generic decorative effects are removed?

Name the largest observable defect, infer its cause, change the relevant relationship, and inspect again. Three equally loud action groups may need clearer priority; a cramped Chinese heading may need a different column measure before a smaller font; a weak hero may need relevant imagery before a stronger gradient. These are examples, not prescribed fixes without observation.

Separate evidence and judgment: “the label clips at 390 px” is an observation; “fewer borders may feel calmer” is a design judgment. Automated scores and declared signatures do not prove aesthetic success.
