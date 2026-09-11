# Interaction design: actions, state, and recovery

Use for meaningful workflow changes. Apply only to controls and risks present in the task; a label correction does not require a whole-product state audit.

## Describe consequential actions

For primary or high-consequence actions, make the applicable sequence testable:

| Point | Decision |
| --- | --- |
| Entry | Current context, input, selection, and action scope. |
| Trigger | Promised intent: navigation, selection, editing, or submission. |
| Feedback | Immediate visible and accessible acknowledgement. |
| Pending | What stays usable; whether cancel, retry, navigation, or new input is supported. |
| Success | Real data/result change, evidence of completion, and focus destination. |
| Failure/cancel | Retained input, rollback or uncertain outcome, and exact recovery action. |
| Return | Context that survives refresh, navigation, resize, or reopening where useful. |

This is a thinking aid, not a mandatory user-facing table. Do not invent APIs, persistence, or offline support. Name simulated prototype behavior; verify actual results in connected builds.

## Design the complete task, not just the control

Trace the actual user goal from entry to a confirmed result. Include only the discovery, comparison, editing, decision, and recovery steps this task needs; the sequence is not a fixed template. Find where uncertainty, repeated work, or error is most costly. Put high-frequency and consequential actions where their context is available, and keep secondary actions discoverable without competing for attention.

Distinguish a first encounter from repeat use when that affects the product. A new user needs understandable action names, visible cues, and sufficient context; a returning user may need preserved filters, a direct route, contextual controls, or an appropriate shortcut. Shortcuts, bulk actions, onboarding, and extra panels are options justified by the workflow, not requirements for every page.

An accessible name helps assistive technology but is not itself a visible cue for a sighted user. If a card or image is the primary way to resume a task, give it an appropriate perceivable affordance; do not leave a secondary removal action as the only explicit action text. Keep recurring action names and icon meaning consistent, and keep outcome or persistence explanations readable within the chosen visual treatment.

If changing an answer returns the user to an earlier step, preserve the other answers and return them to the relevant decision afterward; revisit later steps only when the changed answer makes them necessary. Error recovery should lead to the affected field or object with its label and context visible, retain useful work, and distinguish incorrect input from a service failure the user cannot fix. Reuse the product's accessible validation pattern rather than imposing another site's styling or validation policy.

## State ownership and scope

Represent each fact once and derive visual state from its owner. Keep focus, hover, selection, and editing distinct: keyboard focus is not a selection change unless the widget's intended model says so.

Use the URL for shareable filters or pagination when useful. Preserve temporary edits appropriately; do not put secrets or sensitive drafts in URLs or browser persistence for convenience. Define bulk-selection scope across filtering and pagination before acting.

Preserve the current object and unfinished work when opening inspectors or changing viewport. Retain predictable navigation, browser Back behavior, and useful direct links. Avoid interaction complexity that contributes nothing to the main task.

## Keep operation targets stable

For animated controls, contextual panels, sorted lists, and live updates, preserve the target's identity and a predictable hit area while the user aims, presses, types, or continues a sequence. Decorative refraction, parallax, and hover motion can occur in a separate visual layer instead of moving the critical control away. Intentionally dragging or reordering an object is different: the movement should follow the user's action and preserve that object's identity and focus.

Do not let a refreshed row silently become another record under the same pointer or focus. Choose an appropriate strategy, such as retaining stable item identity, deferring disruptive reordering during an operation, or clearly managing the transition and focus. Test the actual at-risk sequence, including unfinished animation or a viewport change, instead of indiscriminately stress-testing the whole product.

## Asynchronous reality

