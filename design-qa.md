# Original animation refinement QA

- Source visual truth: ../previews/throughline-original-restored-motion.png
- Implementation: ../previews/throughline-original-refined.png
- Combined comparison: ../previews/original-refinement-comparison.png (source above refinement, inspected together).
- Viewport: 1280 × 900 CSS px; matched 1280 × 240 px motif crops at x=0,y=100. No density normalization. Animation phases differ.
- State: entry screen, no company selected.

## Findings

No actionable P0/P1/P2 mismatches against the selected original structure and requested refinement. The original paths, 12 input tracks, convergence and output shape remain unchanged. Moving highlights are intentionally crisper and higher contrast; the logo adds a restrained 4.5% scale response at the outgoing highlight's peak.

## Required surfaces

- Typography: no text in the focused decorative region; page typography unchanged.
- Spacing/layout: original motif geometry and hub anchor retained. Current approved responsive container sizing retained.
- Colors/tokens: approved navy/pink palette retained; highlight weight and opacity intentionally increased.
- Assets: original component reused directly, no replacement illustration or invented paths.
- Copy/content: unchanged.

## Checks and limits

Production build and whitespace checks passed. Browser inspection confirmed original input duration (5.8 seconds) and new highlight/response animations. No browser console errors. At 375px, the document fits the viewport and the lighter mobile stroke rules apply. Existing reduced-motion rules remain in place; OS preference switching was not tested. Static screenshots cannot establish subjective motion quality or full accessibility compliance. No production publication occurred.

## Comparison history

First refinement comparison passed with no actionable visual fixes required.

final result: passed
