#!/usr/bin/env python3
"""Install one self-contained Skill for a supported Agent host."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

from repository_safety import SafetyError, is_link_like, is_within, safe_source_files


ROOT = Path(__file__).resolve().parents[1]
STABLE_ROOT = ROOT / "skills"
EXPERIMENTAL_ROOT = ROOT / "experimental"
PLATFORMS = ("codex", "claude-code", "trae", "codebuddy", "workbuddy", "generic")


def discover() -> dict[str, tuple[Path, str]]:
    found: dict[str, tuple[Path, str]] = {}
    for base, status in ((STABLE_ROOT, "packaged"), (EXPERIMENTAL_ROOT, "experimental")):
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir()):
            if child.is_dir() and (child / "SKILL.md").is_file():
                found[child.name] = (child, status)
    return found


def default_target(platform: str) -> Path | None:
    if platform == "codex":
        codex_home = os.environ.get("CODEX_HOME")
        return (Path(codex_home) if codex_home else Path.home() / ".codex") / "skills"
    if platform == "claude-code":
        return Path.home() / ".claude" / "skills"
    if platform == "trae":
        return Path.cwd() / ".agents" / "skills"
    if platform == "codebuddy":
        return Path.home() / ".codebuddy" / "skills"
    return None


def install(source: Path, target_root: Path, force: bool) -> Path:
    safe_source_files(source)
    target_root = target_root.expanduser().resolve()
    destination = target_root / source.name
    if not is_within(destination.resolve(strict=False), target_root):
        raise SafetyError(f"installation destination escapes target root: {destination}")
    target_root.mkdir(parents=True, exist_ok=True)

    if destination.exists() and not force:
        raise FileExistsError(
            f"{destination} already exists. Re-run with --force only after reviewing the existing copy."
        )
    if destination.exists():
        if is_link_like(destination) or not destination.is_dir():
            raise SafetyError(f"existing installation must be a regular directory: {destination}")
        safe_source_files(destination)

    staging_parent = Path(tempfile.mkdtemp(prefix=f".{source.name}-install-", dir=target_root))
    staging = staging_parent / source.name
    backup = target_root / f".{source.name}.backup-{uuid.uuid4().hex}"
    try:
        shutil.copytree(
            source,
            staging,
            symlinks=True,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc", "*.pyo"),
        )
        safe_source_files(staging)
        if not (staging / "SKILL.md").is_file():
            raise RuntimeError("staged package is missing SKILL.md")
        if destination.exists():
            destination.rename(backup)
        staging.rename(destination)
        if backup.exists():
            shutil.rmtree(backup)
    except Exception:
        if backup.exists() and not destination.exists():
            backup.rename(destination)
        raise
    finally:
        if staging_parent.exists():
            shutil.rmtree(staging_parent)
    return destination


def main() -> int:
    skills = discover()
    parser = argparse.ArgumentParser(
        description="Install one self-contained Open Film Skill from this checkout."
    )
    parser.add_argument("skill", nargs="?", help="Skill directory name")
    parser.add_argument("--list", action="store_true", help="List available Skills")
    parser.add_argument(
        "--platform",
        choices=PLATFORMS,
        help="Agent host. Required unless --target is supplied.",
    )
    parser.add_argument("--target", type=Path, help="Override the destination skills directory")
    parser.add_argument(
        "--experimental",
        action="store_true",
        help="Allow installation of an experimental Skill",
    )
    parser.add_argument("--force", action="store_true", help="Replace an existing installation")
    args = parser.parse_args()

    if args.list:
        for name, (_, status) in skills.items():
            print(f"{name}\t{status}")
        return 0
    if not args.skill:
        parser.error("provide a Skill name or use --list")
    if args.skill not in skills:
        print(f"Unknown Skill: {args.skill}", file=sys.stderr)
        print("Run with --list to see valid names.", file=sys.stderr)
        return 2

    source, status = skills[args.skill]
    if status == "experimental" and not args.experimental:
        print(
            f"{args.skill} is experimental. Re-run with --experimental only after reviewing its status.",
            file=sys.stderr,
        )
        return 3

    if not args.platform and not args.target:
        parser.error("choose --platform or provide --target")
    platform = args.platform or "generic"
    target = args.target or default_target(platform)
    if target is None:
        if platform == "workbuddy":
            parser.error(
                "WorkBuddy uses its Add Skill > Upload Skill interface. Download this Skill's ZIP "
                "from the release page, or provide --target only for a reviewed local test directory."
            )
        parser.error("this platform has no verified default folder; provide --target")

    try:
        destination = install(source, target, args.force)
    except Exception as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Installed {args.skill} for {platform} at {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
