import json
from pathlib import Path


def test_committed_demo_snapshots_contain_only_anonymized_evidence():
    for path in Path("src/data").glob("*.json"):
        snapshot = json.loads(path.read_text(encoding="utf-8"))
        assert snapshot.get("demoData") == "public-analysis-anonymized", path
        for review in snapshot.get("reviews", []):
            assert str(review.get("id", "")).startswith("anonymized-"), path
            assert review.get("author") in {
                "App Store reviewer",
                "Google Play reviewer",
                "Public app reviewer",
            }, path
            assert "Synthetic" not in str(review.get("text", "")), path
            for phrase in review.get("phrases", []):
                assert "Synthetic" not in str(phrase.get("text", "")), path

        for scope in snapshot.get("scopes", {}).values():
            for point in scope.get("painPoints", []):
                assert "Synthetic" not in str(point.get("quote", "")), path
            for example in scope.get("untagged", {}).get("examples", []):
                assert "Synthetic" not in str(example), path
