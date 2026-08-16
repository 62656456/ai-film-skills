#!/usr/bin/env python3
"""Validate D market-analysis CSV or JSONL source records using only stdlib."""

from __future__ import annotations

import csv
import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = [
    "source_name", "source_type", "publisher", "source_url", "published_at",
    "retrieved_at", "data_period_start", "data_period_end", "region", "platform",
    "content_type", "metric_name", "metric_value", "metric_unit", "statistical_scope",
    "methodology", "sample_size", "evidence_level", "raw_excerpt", "limitations",
]
DATE_FIELDS = ["published_at", "retrieved_at", "data_period_start", "data_period_end"]
LEVELS = {"S", "A", "B", "C", "D"}


def load_records(path: Path) -> list[dict[str, object]]:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        records = []
        with path.open("r", encoding="utf-8-sig") as handle:
            for line_no, line in enumerate(handle, 1):
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError as exc:
                        raise ValueError(f"line {line_no}: invalid JSON: {exc}") from exc
        return records
    raise ValueError("expected .csv, .jsonl, or .ndjson")


def is_blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def validate(records: list[dict[str, object]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not records:
        return ["dataset contains no records"], warnings
    seen: set[tuple[str, ...]] = set()
    for index, row in enumerate(records, 1):
        if not isinstance(row, dict):
            errors.append(f"row {index}: record is not an object")
            continue
        missing_columns = [field for field in REQUIRED if field not in row]
        if missing_columns:
            errors.append(f"row {index}: missing columns: {', '.join(missing_columns)}")
        for field in REQUIRED:
            if field in row and is_blank(row[field]):
                warnings.append(f"row {index}: blank {field}")
        for field in DATE_FIELDS:
            value = row.get(field)
            if not is_blank(value):
                try:
                    date.fromisoformat(str(value))
                except ValueError:
                    errors.append(f"row {index}: {field} must use YYYY-MM-DD")
        start, end = row.get("data_period_start"), row.get("data_period_end")
        if not is_blank(start) and not is_blank(end):
            try:
                if date.fromisoformat(str(start)) > date.fromisoformat(str(end)):
                    errors.append(f"row {index}: data period start is after end")
            except ValueError:
                pass
        level = str(row.get("evidence_level", "")).strip().upper()
        if level and level not in LEVELS:
            errors.append(f"row {index}: invalid evidence_level {level!r}")
        url = str(row.get("source_url", "")).strip()
        if url and urlparse(url).scheme not in {"http", "https"}:
            errors.append(f"row {index}: source_url must be an http(s) original link")
        key = tuple(str(row.get(field, "")).strip() for field in
                    ("source_url", "data_period_start", "data_period_end", "platform", "metric_name", "metric_value"))
        if key in seen:
            warnings.append(f"row {index}: possible duplicate record")
        seen.add(key)
    return errors, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_dataset.py <dataset.csv|dataset.jsonl>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        records = load_records(path)
        errors, warnings = validate(records)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}")
    print(json.dumps({"records": len(records), "errors": len(errors), "warnings": len(warnings)}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

