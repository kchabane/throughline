# Throughline

Evidence-led app-review intelligence for product and customer-experience teams.

[View the interactive portfolio demo](https://throughline-product-demo.vercel.app/)

Throughline explores how App Store and Google Play feedback can become
prioritized, evidence-backed product direction. The public website is a static
portfolio build: it replays the intended analysis experience using redacted
demonstration snapshots, so visitors cannot trigger external APIs or consume
model credits.

This repository also includes a sanitized extraction of the Python pipeline
behind the working prototype. The implementation is real; credentials, raw
scraped reviews, model responses, runtime jobs and private caches are not.

## Architecture

```text
Public storefronts
        ↓
Date-aware collectors ──→ coverage metadata
        ↓
Normalize → deduplicate → enforce requested window
        ↓
Batched AI annotation (complete corpus, no silent sampling)
        ↓
CX metrics + statistical validation
        ↓
Dashboard snapshot → React portfolio experience
```

## Module map

| Area | Location | Responsibility |
|---|---|---|
| Portfolio UI | `src/` | Search, staged loading, dashboards and comparison |
| Source adapters | `pipeline/throughline/collectors.py` | Date-aware Google Play and App Store pagination |
| Canonical schema | `pipeline/throughline/schema.py` | Provenance, UTC dates, filtering and deduplication |
| AI analysis | `pipeline/throughline/ai.py` | Bounded Anthropic batches with strict ID validation |
| Metrics | `pipeline/throughline/metrics.py` | NSS, weekly pulse, themes and rating alignment |
| Orchestration | `pipeline/throughline/pipeline.py` | Dashboard-ready snapshot assembly |
| Verification | `tests/` | Deterministic behavior and boundary cases |

## Design decisions

- **Static public experience:** the deployable frontend never receives an API
  key and cannot create model charges.
- **Complete evidence window:** collectors paginate to a date boundary instead
  of making a high-volume product look representative with a small sample.
- **Visible source limits:** collection safety limits produce coverage metadata;
  the pipeline does not silently claim completeness.
- **Separation of fact and narrative:** deterministic metrics are built before
  optional model-generated interpretation.
- **Validation, not false certainty:** Spearman correlation checks whether model
  sentiment moves with ordinal star ratings. Small samples are reported as
  untestable.
- **Privacy by construction:** the public reference implementation omits author
  identity. Its committed sample data is entirely synthetic.

## Run the portfolio

Requires Node.js 18+.

```bash
npm install
npm run dev
```

Open the address printed by Vite, normally `http://localhost:5173`.

## Run the pipeline sample

Requires Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
PYTHONPATH=pipeline python3 pipeline/run_sample.py
pytest
```

The sample runner needs no credentials. It reads synthetic annotated reviews
and writes `sample_data/snapshot.synthetic.json`.

## Optional Anthropic analysis

The integration reads credentials only from the environment:

```bash
cp .env.example .env
export ANTHROPIC_API_KEY="your-own-key"
```

`.env` is ignored. Never commit a real key.

## Scope

This is a portfolio prototype, not a production multi-tenant SaaS service. A
production implementation would add authenticated tenancy, durable job queues,
source-specific rate limiting, observability, billing controls, retention
policies and a larger human-labelled evaluation set.
