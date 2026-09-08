"""End-to-end orchestration from canonical reviews to dashboard-ready JSON."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .metrics import net_sentiment_score, rating_alignment, theme_summary, weekly_pulse
from .schema import deduplicate_reviews, filter_since


def build_snapshot(
    reviews: list[dict[str, Any]], *, since: datetime, generated_at: datetime
) -> dict[str, Any]:
    """Build metrics only after the complete in-window corpus is available."""
    corpus = deduplicate_reviews(filter_since(reviews, since))
    return {
        "generated_at": generated_at.isoformat(),
        "window": {"since": since.isoformat(), "review_count": len(corpus)},
        "kpis": {
            "n_reviews": len(corpus),
            "nss": net_sentiment_score(corpus)["nss"],
            "rating_alignment": rating_alignment(corpus),
        },
        "weekly": weekly_pulse(corpus, end=generated_at),
        "themes": theme_summary(corpus),
    }
