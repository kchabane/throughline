# Throughline interface

The interface uses a calm analytical workspace with findings and actions before the evidence drill-down.

## Brand palette

- Navy `#072D59`: headings, primary controls and navigation.
- Seal Blue `#DBF2FC`: selected areas and the findings surface.
- Crimson Pink `#FD6E88`: the signature signal motif and company identity in comparisons.
- White: reading surfaces. Cool neutrals: borders and secondary text.
- Shared palette and responsive layout rules live in `src/design.css`.

## Satisfaction colors

Brand accents do not replace the traffic-light system. Status is also written in text.

| Metric | Green | Amber | Red |
| --- | --- | --- | --- |
| Average star rating | 4 or higher | 3.3 to below 4 | Below 3.3 |
| Net sentiment | Above +10 | −10 through +10 | Below −10 |

These are interface interpretation thresholds, not external performance benchmarks. Fewer than five reviews keeps both headline metrics neutral and displays an insufficient-evidence message. Rating alignment measures sentiment-to-rating consistency, not customer satisfaction or proof that every finding is accurate.

## Demo and evidence behavior

- Company choices stay visible and filter as the visitor types.
- Weekly pulse sits directly below the KPI cards, followed by Generate insights & actions. Clicking it shows a preparation state, then reveals findings and ranked actions directly below. The public demo clearly labels this as cached analysis with no live model call.
- Snapshot dates describe the reviews actually present.
- Replay is explicitly a demo; it does not collect new reviews.
- Customer evidence is labeled as paraphrased and does not use direct quotation marks.
- Evidence advances only when the reader chooses it.
- Compare uses the original floating right-edge tab. Its dialog supports Escape, focus containment and focus restoration.
- Theme rows become stacked items on narrow screens, preserving the same evidence controls.
- Reduced-motion preferences disable ornamental transitions.
