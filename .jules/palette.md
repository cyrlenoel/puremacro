## 2023-10-27 - Initial Setup
**Learning:** Initializing palette journal.
**Action:** Ready to record UX learnings.
## 2023-10-27 - Keyboard Accessibility for Scatter Plots
**Learning:** Scatter plots in D3 lack native keyboard accessibility for data exploration. While line charts implemented `.on("focus")` and `.on("keydown")` to navigate across data points, scatter plots only supported pointer events (hovering). This means users relying on a keyboard or screen reader couldn't explore individual data points in scatter plots.
**Action:** Added `tabindex="0"`, an `aria-label`, and implemented `focus`, `blur`, and `keydown` event listeners to the transparent overlay rectangle in `MAV.scatter`. When focused, it highlights the first point. Using ArrowLeft/ArrowRight navigates through the points sequentially, updating the tooltip and highlighting ring, providing keyboard users with the same exploratory capabilities as mouse users.
