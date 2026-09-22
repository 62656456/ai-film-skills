#!/usr/bin/env python3
"""Validate that one Skill version is a complete, isolated runtime package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path


BACKTICK_PATH_RE = re.compile(
    r"`(?P<path>(?:references|agents|scripts|assets)[/\\][^`]+|[^`/\\]+\.(?:md|json|ya?ml))`",
    re.IGNORECASE,
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\((?P<path>[^)]+)\)")
FORBIDDEN_RUNTIME_PATH_RE = re.compile(
    r"(?:^|[\s`'\"(])(?:\.\.?[/\\])?(?:versions|history)[/\\]",
    re.IGNORECASE,
)
EXTERNAL_LOCAL_PATH_RE = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:[/\\][^\s`'\"<>|]+")
LEGACY_RUNTIME_DELEGATION_RE = re.compile(
    r"(?:运行时|执行时|使用时|生成时)?.{0,8}(?:读取|调用|参照|沿用|继承|连接|跳转).{0,20}"
    r"(?:旧版|旧版本|父版本|上一版|上个版本|旧Skill|旧技能|B技能|B\s*Skill)",
    re.IGNORECASE,
)
NEGATED_DELEGATION_RE = re.compile(r"不得|禁止|不允许|不能|不要求|不读取|不调用|不参照|不沿用|不继承|不连接|不跳转|无需")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def normalize_relative(raw: str) -> str:
    value = raw.strip().strip("<>").split("#", 1)[0].split("?", 1)[0]
    return value.replace("\\", "/").rstrip(".,;:")


def declared_references(text: str) -> set[str]:
    found = {normalize_relative(match.group("path")) for match in BACKTICK_PATH_RE.finditer(text)}
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw = normalize_relative(match.group("path"))
        if raw and not raw.startswith(("#", "http://", "https://", "mailto:")):
            found.add(raw)
    return {item for item in found if item}


def resolve_declared_reference(version_root: Path, source: Path, raw: str) -> Path:
    if raw.startswith(("references/", "agents/", "scripts/", "assets/")):
        return version_root / raw
    return source.parent / raw


def validate_core(version_root: Path) -> dict:
    root = version_root.resolve()
    manifest_path = root / "VERSION_MANIFEST.json"
    errors: list[dict] = []
    checked_refs: list[dict] = []

    if not manifest_path.exists():
        return {"ready": False, "version_root": str(root), "errors": [{"code": "MANIFEST_MISSING"}]}

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "ready": False,
            "version_root": str(root),
            "errors": [{"code": "MANIFEST_INVALID", "detail": str(exc)}],
        }

    expected_skill = str(manifest.get("skill", "")).strip()
    if not expected_skill:
        errors.append({"code": "SKILL_NAME_MISSING_IN_MANIFEST"})
    if manifest.get("self_contained") is not True:
        errors.append({"code": "SELF_CONTAINED_NOT_TRUE"})
    if manifest.get("cross_version_runtime_references_allowed") is not False:
        errors.append({"code": "CROSS_VERSION_POLICY_NOT_FALSE"})

    runtime_files = manifest.get("runtime_files")
    if not isinstance(runtime_files, list) or not runtime_files:
        errors.append({"code": "RUNTIME_FILES_EMPTY"})
        runtime_files = []

    runtime_paths: list[str] = []
    for entry in runtime_files:
        relative = normalize_relative(str(entry.get("path", "")))
        if not relative:
            errors.append({"code": "RUNTIME_PATH_EMPTY"})
            continue
        runtime_paths.append(relative)
    runtime_set = set(runtime_paths)
    if len(runtime_set) != len(runtime_paths):
        errors.append({"code": "RUNTIME_PATH_DUPLICATE"})

    skill_files = [path for path in root.rglob("SKILL.md") if path.is_file()]
    resolved_skill_files = {path.resolve() for path in skill_files}
    if len(skill_files) != 1 or (root / "SKILL.md").resolve() not in resolved_skill_files:
        errors.append(
            {"code": "SKILL_ENTRYPOINT_COUNT_INVALID", "expected": 1, "actual": len(skill_files)}
        )

    for entry in runtime_files:
        relative = normalize_relative(str(entry.get("path", "")))
        if not relative:
            continue
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            errors.append({"code": "RUNTIME_PATH_ESCAPES_VERSION", "path": relative})
            continue
        if not path.exists() or not path.is_file():
            errors.append({"code": "RUNTIME_FILE_MISSING", "path": relative})
            continue
        if path.is_symlink():
            errors.append({"code": "RUNTIME_SYMLINK_FORBIDDEN", "path": relative})
        actual = sha256(path)
        expected = str(entry.get("sha256", "")).upper()
        if actual != expected:
            errors.append(
                {"code": "RUNTIME_HASH_MISMATCH", "path": relative, "expected": expected, "actual": actual}
            )

        if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"\.\.[/\\]", text):
            errors.append({"code": "PARENT_REFERENCE_FORBIDDEN", "path": relative})
        if FORBIDDEN_RUNTIME_PATH_RE.search(text):
            errors.append({"code": "CROSS_VERSION_REFERENCE_FORBIDDEN", "path": relative})
        for line_number, line in enumerate(text.splitlines(), start=1):
            if LEGACY_RUNTIME_DELEGATION_RE.search(line) and not NEGATED_DELEGATION_RE.search(line):
                errors.append(
                    {
                        "code": "LEGACY_RUNTIME_DELEGATION_FORBIDDEN",
                        "path": relative,
                        "line": line_number,
                        "text": line.strip(),
                    }
                )
        for match in EXTERNAL_LOCAL_PATH_RE.finditer(text):
            errors.append(
                {"code": "ABSOLUTE_LOCAL_REFERENCE_FORBIDDEN", "path": relative, "target": match.group(0)}
            )

        for raw in sorted(declared_references(text)):
            target = resolve_declared_reference(root, path, raw).resolve()
            try:
                target_relative = target.relative_to(root).as_posix()
            except ValueError:
                errors.append({"code": "DECLARED_REFERENCE_ESCAPES_VERSION", "source": relative, "target": raw})
                continue
            exists = target.exists() and target.is_file()
            in_manifest = target_relative in runtime_set
            checked_refs.append(
                {
                    "source": relative,
                    "target": raw,
                    "resolved": target_relative,
                    "exists": exists,
                    "in_runtime_manifest": in_manifest,
                }
            )
            if not exists:
                errors.append({"code": "DECLARED_REFERENCE_MISSING", "source": relative, "target": raw})
            elif not in_manifest:
                errors.append(
                    {"code": "DECLARED_REFERENCE_NOT_IN_RUNTIME_MANIFEST", "source": relative, "target": raw}
                )

    skill_path = root / "SKILL.md"
    if skill_path.exists():
        skill_text = skill_path.read_text(encoding="utf-8")
        frontmatter = skill_text.split("---", 2)[1] if skill_text.startswith("---\n") else ""
        if not frontmatter or not re.search(
            rf"(?m)^name:\s*[\"']?{re.escape(expected_skill)}[\"']?\s*$", frontmatter
        ):
            errors.append({"code": "SKILL_FRONTMATTER_INVALID"})

    unique_refs = {
        (item["source"], item["resolved"])
        for item in checked_refs
        if item.get("resolved")
    }
    return {
        "ready": not errors,
        "skill": expected_skill,
        "version": manifest.get("version"),
        "version_root": str(root),
        "runtime_file_count": len(runtime_set),
        "declared_reference_count": len(unique_refs),
        "declared_references": checked_refs,
        "errors": errors,
    }


def validate_isolated_copy(version_root: Path) -> dict:
    root = version_root.resolve()
    manifest_path = root / "VERSION_MANIFEST.json"
    if not manifest_path.exists():
        return {"ready": False, "errors": [{"code": "ISOLATION_MANIFEST_MISSING"}]}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix=f".{root.name}-isolated-", dir=root.parent) as temp_dir:
        isolated = Path(temp_dir) / root.name
        isolated.mkdir()
        shutil.copy2(manifest_path, isolated / "VERSION_MANIFEST.json")
        for entry in manifest.get("runtime_files", []):
            relative = normalize_relative(str(entry.get("path", "")))
            if not relative:
                continue
            source = root / relative
            destination = isolated / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.exists() and source.is_file():
                shutil.copy2(source, destination)
        isolated_result = validate_core(isolated)
        return {
            "ready": isolated_result["ready"],
            "copied_runtime_file_count": len(manifest.get("runtime_files", [])),
            "parent_or_sibling_versions_present": False,
            "errors": isolated_result["errors"],
        }


def validate(version_root: Path, run_isolation: bool = True) -> dict:
    result = validate_core(version_root)
    if run_isolation and result["ready"]:
        isolation = validate_isolated_copy(version_root)
        result["isolated_copy"] = isolation
        if not isolation["ready"]:
            result["ready"] = False
            result["errors"].append({"code": "ISOLATED_COPY_VALIDATION_FAILED"})
    else:
        result["isolated_copy"] = {"ready": None, "skipped": True}
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("version_root")
    parser.add_argument("--skip-isolation", action="store_true")
    args = parser.parse_args()
    result = validate(Path(args.version_root), run_isolation=not args.skip_isolation)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ready"] else 1)


if __name__ == "__main__":
    main()