- Newer input must not be overwritten by an older response. Advance the current-intent version when input changes, including before a debounce finishes. Cancel superseded requests or guard which result commits; guard errors and loading cleanup with the same version, not only successful results. Test an earlier slow response arriving last. Debouncing alone does not establish correctness.
- Prevent duplicate consequential submissions and show a clear pending state without disabling unrelated navigation indiscriminately.
- Distinguish “failed” from “outcome unknown.” A timeout after a possible server mutation may require status reconciliation before retry. Do not claim an operation was undone without evidence.
- Use truthful waiting feedback. If no measured fraction exists, show indeterminate status or named stages, not fabricated percentages.
- Optimistic updates need an appropriate rollback/reconciliation path. Preserve input and unrelated successful work after failure.
- If editing can continue during a save, acknowledge only the submitted draft version; do not clear or overwrite edits made after submission when its response arrives.

Apply only cases relevant to the operation. A local synchronous filter does not require network-race infrastructure.

## Forms and recovery

Keep labels visible, errors specific and associated with controls, and input intact after recoverable failure. Make submit-time errors reachable. For complex forms, an error summary with links may be more useful than forcing focus immediately to the first field; follow the product's accessible pattern.

Distinguish no content, no matches, pending work, restricted access, and request failure. Offer the recovery actually available: create, clear filters, wait/cancel, request access, or retry. A failed request is not a successful zero-record response.

Match destructive-action protection to consequence and reversibility: clear scope, confirmation or real undo where suitable, and a useful result. Avoid confirmation fatigue for harmless actions. An undo control must restore the operation; a dismissible toast is not undo.

## Keyboard, focus, and navigation

Prefer native links, buttons, inputs, and selects. Use an established accessible composite-widget pattern only when behavior requires it. ARIA roles do not implement keyboard behavior; a visual card grid need not be an ARIA grid.

For modals, prefer native dialog capabilities where suitable. On opening, place focus according to the task and content length; contain focus, make the background inert, provide an accessible name and visible close/cancel route, and support Escape. If dismissal would lose consequential work, handle that explicitly instead of silently trapping the user. On closing, return focus to the invoker or a logical successor when the invoker no longer exists.

When exit animation delays removal, distinguish requested open state, visual presence, focus/inert ownership, and eventual unmount. Choose when focus returns and background access resumes so there is no invisible trap or duplicate active layer. A rapid close/reopen must reverse from the current visual state and keep the correct owner; nested dialogs dismiss only the appropriate layer. On desktop-to-mobile transformations, keep viewport-specific presentation state separate from shared selection or drafts. These lessons come from the shadcn sidebar and Radix dialog/focus-scope implementations linked in [research-to-design.md](research-to-design.md).

A listbox option cannot contain independently operable links, buttons, or checkboxes; consider ordinary semantic lists with native controls or a genuinely suitable grid pattern instead. Follow and test the appropriate pattern rather than adding roles cosmetically.

Do not make hover, dragging, color, or animation the sole way to operate a core function. Provide touch access and applicable non-drag alternatives. Sticky controls and the on-screen keyboard must not hide the action or current focus.

## Verify consequences

Run the happy path and relevant failure/recovery in the real interface. Observe the promised result. Test latest-intent-wins for async filtering; retained input and actual persistence for a save when persistence is in scope; open, keyboard operation, close, and focus restoration for a dialog. Recheck the main workflow after responsive transformations.

Report observed conditions and results, plus simulated or unverified behavior. A screenshot documents appearance; it cannot prove that selection affects the correct records.

For usability, run a complete representative task using the information and controls visible to the intended user. A find–compare–choose–confirm task is useful for a collection, while an editor may need change–undo–resume; choose the path from the brief. Record actual backtracking, loss of context, re-entry, uncertain outcomes, or unreachable controls, and fix the cause when it is in scope. Do not invent a universal click-count limit, time saving, or usability score. A walkthrough by the creating agent is an expert inspection, not evidence from a new user.

## Primary references

Verified 2026-09-08; consult the relevant source when implementing a specialized widget:

- [WAI APG modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
- [W3C native dialog technique](https://www.w3.org/WAI/WCAG21/Techniques/html/H102)
- [WAI APG listbox](https://www.w3.org/WAI/ARIA/apg/patterns/listbox/)
