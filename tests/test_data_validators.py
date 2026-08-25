from __future__ import annotations

import importlib.util
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CANDIDATE = load_module(
    "candidate_validator",
    ROOT / "skills" / "d-data-analysis-semantic-layer" / "scripts" / "validate_candidate.py",
)
DATASET = load_module(
    "dataset_validator",
    ROOT / "skills" / "d-official-market-analysis" / "scripts" / "validate_dataset.py",
)


def valid_candidate() -> dict[str, object]:
    return {
        "record_id": "D-02-2026-TEST",
        "target_section": "D-02",
        "conclusion": "A bounded test conclusion",
        "fact_type": "官方公开事实",
        "source_urls": ["https://example.com/source"],
        "source_publishers": ["Example publisher"],
        "data_cutoff": "2026-08-01",
        "data_period": "2026-07",
        "platforms": ["Example"],
        "regions": ["中国大陆"],
        "evidence_level": "S",
        "valid_until": "2026-12-31",
        "review_on": "2026-10-01",
        "status": "有效",
        "version": "1.0.0",
        "limitations": "Test-only fixture",
        "follow_up_metrics": ["Example metric"],
    }


def valid_dataset_row() -> dict[str, object]:
    return {field: "known" for field in DATASET.REQUIRED} | {
        "source_url": "https://example.com/source",
        "published_at": "2026-08-01",
        "retrieved_at": "2026-08-02",
        "data_period_start": "2026-07-01",
        "data_period_end": "2026-07-31",
        "evidence_level": "S",
        "metric_value": "1",
    }


class CandidateValidatorTests(unittest.TestCase):
    def test_empty_candidate_fails(self) -> None:
        self.assertIn("contains no records", "\n".join(CANDIDATE.validate([])))

    def test_scalar_record_fails_without_traceback(self) -> None:
        self.assertIn("must be an object", "\n".join(CANDIDATE.validate([42])))

    def test_hostless_url_fails(self) -> None:
        row = valid_candidate()
        row["source_urls"] = ["https:"]
        self.assertIn("invalid source URL", "\n".join(CANDIDATE.validate([row])))

    def test_compact_date_fails_strict_format(self) -> None:
        row = valid_candidate()
        row["data_cutoff"] = "20260801"
        self.assertIn("must use YYYY-MM-DD", "\n".join(CANDIDATE.validate([row])))

    def test_as_of_detects_overdue_effective_status(self) -> None:
        row = valid_candidate()
        errors = CANDIDATE.validate([row], as_of=date(2026, 10, 1))
        self.assertIn("requires review", "\n".join(errors))

    def test_valid_candidate_passes(self) -> None:
        self.assertEqual(CANDIDATE.validate([valid_candidate()]), [])

    def test_published_records_match_release_as_of_state(self) -> None:
        records = CANDIDATE.load(
            ROOT
            / "skills"
            / "d-data-analysis-semantic-layer"
            / "references"
            / "records-v1.0.0.json"
        )
        self.assertEqual(CANDIDATE.validate(records, as_of=date(2026, 8, 25)), [])


class DatasetValidatorTests(unittest.TestCase):
    def test_all_blank_record_fails(self) -> None:
        row = {field: "" for field in DATASET.REQUIRED}
        errors, _ = DATASET.validate([row])
        self.assertIn("no usable evidence", "\n".join(errors))

    def test_hostless_url_fails(self) -> None:
        row = valid_dataset_row()
        row["source_url"] = "https:"
        errors, _ = DATASET.validate([row])
        self.assertIn("http(s) original link", "\n".join(errors))

    def test_compact_date_fails(self) -> None:
        row = valid_dataset_row()
        row["published_at"] = "20260801"
        errors, _ = DATASET.validate([row])
        self.assertIn("must use YYYY-MM-DD", "\n".join(errors))

    def test_valid_record_passes(self) -> None:
        errors, _ = DATASET.validate([valid_dataset_row()])
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
