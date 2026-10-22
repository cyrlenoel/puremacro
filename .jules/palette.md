## 2024-10-22 - Injecting CSS for Inline HTML in Notebooks
**Learning:** When injecting custom styles (like focus or hover states) into inline HTML intended for display within a Jupyter Notebook (e.g. via `IPython.display.HTML`), standard external CSS classes are unreliable.
**Action:** Inject a small `<style>` tag directly within the HTML string. When doing this inside a Python f-string, ensure CSS curly braces (`{{` and `}}`) are double-escaped to prevent syntax errors, and use `!important` to force overrides against pre-existing inline attributes.
