#!/usr/bin/env python3
"""Build isolated, deterministic A/B review candidates; never install or promote."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import zipfile

import build_skill_packages as packages
from repository_safety import SafetyError, is_link_like, safe_source_files, validate_output_target

ROOT = Path(__file__).resolve().parents[1]
VERSION = "5.7.1"
REGULAR = frozenset("ai-short-drama-production ai-storyboard-director character-asset cyberpunk-design d-data-analysis-semantic-layer d-official-market-analysis director-agent epic-design fantasy-design horror-design noir-design produce-ai-video prop-asset romance-design scene-asset war-design web-design-director wuxia-design".split())
EXPERIMENTAL = frozenset("guofeng-visual-director hard-sci-fi-visual-director whitebox-previs-executor".split())
STORYBOARD = "skills/ai-storyboard-director/"
FORBIDDEN_NAMES = re.compile(r"(?i)(?:^\.|(?:^|[-_.])(?:credentials?|secrets?|private|api[-_]?keys?|tokens?)(?:[-_.]|$)|^PROJECT_STATE\.json$|^CURRENT_STATE\.md$)")
SECRET = re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{24,}|apikey_[A-Fa-f0-9]{36}_[A-Fa-f0-9]{64}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?i:(?:api[_-]?key|token|password|secret)\s*[=:]\s*[\"'][A-Za-z0-9_./+=-]{20,}[\"']))")
B_SECTION = """

## B版：可选Jev文字复核

创作与本地自检沿用以上相同核心。只有当前任务已明确启用Jev文字复核时，再读 `references/semantic-review.md`，用 `scripts/semantic_review.py` 核对实际成品与少量锁定要求。安装B不授权外发素材，不自动联网、不自动改稿或采用创意候选。缺凭证、服务失败或证据不足时如实保留候选和未完成状态；文字检查不证明实际媒体、审美或用户接受。
"""
B_REFERENCE = """# Jev可选文字复核

保留与A相同的源材料、初稿、锁定要求和修订边界。Jev只核对提交的文字，不生成镜头、不直接看图片或视频，不自动改稿、采用创意候选或决定用户审美。

脚本仅用Python标准库。输入JSON包含source、locked_facts、deliverable、observed_evidence。source和deliverable至少含text；locked_facts最多12项，每项含id、text、severity（major/minor）、target（deliverable或观察id），可选question_type（choice/noul）及唯一原文excerpt。observed_evidence为实际观察的文字数组，每项含id、type:text、text，可为空；计划不是执行证据。

先运行本地检查：`python -B scripts/semantic_review.py --mode local --input INPUT.json`。只有当前材料允许外发、调用范围已获授权且当前进程安全注入TYPESAFE_API_KEY，才运行`python -B scripts/semantic_review.py --mode jev --allow-external --input INPUT.json`。不把密钥写入文档、输入JSON、命令行或回执。

一次批量请求，不自动重试。缺密钥、未允许外发或服务失败返回failed，不伪称B通过；review_required与candidate_repair只供主流程回读原文确认，修复后仅重查受影响要求。no_issue_detected仅表示本次文字未发现明确问题，不等于用户接受、媒体效果或可靠性保证。概率阈值是待校准分流策略，不是准确率。需要核实协议与模型时查官方https://docs.typesafe.ai/api及https://docs.typesafe.ai/models。
"""
README = """# 影视技能整改测试候选

本包包含18项常规技能和3项实验技能；各完整文件夹独立使用，原有许可随包保留。PROFILE.json记录版本、包清单、共同核心摘要和测试边界。

A使用主模型创作与自检，无Jev运行依赖。B保留同一创作核心，仅分镜包增加可选Jev文字复核；默认不联网。创意镜头给用户提供思路、拍法、衔接与取舍，不自动生成媒体或替换主方案。

状态为candidate，用户测试pending；内部检查不等于用户通过。请在明确隔离的测试环境中选用所需完整技能文件夹，保持现有默认。只有用户实际测试并明确认可同一冻结版本后，才可按原有验收流程决定正式切换。此ZIP不安装、启用、晋升或发布任何版本。

