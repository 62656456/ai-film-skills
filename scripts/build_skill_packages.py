#!/usr/bin/env python3
"""Build deterministic, host-neutral ZIP packages for every Skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import validate_skill_independence as independence

from repository_safety import (
    SafetyError,
    commit_staging_output,
    create_staging_output,
    package_source_files,
    remove_owned_output,
    validate_output_target,
)


ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def skill_dirs(base: Path) -> list[Path]:
    if not base.is_dir():
        return []
    return sorted(
        child for child in base.iterdir() if child.is_dir() and (child / "SKILL.md").is_file()
    )


def package_files(skill: Path) -> list[Path]:
    return package_source_files(skill)


def write_file(archive: zipfile.ZipFile, source: Path, arcname: str) -> None:
    info = zipfile.ZipInfo(arcname, FIXED_TIME)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, source.read_bytes())


def verify_archive(path: Path, expected_entry: str) -> None:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"corrupt ZIP entry in {path.name}: {bad}")
        if expected_entry not in archive.namelist():
            raise RuntimeError(f"{path.name} is missing {expected_entry}")


def build_one(skill: Path, output: Path) -> dict[str, object]:
    archive_path = output / f"{skill.name}.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for path in package_files(skill):
            rel = path.relative_to(skill).as_posix()
            write_file(archive, path, f"{skill.name}/{rel}")
    verify_archive(archive_path, f"{skill.name}/SKILL.md")
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    return {
        "name": skill.name,
        "file": archive_path.name,
        "bytes": archive_path.stat().st_size,
        "sha256": digest,
    }


def build_complete(skills: list[Path], output: Path) -> dict[str, object]:
    archive_path = output / "open-film-skills-complete.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for skill in skills:
            for path in package_files(skill):
                rel = path.relative_to(skill).as_posix()
                write_file(archive, path, f"skills/{skill.name}/{rel}")
    verify_archive(archive_path, "skills/director-agent/SKILL.md")
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    return {
        "name": "open-film-skills-complete",
        "file": archive_path.name,
        "bytes": archive_path.stat().st_size,
        "sha256": digest,
    }


def source_commit() -> str:
    github_sha = os.environ.get("GITHUB_SHA")
    if github_sha:
        return github_sha
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def source_tree_state() -> str:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return "unknown"
    return "dirty" if result.stdout.strip() else "clean"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "skills")
    parser.add_argument("--include-experimental", action="store_true")
    parser.add_argument(
        "--allow-external-output",
        action="store_true",
        help="Allow a reviewed external output that is empty or already owned by this tool",
    )
    args = parser.parse_args()

    independent_skills = independence.skill_dirs()
    independent_names = {independence.frontmatter_name(skill) for skill in independent_skills}
    independence_errors = [
        error
        for skill in independent_skills
        for error in independence.validate_skill(skill, independent_names)
    ]
    if independence_errors:
        print("Build refused: one or more Skill packages are not self-contained", file=sys.stderr)
        for error in independence_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    try:
        output = validate_output_target(
            args.output, ROOT, allow_external=args.allow_external_output
        )
        staging = create_staging_output(output)
    except (OSError, SafetyError) as exc:
        print(f"Build refused: {exc}", file=sys.stderr)
        return 2

    try:
        stable = skill_dirs(ROOT / "skills")
        experimental = skill_dirs(ROOT / "experimental") if args.include_experimental else []
        packages: list[dict[str, object]] = []
        for skill in stable:
            item = build_one(skill, staging)
            item["status"] = "packaged"
            packages.append(item)
        for skill in experimental:
            item = build_one(skill, staging)
            item["status"] = "experimental"
            packages.append(item)
        packages.append(build_complete(stable, staging))

        contract = ROOT / "docs" / "skill-contracts.json"
        manifest = {
            "schema_version": 3,
            "package_standard": "Agent Skills compatible SKILL.md folder",
            "source_commit": source_commit(),
            "source_tree_state": source_tree_state(),
            "contract_sha256": hashlib.sha256(contract.read_bytes()).hexdigest(),
            "native_layouts": ["codex", "claude-code", "trae", "codebuddy"],
            "official_upload_hosts": ["workbuddy"],
            "generic_fallback": "attach SKILL.md and local resources as Agent instructions",
            "stable_skill_count": len(stable),
            "experimental_skill_count": len(experimental),
            "packages": packages,
        }
        (staging / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        commit_staging_output(staging, output)
    except Exception as exc:
        if staging.exists():
            remove_owned_output(staging)
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    print(f"Built and verified {len(packages)} archives in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
