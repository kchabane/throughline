"""Deterministic CX metrics and validation used by the dashboard."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from statistics import mean
from typing import Any, Iterable

from scipy import stats

from .schema import parse_datetime

POSITIVE_THRESHOLD = 0.2
NEGATIVE_THRESHOLD = -0.2


def net_sentiment_score(scored_items: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """NSS = percentage positive phrases minus percentage negative phrases."""
    scores = [float(item["sentiment_score"]) for item in scored_items]
    if not scores:
        return {"nss": None, "n_phrases": 0, "positive": 0, "neutral": 0, "negative": 0}
    positive = sum(score > POSITIVE_THRESHOLD for score in scores)
    negative = sum(score < NEGATIVE_THRESHOLD for score in scores)
    neutral = len(scores) - positive - negative
    return {
        "nss": round(100 * (positive - negative) / len(scores), 1),
        "n_phrases": len(scores),
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
    }


def rating_alignment(scored_reviews: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Validate model sentiment against ordinal star ratings with Spearman rho."""
    pairs = [
        (float(row["rating"]), float(row["sentiment_score"]))
        for row in scored_reviews
        if row.get("rating") is not None and row.get("sentiment_score") is not None
    ]
    if len(pairs) < 10:
        return {"testable": False, "n": len(pairs), "reason": "At least 10 pairs are required."}
    ratings, sentiment = zip(*pairs)
    rho, p_value = stats.spearmanr(ratings, sentiment)
    return {
        "testable": True,
        "n": len(pairs),
        "spearman_rho": round(float(rho), 3),
        "p_value": round(float(p_value), 5),
    }


def weekly_pulse(
    reviews: Iterable[dict[str, Any]], *, end: datetime, weeks: int = 4
) -> list[dict[str, Any]]:
    """Aggregate the same complete evidence corpus into fixed weekly buckets."""
    rows = list(reviews)
    end_utc = parse_datetime(end)
    buckets: list[dict[str, Any]] = []
    for index in reversed(range(weeks)):
        bucket_end = end_utc - timedelta(days=index * 7)
        bucket_start = bucket_end - timedelta(days=7)
        current = [r for r in rows if bucket_start <= parse_datetime(r["date"]) < bucket_end]
        ratings = [float(r["rating"]) for r in current if r.get("rating") is not None]
        sentiment = [r for r in current if r.get("sentiment_score") is not None]
        buckets.append(
            {
                "start": bucket_start.date().isoformat(),
                "end": (bucket_end - timedelta(days=1)).date().isoformat(),
                "n_reviews": len(current),
                "avg_rating": round(mean(ratings), 2) if ratings else None,
                "nss": net_sentiment_score(sentiment)["nss"] if sentiment else None,
            }
        )
    return buckets


def theme_summary(scored_reviews: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for review in scored_reviews:
        for theme in review.get("themes", []):
            grouped[str(theme)].append(review)
    output = []
    for theme, rows in grouped.items():
        result = net_sentiment_score(rows)
        output.append({"theme": theme, "volume": len(rows), "nss": result["nss"]})
    return sorted(output, key=lambda row: (-row["volume"], row["theme"]))
