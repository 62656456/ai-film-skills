# Design judgment and acceptance

Use applicable criteria for comparison, review, and delivery. Score only when a comparison benefits; do not turn a local correction into a comprehensive audit. A plausible design argument is different from an observed result.

## Review the outcome

| Dimension | Observable question |
| --- | --- |
| Product and information | Can the intended user identify the current surface, priority, and next useful action? Does grouping match task frequency and consequence? |
| Complete user task | Can the user finish the relevant goal, understand the result, and recover where necessary without avoidable backtracking, repeated entry, or remembering hidden comparison information? |
| Visual identity | Do composition, typography, imagery, and density belong to this product? Does the result visibly achieve the requested degree of distinction or impact? Is expression compatible with locked brand decisions? No mandatory signature count or animation. |
| Visual execution | Do actual words, images, values, contrast, alignment, and rhythm hold together at required widths? Are assets and claims truthful? |
| Interaction | Does the primary action deliver its promised result, with clear feedback and applicable recovery? Are focus, selection, and bulk-action scope unambiguous? Can users recognize the next action, and do its target and identity remain predictable during operation? |
| Accessibility | Can required operations be reached and understood with keyboard, labels, semantics, visible focus, sufficient contrast, and relevant alternatives? |
| Responsiveness | Does narrow-width structure preserve priorities, access, input, and context rather than merely shrink? Are long content and meaningful overflow handled? |
| Engineering | Does state have clear ownership? Are resource costs bounded by an appropriate strategy? Are dependencies, privacy, and compatibility appropriate to scope? |

For each finding, identify observed condition → user impact → likely cause → concrete correction → verification. Distinguish verified defects, hypotheses needing a test, and aesthetic preferences. Use supplied screenshot regions or real code locations; never invent either.

For work that required research, compare the actual rendered result with the chosen reference properties: hierarchy, content sequence, material response, or interaction behavior. State which mechanism was translated and what was deliberately adapted to this product. A source list, framework change, added blur, or higher test count does not establish that learning improved the design. Reading source, reproducing a mechanism, verifying a product outcome, and receiving user acceptance are separate evidence levels.

Assess beauty and usability together. Strong visual execution cannot compensate for an unusable task path, and isolated functional success cannot establish a coherent or appealing interface. Repair the observed conflict: strengthen hierarchy, put comparison information together, stabilize an action, or separate decorative motion from operation. Do not automatically prescribe a plain style, remove every effect, or impose a universal layout.

For a substantive task surface, inspect a representative start-to-finish task without explanatory coaching. Where relevant, inspect a return visit and the main recovery. Record the goal, starting conditions, observed path, friction, resulting state, and a concrete improvement. Internal walkthroughs may identify defects; claims about human ease, satisfaction, or time saved require corresponding user evidence. A pure direction or screenshot-only review must stay within its available evidence.

## Blockers in the requested scope

Do not call an affected workflow ready while any of these remains:

- The primary task is unclear, unreachable, or promised controls do not perform their action.
- A required decision cannot be made with accessible context, or changing targets causes the user to act on the wrong object.
- Keyboard users cannot operate core controls, or essential state/content is inaccessible.
- The interface loses entered work unexpectedly, commits stale results, or misrepresents success.
- A destructive action lacks appropriate protection or its purported undo cannot restore it.
- Secrets or sensitive error details are exposed.
- Required layouts break or hide necessary information and controls.
- Loading, empty, error, or return states trap the user.
- Realistic collection sizes cause unbounded work or interaction failure.
- The implementation contradicts the user's scope, approved content, brand, or design contract.

Unrelated pre-existing defects should be reported when material; do not silently expand the assignment to fix them.

## Evidence levels

Keep these statuses distinct:

- **Implemented:** the requested change exists; this alone says nothing about execution.
- **Build/runtime checked:** relevant commands ran and/or the application loaded.
- **Appearance inspected:** actual rendered views at recorded conditions were examined.
- **Interaction verified:** recorded actions produced their promised observable results.
- **Task walkthrough completed:** the representative user goal was followed through the actual interface and friction was recorded; identify who performed it. This does not imply human usability research.
- **Integration verified:** actual service/data persistence was checked where required.
- **User accepted:** the user explicitly approved the result. Internal or subagent review cannot award this status.

A proposal can be ready for review without implementation evidence. A screenshot review can be complete within visible evidence without claiming interaction tests. A build with blocked browser access can be delivered with the exact remaining check, but cannot be described as visually verified. A few accessibility checks do not establish whole-site WCAG conformance.

If no relevant blocker remains, provide the result and evidence proportionate to the task. State remaining limitations plainly. Stop extra testing or polishing unless a new change, failure, or unresolved concern justifies it.
