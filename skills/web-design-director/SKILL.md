---
name: web-design-director
description: Design, implement, or review websites and application interfaces through product-specific visual direction, information architecture, interaction design, responsive behavior, accessibility, and verified frontend execution. Use for 网页设计、网站设计、界面设计、UI/UX、页面布局、前端视觉、交互设计、设计系统、响应式 and interface work on dashboards, workbenches, asset libraries or landing pages. Mere mentions of these surfaces, file/catalog management, backend-only work, README or repository updates, and maintenance of this skill do not request interface design or deployment.
---

# Web Design Director

Make the product understandable, useful, and visually specific in the actual interface. Usability means the end user can accomplish the real task with understandable, manageable effort while the interface retains its intended aesthetic quality. Direct the design and carry authorized implementation through verification. The user's taste and product priorities remain decisive; a self-review is not user acceptance.

## Match the requested result

Identify the surface, deliverable, stage, and allowed changes from the user's actual intent. A GitHub repository homepage normally means its README and repository content. An existing website does not authorize a Pages redesign, a new site, or deployment. File organization, asset production, workbench status checks, and skill maintenance alone are outside this workflow. Negative mentions such as “整理资产库文件，不设计网页” must not become UI work.

Choose the appropriate mode:

- **Direction:** a concept, rough sketch, scheme, or comparison. Deliver at the requested fidelity; do not start production code merely to illustrate a suggestion. A rough sketch should let the user judge hierarchy before polish.
- **Review:** inspect the supplied page, screenshot, or code and return ranked, actionable findings. A screenshot supports visual observations; it cannot establish keyboard behavior, API results, or hidden states. Cite exact file lines when code is available; otherwise identify the visible region without inventing code locations.
- **Build:** create or change the requested interface, verify it, and show the result. “Help me improve this page” normally authorizes relevant, reversible changes when the target is clear. Do not repeatedly request approval for that work.

For a local correction, retain the established direction and verify the changed behavior and likely regressions. For a new product or substantial redesign, establish a compact design contract. Ask only when an unknown changes the product, deliverable, cost, or an irreversible action. Otherwise state a reasonable assumption and continue.

## Load only what changes the decision

- New identity, major layout work, or a visual problem: [creative-direction.md](references/creative-direction.md).
- Research before a new direction, technology choice, or substantial implementation: [research-to-design.md](references/research-to-design.md).
- Forms, navigation, filtering, editing, selection, dialogs, or asynchronous workflows: [interaction-design.md](references/interaction-design.md).
- Glass, refractive material, animated backgrounds, scroll narratives, Canvas, or 3D: [material-and-motion.md](references/material-and-motion.md).
- Implementation or behavioral review: relevant sections of [web-quality-checklist.md](references/web-quality-checklist.md).
- Direction comparison and final review: applicable gates in [design-rubric.md](references/design-rubric.md).

These references are the skill's own runtime knowledge; no personal knowledge base or sibling skill is required. Use Figma only when the user supplies or requests it, or the project identifies it as the relevant design source. Tool availability alone is not a reason to introduce Figma, a framework, generated imagery, or hosting. Follow required tool-specific instructions when using those capabilities.

## Derive the design from observable needs

Establish the user, the task they need to finish, and an observable definition of success. Identify real content and actions, representative long text and data volume, existing behavior, brand decisions, stack, devices, and data ownership. Separate verified constraints from unknowns and assumptions. Existing conventions are inputs to examine, not sufficient reasons to copy them.

For a workflow surface, trace a representative complete user task, including the finding, understanding, comparison, decision, action, and confirmation it actually needs. Identify its main bottleneck and repeated work before allocating space and controls. Prioritize by task frequency, decision importance, and error consequence; do not substitute a working primary button for a completed task. Keep this reasoning internal unless a missing fact needs the user's decision, rather than asking them to complete another requirements form.

For existing interfaces, inspect relevant rendered screens, current components/styles, behavior, and representative data before deciding what to retain or change. Derive the solution from the cause, then compare total effort, compatibility, expected benefit, and reversibility. Neither a rewrite nor a small patch is automatically the right answer.

Distinguish task surfaces: marketing needs a credible reading and decision sequence; a workbench needs stable tools and room for the work; an asset browser needs recognition, comparison, and retrieval; a reading page needs typographic continuity. These distinctions diagnose needs; they do not prescribe mandatory layouts.

## Research before choosing and building

Before a new direction or substantive implementation, examine relevant excellent finished interfaces **and** actual open-source implementations. Observe the rendered behavior, then read the license and code that explains the effect or interaction. A repository list, README, screenshot, or dependency name alone does not satisfy this research. Use [research-to-design.md](references/research-to-design.md) to connect observed effect → mechanism → product-specific choice → cost/fallback → verification. Existing evidence may be reused when it covers the present decision and its version remains applicable; research only the gap.

For a local correction, inspecting the affected product and its relevant implementation may be sufficient. Research should resolve uncertainty that changes the result, not force a full website survey for a label fix. If a requested reference cannot be inspected, identify the missing evidence, find a relevant alternative when possible, and do not claim the unavailable source was studied.

Treat lists such as “interaction, visual impact, layout, color, language, frosted glass, liquid glass, dynamic visuals, etc.” as non-exhaustive capability dimensions. They neither limit the task to one demo nor require every effect on one page. Learn broadly when requested, select deliberately for the current product, and deliver the requested visible result. A request to “only see the effect” changes presentation, not the need for research and verification.

