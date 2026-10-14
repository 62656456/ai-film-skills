#!/usr/bin/env python3
"""Offline shortlist, selected-mechanism retrieval and explicit variable binding.

This is a reference lookup, not a director, model selector, media generator or
artistic judge. An adopted design is compiled from its saved photography notes;
the compiler must not run search again or replace locked shots.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from string import Formatter
import sys

LIBRARY = Path(__file__).resolve().parents[1] / "assets/fcml-motion-library.json"
OPERATIONS = {"translation", "orientation", "focal_length", "focus", "time", "composition", "post"}
UNFINISHED = {"todo", "tbd", "pending", "待填", "占位", "...", "待补"}


class LibraryError(ValueError):
    pass


def meaningful_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value.strip().lower() not in UNFINISHED


def load_library(path: Path = LIBRARY) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_summary(library: dict) -> dict:
    audit = library["source_audit"]
    records = library["source_records"]
    complete = audit.get("enumeration_complete") is True
    count = len(records)
    read_count = sum(r.get("full_prompt_read") is True for r in records)
    mapped = sum(bool(r.get("canonical_id")) for r in records)
    return {
        "status": audit.get("status"), "enumeration_complete": complete,
        "scope": audit.get("enumeration_scope"), "retrieved_at_utc": audit.get("retrieved_at_utc"),
        "advertised_homepage": audit.get("homepage_advertised_counts"),
        "advertised_system_descriptions": [
            {"id": s["id"], "categories": s.get("advertised_categories"), "items": s.get("advertised_items")}
            for s in audit["systems"]],
        "actual_systems": len(audit["systems"]), "actual_categories": len(audit["categories"]),
        "catalog_count": count, "full_content_read_count": read_count,
        "canonical_count": len(library["motions"]), "mapped_source_count": mapped,
        "coverage_denominator": count if complete else None,
        "directory_coverage": 1.0 if complete else None,
        "full_content_coverage": read_count / count if complete and count else None,
        "duplicate_groups": audit.get("exact_duplicate_groups", []),
        "gaps": [{"source_id": r["source_id"], "full_prompt_read": r.get("full_prompt_read", False),
                  "canonical_id": r.get("canonical_id"), "reason": r.get("missing_reason")}
                 for r in records if not r.get("full_prompt_read") or not r.get("canonical_id")],
        "missing_items": audit.get("missing_items", []),
        "platform_verification": audit.get("platform_verification"),
    }


def validate_library(library: dict) -> list[str]:
    """Validate evidence/mapping coherence; no automatic semantic/artistic pass."""
    errors = []
    try:
        records, motions, audit = library["source_records"], library["motions"], library["source_audit"]
        source_ids = [r["source_id"] for r in records]
        ids = [m["id"] for m in motions]
        if len(set(source_ids)) != len(source_ids):
            errors.append("duplicate_source_id")
        if len(set(ids)) != len(ids):
            errors.append("duplicate_canonical_id")
        by_id = {m["id"]: m for m in motions}
        by_source = {r["source_id"]: r for r in records}
        for row in records:
            sid, cid = row["source_id"], row.get("canonical_id")
            if cid:
                if cid not in by_id or sid not in by_id[cid].get("source_ids", []):
                    errors.append(f"source_mapping:{sid}")
            elif not meaningful_text(row.get("missing_reason")):
                errors.append(f"unexplained_mapping_gap:{sid}")
            if row.get("full_prompt_read"):
                if not row.get("complete_prompt_available") or not re.fullmatch(
                        r"[0-9a-f]{64}", row.get("prompt_sha256", "")):
                    errors.append(f"unsupported_full_read:{sid}")
            elif not meaningful_text(row.get("missing_reason")):
                errors.append(f"unexplained_unread:{sid}")
            original = row.get("duplicate_of")
            if original:
                other = by_source.get(original, {})
                if (row.get("duplicate_kind") != "exact_prompt"
                        or row.get("prompt_sha256") != other.get("prompt_sha256")
                        or row.get("canonical_id") != other.get("canonical_id")):
                    errors.append(f"invalid_duplicate_mapping:{sid}")
        for motion in motions:
            mid = motion["id"]
            for key in ("name", "purpose", "attention_change", "template_zh", "trigger", "speed_and_pauses"):
                if not meaningful_text(motion.get(key)):
                    errors.append(f"unusable_text:{mid}:{key}")
            kinds = motion.get("operation_types", [])
            actual_kinds = list(dict.fromkeys(op["type"] for op in motion.get("operations", [])))
            if not kinds or set(kinds) - OPERATIONS or kinds != actual_kinds:
                errors.append(f"operation_classification:{mid}")
            if not motion.get("source_ids") or any(s not in by_source or by_source[s].get("canonical_id") != mid
                                                   for s in motion["source_ids"]):
                errors.append(f"canonical_mapping:{mid}")
            placeholders = [field for _, field, _, _ in Formatter().parse(motion.get("template_zh", "")) if field]
            if set(placeholders) != set(motion.get("variables", [])):
                errors.append(f"variables_mismatch:{mid}")
            for clause in motion.get("optional_clauses", []):
                fields = {f for _, f, _, _ in Formatter().parse(clause.get("template_zh", "")) if f}
                if fields != set(clause.get("variables", [])) or clause.get("position") != "before_end":
                    errors.append(f"optional_clause_mismatch:{mid}")
            if len(set(placeholders) - {"起始构图", "终点构图", "环境承接"}) == 0:
                errors.append(f"mechanism_missing:{mid}")
            phases = motion.get("phases", [])
            if [p.get("stage") for p in phases] != ["start", "process", "end"]:
                errors.append(f"phases_missing:{mid}")
            elif not meaningful_text(phases[1].get("camera_and_attention")):
                errors.append(f"process_missing:{mid}")
            if any(not motion.get(key) or any(not meaningful_text(x) for x in motion[key])
                   for key in ("constraints", "common_errors", "applicable_space", "implementation_options")):
                errors.append(f"implementation_missing:{mid}")
        summary = audit_summary(library)
        for key in ("catalog_count", "full_content_read_count", "canonical_count", "mapped_source_count"):
            if key in audit and audit[key] != summary[key]:
                errors.append(f"stale_audit_count:{key}")
        if audit.get("enumeration_complete") is not True:
            for key in ("coverage_denominator", "directory_coverage", "full_content_coverage"):
                if audit.get(key) is not None:
                    errors.append(f"unverified_denominator:{key}")
            if str(audit.get("status", "")).startswith("complete"):
                errors.append("incomplete_enumeration_claimed_complete")
        else:
            declared = sum(c["actual_items"] for c in audit["categories"])
            system_total = sum(s["actual_items"] for s in audit["systems"])
            if declared != len(records) or system_total != len(records):
                errors.append("catalog_totals_disagree")
            if audit.get("coverage_denominator") != len(records):
                errors.append("complete_denominator_disagrees")
        if str(audit.get("status", "")).startswith("complete") and (
                summary["gaps"] or audit.get("missing_items")):
            errors.append("content_or_mapping_gap_claimed_complete")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid_schema:{exc}")
    return errors


def get_motion(library: dict, identifier: str) -> dict:
    source = next((r for r in library["source_records"] if r["source_id"] == identifier), None)
    canonical = source.get("canonical_id") if source else identifier
    found = next((m for m in library["motions"] if m["id"] == canonical), None)
    if found is None:
        raise LibraryError(f"Unknown or unmapped mechanism: {identifier}")
    return found


def search(library: dict, query: str = "", operations: list[str] | None = None, limit: int = 6) -> list[dict]:
    if not 1 <= limit <= 30:
        raise LibraryError("Shortlist limit must be between 1 and 30; use get for selected mechanisms")
    operations = operations or []
    if set(operations) - OPERATIONS:
        raise LibraryError("Unknown operation type")
    tokens = [s.lower() for s in re.split(r"\s+", query.strip()) if s]
    ranked = []
    for motion in library["motions"]:
        if set(operations) - set(motion["operation_types"]):
            continue
        haystack = " ".join([motion["id"], motion["name"], motion["purpose"], *motion["aliases"],
                             *motion["source_ids"], *motion["applicable_space"]]).lower()
        score = sum(4 if token in motion["name"].lower() else 2 if token in haystack else 0 for token in tokens)
        if tokens and not score:
            continue
        ranked.append((score, motion))
    ranked.sort(key=lambda row: (-row[0], row[1]["id"]))
    return [{key: motion[key] for key in ("id", "name", "purpose", "operation_types", "complexity", "effect_policy")}
            for _, motion in ranked[:limit]]


def adapt(motion: dict, context: dict) -> str:
    variables = context.get("variables", {})
    if not isinstance(variables, dict):
        raise LibraryError("variables must be an object populated from current scene/directing decisions")
    missing = [key for key in motion["variables"] if not meaningful_text(variables.get(key))]
    if missing:
        raise LibraryError("Unbound current-scene variables: " + ", ".join(missing))
    policy = motion["effect_policy"]
    adopted = context.get("adopted_effects", [])
    if not isinstance(adopted, list) or any(not isinstance(x, str) for x in adopted):
        raise LibraryError("adopted_effects must list existing explicit adoption decisions")
    if policy["requires_explicit_adoption"] and policy["kind"] not in adopted:
        raise LibraryError(f"Effect not adopted in this design: {policy['kind']}")
    if motion["medium_policy"]["explicit_transition_required"] and context.get("approved_medium_transition") is not True:
        raise LibraryError("A locked medium cannot be changed without an existing adopted transition")
    result = motion["template_zh"].format_map(variables)
    for clause in motion.get("optional_clauses", []):
        provided = [key for key in clause["variables"] if key in variables]
        if not provided:
            continue
        if any(not meaningful_text(variables.get(key)) for key in clause["variables"]):
            raise LibraryError("Incomplete optional existing-design handoff: " + ", ".join(clause["variables"]))
        phrase = clause["template_zh"].format_map(variables)
        result = result.replace("。最终", "；" + phrase + "。最终", 1)
    if re.search(r"\{[^{}]+\}", result):
        raise LibraryError("Bound values contain unresolved placeholders")
    return result


def main() -> int:
    # The JSON CLI emits readable Chinese even when a Windows pipe defaults to a legacy codec.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    find = subs.add_parser("search", help="Read a small shortlist; does not adopt a shot")
    find.add_argument("--query", default="")
    find.add_argument("--operation", action="append", choices=sorted(OPERATIONS), default=[])
    find.add_argument("--limit", type=int, default=6)
    get = subs.add_parser("get", help="Read selected canonical or source IDs only")
    get.add_argument("--id", action="append", required=True)
    render = subs.add_parser("adapt", help="Bind a selected mechanism to existing scene variables")
    render.add_argument("--id", required=True)
    render.add_argument("--input", type=Path, required=True)
    subs.add_parser("audit", help="Show live counts derived from the bundled ledger")
    subs.add_parser("validate", help="Check evidence, mappings and usable structure")
    args = parser.parse_args()
    try:
        library = load_library()
        if args.command == "search":
            result = {"selection_status": "candidates_only", "motions": search(library, args.query, args.operation, args.limit)}
        elif args.command == "get":
            result = {"selection_status": "retrieved_not_adopted", "motions": [get_motion(library, i) for i in args.id]}
        elif args.command == "adapt":
            motion = get_motion(library, args.id)
            context = json.loads(args.input.read_text(encoding="utf-8-sig"))
            result = {"id": motion["id"], "camera_paragraph": adapt(motion, context),
                      "verification": "variable_binding_only; spatial/semantic review and media execution not certified"}
        elif args.command == "audit":
            result = audit_summary(library)
        else:
            errors = validate_library(library)
            result = {"passed": not errors, "errors": errors,
                      "scope": "evidence/mapping/structure; not semantic or artistic acceptance"}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return int(bool(errors))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
