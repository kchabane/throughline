import json
from pathlib import Path


def test_committed_demo_snapshots_contain_only_synthetic_evidence():
    for path in Path("src/data").glob("*.json"):
        snapshot = json.loads(path.read_text(encoding="utf-8"))
        assert snapshot.get("demoData") == "synthetic-redacted", path
        for review in snapshot.get("reviews", []):
            assert str(review.get("id", "")).startswith("synthetic-"), path
            assert str(review.get("author", "")).startswith("Synthetic reviewer"), path
            assert str(review.get("text", "")).startswith("Synthetic example:"), path
            for phrase in review.get("phrases", []):
                assert str(phrase.get("text", "")).startswith("Synthetic example:"), path

        for scope in snapshot.get("scopes", {}).values():
            for point in scope.get("painPoints", []):
                assert str(point.get("quote", "")).startswith("Synthetic example:"), path
            for example in scope.get("untagged", {}).get("examples", []):
                assert str(example).startswith("Synthetic example:"), path