分镜包的VERSION_MANIFEST.json列出实际文件SHA-256，VERSION_MANIFEST.sha256校验清单自身。根manifest.json与ZIP的SHA文件由构建器另外交付。维护质量门依赖完整仓库与验证资源，未塞入此运行包；需在来源仓库按docs/RELEASE_WORKFLOW.md执行。
"""


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reject_links(path: Path) -> None:
    for node in (path, *path.parents):
        if is_link_like(node):
            raise SafetyError(f"link or junction is forbidden: {node}")


def public_bytes(path: Path, relative: str) -> bytes:
    reject_links(path)
    if any(FORBIDDEN_NAMES.search(part) for part in Path(relative).parts) or path.suffix.lower() in {".pem", ".pfx", ".p12", ".key", ".sqlite", ".db"}:
        raise SafetyError(f"private or hidden source file refused: {relative}")
    data = path.read_bytes()
    if SECRET.search(data.decode("utf-8", errors="replace")):
        raise SafetyError(f"possible credential refused in source: {relative}")
    return data


def collect_core(repo: Path) -> tuple[dict[str, bytes], list[dict], list[dict]]:
    reject_links(repo)
    core: dict[str, bytes] = {}
    catalog: list[dict] = []
    licenses: list[dict] = []
    previous_root = packages.ROOT
    packages.ROOT = repo
    try:
        for area, expected in (("skills", REGULAR), ("experimental", EXPERIMENTAL)):
            base = repo / area
            reject_links(base)
            found = packages.skill_dirs(base)
            if {p.name for p in found} != expected:
                raise SafetyError(f"expected exact {len(expected)} {area} package names")
            for skill in found:
                reject_links(skill)
                if packages.independence.frontmatter_name(skill) != skill.name:
                    raise SafetyError(f"package identity differs from directory: {skill.name}")
                # Review profiles refuse private sources even when the regular
                # distribution filter would omit them from the archive.
                for source in safe_source_files(skill):
                    public_bytes(source, source.relative_to(skill).as_posix())
                entries, notices = packages.archive_files(skill)
                prefix = f"{area}/{skill.name}/"
                for source, relative in entries:
                    if relative in {"VERSION_MANIFEST.json", "VERSION_MANIFEST.sha256"}:
                        raise SafetyError("source must be the editable repository, not a frozen version")
                    target = prefix + relative
                    if any(key.casefold() == target.casefold() for key in core):
                        raise SafetyError(f"duplicate package path: {target}")
                    core[target] = public_bytes(source, relative)
                catalog.append({"name": skill.name, "path": prefix.rstrip("/"), "distribution": area})
                licenses.extend({**notice, "skill": skill.name, "path": prefix + notice["path"]} for notice in notices)
    finally:
        packages.ROOT = previous_root
    entry = core[STORYBOARD + "SKILL.md"].decode("utf-8")
    if entry.count(f"**{VERSION}**") != 1:
        raise SafetyError(f"storyboard entry must declare exactly one maintenance version {VERSION}")
    if STORYBOARD + "scripts/semantic_review.py" in core or STORYBOARD + "references/semantic-review.md" in core:
        raise SafetyError("A source already contains a Jev runtime overlay")
    if any(sha(core[item["path"]]) != item["sha256"] for item in licenses):
        raise SafetyError("license changed while collecting package sources")
    return core, catalog, licenses


def zip_bytes(path: Path, files: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "x") as archive:
        for name in sorted(files):
            info = zipfile.ZipInfo(name, packages.FIXED_TIME)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, files[name])
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() or set(archive.namelist()) != set(files):
            raise SafetyError("archive verification failed")
        for name, data in files.items():
            if archive.read(name) != data:
                raise SafetyError(f"archive bytes changed: {name}")


def validate_dest(output: Path, repo: Path, allow_external: bool) -> Path:
    reject_links(output.absolute())
    target = validate_output_target(output, repo, allow_external=allow_external)
    if target.is_relative_to(repo) and not target.is_relative_to(repo / "dist"):
        raise SafetyError("repository outputs must remain under dist, away from source packages")
    if target.drive.casefold() == "c:":
        raise SafetyError("C drive output is not permitted")
    if target.exists() and any(target.iterdir()):
        raise SafetyError("output must be new or empty; frozen packages are never overwritten")
    return target


def build_profiles(repo: Path, output: Path, temp_dir: Path, *, allow_external: bool = False) -> dict:
    repo = repo.absolute()
    reject_links(repo)
    repo = repo.resolve(strict=True)
    output = validate_dest(output, repo, allow_external)
    temp_dir = temp_dir.absolute()
    reject_links(temp_dir)
    temp_dir = temp_dir.resolve(strict=True)
    if not temp_dir.is_dir() or temp_dir.drive.casefold() == "c:" or temp_dir.is_relative_to(repo) or repo.is_relative_to(temp_dir):
        raise SafetyError("temp-dir must be an existing isolated directory outside the repository and C drive")
    if output.is_relative_to(temp_dir) or temp_dir.is_relative_to(output):
        raise SafetyError("output and temporary directory must be separate")
    core, catalog, licenses = collect_core(repo)
    semantic_source = repo / "scripts" / "semantic_review.py"
    semantic_data = public_bytes(semantic_source, "scripts/semantic_review.py")
    common_files = [{"path": p, "sha256": sha(data)} for p, data in sorted(core.items())]
    common_digest = sha(json_bytes(common_files))
    manifest = {"schema_version": 1, "version": VERSION, "status": "candidate", "user_test_status": "pending", "default_network": False,
                "common_core_digest": common_digest, "common_core_files": common_files, "packages": catalog, "licenses": licenses, "artifacts": []}
    with tempfile.TemporaryDirectory(prefix="film-review-profiles-", dir=temp_dir) as scratch:
        staging = Path(scratch)
        for profile, name in (("A", "方案A_无Jev.zip"), ("B", "方案B_Jev辅助复核.zip")):
            files = dict(core)
            version = VERSION if profile == "A" else VERSION + "-jev"
            if profile == "B":
                text = files[STORYBOARD + "SKILL.md"].decode("utf-8")
                files[STORYBOARD + "SKILL.md"] = (text.replace(f"**{VERSION}**", f"**{version}**", 1) + B_SECTION).encode("utf-8")
                files[STORYBOARD + "references/semantic-review.md"] = B_REFERENCE.encode("utf-8")
                files[STORYBOARD + "scripts/semantic_review.py"] = semantic_data
            version_manifest = {"schema_version": "1.0", "skill": "ai-storyboard-director", "version": version, "profile": profile,
                                "status": "candidate", "user_test_status": "pending", "default_network": False,
                                "self_contained": True, "cross_version_runtime_references_allowed": False, "common_core_digest": common_digest, "hash_algorithm": "SHA-256",
                                "runtime_files": [{"path": p[len(STORYBOARD):], "sha256": sha(data)} for p, data in sorted(files.items()) if p.startswith(STORYBOARD)]}
            manifest_data = json_bytes(version_manifest)
            files[STORYBOARD + "VERSION_MANIFEST.json"] = manifest_data
            files[STORYBOARD + "VERSION_MANIFEST.sha256"] = (sha(manifest_data) + "  VERSION_MANIFEST.json\n").encode("ascii")
            files["PROFILE.json"] = json_bytes({"schema_version": 1, "profile": profile, "version": version, "status": "candidate", "user_test_status": "pending",
                                               "default_network": False, "default_enabled": False, "common_core_digest": common_digest,
                                               "regular_skill_count": 18, "experimental_skill_count": 3, "packages": catalog,
                                               "jev": "not_included" if profile == "A" else "optional_explicit_request_and_external_permission_only",
                                               "promotion": "explicit_user_test_acceptance_of_this_exact_frozen_artifact_required"})
            files["使用说明.md"] = README.encode("utf-8")
            zip_bytes(staging / name, files)
            digest = sha((staging / name).read_bytes())
            (staging / (name + ".sha256")).write_text(digest + "  " + name + "\n", encoding="utf-8")
            manifest["artifacts"].append({"profile": profile, "version": version, "file": name, "sha256": digest, "bytes": (staging / name).stat().st_size})
        (staging / "manifest.json").write_bytes(json_bytes(manifest))
        # Recheck destination after building; exclusive creation never replaces user files.
        output = validate_dest(output, repo, allow_external)
        output.mkdir(parents=True, exist_ok=True)
        created: list[Path] = []
        try:
            for source in sorted(staging.iterdir()):
                target = output / source.name
                with target.open("xb") as stream:
                    created.append(target)
                    with source.open("rb") as incoming:
                        shutil.copyfileobj(incoming, stream)
        except Exception:
            for target in created:
                target.unlink()
            raise
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--temp-dir", type=Path, required=True)
    parser.add_argument("--allow-external-output", action="store_true")
    args = parser.parse_args()
    try:
        build_profiles(ROOT, args.output, args.temp_dir, allow_external=args.allow_external_output)
    except (OSError, SafetyError, ValueError) as exc:
        print(f"Candidate build refused: {exc}", file=sys.stderr)
        return 2
    print(f"Built A/B {VERSION} candidates; user testing pending; no installation or promotion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
