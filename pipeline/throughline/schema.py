"""Canonical review schema and deterministic corpus preparation."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Iterable


def parse_datetime(value: str | datetime) -> datetime:
    """Parse an ISO timestamp and always return an aware UTC datetime."""
    if isinstance(value, datetime):
        parsed = value
    else:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def normalize_review(
    review: dict[str, Any],
    *,
    company: str,
    app_name: str,
    app_id: str,
    source: str,
    country: str,
) -> dict[str, Any]:
    """Map a storefront-specific record to Throughline's stable schema."""
    text = str(review.get("text") or "").strip()
    date = parse_datetime(review["date"]).isoformat()
    review_id = str(review.get("id") or "").strip()
    if not review_id:
        fingerprint = f"{source}|{country}|{date}|{text}"
        review_id = "hash-" + hashlib.sha256(fingerprint.encode()).hexdigest()[:24]

    return {
        "id": review_id,
        "source_key": f"{source}:{country}:{review_id}",
        "company": company,
        "app_name": app_name,
        "app_id": app_id,
        "source": source,
        "country": country.lower(),
        "date": date,
        "rating": review.get("rating"),
        "text": text,
        "app_version": review.get("app_version"),
        "engagement": review.get("engagement"),
    }


def deduplicate_reviews(reviews: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Preserve source provenance while removing repeated records."""
    seen: set[str] = set()
    output: list[dict[str, Any]] = []
    for review in reviews:
        key = str(review["source_key"])
        if key not in seen:
            seen.add(key)
            output.append(review)
    return output


def filter_since(
    reviews: Iterable[dict[str, Any]], since: datetime
) -> list[dict[str, Any]]:
    """Keep the complete collected corpus inside the requested window."""
    boundary = parse_datetime(since)
    return [r for r in reviews if parse_datetime(r["date"]) >= boundary]
