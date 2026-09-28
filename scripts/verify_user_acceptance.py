#!/usr/bin/env python3
"""Read-only gate for explicitly user-tested A/B Skill upgrade activation.

Reads only the supplied canonical PROJECT_STATE.json and the selected ZIP.
No state writes, network requests, publication permission, or trial-count gate.
The activating caller must use the same verified artifact bytes and stop if they
change. A successful decision grants only the recorded formal_activation scope.

Profile record fields: status=user_test_passed, evidence_author=user, user_quote,
source, reviewed_artifact_sha256, scope containing the exact formal_activation
token. The profile lives under acceptance.film_skills_overhaul_20260928.profiles.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import zipfile


ACCEPTANCE_KEY = "film_skills_overhaul_20260928"
PROFILE_RE = re.compile(r"(?<![A-Za-z0-9])([AB])(?=$|[^A-Za-z0-9])", re.I)
PASS_WORD = re.compile(r"通过|验收合格|\bpass(?:ed|es)?\b|\bapproved?\b", re.I)
NEGATIVE_PASS = re.compile(
    r"(?:不|没|未|没有|尚未|不能|不算|无法|并非|不是|不予|撤回|取消|拒绝).{0,14}(?:通过|验收合格)|"
    r"通过(?:不了|不算|无效)|(?:not|never|no|isn't|isn’t|wasn't|wasn’t|hasn't|hasn’t|didn't|didn’t|don't|don’t|cannot|can't|can’t)"
    r".{0,25}\b(?:pass(?:ed|es)?|approv\w*)\b", re.I)
DEFERRED_PASS = re.compile(
    r"如果|假如|假设|要是|待.{0,14}通过|等.{0,14}通过|通过(?:后|以后|之后|了再)|"
    r"必须|需要.{0,14}通过|通过.{0,8}(?:才|的话)|过了再|只要|只有.{0,14}通过|"
    r"应该|可能|预计|看起来|希望|争取|大概|尚待|待定|能否|是否|通过吗|通过了吗|"
    r"\b(?:if|once|when|might|may|could|should|would|will|hopefully|expect(?:ed)?)\b", re.I)
INTERNAL_ONLY = re.compile(
    r"(?:内部|结构|单元|自动化|脚本|模型自评|自检|机器检查).{0,12}(?:通过|合格)|"
    r"\b(?:unit|automated|internal|structural|self[- ]review)\b.{0,25}\bpass(?:ed|es)?\b", re.I)
NOT_TESTED = re.compile(
    r"(?:尚未|还没|没有|未曾|没实际|未实际).{0,10}(?:测试|试用|使用|体验)|"
    r"(?:not|never|haven't|haven’t|hasn't|hasn’t|didn't|didn’t).{0,15}\b(?:tested|tried|used)\b", re.I)
EXPLICIT_PASS = re.compile(
    r"(?:测试|实测|试用|验收).{0,6}(?:通过|合格)|"
    r"(?:这版|此版|这个版本|该版本|本版本|本版|A(?:版|方案)?|B(?:版|方案)?).{0,8}通过|"
    r"^(?:我确认|确认|确认本版)?\s*(?:已)?通过(?:了)?\s*$|"
    r"\b(?:I\s+)?(?:tested|tried)\b.{0,40}\b(?:passed|approved)\b|"
    r"\b(?:version|profile|candidate)\s*[AB]?\b.{0,20}\b(?:passed|approved)\b|"
    r"\b[AB]\s+(?:has\s+)?passed\b|^\s*(?:passed|approved)\s*$", re.I)


def _safe_absolute(path):
    path = Path(path)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("absolute path required")
    for item in reversed((path, *path.parents)):
        if os.path.lexists(item):
            info = item.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise ValueError("linked path refused")
    return path


def _path_key(path):
    value = str(Path(path)).replace("\\", "/")
    return value.casefold() if os.name == "nt" else value


def _nonempty_source(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return any(_nonempty_source(item) for item in value.values())
    if isinstance(value, list):
        return any(_nonempty_source(item) for item in value)
    return False


def _quote_confirms_pass(quote, profile):
    """Fail closed on negation, deferral, machine-only checks and another profile."""
    if not isinstance(quote, str) or not quote.strip():
        return False
    if NOT_TESTED.search(quote):
        return False
    positive = False
    for clause in re.split(r"[，,。.;；\n\r]+", quote):
        clause = clause.strip()
        if not clause or not PASS_WORD.search(clause):
            continue
        references = {x.upper() for x in PROFILE_RE.findall(clause)}
        if references and profile not in references:
            continue
        if (NEGATIVE_PASS.search(clause) or DEFERRED_PASS.search(clause)
                or INTERNAL_ONLY.search(clause) or "?" in clause or "？" in clause):
            return False
        if EXPLICIT_PASS.search(clause.rstrip("!！")):
            positive = True
    if positive:
        return True
    # A direct colloquial acceptance can span clauses without the literal word 通过.
    # Require all three: completed personal trial, an unambiguous good result, and
    # a present instruction to make this version formal. Mere selection is not enough.
    references = {x.upper() for x in PROFILE_RE.findall(quote)}
    if references and profile not in references:
        return False
    if re.search(r"(?:等|如果|假如|若|要是|待|必须|需要).{0,20}(?:测试|试用|体验)|"
                 r"(?:不是|不算|不能算|不能说|并非).{0,8}(?:没问题|没有问题|合格|符合要求)|"
                 r"(?:仍有|还有).{0,8}(?:问题|错误|缺陷)|"
                 r"(?:暂不|不要|不能|尚不能|别).{0,8}(?:转|升|设).{0,8}正式|[?？]", quote):
        return False
    tested = re.search(r"(?:我|本人).{0,10}(?:测试|试用|使用|体验)过(?:了)?", quote)
    good = re.search(r"没问题|没有问题|验收合格|符合要求|满足要求", quote)
    activate = re.search(r"(?:转|升|改|设)(?:为|成)?(?:正式|默认)", quote)
    return bool(tested and good and activate)


def _quote_is_clearly_refusal_or_rule(quote, profile):
    if not isinstance(quote, str) or not quote.strip() or NOT_TESTED.search(quote):
        return True
    for clause in re.split(r"[，,。.;；\n\r]+", quote):
        refs = {x.upper() for x in PROFILE_RE.findall(clause)}
        if refs and profile not in refs:
            continue
        if PASS_WORD.search(clause) and (
                NEGATIVE_PASS.search(clause) or DEFERRED_PASS.search(clause) or INTERNAL_ONLY.search(clause)):
            return True
    return False


def _formal_scope(value):
    return value == "formal_activation" or (
        isinstance(value, list) and "formal_activation" in value)


def verify_user_acceptance(state_path, profile, artifact_path, *, expected_project_id=None):
    """Return a privacy-preserving decision; never writes or mutates either input.

    ready=True means this precise profile and artifact have an explicit recorded
    user pass for formal activation. It never grants publication permission.
    User pass count is irrelevant: one explicit pass of this artifact suffices.
    """
    issues = []
    ambiguous_quote = False
    actual_sha = reviewed_sha = state_sha = None
    selected = str(profile).upper()
    if selected not in {"A", "B"}:
        issues.append("PROFILE_MUST_BE_A_OR_B")
    payload = None
    try:
        state_file = _safe_absolute(state_path)
        if state_file.name != "PROJECT_STATE.json":
            issues.append("CANONICAL_STATE_FILENAME_REQUIRED")
        raw = state_file.read_bytes()
        state_sha = hashlib.sha256(raw).hexdigest()
        payload = json.loads(raw.decode("utf-8"))
        if not isinstance(payload, dict):
            issues.append("STATE_OBJECT_REQUIRED")
            payload = None
        else:
            project_root = payload.get("project_root")
            project_id = payload.get("canonical_project_id")
            if (not isinstance(project_root, str) or not Path(project_root).is_absolute()
                    or _path_key(project_root) != _path_key(state_file.parent)
                    or not isinstance(project_id, str) or not project_id.strip()):
                issues.append("CANONICAL_STATE_IDENTITY_INVALID")
            if expected_project_id is not None and project_id != expected_project_id:
                issues.append("PROJECT_ID_MISMATCH")
            if not isinstance(payload.get("revision"), int) or payload["revision"] < 1:
                issues.append("STATE_REVISION_INVALID")
    except (OSError, ValueError, TypeError):
        issues.append("STATE_UNREADABLE_OR_INVALID")

    try:
        artifact = _safe_absolute(artifact_path)
        if not artifact.is_file() or artifact.suffix.lower() != ".zip" or not zipfile.is_zipfile(artifact):
            issues.append("ARTIFACT_MUST_BE_ZIP")
        else:
            before = artifact.stat()
            digest = hashlib.sha256()
            with artifact.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            after = artifact.stat()
            if (before.st_size, before.st_mtime_ns, before.st_ino) != (
                    after.st_size, after.st_mtime_ns, after.st_ino):
                issues.append("ARTIFACT_CHANGED_DURING_CHECK")
            actual_sha = digest.hexdigest()
    except (OSError, ValueError, TypeError, zipfile.BadZipFile):
        issues.append("ARTIFACT_UNREADABLE_OR_INVALID")

    record = None
    if payload is not None:
        acceptance = payload.get("acceptance")
        group = acceptance.get(ACCEPTANCE_KEY) if isinstance(acceptance, dict) else None
        profiles = group.get("profiles") if isinstance(group, dict) else None
        record = profiles.get(selected) if isinstance(profiles, dict) else None
    if not isinstance(record, dict):
        issues.append("PROFILE_USER_ACCEPTANCE_MISSING")
    else:
        if record.get("status") != "user_test_passed":
            issues.append("USER_TEST_PASS_STATUS_REQUIRED")
        if record.get("evidence_author") != "user":
            issues.append("USER_AUTHORED_EVIDENCE_REQUIRED")
        if not _quote_confirms_pass(record.get("user_quote"), selected):
            issues.append("EXPLICIT_USER_PASS_QUOTE_REQUIRED")
            ambiguous_quote = not _quote_is_clearly_refusal_or_rule(record.get("user_quote"), selected)
        if not _nonempty_source(record.get("source")):
            issues.append("USER_EVIDENCE_SOURCE_REQUIRED")
        if not _formal_scope(record.get("scope")):
            issues.append("FORMAL_ACTIVATION_SCOPE_REQUIRED")
        if record.get("reviewed_profile", selected) != selected:
            issues.append("REVIEWED_PROFILE_MISMATCH")
        reviewed = record.get("reviewed_artifact_sha256")
        if not isinstance(reviewed, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", reviewed):
            issues.append("REVIEWED_ARTIFACT_SHA256_REQUIRED")
        else:
            reviewed_sha = reviewed.lower()
            if actual_sha is None or actual_sha != reviewed_sha:
                issues.append("REVIEWED_ARTIFACT_SHA256_MISMATCH")
    # Re-read the canonical manifest after the artifact check to catch a concurrent decision change.
    if state_sha is not None:
        try:
            if hashlib.sha256(_safe_absolute(state_path).read_bytes()).hexdigest() != state_sha:
                issues.append("STATE_CHANGED_DURING_CHECK")
        except (OSError, ValueError, TypeError):
            issues.append("STATE_CHANGED_DURING_CHECK")
    issues = list(dict.fromkeys(issues))
    ready = not issues
    conclusion = "accepted_for_formal_activation" if ready else (
        "needs_review" if ambiguous_quote and issues == ["EXPLICIT_USER_PASS_QUOTE_REQUIRED"] else "refused")
    return {"ready": ready, "status": conclusion,
            "profile": selected if selected in {"A", "B"} else None,
            "artifact_sha256": actual_sha, "reviewed_artifact_sha256": reviewed_sha,
            "state_sha256": state_sha, "missing_or_invalid": issues,
            "formal_activation_authorized": ready, "external_publication_authorized": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--profile", choices=("A", "B"), required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--project-id")
    args = parser.parse_args(argv)
    result = verify_user_acceptance(args.state, args.profile, args.artifact,
                                    expected_project_id=args.project_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
