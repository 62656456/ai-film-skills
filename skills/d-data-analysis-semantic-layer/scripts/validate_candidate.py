#!/usr/bin/env python3
"""Validate D semantic-layer candidate records; this script never grants approval."""

from __future__ import annotations

import json
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


def load(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    payload = json.loads(text)
    return payload if isinstance(payload, list) else [payload]


def validate(records: list[dict]) -> list[str]:
    errors: list[str] = []
    for index, row in enumerate(records, 1):
        missing = sorted(REQUIRED - set(row))
        if missing:
            errors.append(f"row {index}: missing {', '.join(missing)}")
            continue
        level = str(row["evidence_level"]).upper()
        if level not in LEVELS:
            errors.append(f"row {index}: invalid evidence_level")
        if row["fact_type"] not in FACT_TYPES:
            errors.append(f"row {index}: invalid fact_type")
        if row["status"] not in STATUSES:
            errors.append(f"row {index}: invalid status")
        if level == "D" and row["target_section"] != "D-09":
            errors.append(f"row {index}: D evidence must target D-09")
        for field in ("data_cutoff", "valid_until", "review_on"):
            try:
                date.fromisoformat(str(row[field]))
            except ValueError:
                errors.append(f"row {index}: {field} must use YYYY-MM-DD")
        urls = row["source_urls"]
        if not isinstance(urls, list) or not urls:
            errors.append(f"row {index}: source_urls must be a non-empty list")
        else:
            for url in urls:
                if urlparse(str(url)).scheme not in {"http", "https"}:
                    errors.append(f"row {index}: invalid source URL {url!r}")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_candidate.py <candidate.json|candidate.jsonl>", file=sys.stderr)
        return 2
    try:
        records = load(Path(sys.argv[1]))
        errors = validate(records)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for error in errors:
        print(f"ERROR: {error}")
    print(json.dumps({"records": len(records), "errors": len(errors), "approval_granted": False}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

