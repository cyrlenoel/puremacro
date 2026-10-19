## 2024-10-19 - Terse UI Element Accessibility
**Learning:** Icon-only or overly terse text buttons (e.g. "CSV") severely lack context. Tooltips (via `title`) and explicit `aria-label`s significantly boost user confidence and assistive technology compatibility for these controls.
**Action:** Always complement icon-only or very terse button actions with localized `aria-label` attributes and consider `title` attributes for visual tooltip support.
