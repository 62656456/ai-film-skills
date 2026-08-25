#!/usr/bin/env python3
"""Shared filesystem safety boundaries for repository tooling."""

from __future__ import annotations

import json
import shutil
import tempfile
import uuid
from pathlib import Path


OUTPUT_MARKER = ".open-film-skills-output.json"
MARKER_PAYLOAD = {
    "schema_version": 1,
    "owner": "open-film-skills",
    "purpose": "generated-package-output",
}
EXCLUDED_SOURCE_PARTS = {"__pycache__", ".pytest_cache"}
EXCLUDED_SOURCE_SUFFIXES = {".pyc", ".pyo"}


class SafetyError(RuntimeError):
    """Raised when a requested filesystem operation crosses an ownership boundary."""


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def is_link_like(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction and is_junction())


def safe_source_files(root: Path) -> list[Path]:
    """Return regular files whose resolved locations remain inside ``root``.

    Standalone Skill packages intentionally reject symbolic links and Windows
    junctions. A package that needs another file must carry a real local copy.
    """

    if is_link_like(root):
        raise SafetyError(f"source root must not be a link or junction: {root}")
    resolved_root = root.resolve(strict=True)
    files: list[Path] = []
    for path in root.rglob("*"):
        if is_link_like(path):
            raise SafetyError(f"links and junctions are forbidden in Skill packages: {path}")
        resolved = path.resolve(strict=True)
        if not is_within(resolved, resolved_root):
            raise SafetyError(f"source path escapes Skill root: {path} -> {resolved}")
        if path.is_file():
            files.append(path)
    return sorted(
        files,
        key=lambda path: (
            path.relative_to(root).as_posix().casefold(),
            path.relative_to(root).as_posix(),
        ),
    )


def package_source_files(root: Path) -> list[Path]:
    """Return safe source files while excluding local interpreter/test caches."""

    return [
        path
        for path in safe_source_files(root)
        if not (set(path.relative_to(root).parts) & EXCLUDED_SOURCE_PARTS)
        and path.suffix.lower() not in EXCLUDED_SOURCE_SUFFIXES
    ]


def write_output_marker(directory: Path) -> None:
    (directory / OUTPUT_MARKER).write_text(
        json.dumps(MARKER_PAYLOAD, sort_keys=True) + "\n", encoding="utf-8"
    )


def has_valid_output_marker(directory: Path) -> bool:
    marker = directory / OUTPUT_MARKER
    if not marker.is_file() or is_link_like(marker):
        return False
    try:
        payload = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return payload == MARKER_PAYLOAD


def validate_output_target(
    output: Path, repo_root: Path, *, allow_external: bool = False
) -> Path:
    """Validate an output directory without deleting or creating it."""

    repo_root = repo_root.resolve(strict=True)
    requested = output.expanduser()
    if requested.exists() and is_link_like(requested):
        raise SafetyError(f"output directory must not be a link or junction: {requested}")
    output = requested.resolve(strict=False)
    dist_root = (repo_root / "dist").resolve(strict=False)
    dangerous = {repo_root, Path.home().resolve(), Path.cwd().resolve()}
    if output.parent == output:
        dangerous.add(output)
    if output in dangerous:
        raise SafetyError(f"refusing dangerous output directory: {output}")

    internal = is_within(output, dist_root)
    if not internal and not allow_external:
        raise SafetyError(
            f"output must stay under {dist_root}; use --allow-external-output only "
            "for a reviewed empty or tool-owned directory"
        )
    if not internal and not output.parent.exists():
        raise SafetyError(f"external output parent must already exist: {output.parent}")

    if output.exists():
        if is_link_like(output):
            raise SafetyError(f"output directory must not be a link or junction: {output}")
        if not output.is_dir():
            raise SafetyError(f"output path is not a directory: {output}")
        entries = list(output.iterdir())
        if entries and not has_valid_output_marker(output):
            raise SafetyError(
                f"refusing to replace non-empty directory not owned by this tool: {output}"
            )
    return output


def create_staging_output(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{output.name}.build-", dir=str(output.parent))
    )
    write_output_marker(staging)
    return staging


def remove_owned_output(directory: Path) -> None:
    if not has_valid_output_marker(directory):
        raise SafetyError(f"refusing to remove unowned generated directory: {directory}")
    shutil.rmtree(directory)


def commit_staging_output(staging: Path, output: Path) -> None:
    """Atomically replace a validated output and restore it if the swap fails."""

    if not has_valid_output_marker(staging):
        raise SafetyError(f"staging directory has no valid ownership marker: {staging}")
    backup: Path | None = None
    try:
        if output.exists():
            if any(output.iterdir()):
                if not has_valid_output_marker(output):
                    raise SafetyError(f"refusing to replace unowned output directory: {output}")
                backup = output.with_name(f".{output.name}.backup-{uuid.uuid4().hex}")
                output.rename(backup)
            else:
                output.rmdir()
        staging.rename(output)
    except Exception:
        if backup is not None and backup.exists() and not output.exists():
            backup.rename(output)
        raise
    if backup is not None and backup.exists():
        remove_owned_output(backup)
