from datetime import datetime, timedelta, timezone

import pytest

from throughline.metrics import net_sentiment_score, rating_alignment, weekly_pulse
from throughline.collectors import collect_google_play
from throughline.schema import deduplicate_reviews, filter_since, normalize_review


NOW = datetime(2026, 9, 8, tzinfo=timezone.utc)


def review(identifier: str, days_ago: int, score: float, rating: int = 3):
    return {
        "source_key": f"test:{identifier}",
        "date": (NOW - timedelta(days=days_ago)).isoformat(),
        "rating": rating,
        "sentiment_score": score,
        "themes": ["Reliability"],
    }


def test_normalize_generates_stable_id_without_author_data():
    raw = {"date": "2026-09-01T12:00:00Z", "text": "Synthetic comment", "rating": 4}
    first = normalize_review(raw, company="Example", app_name="Example App", app_id="app", source="app_store", country="se")
    second = normalize_review(raw, company="Example", app_name="Example App", app_id="app", source="app_store", country="se")
    assert first["source_key"] == second["source_key"]
    assert "author" not in first


def test_deduplication_preserves_cross_source_records():
    rows = [review("a", 1, 0.5), review("a", 1, 0.5), review("b", 1, -0.5)]
    assert [row["source_key"] for row in deduplicate_reviews(rows)] == ["test:a", "test:b"]


def test_date_filter_keeps_full_window_and_excludes_boundary_violations():
    rows = [review("recent", 2, 0.5), review("old", 31, -0.5)]
    assert [row["source_key"] for row in filter_since(rows, NOW - timedelta(days=30))] == ["test:recent"]


def test_nss_uses_explicit_neutral_band():
    result = net_sentiment_score([review("a", 1, 0.8), review("b", 1, -0.7), review("c", 1, 0.1), review("d", 1, 0.9)])
    assert result == {"nss": 25.0, "n_phrases": 4, "positive": 2, "neutral": 1, "negative": 1}


def test_weekly_pulse_uses_real_bucket_counts():
    result = weekly_pulse([review("a", 2, 0.8), review("b", 9, -0.8)], end=NOW)
    assert [week["n_reviews"] for week in result] == [0, 0, 1, 1]


def test_rating_alignment_requires_enough_evidence():
    assert rating_alignment([review("a", 1, 0.5, 5)])["testable"] is False


def test_rating_alignment_detects_ordering():
    rows = [review(str(i), 1, score=(i - 5) / 5, rating=(i % 5) + 1) for i in range(10)]
    result = rating_alignment(rows)
    assert result["testable"] is True
    assert -1 <= result["spearman_rho"] <= 1


def test_missing_date_is_rejected():
    with pytest.raises(KeyError):
        normalize_review({"text": "Synthetic"}, company="Example", app_name="App", app_id="x", source="app_store", country="us")


def test_google_collection_paginates_until_date_boundary():
    pages = [
        ([{"reviewId": "1", "at": NOW - timedelta(days=2), "score": 5, "content": "Synthetic one"}], "next"),
        ([
            {"reviewId": "2", "at": NOW - timedelta(days=20), "score": 3, "content": "Synthetic two"},
            {"reviewId": "3", "at": NOW - timedelta(days=31), "score": 1, "content": "Synthetic old"},
        ], "unused"),
    ]

    def fake_page(**_kwargs):
        return pages.pop(0)

    result = collect_google_play(
        "example.app",
        company="Example",
        app_name="Example App",
        since=NOW - timedelta(days=30),
        fetch_page=fake_page,
    )
    assert [row["id"] for row in result.reviews] == ["1", "2"]
    assert result.pages_requested == 2
    assert result.complete_to_boundary is True


def test_google_collection_discloses_safety_limit():
    def fake_page(**_kwargs):
        return ([{"reviewId": "1", "at": NOW - timedelta(days=1), "score": 5, "content": "Synthetic"}], "more")

    result = collect_google_play(
        "example.app",
        company="Example",
        app_name="Example App",
        since=NOW - timedelta(days=30),
        max_pages=1,
        fetch_page=fake_page,
    )
    assert result.complete_to_boundary is False
    assert "safety limit" in result.note
