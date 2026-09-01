#!/usr/bin/env python3
"""Reject Skill packages that require machine-local or sibling runtime content."""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_BASES = (ROOT / "skills", ROOT / "experimental")
LOCAL_DEPENDENCY = re.compile(
    r"(?<![A-Za-z0-9_/-])((?:references|scripts|assets|agents)/"
    r"[A-Za-z0-9_.\-/]+\.(?:md|json|jsonl|py|sh|ps1|yaml|yml|txt))"
)
LOCAL_ABSOLUTE_PATH = re.compile(r"(?i)(?<![A-Za-z0-9])(?:[A-Z]:[\\/]|file://)")
UPWARD_PATH = re.compile(r"(?:^|[\s`'\"(])\.\.[\\/]")
UNC_PATH = re.compile(r"(?:^|[\s`'\"(])(?:\\\\[^\\\s]+\\[^\\\s]+|//[^/\s]+/[^/\s]+)")
POSIX_LOCAL_PATH = re.compile(r"(?:^|[\s`'\"(])(?:~[/\\]|/(?:home|Users|tmp|var|opt)/)")
MACHINE_PLACEHOLDER = re.compile(
    r"(?i)<(?:knowledge-repository|user-configured-workbench|local-knowledge|private-[^>]+)>"
)
EXTERNAL_RUNTIME = re.compile(
    r"(?i)(?:read|load|retrieve|sync|call|route|hand\s*off|depend|"
    r"读取|加载|检索|同步|调用|路由|转交|交给|依赖).{0,60}"
    r"(?:knowledge\s*base|private\s*repository|知识库|知识卡|工作台|共享目录|旧版本)"
)
LEGACY_RUNTIME = re.compile(
    r"(?i)(?:7-Agent|02-art-director|03-storyboard-director|04-prompt-engineer|"
    r"06-qc-supervisor|01-screenwriter|03/04|03、04、06|"
    r"(?:0[1-6]\s*(?:receives|接收).{0,30}){2,}|"
    r"ai-storyboard-director\s+v5\.3|5\.4\.2-candidate|"
    r"(?<![A-Za-z0-9])(?:A[123]|B[123]|C[12]|D1)-\d{2}(?![A-Za-z0-9]))"
)
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yaml", ".yml", ".py", ".ps1", ".sh", ".txt"}
TEXT_SUFFIXES.update({".toml", ".ini", ".cfg", ".csv", ".tsv"})
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)#]+)")
BACKTICK_FILE = re.compile(
    r"`((?:(?:references|scripts|assets|agents)/)?[A-Za-z0-9_.\-/]+"
    r"\.(?:md|json|jsonl|yaml|yml|py|ps1|txt|toml|ini|cfg|csv|tsv))`"
)
REFERENCE_ACTION = re.compile(r"(?i)(?:read|load|open|see|follow|use|读取|加载|打开|参见|详见|按|使用)")
WRITE_CONTEXT = re.compile(r"(?i)(?:write|output|save|create|export|写入|写进|输出|保存|创建|导出)")
NEGATED_RUNTIME = re.compile(r"(?i)(?:do not|does not|never|must not|不得|不读取|不加载|无需|不需要|禁止)")
GENERIC_SKILL_REFERENCE = re.compile(
    r"(?i)(?:call|use|read|load|route|hand\s*off|调用|使用|读取|加载|路由|转交|交给)"
    r".{0,30}[`$]?([a-z][a-z0-9-]*-skill)[`]?"
)
PERSONAL_SKILL_NAMES = {
    "01-sketch-to-film", "02-action-choreography", "03-cinematic-lighting",
    "04-character-creation", "05-shot-design", "06-asset-library",
    "07-control-maps", "08-screenwriting", "ai-short-drama-production",
    "ai-storyboard-director", "whitebox-previs-executor",
    "character-asset", "context-router", "cyberpunk-design",
    "d-data-analysis-semantic-layer", "d-official-market-analysis",
    "director-agent", "epic-design", "fantasy-design", "frontend-design",
    "hard-sci-fi-visual-director", "horror-design", "industrial-aigc-director",
    "noir-design", "produce-ai-video", "prop-asset", "romance-design",
    "scene-asset", "sci-fi-design", "war-design", "web-design-director",
    "wuxia-design", "xianxia-visual-director",
}


def skill_dirs(bases: tuple[Path, ...] = SKILL_BASES) -> list[Path]:
    return [
        child
        for base in bases
        if base.is_dir()
        for child in ([base] if (base / "SKILL.md").is_file() else sorted(base.iterdir()))
        if child.is_dir() and (child / "SKILL.md").is_file()
    ]


