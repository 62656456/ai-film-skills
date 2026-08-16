# Audited Web Quality Checklist

Use this local checklist for implementation and review. It is a stable, reviewed baseline; verify current platform documentation when a task depends on recently changed browser or framework behavior.

## Semantics and access

- Use button elements for actions and anchor elements for navigation.
- Give controls programmatic labels; give icon-only buttons an aria-label.
- Give images meaningful alt text, or empty alt text when decorative.
- Mark decorative icons hidden from assistive technology.
- Keep headings hierarchical and provide a skip link for substantial applications.
- Announce asynchronous validation, progress, and completion where needed.
- Preserve browser zoom.
- Provide visible focus-visible styling and a complete keyboard path.

## Forms and decisions

- Use associated labels, meaningful names, correct input types, input modes, and autocomplete.
- Never block paste.
- Keep validation next to the field and focus the first invalid control after submit.
- Start the loading state only after submission begins.
- Warn about unsaved changes.
- Give destructive actions confirmation or a time-bounded undo.
- Keep API keys, account identity, cost estimates, and active service clearly separated.

## Layout and content

- Prefer grid and flex layout over JavaScript measurement.
- Give flex children min-width zero when truncation is expected.
- Define overflow behavior instead of hiding unexplained overflow globally.
- Test short, normal, very long, empty, missing, and multilingual content.
- Give media explicit dimensions; lazy-load noncritical images.
- Consider safe-area insets for full-bleed mobile surfaces.
- Make Windows and native dark form controls explicit with color-scheme, foreground, and background colors.

## Motion

- Respect prefers-reduced-motion.
- Animate transform and opacity when possible.
- Never use transition all.
- Use a deliberate transform origin.
- Keep animations interruptible and subordinate to the user's action.

## Performance

- Virtualize or use content-visibility for large collections.
- Avoid layout reads during render and batch DOM reads and writes.
- Keep per-keystroke controlled-input work small.
- Preload only critical fonts and assets.
- Avoid loading heavy libraries before the related feature is used.
- Measure image-heavy grids, filters, drag operations, and resize behavior with realistic data.

## State, locale, and resilience

- Persist filters, tabs, pagination, and other shareable state in the URL when useful.
- Use Intl.DateTimeFormat and Intl.NumberFormat.
- Handle loading, empty, partial, stale, success, warning, offline, and error states.
- Make recovery actions specific: state what failed and what the user can do next.
- Keep action names consistent across buttons, progress messages, toasts, and history.

## Security-facing interface checks

- Never expose secrets in client state, URLs, screenshots, logs, or error text.
- Validate and constrain uploads, external image URLs, and rich user content on the server.
- Avoid rendering untrusted HTML.
- Require explicit intent for deletion, account switching, paid generation, and bulk operations.
- Show server-trusted cost and final confirmation before an irreversible paid action.

## Provenance

This checklist was adapted and condensed from the Vercel Web Interface Guidelines reviewed on 2026-07-15:
https://github.com/vercel-labs/web-interface-guidelines

The upstream project is licensed under the MIT License, Copyright (c) 2025 Vercel Labs. The complete upstream license remains available at:
https://github.com/vercel-labs/web-interface-guidelines/blob/main/LICENSE
