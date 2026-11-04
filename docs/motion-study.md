# Isolated motion comparison

Open `/motion-study.html` on the Vite development server. This page does not change the product entry screen or dashboard. It is intentionally not an entry in the default production build.

- A: original timing, with the current approved palette and stationary logo disc.
- B: the same source paths and logo, with independently timed arrivals, acceleration toward convergence, bolder 2.3–3.2px strokes against quieter background tracks, and a stronger eased outgoing highlight. No glows, orbit rings or logo pumping.
- B opens at full width. Compare with original and Focus on B switch between the two layouts.
- Pause stops both versions; Restart remounts and resumes both.
- The page follows reduced-motion styling and stacks on narrow screens.

## Verification

The source and proposed rendering appear together in `../previews/throughline-b-stronger-comparison.png`, captured and inspected at 1440 × 900. The left panel reproduces the original component; the right panel changes timing, signal weight and track contrast only. No new illustration paths were drawn. Fonts, layout, colors and copy belong to the comparison page and do not alter the product.

The explicit Vite build with `rollupOptions.input: "motion-study.html"` passed. Comparison/focus toggles, pause and restart were tested in the browser; animation play states changed from paused to running for both panels. At 375px the document fits the viewport and the panels stack. No browser console errors. Static evidence does not establish subjective motion preference. The homepage files are unchanged.

final result: passed

Next: review the strengthened B at full width before integrating it into the product.
