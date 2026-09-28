#!/usr/bin/env python3
"""Read-only gate for a precise, present user instruction to activate a Skill.

This is independent of verify_user_acceptance.py: authorization is not a test
pass. Reads acceptance.film_skills_overhaul_20260928.explicit_activation_authorization
from the canonical PROJECT_STATE.json and hashes an existing ordinary artifact.
Archive structure/CRC and deployment remain the caller's responsibility.

Required record: status=approved_by_user_instruction, evidence_author=user,
user_quote, source, selection_source={user_quote, source}, profile, version,
artifact_sha256, scope containing the exact local_activation token. The selected
profiles entry must bind the same version and artifact_sha256. Neither user test
status nor any other input is written. This gate never authorizes publication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat


ACCEPTANCE_KEY = "film_skills_overhaul_20260928"
AUTHORIZATION_KEY = "explicit_activation_authorization"
PROFILE_RE = re.compile(r"(?<![A-Za-z0-9])([AB])(?=$|[^A-Za-z])", re.I)
VERSION_RE = re.compile(r"(?<![0-9])v?(\d+\.\d+(?:\.\d+)?(?:[-+][A-Za-z0-9.-]+)?)(?![A-Za-z0-9])")
ACTIVATION = r"(?:启用|激活|切换|设为默认|设成默认|转为默认|升为正式|设为正式|上线|activate|enable)"
ACTIVATION_RE = re.compile(ACTIVATION, re.I)
NEGATIVE = re.compile(
    r"(?:不要|别|勿|禁止|不能|不许|不准|不允许|不授权|未授权|没有授权|拒绝|取消|撤回|暂不|尚不|不再|不应|不该|不必|无需|不).{0,14}"
    + ACTIVATION + r"|(?:not|never|do\s+not|don't|don’t|cannot|can't|can’t|refuse|revoke|cancel).{0,20}"
    + ACTIVATION, re.I)
CONDITIONAL_OR_FUTURE = re.compile(
    r"如果|假如|假设|要是|倘若|只要|只有|一旦|前提|等.{0,20}(?:通过|测试|验收|确认|批准|授权)|"
    r"待.{0,20}(?:通过|测试|验收|确认|批准|授权)|(?:通过|测试|验收|确认|批准|授权)(?:完|完成|了)?(?:之后|以后|后|再)|"
    r"(?:通过|测试|验收|确认|批准|授权|没问题|合格|准备好).{0,12}(?:之后|以后|后再|后|再启用|才启用)|"
    r"明天|后天|下周|下个月|以后|稍后|等会|过会|一会儿|回头|将来|到时候|届时|"
    r"\b(?:if|once|when|unless|after|later|tomorrow|eventually|next\s+week)\b", re.I)
DISCUSSION = re.compile(
    r"讨论|商量|研究|评估|分析|考虑|建议|计划|准备|示例|举例|引用|引述|转述|模拟|复述|"
    r"不是授权|不代表授权|不等于授权|未确认|待确认|待批准|未经批准|未经确认|"
    r"能否|是否|可否|要不要|该不该|可以吗|行不行|[?？]|"
    r"\b(?:discuss|consider|evaluate|propose|suggest|plan|might|could|should|would)\b", re.I)
MODEL_PROXY = re.compile(
    r"(?:模型|助手|智能体|AI|Jev|Codex|系统).{0,10}(?:说|认为|建议|判断|批准|同意|授权|代批|代为|替我)|"
    r"(?:作为|我作为).{0,5}(?:模型|助手|智能体|AI)|"
    r"(?:由|让).{0,8}(?:模型|助手|智能体|AI|Jev|Codex).{0,8}(?:代批|批准|授权)|"
    r"\b(?:model|assistant|agent|AI)\b.{0,20}\b(?:approves?|authorizes?|says?|suggests?)\b", re.I)
TRIAL_ONLY = re.compile(
    r"候选|试用|试跑|试运行|试验|体验一下|临时使用|仅供测试|只供测试|测试一下|"
    r"\b(?:candidate|trial|temporary|try\s+out|test\s+only)\b", re.I)
PRESENT_INSTRUCTION = re.compile(
    r"(?:现在(?:就)?|立即|立刻|马上|直接|请|同意|允许|授权|可以|先).{0,12}" + ACTIVATION
    + r"|^(?:就)?" + ACTIVATION
    + r"|\b(?:activate|enable)\b.{0,30}\bnow\b|^\s*(?:please\s+)?(?:activate|enable)\b", re.I)
SELECTION = re.compile(r"(?:先(?:选|用|启用|采用)?|选择|选定|选用|采用|启用|用)\s*([AB])(?=$|[^A-Za-z])", re.I)
NEGATIVE_SELECTION = re.compile(r"(?:不要|别|勿|禁止|不能|不许|不准|拒绝|取消|撤回|暂不|不再|不).{0,12}(?:选|用|采用)")


def _safe_absolute(value):
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("absolute path required")
    for part in reversed((path, *path.parents)):
        if os.path.lexists(part):
            info = part.lstat()
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
        return any(_nonempty_source(v) for v in value.values())
    if isinstance(value, list):
        return any(_nonempty_source(v) for v in value)
    return False


def _sha_value(value):
    return value.lower() if isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{64}", value) else None


def _signature(info):
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns


def _hash_stable_file(value):
    path = _safe_absolute(value)
    before = path.stat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError("regular file required")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    _safe_absolute(path)
    after = path.stat()
    if _signature(before) != _signature(after):
        raise ValueError("file changed during check")
    return digest.hexdigest(), _signature(after)


def _clauses(quote):
    return [part.strip() for part in re.split(r"[，,。;；\n\r]+", quote) if part.strip()]


def _quote_authorizes_activation(quote, profile, version):
    if not isinstance(quote, str) or not quote.strip():
        return False
    # Conditions can occur in a preceding clause; they cannot be stripped away
    # to turn the consequent into a present instruction.
    if CONDITIONAL_OR_FUTURE.search(quote) or DISCUSSION.search(quote) or MODEL_PROXY.search(quote):
        return False
    positive = False
    for clause in _clauses(quote):
        if not ACTIVATION_RE.search(clause):
            continue
        refs = {p.upper() for p in PROFILE_RE.findall(clause)}
        if refs and profile not in refs:
            if PRESENT_INSTRUCTION.search(clause) and not NEGATIVE.search(clause):
                return False
            continue
        if NEGATIVE.search(clause) or TRIAL_ONLY.search(clause):
            return False
        versions = set(VERSION_RE.findall(clause))
        if versions and versions != {version}:
            return False
        # A clause authorizing two profiles does not identify this one alone.
        if refs and refs != {profile}:
            return False
        if PRESENT_INSTRUCTION.search(clause):
            positive = True
    return positive


def _selection_matches(selection, profile):
    if not isinstance(selection, dict) or not _nonempty_source(selection.get("source")):
        return False
    if selection.get("evidence_author", "user") != "user":
        return False
    quote = selection.get("user_quote")
    if not isinstance(quote, str) or not quote.strip():
        return False
    if (CONDITIONAL_OR_FUTURE.search(quote) or DISCUSSION.search(quote)
            or MODEL_PROXY.search(quote) or TRIAL_ONLY.search(quote)):
        return False
    chosen = set()
    for clause in _clauses(quote):
        choices = {p.upper() for p in SELECTION.findall(clause)}
        if choices and (NEGATIVE.search(clause) or NEGATIVE_SELECTION.search(clause)):
            return False
        chosen.update(choices)
    return chosen == {profile}


def verify_activation_authorization(state_path, profile, version, artifact_path, *, expected_project_id=None):
    """Return an exact-object local activation decision without mutating inputs.

    ready=True is explicit instruction authorization, never a user-test pass or
    permission to publish. The caller must use the same state/artifact bytes.
    """
    issues = []
    selected = str(profile).upper()
    if selected not in {"A", "B"}:
        issues.append("PROFILE_MUST_BE_A_OR_B")
    if not isinstance(version, str) or not version.strip():
        issues.append("VERSION_REQUIRED")
    payload = None
    state_sha = actual_sha = authorized_sha = None
    artifact_signature = None
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
            root, project_id = payload.get("project_root"), payload.get("canonical_project_id")
            if (not isinstance(root, str) or not Path(root).is_absolute()
                    or _path_key(root) != _path_key(state_file.parent)
                    or not isinstance(project_id, str) or not project_id.strip()):
                issues.append("CANONICAL_STATE_IDENTITY_INVALID")
            if expected_project_id is not None and project_id != expected_project_id:
                issues.append("PROJECT_ID_MISMATCH")
            if type(payload.get("revision")) is not int or payload["revision"] < 1:
                issues.append("STATE_REVISION_INVALID")
    except (OSError, ValueError, TypeError):
        issues.append("STATE_UNREADABLE_OR_INVALID")
    try:
        actual_sha, artifact_signature = _hash_stable_file(artifact_path)
    except (OSError, ValueError, TypeError):
        issues.append("ARTIFACT_UNREADABLE_OR_CHANGED")

    record = group = profile_record = None
    if payload is not None:
        acceptance = payload.get("acceptance")
        group = acceptance.get(ACCEPTANCE_KEY) if isinstance(acceptance, dict) else None
        record = group.get(AUTHORIZATION_KEY) if isinstance(group, dict) else None
        profiles = group.get("profiles") if isinstance(group, dict) else None
        profile_record = profiles.get(selected) if isinstance(profiles, dict) else None
    if not isinstance(record, dict):
        issues.append("EXPLICIT_ACTIVATION_AUTHORIZATION_MISSING")
    else:
        if record.get("status") != "approved_by_user_instruction":
            issues.append("EXPLICIT_USER_INSTRUCTION_STATUS_REQUIRED")
        if record.get("evidence_author") != "user":
            issues.append("USER_AUTHORED_EVIDENCE_REQUIRED")
        if not _nonempty_source(record.get("source")):
            issues.append("USER_INSTRUCTION_SOURCE_REQUIRED")
        if not _selection_matches(record.get("selection_source"), selected):
            issues.append("EXPLICIT_PROFILE_SELECTION_SOURCE_REQUIRED")
        if record.get("profile") != selected:
            issues.append("AUTHORIZED_PROFILE_MISMATCH")
        if record.get("version") != version:
            issues.append("AUTHORIZED_VERSION_MISMATCH")
        if not _quote_authorizes_activation(record.get("user_quote"), selected, version):
            issues.append("PRESENT_USER_ACTIVATION_INSTRUCTION_REQUIRED")
        scope = record.get("scope")
        if scope != "local_activation" and not (isinstance(scope, list) and "local_activation" in scope):
            issues.append("LOCAL_ACTIVATION_SCOPE_REQUIRED")
        authorized_sha = _sha_value(record.get("artifact_sha256"))
        if authorized_sha is None:
            issues.append("AUTHORIZED_ARTIFACT_SHA256_REQUIRED")
        elif actual_sha != authorized_sha:
            issues.append("AUTHORIZED_ARTIFACT_SHA256_MISMATCH")
    if not isinstance(profile_record, dict):
        issues.append("CANONICAL_PROFILE_RECORD_REQUIRED")
    else:
        if profile_record.get("version") != version:
            issues.append("PROFILE_STATE_VERSION_MISMATCH")
        profile_sha = _sha_value(profile_record.get("artifact_sha256"))
        if profile_sha is None or profile_sha != actual_sha or profile_sha != authorized_sha:
            issues.append("PROFILE_STATE_ARTIFACT_SHA256_MISMATCH")

    if artifact_signature is not None:
        try:
            final_sha, final_signature = _hash_stable_file(artifact_path)
            if final_sha != actual_sha or final_signature != artifact_signature:
                issues.append("ARTIFACT_CHANGED_DURING_CHECK")
        except (OSError, ValueError, TypeError):
            issues.append("ARTIFACT_CHANGED_DURING_CHECK")
    # Recheck the authorization after the potentially expensive final artifact
    # read, so a revocation during that read is also refused.
    if state_sha is not None:
        try:
            if hashlib.sha256(_safe_absolute(state_path).read_bytes()).hexdigest() != state_sha:
                issues.append("STATE_CHANGED_DURING_CHECK")
        except (OSError, ValueError, TypeError):
            issues.append("STATE_CHANGED_DURING_CHECK")
    issues = list(dict.fromkeys(issues))
    ready = not issues
    test_status = (profile_record.get("user_test_status", profile_record.get("status", "unknown"))
                   if isinstance(profile_record, dict) else "unknown")
    return {"ready": ready, "status": "authorized_for_local_activation" if ready else "refused",
            "authorization_basis": "explicit_user_instruction" if ready else None,
            "profile": selected if selected in {"A", "B"} else None,
            "version": version if isinstance(version, str) else None,
            "artifact_sha256": actual_sha, "authorized_artifact_sha256": authorized_sha,
            "state_sha256": state_sha, "missing_or_invalid": issues,
            "local_activation_authorized": ready, "external_publication_authorized": False,
            "user_test_status": test_status, "user_test_status_unchanged": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--profile", choices=("A", "B"), required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--project-id")
    args = parser.parse_args(argv)
    result = verify_activation_authorization(args.state, args.profile, args.version, args.artifact,
                                             expected_project_id=args.project_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
