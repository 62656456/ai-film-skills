# Web implementation and verification

Use relevant sections for implementation and review. This is a maintained baseline, not a claim that every item has been audited in every project. Verify current browser/framework documentation when a decision depends on changing support.

## Semantic controls, forms, and focus

- Use buttons for actions, anchors for navigation, associated labels for controls, and meaningful input types, inputmode, names, and autocomplete. Do not block paste.
- Give icon-only actions accessible names. Use useful image alt text or empty alt for decoration; hide decorative icons from assistive technology.
- Preserve heading structure, browser zoom, and a skip link where repeated navigation warrants it.
- Expose asynchronous status, validation, and completion where needed without noisy repeated announcements.
- Provide visible keyboard focus and a complete operation path. Test dialogs, menus, and other composites using their real keyboard model.
- Keep validation near its field, preserve input after failure, and use a suitable focus/error-summary strategy.
- Start submission feedback with actual submission; distinguish pending, success, failure, and unknown outcomes.
- Warn about meaningful unsaved work and protect consequential destructive actions with confirmation or actual undo, proportionate to risk.

## Measurable accessibility checks

Use these WCAG 2.2 AA criteria where applicable; checking this subset does not prove full conformance:

- Normal text contrast at least 4.5:1; large text at least 3:1. Large means at least 18 pt, or 14 pt bold (approximately 24 or 18.67 CSS px). Applicable exceptions include inactive controls, incidental/decorative text, and logotypes.
- Visual information needed to identify controls/states and essential graphical objects needs 3:1 against adjacent colors. This is not a rule for every decorative divider.
- Targets should accommodate 24 × 24 CSS px, or meet the actual spacing/equivalent/inline/user-agent/essential exceptions. For undersized targets, check 24 CSS px diameter circles centered on their bounding boxes against other targets and undersized-target circles; a generic “4 px gap” does not prove compliance.
- Focus must be visible. AA 2.4.11 requires the focused component not be entirely hidden by author-created content; fully unobscured focus is the stronger 2.4.12 AAA criterion and a useful engineering aim.
- For vertical reading, preserve information and functionality at equivalent 320 CSS px width without two-dimensional page scrolling. Content requiring a two-dimensional layout may scroll locally; a data-table exception does not exempt text within individual cells. Test text enlargement and relevant zoom, not only device presets.
- Provide applicable alternatives to dragging and avoid dependence on color, hover, or animation alone.

## Responsive structure and content

- Prefer CSS grid/flex for layout; use JavaScript measurement when its behavior actually requires it.
- Define how navigation, sidebars, inspectors, dialogs, tables, grids, and action bars transform at narrow widths. Reordering must preserve understandable reading/tab order and current task context.
- Choose breakpoints from where content or interaction stops working. Include the project's main desktop width and a narrow mobile width; check a boundary/intermediate width when a layout transition warrants it.
- Define intentional overflow. Do not hide page-wide overflow to conceal a defect; use min-width: 0 where flex/grid content must shrink.
- Test representative long Chinese/mixed-language strings, amounts, missing media, empty data, and real collection density as relevant.
- Give media dimensions or aspect ratios; lazy-load noncritical images without delaying the actual LCP candidate. Provide appropriately sized thumbnails and responsive sources.
- Consider safe-area insets, sticky overlap, and on-screen keyboards. Inspect native Windows/dark controls with deliberate color-scheme and foreground/background colors.
- Use Intl date/number formatting where locale matters and preserve useful URL state without exposing secrets.

## Motion and performance

- Respect prefers-reduced-motion; preserve essential feedback without unnecessary spatial movement. Prefer transform/opacity for suitable animations; specify properties instead of transition: all. Keep motion interruptible with an intentional origin.
- Identify the bottleneck before choosing a remedy. Pagination/virtualization can bound fetched/rendered items; content-visibility skips some offscreen rendering but does not bound DOM count, retained data, or network work. They are not equivalent solutions.
- Keep per-keystroke work bounded, avoid repeated synchronous layout, batch relevant DOM reads/writes, and defer heavy libraries until needed. Measure actual scrolling, filtering, dragging, and resize when they are affected.
- For glass, shaders, animated backgrounds, or 3D, apply [material-and-motion.md](material-and-motion.md): use a bounded rendering resolution, stop or invalidate work according to actual need, clean up listeners/resources, and verify static/unsupported/reduced-motion states. Reusing a rendering library does not establish that these application policies exist.
- For relevant loading/interaction/layout changes, use Core Web Vitals as diagnostic targets: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1. A formal pass uses real-user 75th-percentile data, segmented by mobile and desktop, with all three passing. Lab runs diagnose regressions; a Lighthouse score, single measurement, or TBT proxy cannot prove field INP or a field pass.
- Record relevant tool, viewport/device, throttling, data scale, and scenario. Do not claim a performance improvement from adopting an optimization without measurement.

## Data and security boundaries

- Keep secrets out of client bundles, URLs, screenshots, logs, and error messages. Protect uploads, external URLs, and rich user content at the appropriate server boundary; do not render untrusted HTML.
- Make identity, active service, consequential action scope, and trustworthy cost clear where applicable. Respect existing authorization before external, paid, or irreversible actions.
- Do not add backend behavior, persistence, account changes, or service calls simply to make a visual prototype appear complete. Distinguish simulated from real data and integration.

## Bounded browser verification

1. Establish what changed and which user outcome it must preserve or improve; retain a before view when useful and available.
2. Run the project's relevant existing build/check and load the actual page. Investigate errors relevant to the change; do not infer rendering success from the build alone.
3. Inspect the changed views at required widths with representative content. Check crop, wrapping, hierarchy, contrast, overflow, and control reachability.
4. Follow the representative user task from entry to an understood result, including the most consequential applicable failure/recovery. Check visible discoverability, comparison context, stable action targets, and avoidable backtracking when relevant. Then check keyboard/focus, reduced motion, and content extremes where affected; isolated button checks do not replace the task path.
5. Compare the observable result with the design/interaction contract. Fix concrete failures and repeat the affected check.
6. Record compact evidence: view/conditions, action, expected versus observed result, artifact if useful, and pass/fail/unverified. Stop after relevant gates pass.

Use existing approved browser tools and local validation mechanisms. If a browser or service is unavailable, finish independent checks and report the exact verification gap. Do not fabricate screenshots, interaction results, persistence, or user acceptance.

## Sources and provenance

The earlier local checklist condensed the MIT-licensed [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines), reviewed 2026-07-15; [upstream license](https://github.com/vercel-labs/web-interface-guidelines/blob/main/LICENSE), Copyright (c) 2025 Vercel Labs. This revision retains that provenance and adds task-scoped verification and primary-standard clarifications.

Primary standards verified 2026-09-08:

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Target size minimum and exceptions](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- [web.dev Web Vitals](https://web.dev/articles/vitals)
