# Design Director Rubric

Use this rubric for design proposals, reviews, and build verification. Score only when comparison helps; do not turn every response into a report.

## 1. Product truth

- Can a first-time user identify the product, the current surface, and the next useful action?
- Does the hierarchy match the user's real task frequency and consequence?
- Is the interface vocabulary written from the user's perspective?
- Are cost, progress, risk, and destructive consequences visible before commitment?

## 2. Information architecture

- Does every region have one clear responsibility?
- Are navigation, creation, inspection, and management functions spatially distinct?
- Are advanced controls progressively disclosed without concealing essential state?
- Can users recover context after refresh, navigation, or reopening a project?
- Is density intentional for the surface rather than copied from a landing page or generic admin dashboard?

## 3. Distinctiveness

- Does the direction arise from the product's subject, materials, workflow, or culture?
- Could the same palette, typography, layout, and signature be pasted onto an unrelated product?
- Is there exactly one memorable signature move with a clear reason?
- Has the design avoided unearned gradients, glass, glow, pills, cards, ornamental numbering, and fake metrics?
- Is real content doing visual work instead of placeholder copy?

## 4. Visual system

- Is there a controlled token system for color, type, spacing, radii, elevation, iconography, and motion?
- Is typography a hierarchy rather than a collection of sizes?
- Do contrast, alignment, rhythm, and whitespace reveal priority?
- Are dense regions calm and scannable?
- Are icons consistent in stroke, size, alignment, and meaning?

## 5. Interaction and motion

- Does each control communicate default, hover, focus, active, selected, disabled, loading, success, warning, and error states as applicable?
- Are actions named consistently from trigger through confirmation?
- Is motion used to explain hierarchy, continuity, status, or causality?
- Is there one orchestrated moment rather than unrelated effects?
- Are animations interruptible and reduced for prefers-reduced-motion?

## 6. Accessibility

- Does semantic HTML carry the interaction before ARIA is added?
- Can every operation be completed by keyboard with visible focus?
- Are labels, names, roles, status announcements, and error relationships exposed?
- Does zoom remain enabled, and do contrast and target sizes remain usable?
- Is meaning independent of color, hover, or animation alone?

## 7. Responsive and content resilience

- Does the layout adapt structurally instead of merely shrinking?
- Are long names, translated strings, large numbers, empty sets, and broken media handled?
- Do sidebars, inspectors, dialogs, grids, and toolbars have deliberate narrow-width behavior?
- Are safe areas, overflow, sticky regions, and virtual keyboards considered?

## 8. Engineering quality

- Do component boundaries follow behavior and ownership?
- Are tokens centralized and state represented once?
- Does the solution respect the current stack and avoid unnecessary migration?
- Are large lists, images, effects, and network work bounded?
- Are secrets, uploads, external URLs, destructive actions, and error details handled safely?
- Can important behavior be tested without relying only on screenshots?

## Quality gates

Treat any of these as a blocker:

- the primary journey is unclear or inaccessible;
- a destructive action has neither confirmation nor undo;
- keyboard users cannot reach or operate core controls;
- secrets or sensitive error details can reach the client or logs;
- the layout breaks at the project's required viewport;
- loading, error, or empty states trap the user;
- a large collection causes unbounded rendering or interaction failure;
- the implementation contradicts the approved design contract.

Call a result ready only when no blocker remains and the product identity, main workflow, accessibility, responsiveness, and buildability are all defensible. The user's aesthetic judgment remains final.
