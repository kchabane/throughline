# Isolated motion comparison

Open `/motion-study.html` on the Vite development server. This page does not change the product entry screen or dashboard. It is intentionally not an entry in the default production build.

- A: original timing, with the current approved palette and stationary logo disc.
- B: the same source paths and logo, with independently timed arrivals, acceleration toward convergence, and eased outgoing highlights. No glows, orbit rings or logo pumping.
- Pause stops both versions; Restart remounts and resumes both.
- The page follows reduced-motion styling and stacks on narrow screens.

## Verification

The source and proposed rendering appear together in `../previews/throughline-motion-comparison.png`, captured and inspected at 1440 × 900. The left panel reproduces the original component; the right panel changes timing and subtle signal weight only. No new illustration paths were drawn. Fonts, layout, colors and copy belong to the comparison page and do not alter the product.

The explicit Vite build with `rollupOptions.input: "motion-study.html"` passed. Pause and restart were tested in the browser; animation play states changed from paused to running for both panels. At 375px the document fits the viewport and the panels stack. No browser console errors. Static evidence does not establish subjective motion preference. The homepage files are unchanged.

final result: passed

Next: select A or B before integrating any motion changes into the product.
