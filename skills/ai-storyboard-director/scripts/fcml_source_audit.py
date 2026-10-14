#!/usr/bin/env python3
"""Inspect an explicitly downloaded public FCML app; never fetch or ship its text.

Developer maintenance only. Reads the same data bound to expanded prompt cards,
emits hashes and inventory, and compares mappings without changing the library.
Raw HTML/JavaScript should live in the task's temporary directory and be removed
after reading. This tool cannot certify that a human read the prompts.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def extract_catalog(script: str) -> list[dict]:
    candidates = []
    escape = re.escape(chr(92))
    quoted_literal = "'(?:" + escape + ".|[^'" + escape + "])*'"
    pattern = r"JSON\.parse\((" + quoted_literal + r")\)"
    for match in re.finditer(pattern, script):
        try:
            value = json.loads(ast.literal_eval(match.group(1)))
        except (ValueError, SyntaxError, json.JSONDecodeError):
            continue
        if isinstance(value, list) and value and all(
                isinstance(row, dict) and isinstance(row.get("categories"), list) for row in value):
            candidates.append(value)
    if len(candidates) != 1:
        raise ValueError(f"Expected one public catalog, found {len(candidates)}; enumerate manually")
    return candidates[0]


def inspect(script: str, *, enumeration_verified: bool = False) -> dict:
    """A nonempty extracted subset alone never marks the denominator complete."""
    catalog = extract_catalog(script)
    records = []
    seen_prompts: dict[str, str] = {}
    seen_ids: set[str] = set()
    systems = []
    categories = []
    for si, system in enumerate(catalog):
        advertised = re.search(r"(\d+)\s*大类[、,，]\s*(\d+)\s*种", system.get("description", ""))
        systems.append({"id": system["id"], "name": system["name"],
                        "advertised_categories": int(advertised[1]) if advertised else None,
                        "advertised_items": int(advertised[2]) if advertised else None,
                        "actual_categories": len(system["categories"]),
                        "actual_items": sum(len(c["items"]) for c in system["categories"])})
        for ci, category in enumerate(system["categories"]):
            categories.append({"id": category["id"], "name": category["name"],
                               "system_id": system["id"], "actual_items": len(category["items"])})
            for ii, item in enumerate(category["items"]):
                if item["id"] in seen_ids:
                    raise ValueError(f"Duplicate source ID: {item['id']}")
                seen_ids.add(item["id"])
                prompt = item.get("prompt", "")
                prompt_hash = sha256(prompt.encode("utf-8")) if isinstance(prompt, str) and prompt.strip() else None
                duplicate_of = seen_prompts.get(prompt_hash) if prompt_hash else None
                if prompt_hash and not duplicate_of:
                    seen_prompts[prompt_hash] = item["id"]
                records.append({"source_id": item["id"], "name": item["name"],
                                "system_id": system["id"], "category_id": category["id"],
                                "original_category": category["name"],
                                "locator": f"systems[{si}].categories[{ci}].items[{ii}] id={item['id']}",
                                "complete_prompt_available": bool(prompt_hash),
                                "prompt_sha256": prompt_hash,
                                "prompt_characters": len(prompt) if isinstance(prompt, str) else 0,
                                "duplicate_of": duplicate_of})
    return {"enumeration_complete": enumeration_verified,
            "enumeration_scope": "public homepage catalog in the supplied application bundle",
            "coverage_denominator": len(records) if enumeration_verified else None,
            "catalog_count": len(records),
            "full_content_available_count": sum(r["complete_prompt_available"] for r in records),
            "directory_coverage": 1.0 if enumeration_verified else None,
            "full_content_coverage": (sum(r["complete_prompt_available"] for r in records) / len(records)
                                      if enumeration_verified and records else None),
            "systems": systems, "categories": categories, "records": records}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--bundle-url", required=True)
    parser.add_argument("--html", type=Path)
    parser.add_argument("--library", type=Path)
    parser.add_argument("--enumeration-verified", action="store_true",
                        help="Only after checking the app lists this entire catalog without omitted pages/requests")
    args = parser.parse_args()
    try:
        raw = args.bundle.read_bytes()
        result = inspect(raw.decode("utf-8-sig"), enumeration_verified=args.enumeration_verified)
        result.update({"bundle_url": args.bundle_url, "bundle_sha256": sha256(raw),
                       "audit_time_utc": datetime.now(timezone.utc).isoformat()})
        if args.html:
            result["html_sha256"] = sha256(args.html.read_bytes())
        if args.library:
            library = json.loads(args.library.read_text(encoding="utf-8"))
            previous = {r["source_id"]: r for r in library["source_records"]}
            current = {r["source_id"]: r for r in result["records"]}
            result["comparison"] = {
                "added_ids": sorted(current.keys() - previous.keys()),
                "removed_ids": sorted(previous.keys() - current.keys()),
                "changed_prompt_ids": sorted(k for k in current.keys() & previous.keys()
                                             if current[k]["prompt_sha256"] != previous[k]["prompt_sha256"]),
                "mapping_gaps": sorted(k for k, v in current.items()
                                       if k not in previous or not previous[k].get("canonical_id")),
            }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
