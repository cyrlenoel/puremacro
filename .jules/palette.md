
## 2024-05-14 - ARIA Labels overriding visible text (WCAG 2.5.3)
**Learning:** Adding an `aria-label` to a button that already has visible text (like the "CSV" button populated via JS or HTML) overrides the element's visible text for screen readers. This violates WCAG 2.5.3 (Label in Name) because users relying on voice control might try to activate the button by saying its visible text, but the accessible name is different.
**Action:** When adding accessible text to buttons that already have a visible label, use the `title` attribute for tooltips or add visually hidden text (`.sr-only`) instead of `aria-label`. Only use `aria-label` for icon-only buttons or when the visible text is completely non-descriptive.
