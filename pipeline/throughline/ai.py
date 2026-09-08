"""Batched Anthropic analysis with strict JSON validation and no embedded key."""

from __future__ import annotations

import json
import os
from typing import Any, Iterable

from anthropic import Anthropic


SYSTEM_PROMPT = """You analyse product feedback conservatively.
Return JSON only: an array with one object per supplied review containing
id, sentiment_score (-1 to 1), primary_emotion, and themes (0 to 3 concise
labels). Do not infer demographics or sensitive traits. Preserve every id."""


def _chunks(rows: list[dict[str, Any]], size: int) -> Iterable[list[dict[str, Any]]]:
    for start in range(0, len(rows), size):
        yield rows[start : start + size]


def analyse_reviews(
    reviews: list[dict[str, Any]], *, batch_size: int = 30, model: str | None = None
) -> list[dict[str, Any]]:
    """Score the complete corpus in bounded batches; never silently sample it."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is required for AI analysis.")
    client = Anthropic(api_key=api_key, max_retries=2, timeout=60.0)
    selected_model = model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
    analysed: list[dict[str, Any]] = []

    for batch in _chunks(reviews, batch_size):
        payload = [{"id": row["source_key"], "text": row["text"], "rating": row["rating"]} for row in batch]
        response = client.messages.create(
            model=selected_model,
            max_tokens=4096,
            temperature=0,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
        )
        raw = next(block.text for block in response.content if block.type == "text")
        annotations = json.loads(raw)
        by_id = {str(item["id"]): item for item in annotations}
        if set(by_id) != {row["source_key"] for row in batch}:
            raise ValueError("Model response IDs do not match the submitted batch.")
        for row in batch:
            annotation = by_id[row["source_key"]]
            analysed.append({**row, **annotation})
    return analysed
