"""Isolated public-store adapters with date-aware pagination.

The adapters stop after crossing the requested date boundary, not after an
arbitrary number of reviews. Source limitations are returned as coverage
metadata so incomplete collection is visible to downstream consumers.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    import requests

from .schema import normalize_review, parse_datetime


@dataclass(frozen=True)
class CollectionResult:
    reviews: list[dict[str, Any]]
    source: str
    complete_to_boundary: bool
    pages_requested: int
    note: str | None = None


def collect_google_play(
    app_id: str,
    *,
    company: str,
    app_name: str,
    since: datetime,
    country: str = "us",
    language: str = "en",
    page_size: int = 200,
    max_pages: int = 50,
    fetch_page: Callable[..., tuple[list[dict[str, Any]], Any]] | None = None,
) -> CollectionResult:
    """Collect newest-first Google Play pages until `since` is crossed."""
    if fetch_page is None:
        from google_play_scraper import Sort, reviews as google_reviews

        def fetch_page(**kwargs):
            return google_reviews(sort=Sort.NEWEST, **kwargs)

    collected: list[dict[str, Any]] = []
    token = None
    crossed = False
    pages = 0

    for _ in range(max_pages):
        rows, token = fetch_page(
            app_id=app_id,
            lang=language,
            country=country,
            count=page_size,
            continuation_token=token,
        )
        pages += 1
        if not rows:
            break
        for row in rows:
            date = row.get("at") or row.get("date")
            if not date:
                continue
            if parse_datetime(date) < parse_datetime(since):
                crossed = True
                continue
            collected.append(
                normalize_review(
                    {
                        "id": row.get("reviewId") or row.get("id"),
                        "date": date,
                        "rating": row.get("score") or row.get("rating"),
                        "text": row.get("content") or row.get("text"),
                        "app_version": row.get("reviewCreatedVersion"),
                        "engagement": row.get("thumbsUpCount"),
                    },
                    company=company,
                    app_name=app_name,
                    app_id=app_id,
                    source="google_play",
                    country=country,
                )
            )
        if crossed or token is None:
            break

    complete = crossed or token is None
    note = None if complete else f"Stopped at the configured {max_pages}-page safety limit."
    return CollectionResult(collected, "google_play", complete, pages, note)


def collect_app_store(
    app_id: str,
    *,
    company: str,
    app_name: str,
    since: datetime,
    country: str = "us",
    max_pages: int = 10,
    session: "requests.Session | None" = None,
) -> CollectionResult:
    """Collect Apple's public RSS pages with explicit coverage reporting."""
    if session is None:
        import requests

        client = requests.Session()
    else:
        client = session
    collected: list[dict[str, Any]] = []
    crossed = False
    pages = 0

    for page in range(1, max_pages + 1):
        url = (
            f"https://itunes.apple.com/{country}/rss/customerreviews/"
            f"page={page}/id={app_id}/sortby=mostrecent/json"
        )
        response = client.get(url, timeout=10, headers={"User-Agent": "Throughline/portfolio"})
        response.raise_for_status()
        entries = response.json().get("feed", {}).get("entry", [])
        if isinstance(entries, dict):
            entries = [entries]
        pages += 1
        review_entries = [e for e in entries if "im:rating" in e]
        if not review_entries:
            break

        for entry in review_entries:
            date = entry.get("updated", {}).get("label")
            if not date:
                continue
            if parse_datetime(date) < parse_datetime(since):
                crossed = True
                continue
            collected.append(
                normalize_review(
                    {
                        "id": entry.get("id", {}).get("label"),
                        "date": date,
                        "rating": int(entry["im:rating"]["label"]),
                        "text": entry.get("content", {}).get("label", ""),
                        "app_version": entry.get("im:version", {}).get("label"),
                        "engagement": entry.get("im:voteSum", {}).get("label"),
                    },
                    company=company,
                    app_name=app_name,
                    app_id=app_id,
                    source="app_store",
                    country=country,
                )
            )
        if crossed:
            break

    complete = crossed or pages < max_pages
    note = None if complete else "Apple RSS page limit reached before the date boundary."
    return CollectionResult(collected, "app_store", complete, pages, note)
