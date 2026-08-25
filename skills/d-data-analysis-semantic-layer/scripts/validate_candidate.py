#!/usr/bin/env python3
"""Validate D semantic-layer candidate records; this script never grants approval."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REQUIRED = {
    "record_id", "target_section", "conclusion", "fact_type", "source_urls",
    "source_publishers", "data_cutoff", "data_period", "platforms", "regions",
    "evidence_level", "valid_until", "review_on", "status", "version",
    "limitations", "follow_up_metrics",
}
FACT_TYPES = {"官方公开事实", "平台官方解释", "权威第三方数据", "行业案例", "数据推断", "尚未验证的市场观察"}
STATUSES = {"有效", "待复查", "已过期", "已被新数据替代", "证据不足", "存在争议"}
LEVELS = {"S", "A", "B", "C", "D"}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TARGET_PATTERN = re.compile(r"^D-\d{2}$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
STRING_FIELDS = {
    "record_id", "target_section", "conclusion", "fact_type", "data_cutoff",
    "data_period", "evidence_level", "valid_until", "review_on", "status",
    "version", "limitations",
}
LIST_FIELDS = {"source_urls", "source_publishers", "platforms", "regions", "follow_up_metrics"}


def load(path: Path) -> list[object]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        records: list[object] = []
        for line_no, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {line_no}: invalid JSON: {exc}") from exc
        return records
    payload = json.loads(text)
    return payload if isinstance(payload, list) else [payload]


def parse_strict_date(value: object) -> date:
    text = str(value).strip()
    if not DATE_PATTERN.fullmatch(text):
        raise ValueError("must use YYYY-MM-DD")
    return date.fromisoformat(text)


def valid_http_url(value: object) -> bool:
    parsed = urlparse(str(value).strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.hostname)


def validate(records: list[object], as_of: date | None = None) -> list[str]:
    errors: list[str] = []
    if not records:
        return ["candidate contains no records"]
    seen_ids: set[str] = set()
    for index, row in enumerate(records, 1):
        if not isinstance(row, dict):
            errors.append(f"row {index}: record must be an object")
            continue
        missing = sorted(REQUIRED - set(row))
        if missing:
            errors.append(f"row {index}: missing {', '.join(missing)}")
            continue
        for field in sorted(STRING_FIELDS):
            if not isinstance(row[field], str) or not row[field].strip():
                errors.append(f"row {index}: {field} must be a non-empty string")
        for field in sorted(LIST_FIELDS):
            value = row[field]
            if not isinstance(value, list) or not value:
                errors.append(f"row {index}: {field} must be a non-empty list")
            elif any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"row {index}: {field} entries must be non-empty strings")

        record_id = str(row["record_id"]).strip()
        if record_id in seen_ids:
            errors.append(f"row {index}: duplicate record_id {record_id!r}")
        seen_ids.add(record_id)
        if not TARGET_PATTERN.fullmatch(str(row["target_section"]).strip()):
            errors.append(f"row {index}: target_section must use D-NN")
        if not VERSION_PATTERN.fullmatch(str(row["version"]).strip()):
            errors.append(f"row {index}: version must use X.Y.Z")

        level = str(row["evidence_level"]).upper()
        if level not in LEVELS:
            errors.append(f"row {index}: invalid evidence_level")
        if row["fact_type"] not in FACT_TYPES:
            errors.append(f"row {index}: invalid fact_type")
        if row["status"] not in STATUSES:
            errors.append(f"row {index}: invalid status")
        if level == "D" and row["target_section"] != "D-09":
            errors.append(f"row {index}: D evidence must target D-09")
        parsed_dates: dict[str, date] = {}
        for field in ("data_cutoff", "valid_until", "review_on"):
            try:
                parsed_dates[field] = parse_strict_date(row[field])
            except ValueError:
                errors.append(f"row {index}: {field} must use YYYY-MM-DD")
        if len(parsed_dates) == 3:
            if parsed_dates["data_cutoff"] > parsed_dates["review_on"]:
                errors.append(f"row {index}: data_cutoff is after review_on")
            if parsed_dates["review_on"] > parsed_dates["valid_until"]:
                errors.append(f"row {index}: review_on is after valid_until")
            if as_of is not None:
                if row["status"] == "有效" and as_of >= parsed_dates["review_on"]:
                    errors.append(f"row {index}: status 有效 requires review before the as-of date")
                if as_of > parsed_dates["valid_until"] and row["status"] not in {
                    "已过期", "已被新数据替代"
                }:
                    errors.append(f"row {index}: status conflicts with expired valid_until")
        urls = row["source_urls"]
        if isinstance(urls, list):
            for url in urls:
                if not valid_http_url(url):
                    errors.append(f"row {index}: invalid source URL {url!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--as-of", type=parse_strict_date, help="Evaluate review and expiry state on YYYY-MM-DD")
    args = parser.parse_args()
    try:
        records = load(args.candidate)
        errors = validate(records, as_of=args.as_of)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for error in errors:
        print(f"ERROR: {error}")
    print(json.dumps({"records": len(records), "errors": len(errors), "approval_granted": False}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
