"""Remove identities and verbatim text from cached portfolio snapshots.

Usage:
    python3 scripts/sanitize_demo_data.py src/data/*.json

The aggregate metrics and product structure remain intact. Evidence strings are
replaced with explicitly synthetic copy derived only from broad theme labels and
rating bands, never from the original wording.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def synthetic_text(theme: str, rating: int | float | None) -> str:
    subject = theme.strip() if theme else "overall product experience"
    if rating is not None and float(rating) <= 2:
        return f"Synthetic example: the reviewer encountered difficulty with {subject.lower()}."
    if rating is not None and float(rating) >= 4:
        return f"Synthetic example: the reviewer was satisfied with {subject.lower()}."
    return f"Synthetic example: the reviewer gave mixed feedback about {subject.lower()}."


def sanitize_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    snapshot["demoData"] = "synthetic-redacted"
    ingestion = snapshot.get("ingestion")
    if isinstance(ingestion, dict):
        ingestion["mode"] = "redacted_demo"
        ingestion.pop("review_fingerprint", None)

    for index, review in enumerate(snapshot.get("reviews", []), start=1):
        themes = review.get("themes") or []
        theme = str(themes[0]) if themes else "overall product experience"
        replacement = synthetic_text(theme, review.get("rating"))
        review["id"] = f"synthetic-{index:03d}"
        review["author"] = f"Synthetic reviewer {index:03d}"
        review["text"] = replacement
        for phrase in review.get("phrases", []):
            if isinstance(phrase, dict):
                phrase["text"] = replacement

    for scope in snapshot.get("scopes", {}).values():
        if not isinstance(scope, dict):
            continue
        for point in scope.get("painPoints", []):
            if isinstance(point, dict):
                point["quote"] = synthetic_text(str(point.get("tag") or "product experience"), point.get("rating", 1))
        untagged = scope.get("untagged")
        if isinstance(untagged, dict) and untagged.get("examples"):
            untagged["examples"] = ["Synthetic example: feedback did not map cleanly to a recurring theme."]
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
