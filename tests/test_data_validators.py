from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
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

    def test_pending_review_status_matches_both_prose_views(self) -> None:
        references = ROOT / "skills/d-data-analysis-semantic-layer/references"
        records = CANDIDATE.load(references / "records-v1.0.0.json")
        record = next(item for item in records if item["record_id"] == "D-07-2026-URBAN-ROMANCE-SATURATION")
        self.assertEqual(record["status"], "待复查")
        evidence = (references / "evidence.md").read_text(encoding="utf-8")
        row = next(line for line in evidence.splitlines() if record["record_id"] in line)
        self.assertEqual(row.split("|")[6].strip(), record["status"])
        semantic = (references / "semantic-layer.md").read_text(encoding="utf-8")
        section = semantic.split("### 都市情感需求稳定，但同质化风险突出", 1)[1].split("###", 1)[0]
        self.assertIn(f"- 状态：{record['status']}。", section)


class DatasetValidatorTests(unittest.TestCase):
    def call(self, row: dict[str, object]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "dataset.jsonl"
            path.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
            process = subprocess.run([sys.executable, "-B", str(ROOT / "skills/d-official-market-analysis/scripts/validate_dataset.py"),
                                      str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15)
            self.assertFalse(process.stderr.strip(), process.stderr)
            return process

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

    def test_qualitative_excerpt_does_not_require_an_invented_metric(self) -> None:
        row = valid_dataset_row()
        row.update(metric_name="", metric_value="", metric_unit="", raw_excerpt="The platform announced a bounded policy change.")
        process = self.call(row)
        self.assertEqual(process.returncode, 0, process.stdout)
        self.assertEqual(json.loads(process.stdout.splitlines()[-1])["errors"], 0)

    def test_numeric_value_still_requires_a_metric_name_even_with_an_excerpt(self) -> None:
        row = valid_dataset_row()
        row.update(metric_name="", metric_value=0, raw_excerpt="The source also contains a qualitative statement.")
        process = self.call(row)
        self.assertEqual(process.returncode, 1, process.stdout)
        self.assertIn("metric_name is required when metric_value is provided", process.stdout)

    def test_qualitative_record_still_needs_the_full_column_schema(self) -> None:
        row = valid_dataset_row()
        row["metric_value"] = ""
        del row["metric_name"]
        errors, _ = DATASET.validate([row])
        self.assertIn("missing columns: metric_name", "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
