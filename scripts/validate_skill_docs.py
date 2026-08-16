#!/usr/bin/env python3
"""Validate bilingual Skill design guides and their complete source links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "docs" / "skill-contracts.json"
DOCS = ROOT / "docs" / "skills"
LOCALES = ("en", "zh-CN")
MARKERS = (
    "purpose", "principles", "standalone", "inputs", "workflow", "returns",
    "review", "pass", "outputs", "boundaries", "agents", "sources",
)
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def discovered() -> dict[str, Path]:
    result: dict[str, Path] = {}
    for base in (ROOT / "skills", ROOT / "experimental"):
        for child in sorted(base.iterdir()):
            if child.is_dir() and (child / "SKILL.md").is_file():
                result[child.name] = child
    return result


def main() -> int:
    errors: list[str] = []
    data = json.loads(CONTRACTS.read_text(encoding="utf-8"))
    items = data.get("skills", [])
    manifest = {item["name"]: item for item in items}
    skills = discovered()

    if set(manifest) != set(skills):
        errors.append(f"contract names differ from Skill folders: contracts={sorted(manifest)}, skills={sorted(skills)}")

    for skill in skills.values():
        for forbidden in ("README.md", "INSTALLATION_GUIDE.md", "CHANGELOG.md"):
            if (skill / forbidden).exists():
                errors.append(f"extraneous human doc inside Skill folder: {(skill / forbidden).relative_to(ROOT)}")

    expected_pages = {f"{name}.md" for name in manifest}
    for locale in LOCALES:
        actual = {path.name for path in (DOCS / locale).glob("*.md")} if (DOCS / locale).is_dir() else set()
        if actual != expected_pages:
            errors.append(f"{locale} guide set mismatch: expected={sorted(expected_pages)}, actual={sorted(actual)}")
        for name, skill in skills.items():
            page = DOCS / locale / f"{name}.md"
            if not page.is_file():
                continue
            text = page.read_text(encoding="utf-8-sig")
            for marker in MARKERS:
                token = f"<!-- contract:{marker} -->"
                if text.count(token) != 1:
                    errors.append(f"{page.relative_to(ROOT)}: expected one {token}")
            runtime_rel = skill.relative_to(ROOT).as_posix() + "/SKILL.md"
            if runtime_rel not in text and f"../../../{runtime_rel}" not in text:
                errors.append(f"{page.relative_to(ROOT)}: missing direct runtime link")
            if manifest[name]["status"] == "experimental":
                lower = text.casefold()
                if "experimental" not in lower and "实验" not in text:
                    errors.append(f"{page.relative_to(ROOT)}: experimental state not visible")

            linked: set[Path] = set()
            for raw in LINK.findall(text):
                target = unquote(raw.strip().split()[0].strip("<>").split("#", 1)[0])
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (page.parent / target).resolve()
                if not resolved.exists():
                    errors.append(f"broken guide link: {page.relative_to(ROOT)} -> {raw}")
                linked.add(resolved)
            for source in sorted(path for path in skill.rglob("*") if path.is_file()):
                if source.resolve() not in linked:
                    errors.append(f"{page.relative_to(ROOT)}: packaged file is not linked: {source.relative_to(skill)}")

    if not (DOCS / "INDEX.md").is_file():
        errors.append("missing docs/skills/INDEX.md")
    else:
        index = (DOCS / "INDEX.md").read_text(encoding="utf-8-sig")
        for name in manifest:
            for locale in LOCALES:
                if f"{locale}/{name}.md" not in index:
                    errors.append(f"docs/skills/INDEX.md missing {locale}/{name}.md")

    all_text = "\n".join(
        path.read_text(encoding="utf-8-sig", errors="replace")
        for root in (ROOT / "skills", ROOT / "docs")
        for path in root.rglob("*.md")
    )
    if "ai-storyboard-director v5.3" in all_text:
        errors.append("stale ai-storyboard-director v5.3 reference remains")
    architecture = (ROOT / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8-sig")
    if "references/                shared contracts" in architecture:
        errors.append("architecture still claims a shared references directory")

    print(f"Contract entries: {len(manifest)}")
    print(f"Guides expected: {len(manifest) * len(LOCALES)}")
    print(f"Packaged source files covered: {sum(1 for skill in skills.values() for path in skill.rglob('*') if path.is_file())}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
