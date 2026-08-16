#!/usr/bin/env python3
"""Build deterministic, host-neutral ZIP packages for every Skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (2026, 1, 1, 0, 0, 0)
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def skill_dirs(base: Path) -> list[Path]:
    if not base.is_dir():
        return []
    return sorted(
        child for child in base.iterdir() if child.is_dir() and (child / "SKILL.md").is_file()
    )


def package_files(skill: Path) -> list[Path]:
    return sorted(
        path
        for path in skill.rglob("*")
        if path.is_file()
        and not (set(path.parts) & EXCLUDED_PARTS)
        and path.suffix.lower() not in EXCLUDED_SUFFIXES
    )


def write_file(archive: zipfile.ZipFile, source: Path, arcname: str) -> None:
    info = zipfile.ZipInfo(arcname, FIXED_TIME)
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "skills")
    parser.add_argument("--include-experimental", action="store_true")
    args = parser.parse_args()

    output = args.output.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    stable = skill_dirs(ROOT / "skills")
    experimental = skill_dirs(ROOT / "experimental") if args.include_experimental else []
    packages: list[dict[str, object]] = []
    for skill in stable:
        item = build_one(skill, output)
        item["status"] = "packaged"
        packages.append(item)
    for skill in experimental:
        item = build_one(skill, output)
        item["status"] = "experimental"
        packages.append(item)
    packages.append(build_complete(stable, output))

    manifest = {
        "schema_version": 2,
        "package_standard": "Agent Skills compatible SKILL.md folder",
        "native_layouts": ["codex", "claude-code", "trae", "codebuddy"],
        "official_upload_hosts": ["workbuddy"],
        "generic_fallback": "attach SKILL.md and local resources as Agent instructions",
        "stable_skill_count": len(stable),
        "experimental_skill_count": len(experimental),
        "packages": packages,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Built and verified {len(packages)} archives in {output}")


if __name__ == "__main__":
    main()
