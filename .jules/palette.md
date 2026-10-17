
## 2026-10-17 - Interactive States in Jupyter HTML Outputs
**Learning:** Inline styles in IPython.display.HTML outputs cannot support pseudo-classes like :hover or :focus-visible, which are essential for accessibility and UX.
**Action:** Inject a small <style> tag within the HTML string to define CSS classes for interactive elements.
