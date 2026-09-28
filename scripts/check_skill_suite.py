#!/usr/bin/env python3
"""Run repository gates and optional text review; no deployment or publication."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    ("regression", ["-m", "unittest", "discover", "-s", "tests"]),
    ("portable_repository", ["scripts/validate_repository.py"]),
    ("independent_packages", ["scripts/validate_skill_independence.py"]),
    ("generated_guides", ["scripts/validate_skill_docs.py"]),
    ("existing_showcase", ["scripts/validate_style_gallery.py"]),
    ("existing_pages", ["scripts/validate_pages_site.py"]),
)


def runtime_digest(root: Path) -> str:
    h = hashlib.sha256()
    for folder in ("skills", "experimental"):
        for p in sorted((root / folder).rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                h.update(p.relative_to(root).as_posix().encode())
                h.update(b"\0" + hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def run_gate(*, profile: str, temporary: Path, sample: Path | None,
             allow_external: bool, root: Path = ROOT, run=subprocess.run) -> dict:
    start = time.perf_counter()
    if profile not in {"A", "B"}:
        raise ValueError("Unknown profile")
    temporary = temporary.resolve()
    if not temporary.is_dir():
        raise ValueError("An existing explicit temporary directory is required")
    report = {"schema": "film-skills-quality-gate/1", "profile": profile,
              "status": "failed", "checks": [], "runtime_sha256": runtime_digest(root),
              "user_acceptance": "required_before_formal_activation", "formal_activation_allowed": False,
              "real_video": "not_tested",
              "semantic_review": "not_performed", "seconds": None}
    env = dict(os.environ, TEMP=str(temporary), TMP=str(temporary), PYTHONDONTWRITEBYTECODE="1",
               PYTHONUTF8="1")
    commands = list(CHECKS)
    if profile == "B" and (sample is None or not allow_external):
        report["code"] = "B_requires_explicit_text_sample_and_external_consent"
        report["seconds"] = round(time.perf_counter() - start, 3)
        return report
    if sample:
        args = ["scripts/semantic_review.py", "--input", str(sample.resolve()),
                "--mode", "jev" if profile == "B" else "local"]
        if profile == "B":
            args.append("--allow-external")
        commands.append(("jev_text_review" if profile == "B" else "declared_text_checks", args))
    for name, args in commands:
        tick = time.perf_counter()
        try:
            result = run([sys.executable, "-B", *args], cwd=root, env=env,
                         capture_output=True, text=True, encoding="utf-8", errors="replace",
                         timeout=180, shell=False)
            item = {"name": name, "exit_code": result.returncode,
                    "seconds": round(time.perf_counter() - tick, 3)}
        except (OSError, subprocess.TimeoutExpired):
            report["checks"].append({"name": name, "status": "execution_failed"})
            report["code"] = "check_unavailable_or_timed_out"
            break
        # Detailed output remains in the caller's task temporary directory.
        log = temporary / ("quality-" + profile + "-" + name + ".txt")
        log.write_text(result.stdout + result.stderr, encoding="utf-8")
        item["log"] = str(log)
        report["checks"].append(item)
        if name == "jev_text_review":
            try:
                semantic = json.loads(result.stdout)
                report["semantic_review"] = semantic.get("semantic_review", "not_performed")
                report["semantic_status"] = semantic.get("status", "failed")
            except ValueError:
                report["semantic_status"] = "invalid_report"
                item["exit_code"] = 1
        if item["exit_code"]:
            report["code"] = "check_failed"
            break
    else:
        report["status"] = "passed"
    if runtime_digest(root) != report["runtime_sha256"]:
        report.update(status="failed", code="runtime_changed_during_checks")
    report["seconds"] = round(time.perf_counter() - start, 3)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=["A", "B"], default="A")
    parser.add_argument("--temp-dir", required=True, type=Path)
    parser.add_argument("--sample", type=Path)
    parser.add_argument("--allow-external", action="store_true")
    args = parser.parse_args()
    try:
        report = run_gate(profile=args.profile, temporary=args.temp_dir, sample=args.sample,
                          allow_external=args.allow_external)
    except (ValueError, OSError):
        report = {"status": "failed", "code": "invalid_local_configuration"}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
