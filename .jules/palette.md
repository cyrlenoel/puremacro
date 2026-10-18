## 2024-10-18 - Inline Style Blocks for Jupyter Outputs
**Learning:** Standard external CSS classes are unreliable for inline HTML in Jupyter notebook outputs. Injecting a small `<style>` tag directly within the HTML string is an effective way to add custom styling like focus or hover states.
**Action:** When adding UX enhancements to Jupyter notebook outputs via `IPython.display.HTML`, use an inline `<style>` tag. Double-escape CSS curly braces (`{{` and `}}`) in Python f-strings, and use `!important` to override any pre-existing inline `style="..."` attributes.