def frontmatter_name(skill: Path) -> str:
    for line in (skill / "SKILL.md").read_text(encoding="utf-8-sig").splitlines()[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"name:\s*[\"']?([^\"']+?)[\"']?\s*$", line)
        if match:
            return match.group(1).strip()
    return skill.name


def validate_skill(skill: Path, known_names: set[str]) -> list[str]:
    errors: list[str] = []
    name = frontmatter_name(skill)
    nested = [path for path in skill.rglob("SKILL.md") if path.is_file()]
    if len(nested) != 1:
        errors.append(f"{name}: expected exactly one SKILL.md, found {len(nested)}")

    entry = (skill / "SKILL.md").read_text(encoding="utf-8-sig")
    for path in skill.rglob("*"):
        if path.is_symlink():
            errors.append(f"{name}: link-like runtime file forbidden: {path.relative_to(skill)}")
            continue
        if not path.is_file() or path.suffix.casefold() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(skill).as_posix()
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        dependencies = set(LOCAL_DEPENDENCY.findall(text))
        dependencies.update(match.group(1).strip().split()[0].strip("<>") for match in MARKDOWN_LINK.finditer(text))
        for line in text.splitlines():
            if REFERENCE_ACTION.search(line) and not WRITE_CONTEXT.search(line):
                dependencies.update(match.group(1) for match in BACKTICK_FILE.finditer(line))
        for dependency in sorted(dependencies):
            if not dependency or dependency.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if dependency == "SKILL.md":
                candidate = skill / dependency
            else:
                candidate = (skill / dependency) if dependency.startswith(("references/", "scripts/", "assets/", "agents/")) else (path.parent / dependency)
            target = candidate.resolve()
            try:
                target.relative_to(skill.resolve())
            except ValueError:
                errors.append(f"{name}: dependency escapes package: {relative} -> {dependency}")
                continue
            if not target.is_file():
                errors.append(f"{name}: missing packaged dependency: {relative} -> {dependency}")

        for line_no, line in enumerate(text.splitlines(), 1):
            if LOCAL_ABSOLUTE_PATH.search(line):
                errors.append(f"{name}: machine-local path: {relative}:{line_no}")
            if UNC_PATH.search(line):
                errors.append(f"{name}: UNC runtime path: {relative}:{line_no}")
            if POSIX_LOCAL_PATH.search(line):
                errors.append(f"{name}: POSIX machine-local path: {relative}:{line_no}")
            if UPWARD_PATH.search(line):
                errors.append(f"{name}: upward runtime path: {relative}:{line_no}")
            if MACHINE_PLACEHOLDER.search(line):
                errors.append(f"{name}: machine-specific placeholder: {relative}:{line_no}")
            for runtime_match in EXTERNAL_RUNTIME.finditer(line):
                clause_start = max(line.rfind(separator, 0, runtime_match.start()) for separator in (";", "；", ".", "。")) + 1
                if not NEGATED_RUNTIME.search(line[clause_start:runtime_match.start()]):
                    errors.append(f"{name}: external runtime instruction: {relative}:{line_no}")
                    break
            if LEGACY_RUNTIME.search(line):
                errors.append(f"{name}: legacy runtime instruction: {relative}:{line_no}")
            lowered = line.casefold()
            for other in (known_names | PERSONAL_SKILL_NAMES) - {name}:
                if other.casefold() in name.casefold():
                    continue
                if other.casefold() in lowered:
                    errors.append(f"{name}: references sibling Skill {other}: {relative}:{line_no}")
                    break
            generic = GENERIC_SKILL_REFERENCE.search(line)
            if generic and generic.group(1).casefold() != name.casefold():
                errors.append(f"{name}: references unregistered Skill {generic.group(1)}: {relative}:{line_no}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="*", type=Path)
    args = parser.parse_args()
    bases = tuple(path.resolve() for path in args.roots) if args.roots else SKILL_BASES
    skills = skill_dirs(bases)
    names = {frontmatter_name(skill) for skill in skills}
    errors: list[str] = []
    if not args.roots:
        contracts = json.loads((ROOT / "docs" / "skill-contracts.json").read_text(encoding="utf-8"))
        expected = {item["name"] for item in contracts.get("skills", [])}
        if names != expected:
            errors.append(f"repository Skill identities differ from contracts: actual={sorted(names)}, expected={sorted(expected)}")
    errors.extend(error for skill in skills for error in validate_skill(skill, names))

    with tempfile.TemporaryDirectory(prefix="skill-isolation-") as temporary:
        temp_root = Path(temporary)
        for skill in skills:
            isolated = temp_root / skill.name
            shutil.copytree(skill, isolated)
            errors.extend(validate_skill(isolated, names))

    errors = list(dict.fromkeys(errors))
    print(f"Skills checked: {len(skills)}")
    print(f"Isolation copies checked: {len(skills)}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
