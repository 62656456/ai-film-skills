#!/usr/bin/env python3
"""Shared filesystem safety boundaries for repository tooling."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import uuid
from pathlib import Path


OUTPUT_MARKER = ".open-film-skills-output.json"
MARKER_PAYLOAD = {
    "schema_version": 1,
    "owner": "open-film-skills",
    "purpose": "generated-package-output",
}
# Distribution is opt-in by file type. These are source documents, executable
# helpers, declared configuration, and reference media; unknown local files do
# not become public merely because they were left in a Skill directory.
PACKAGE_SOURCE_SUFFIXES = {
    ".md", ".rst", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml",
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".sh", ".ps1",
    ".bat", ".cmd", ".html", ".css", ".svg", ".csv", ".tsv",
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".pdf",
    ".wav", ".mp3", ".ogg", ".mp4", ".webm", ".woff", ".woff2", ".ttf",
    ".otf", ".glb", ".gltf", ".obj", ".mtl", ".blend", ".stl",
}
PACKAGE_SOURCE_NAMES = {
    "license", "licence", "copying", "unlicense", "notice", "authors",
}
EXCLUDED_SOURCE_PARTS = {
    ".git", ".hg", ".svn", ".idea", ".vscode", ".venv", "venv",
    "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".cache", ".tox", ".nox", ".hypothesis", "coverage",
    "htmlcov", "build", "dist", "log", "logs", "tmp", "temp",
}
PRIVATE_SOURCE_NAMES = {
    "credentials", "credential", "secrets", "secret", "private-key",
    "private_key", "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519",
}


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
    """Return the explicit public file set shared by packaging and installation.

    The policy also applies to exported folders without Git metadata, and does
    not trust tracked or ignored status to make credentials distributable.
    """

    def distributable(path: Path) -> bool:
        parts = [part.casefold() for part in path.relative_to(root).parts]
        if any(
            part in EXCLUDED_SOURCE_PARTS or part.startswith(".env")
            or part in PRIVATE_SOURCE_NAMES
            or part.split(".", 1)[0] in PRIVATE_SOURCE_NAMES
            for part in parts
        ):
            return False
        name = parts[-1]
        if name.startswith(".") or name.endswith("~"):
            return False
        return (
            path.suffix.casefold() in PACKAGE_SOURCE_SUFFIXES
            or name in PACKAGE_SOURCE_NAMES
            or (name.startswith(("license-", "licence-")) and not path.suffix)
        )

    return [path for path in safe_source_files(root) if distributable(path)]


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
        try:
            remove_owned_output(backup)
        except (OSError, SafetyError) as exc:
            # The new output has already committed. Cleanup failure must not
            # claim that the valid replacement was rolled back or failed.
            print(
                f"Warning: output committed at {output}; backup cleanup failed; "
                f"remaining backup at {backup}: {exc}",
                file=sys.stderr,
            )
