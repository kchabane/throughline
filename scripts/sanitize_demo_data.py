"""Remove identities and verbatim text from cached portfolio snapshots.

Usage:
    python3 scripts/sanitize_demo_data.py src/data/*.json

The aggregate metrics and product structure remain intact. Evidence strings are
replaced with short paraphrases derived only from broad theme labels and rating
bands, never from the original wording.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def paraphrased_text(theme: str, rating: int | float | None) -> str:
    subject = theme.strip() if theme else "overall product experience"
    if rating is not None and float(rating) <= 2:
        return f"Describes recurring difficulty with {subject.lower()}."
    if rating is not None and float(rating) >= 4:
        return f"Highlights a positive experience with {subject.lower()}."
    return f"Reports a mixed experience with {subject.lower()}."


def reviewer_label(source: str | None) -> str:
    return {
        "app_store": "App Store reviewer",
        "google_play": "Google Play reviewer",
    }.get(str(source), "Public app reviewer")


def sanitize_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    snapshot["demoData"] = "public-analysis-anonymized"
    ingestion = snapshot.get("ingestion")
    if isinstance(ingestion, dict):
        ingestion["mode"] = "redacted_demo"
        ingestion.pop("review_fingerprint", None)

    id_map: dict[Any, str] = {}
    for index, review in enumerate(snapshot.get("reviews", []), start=1):
        old_id = review.get("id")
        new_id = f"anonymized-{index:03d}"
        # Some historical snapshots use a one-based numeric review ID while
        # others already contain anonymized IDs. Keep both addressable so
        # every theme can be migrated without losing its evidence links.
        id_map[index] = new_id
        id_map[str(index)] = new_id
        if old_id is not None:
            id_map[old_id] = new_id
            id_map[str(old_id)] = new_id
        themes = review.get("themes") or []
        theme = str(themes[0]) if themes else "overall product experience"
        replacement = paraphrased_text(theme, review.get("rating"))
        review["id"] = new_id
        review["author"] = reviewer_label(review.get("source"))
        review["text"] = replacement
        for phrase in review.get("phrases", []):
            if isinstance(phrase, dict):
                phrase["text"] = replacement

    for scope in snapshot.get("scopes", {}).values():
        if not isinstance(scope, dict):
            continue
        for theme in scope.get("themes", []):
            if not isinstance(theme, dict):
                continue
            theme["verbatimIds"] = [
                id_map.get(review_id, id_map.get(str(review_id), review_id))
                for review_id in theme.get("verbatimIds", [])
            ]
        for point in scope.get("painPoints", []):
            if isinstance(point, dict):
                point["quote"] = paraphrased_text(str(point.get("tag") or "product experience"), point.get("rating", 1))
        untagged = scope.get("untagged")
        if isinstance(untagged, dict) and untagged.get("examples"):
            untagged["examples"] = ["Mentions an issue that does not map clearly to a recurring theme."]
    return snapshot


def main(paths: list[str]) -> None:
    if not paths:
        raise SystemExit("Pass one or more snapshot paths.")
    for raw_path in paths:
        path = Path(raw_path)
        snapshot = json.loads(path.read_text(encoding="utf-8"))
        sanitized = sanitize_snapshot(snapshot)
        path.write_text(json.dumps(sanitized, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"Sanitized {path}")


if __name__ == "__main__":
    main(sys.argv[1:])