## Make design choices concrete

For a new direction, compare materially different compositions internally and recommend the one best supported by the task. Changing only the palette is not a different direction. Show alternatives when their tradeoff needs the user's judgment, not as a routine extra deliverable.

Translate the direction into implementable choices:

- Content priority, first useful action, reading order, and grouping.
- Layout relationships, density, alignment, whitespace, and narrow-width transformations.
- Typography roles, actual font availability, Chinese/Latin fallback, line length, and wrapping.
- Color and contrast roles; image subject, crop, placement, and provenance; consistent icons.
- Reusable tokens for type, color, spacing, borders, radii, elevation, and motion as needed.

Decide which information must be visible together to make the user's decision, which can wait in detail, and where the associated action belongs. Check avoidable back-and-forth, re-entry, and remembering values from closed views. Choose density and visual emphasis for that task; neither an empty-looking screen nor maximum information density is a general usability solution. Preserve visual identity through grouping, type, alignment, color, and material while making the work easier.

A distinctive composition can use no special effect, one expressive device, or several coordinated elements. Choose expression for its benefit to this product. Do not require a signature animation or redesign a locked brand for novelty. Gradients, glass, cards, neon, and minimalism are choices requiring a reason, never automatic defaults or universal bans.

Resolve the key screen with representative content, inspect the composition, and correct the largest visible problem before spreading its pattern. Use the creative reference for typography, imagery, density, and reference analysis. Style adjectives and a token list alone are not a finished design decision.

## Connect interaction to real consequences

For the few actions that determine the product's value, specify trigger → immediate feedback → pending behavior → successful data/result change → failure or cancellation recovery. Distinguish selection, focus, navigation, and editing. Preserve context where users return, retry, refresh, or narrow the viewport.

Use the interaction reference for applicable async races, duplicate submissions, validation, focus, and recovery. Do not add every conceivable state to every control. A working button must carry out its promised action; a toast or style change alone does not prove it. If data or APIs are simulated, state that boundary and do not claim persistence or backend integration.

When relevant, check both first-use discovery and return use: can a person infer the action from the visible interface, and can a returning user resume without repeating an introduction or reconstructing context? Keep high-value actions recognizable and close to their objects. Expressive motion may enhance them, but must not make users chase targets or lose the identity of the item they are operating on. See the task and target-stability guidance in [interaction-design.md](references/interaction-design.md).

## Implement the agreed behavior

For substantive builds, keep a short implementation contract: touched components, token source, state ownership, responsive transformations, keyboard semantics, main performance risk, verification cases, and rollback. Keep it internal or in the project's existing work record unless the user needs to review it.

Preserve user edits, approved content, routes, and existing behavior within the agreed scope. Choose language, application framework, and rendering technique separately from the mechanism the product needs; see the research reference. Reuse the current stack where suitable; add dependencies or restructure only when the outcome justifies the cost and verification. Choose pagination, virtualization, media optimization, or rendering containment against the actual bottleneck.

Use genuine product content and assets. Do not invent testimonials, customer logos, statistics, capabilities, API results, or progress percentages. For routine UI polish, do not invoke image-generation services without an explicit request for generated imagery; use available assets or an appropriate transparent fallback.

Implement a coherent slice, check it, then finish the remaining authorized scope. A slice is a feedback point, not permission to stop with a partial product. Preserve visible focus, content resilience, meaningful semantics, and reduced-motion behavior throughout.

## Verify and deliver with evidence

Inspect the rendered interface when a browser is available. Match tests to the change: required widths, representative content, the primary action, and the most consequential applicable failure or recovery. Use the web checklist's bounded verification procedure. Source inspection and builds supplement observed behavior.

For a task-bearing interface, perform the relevant end-to-end task using visible affordances before reducing it to isolated control assertions. Note where the user would need unprovided explanation, repeated navigation, remembered values, or recovery work. Use [design-rubric.md](references/design-rubric.md) to judge task flow and visual quality together. A task walkthrough by an agent is not a human usability study; do not claim first-time discoverability from a test that already knows hidden selectors or implementation details.

Compare the rendered result with the actual design contract and the specific qualities learned from the references. Locate concrete defects such as competing focal points, awkward Chinese line breaks, illegible secondary text, misleading selection, incorrect image crops, hidden controls, or stale results. Fix them and repeat affected checks. Functional tests do not establish visual distinction; effects being present do not establish good composition. If the user rejects the aesthetic result, withdraw the acceptance claim, diagnose the gap, and revise the direction from evidence before another implementation pass.

Separate claims: implemented; build/runtime checked; rendered appearance inspected; interaction verified; integrated/persistent behavior verified; user accepted. Record only evidence obtained. If browser, backend, assets, or credentials are unavailable, complete independent work and identify exact unverified behavior. Never label a source-only result visually verified.

Lead with the requested deliverable:

- **Direction:** recommended design and sketch or concrete layout at the requested fidelity, with the decisive tradeoff.
- **Review:** findings ordered by impact, evidence, and a specific correction; distinguish defects, hypotheses, and taste choices.
- **Build:** show the implemented page or preview, report observed results and unverified behavior, and link relevant files. A report does not substitute for the page.

Keep explanations proportional. Preserve scope and aesthetic authority without turning every task into an exhaustive design report.
