# Analysis pipeline

This directory is a sanitized extraction of the pipeline behind the product
prototype. It preserves the engineering decisions that matter in review while
excluding API credentials, raw scraped reviews, generated model responses,
runtime jobs and local caches.

## Data flow

1. `collectors.py` paginates public store adapters until the requested date
   boundary is crossed and reports incomplete coverage.
2. `schema.py` normalizes provenance, filters the date window and deduplicates
   records without merging distinct sources.
3. `ai.py` scores every retained review in bounded Anthropic batches. It does
   not silently sample the final corpus.
4. `metrics.py` calculates Net Sentiment Score, weekly movement, theme volume
   and Spearman alignment between model sentiment and star ratings.
5. `pipeline.py` assembles a dashboard-ready snapshot only after the corpus is
   complete.

The committed sample is synthetic and pre-annotated so the deterministic
pipeline and tests run without a network connection or API key.
