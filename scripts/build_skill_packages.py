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
    is_link_like,
    remove_owned_output,
    validate_output_target,
)


ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (2026, 1, 1, 0, 0, 0)
LICENSE_NAMES = {"license", "license.txt", "license.md", "license.rst",
                 "licence", "licence.txt", "licence.md", "copying", "copying.txt", "copying.md", "copying.rst", "unlicense"}


def is_license_name(name: str) -> bool:
    normalized = name.casefold()
    return normalized in LICENSE_NAMES or (
        normalized.startswith(("license-", "licence-"))
        and Path(normalized).suffix in {"", ".txt", ".md", ".rst"}
    )


def skill_dirs(base: Path) -> list[Path]:
    if not base.is_dir():
        return []
    return sorted(
        child for child in base.iterdir() if child.is_dir() and (child / "SKILL.md").is_file()
    )


def package_files(skill: Path) -> list[Path]:
    return package_source_files(skill)


def archive_files(skill: Path) -> tuple[list[tuple[Path, str]], list[dict[str, str]]]:
    """Attach distribution notices without writing to or relicensing Skill sources."""
    files = package_files(skill)
    entries = [(path, path.relative_to(skill).as_posix()) for path in files]
    own_licenses = [path for path in files if path.parent == skill and is_license_name(path.name)]
    if any(not path.read_bytes().strip() for path in own_licenses):
        raise SafetyError(f"package license must not be empty: {skill.name}")
    own_license = bool(own_licenses)
    inherited: set[str] = set()
    if not own_license:
        source = ROOT / "LICENSE"
        if is_link_like(source) or not source.is_file() or not source.resolve().is_relative_to(ROOT.resolve()):
            raise SafetyError("repository LICENSE must be a regular file inside the repository")
        if not source.read_bytes().strip():
            raise SafetyError("repository LICENSE must not be empty")
        if any(relative.split("/")[0].casefold() == "license" for _, relative in entries):
            raise SafetyError(f"cannot attach LICENSE over an existing package directory: {skill.name}")
        entries.append((source, "LICENSE"))
        inherited.add("LICENSE")
        notice = ROOT / "NOTICE"
        if notice.exists() and not any(path.parent == skill and path.name.casefold() == "notice" for path in files):
            if is_link_like(notice) or not notice.is_file() or not notice.resolve().is_relative_to(ROOT.resolve()):
                raise SafetyError("repository NOTICE must be a regular file inside the repository")
            if any(relative.split("/")[0].casefold() == "notice" for _, relative in entries):
                raise SafetyError(f"cannot attach NOTICE over an existing package directory: {skill.name}")
            entries.append((notice, "NOTICE"))
            inherited.add("NOTICE")
    entries.sort(key=lambda item: (item[1].casefold(), item[1]))
    licenses = [
        {"path": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
         "source": "repository_default" if relative in inherited else "package"}
        for path, relative in entries
        if is_license_name(path.name) or path.name.casefold() == "notice"
    ]
    return entries, licenses


def write_file(archive: zipfile.ZipFile, source: Path, arcname: str) -> None:
    info = zipfile.ZipInfo(arcname, FIXED_TIME)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, source.read_bytes())


def verify_archive(path: Path, expected_entry: str, licenses: list[dict[str, str]] | None = None) -> None:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"corrupt ZIP entry in {path.name}: {bad}")
        if expected_entry not in archive.namelist():
            raise RuntimeError(f"{path.name} is missing {expected_entry}")
        for item in licenses or []:
            if item["path"] not in archive.namelist():
                raise RuntimeError(f"{path.name} is missing license entry {item['path']}")
            if hashlib.sha256(archive.read(item["path"])).hexdigest() != item["sha256"]:
                raise RuntimeError(f"{path.name} license bytes differ from the manifest: {item['path']}")


def build_one(skill: Path, output: Path) -> dict[str, object]:
    archive_path = output / f"{skill.name}.zip"
    entries, notices = archive_files(skill)
    licenses = [{**item, "path": f"{skill.name}/{item['path']}"} for item in notices]
    with zipfile.ZipFile(archive_path, "w") as archive:
        for path, rel in entries:
            write_file(archive, path, f"{skill.name}/{rel}")
    verify_archive(archive_path, f"{skill.name}/SKILL.md", licenses)
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    return {
        "name": skill.name,
        "file": archive_path.name,
        "bytes": archive_path.stat().st_size,
        "sha256": digest,
        "licenses": licenses,
    }


def build_complete(skills: list[Path], output: Path) -> dict[str, object]:
    archive_path = output / "open-film-skills-complete.zip"
    planned = [(skill, *archive_files(skill)) for skill in skills]
    licenses = [{**item, "skill": skill.name, "path": f"skills/{skill.name}/{item['path']}"}
                for skill, _, notices in planned for item in notices]
    with zipfile.ZipFile(archive_path, "w") as archive:
        for skill, entries, _ in planned:
            for path, rel in entries:
                write_file(archive, path, f"skills/{skill.name}/{rel}")
    verify_archive(archive_path, "skills/director-agent/SKILL.md", licenses)
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    return {
        "name": "open-film-skills-complete",
        "file": archive_path.name,
        "bytes": archive_path.stat().st_size,
        "sha256": digest,
        "licenses": licenses,
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
            "license_policy": "Keep package licenses and notices; when no top-level package license exists, attach repository LICENSE and applicable NOTICE to the archive only. Existing third-party notices retain their own terms.",
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
