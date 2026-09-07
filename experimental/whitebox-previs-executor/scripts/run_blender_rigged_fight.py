#!/usr/bin/env python3
"""Locate Blender and run the rigged fight previs backend headlessly."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from validate_compiled_previs import validate


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blender")
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--frames-dir")
    parser.add_argument("--runtime-dir", required=True)
    return parser.parse_args()


def find_blender(explicit: str | None, search_root: Path) -> Path:
    configured = explicit or os.environ.get("WHITEBOX_BLENDER")
    if configured:
        candidate = Path(configured).expanduser().resolve()
        if candidate.is_file():
            return candidate
        raise FileNotFoundError(f"Configured Blender executable does not exist: {candidate}")
    system = shutil.which("blender") or shutil.which("blender.exe")
    if system:
        return Path(system).resolve()
    candidates = sorted(search_root.glob("_runtime/blender-*-windows-x64/blender.exe"), reverse=True)
    if candidates:
        return candidates[0].resolve()
    raise FileNotFoundError("Blender was not found; pass --blender, set WHITEBOX_BLENDER, add Blender to PATH, or place a portable build under _runtime")


def verify_blender(blender: Path) -> bool:
    """Check the selected executable before creating task output or cache paths."""
    try:
        result = subprocess.run([str(blender), "--version"], capture_output=True, text=True,
                                encoding="utf-8", errors="replace", check=False, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"Blender executable preflight failed: {exc}", file=sys.stderr)
        return False
    if result.returncode != 0 or not re.search(r"^Blender\s+\d+\.\d+", result.stdout, re.MULTILINE):
        print(f"Selected executable did not identify a working Blender (exit code {result.returncode}).", file=sys.stderr)
        return False
    return True


def main() -> int:
    args = arguments()
    try:
        data = json.loads(Path(args.spec).read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError("the compiled specification must be a JSON object")
        result = validate(data)
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        print(f"Invalid compiled specification: {exc}", file=sys.stderr)
        return 2
    if result["status"] != "pass" or not isinstance(data.get("action_program"), dict):
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        print("The rigged backend requires a valid previs-action/1.0 action_program.", file=sys.stderr)
        return 2
    script = Path(__file__).resolve().with_name("blender_rigged_fight_adapter.py")
    try:
        blender = find_blender(args.blender, Path.cwd().resolve())
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    if not verify_blender(blender):
        return 3
    runtime = Path(args.runtime_dir).resolve()
    temp_dir = runtime / "temp"
    appdata_dir = runtime / "appdata"
    temp_dir.mkdir(parents=True, exist_ok=True)
    appdata_dir.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment.update(
        {
            "TEMP": str(temp_dir),
            "TMP": str(temp_dir),
            "LOCALAPPDATA": str(appdata_dir),
            "APPDATA": str(appdata_dir),
        }
    )
    command = [
        str(blender),
        "--background",
        "--factory-startup",
        "--python-exit-code",
        "1",
        "--python",
        str(script),
        "--",
        "--spec",
        str(Path(args.spec).resolve()),
        "--output",
        str(Path(args.output).resolve()),
        "--project",
        str(Path(args.project).resolve()),
        "--validation",
        str(Path(args.validation).resolve()),
    ]
    if args.frames_dir:
        command.extend(["--frames-dir", str(Path(args.frames_dir).resolve())])
    try:
        return_code = subprocess.run(command, env=environment, check=False).returncode
    except OSError as exc:
        print(f"Blender launch failed after executable preflight: {exc}", file=sys.stderr)
        return 3
    if return_code != 0:
        print(f"Blender execution failed with exit code {return_code}.", file=sys.stderr)
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
