"""Run the deterministic pipeline against synthetic, pre-annotated reviews."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from throughline.pipeline import build_snapshot


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "sample_data" / "reviews.synthetic.json"
OUTPUT = ROOT / "sample_data" / "snapshot.synthetic.json"


def main() -> None:
    reviews = json.loads(INPUT.read_text(encoding="utf-8"))
    generated_at = datetime(2026, 9, 8, tzinfo=timezone.utc)
    snapshot = build_snapshot(
        reviews,
        since=generated_at - timedelta(days=30),
        generated_at=generated_at,
    )
    OUTPUT.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
