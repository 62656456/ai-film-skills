#!/usr/bin/env python3
"""Validate the public Skill collection without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOTS = (ROOT / "skills", ROOT / "experimental")
FORBIDDEN_SKILL_DIRS = {
    "frontend-design",
    "sci-fi-design",
    "xianxia-visual-director",
}
ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}"),
    "GitHub fine-grained token": re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
    "OpenAI-style key": re.compile(r"sk-[A-Za-z0-9_-]{24,}"),
    "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
PRIVATE_WINDOWS_PATH = re.compile(
    r"(?i)(?:[A-Z]:\\(?:Codex|zhishiku|Claude cold)\\|C:/Users/)[^\s`\"'<>]+"
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], set[str], str | None]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, set(), "missing opening frontmatter delimiter"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, set(), "missing closing frontmatter delimiter"

    values: dict[str, str] = {}
    keys: set[str] = set()
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            key, value = match.groups()
            keys.add(key)
            values[key] = value.strip().strip('"\'')
    return values, keys, None


def validate_markdown_links(markdown_files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in markdown_files:
        text = path.read_text(encoding="utf-8-sig")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"broken relative link: {path.relative_to(ROOT)} -> {raw_target}")
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    skills: list[Path] = []

    for skill_root in SKILL_ROOTS:
        if not skill_root.is_dir():
            errors.append(f"missing directory: {skill_root.relative_to(ROOT)}")
            continue
        for child in sorted(p for p in skill_root.iterdir() if p.is_dir()):
            skill_file = child / "SKILL.md"
            if skill_file.exists():
                skills.append(child)

    names = {path.name for path in skills}
    forbidden = sorted(names & FORBIDDEN_SKILL_DIRS)
    if forbidden:
        errors.append("forbidden Skill directories present: " + ", ".join(forbidden))

    if len(skills) != 19:
        errors.append(f"expected 19 packaged Skills (18 stable + 1 experimental), found {len(skills)}")

    for skill in skills:
        rel = skill.relative_to(ROOT)
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill.name):
            errors.append(f"invalid Skill directory name: {rel}")

        skill_file = skill / "SKILL.md"
        values, keys, parse_error = parse_frontmatter(skill_file)
        if parse_error:
            errors.append(f"{skill_file.relative_to(ROOT)}: {parse_error}")
            continue
        extras = keys - ALLOWED_FRONTMATTER_KEYS
        missing = ALLOWED_FRONTMATTER_KEYS - keys
        if extras:
            errors.append(f"{skill_file.relative_to(ROOT)}: unsupported frontmatter keys {sorted(extras)}")
        if missing:
            errors.append(f"{skill_file.relative_to(ROOT)}: missing frontmatter keys {sorted(missing)}")
        if values.get("name") != skill.name:
            errors.append(
                f"{skill_file.relative_to(ROOT)}: name {values.get('name')!r} does not match directory"
            )
        description = values.get("description", "")
        if not description or len(description) > 1024:
            errors.append(f"{skill_file.relative_to(ROOT)}: description must be 1-1024 characters")

        agent_file = skill / "agents" / "openai.yaml"
        if not agent_file.exists():
            errors.append(f"missing agent metadata: {agent_file.relative_to(ROOT)}")
        else:
            agent_text = agent_file.read_text(encoding="utf-8-sig")
            for required in ("display_name:", "short_description:", "default_prompt:"):
                if required not in agent_text:
                    errors.append(f"{agent_file.relative_to(ROOT)}: missing {required[:-1]}")
            if f"${skill.name}" not in agent_text:
                errors.append(f"{agent_file.relative_to(ROOT)}: default_prompt must mention ${skill.name}")

    markdown_files = sorted(ROOT.rglob("*.md"))
    errors.extend(validate_markdown_links(markdown_files))

    scan_files = [
        path
        for base in SKILL_ROOTS
        for path in base.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml", ".json", ".py", ".txt"}
    ]
    for path in scan_files:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {label}: {path.relative_to(ROOT)}")
        if PRIVATE_WINDOWS_PATH.search(text):
            warnings.append(f"local absolute path reference: {path.relative_to(ROOT)}")

    print(f"Skills checked: {len(skills)} (stable={sum(1 for p in skills if p.parent.name == 'skills')}, experimental={sum(1 for p in skills if p.parent.name == 'experimental')})")
    print(f"Markdown files checked: {len(markdown_files)}")
    print(f"Warnings: {len(warnings)}")
    for warning in sorted(set(warnings)):
        print(f"WARN: {warning}")
    print(f"Errors: {len(errors)}")
    for error in sorted(set(errors)):
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
