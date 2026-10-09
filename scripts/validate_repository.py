#!/usr/bin/env python3
"""Validate the public, self-contained Agent Skill collection."""

from __future__ import annotations

import json
import hashlib
import re
import struct
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml
from yaml.constructor import ConstructorError

from repository_safety import SafetyError, is_link_like, is_within, safe_source_files
from generate_skill_guides import download_link


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOTS = (ROOT / "skills", ROOT / "experimental")
FORBIDDEN_SKILL_DIRS = {"frontend-design", "sci-fi-design", "xianxia-visual-director"}
ALLOWED_FRONTMATTER_KEYS = {"name", "description", "metadata"}
REQUIRED_REPOSITORY_FILES = {
    ".github/workflows/package-release.yml",
    ".github/workflows/validate.yml",
    ".github/ISSUE_TEMPLATE/showcase.yml",
    "CONTACT.md",
    "CONTRIBUTING.md",
    "PUBLICATION_SCOPE.md",
    "README.md",
    "RELEASE_NOTES.md",
    "SECURITY.md",
    "SKILL_CATALOG.md",
    "docs/COMPATIBILITY.md",
    "docs/INSTALLATION.md",
    "docs/.nojekyll",
    "docs/index.html",
    "docs/LAUNCH_KIT.md",
    "docs/SKILL_DESIGN_SYSTEM.md",
    "docs/site.css",
    "docs/style-gallery/manifest.json",
    "docs/showcase/manifest.json",
    "docs/style-gallery/cyberpunk-design.jpg",
    "docs/style-gallery/epic-design.jpg",
    "docs/style-gallery/fantasy-design.jpg",
    "docs/style-gallery/hard-sci-fi-visual-director.jpg",
    "docs/style-gallery/horror-design.jpg",
    "docs/style-gallery/noir-design.jpg",
    "docs/style-gallery/romance-design.jpg",
    "docs/style-gallery/war-design.jpg",
    "docs/style-gallery/wuxia-design.jpg",
    "docs/media/media-manifest.json",
    "docs/media/previs-blocking-5s.mp4",
    "docs/media/previs-blocking-preview.gif",
    "docs/media/previs-blocking-poster.png",
    "docs/media/rigged-contact-gate-2.8s.mp4",
    "docs/media/rigged-contact-preview.gif",
    "docs/media/rigged-contact-poster.png",
    "docs/assets/launch-assets.json",
    "docs/assets/review-loop.svg",
    "docs/assets/social-preview.png",
    "docs/assets/social-preview.svg",
    "docs/assets/storyboard-544-proof.png",
    "docs/assets/storyboard-544-proof.svg",
    "docs/skill-contracts.json",
    "docs/skills/INDEX.md",
    "examples/storyboard-director-5.4.4-visible-camera-plan.md",
    "examples/skills-cli-install-verification.md",
    "examples/skills-sh-index-verification.md",
    "examples/director-agent-before-after.md",
    "scripts/build_skill_packages.py",
    "scripts/generate_skill_guides.py",
    "scripts/install_skill.py",
    "scripts/repository_safety.py",
    "scripts/render_social_preview.py",
    "scripts/render_storyboard_proof.py",
    "scripts/validate_pages_site.py",
    "scripts/validate_style_gallery.py",
    "scripts/validate_skill_docs.py",
    "scripts/validate_skill_independence.py",
    "requirements-dev.txt",
}
PUBLIC_COUNT_PATTERNS = {
    "modules": re.compile(r"\b(\d+)\s+(?:(?:standalone|self-contained|independent|Agent|repository)\s+)*(?:modules|skills)\b|\b(\d+)\s+module guides\b|(\d+)\s*个(?:独立)?模块|(\d+)개\s*모듈|(\d+)\s*モジュール|本仓库\s*(\d+)\s*个?(?:源码)?包", re.I),
    "guides": re.compile(r"\b(\d+)\s+(?:bilingual\s+)?(?:pages|guides)\b|(\d+)\s*(?:个(?:逐模块页面|设计说明)|份(?:英文[／/]\s*简体中文|中英|双语)?指南)|(\d+)개\s*(?:상세 페이지|가이드)|计\s*(\d+)\s*页|計\s*(\d+)\s*ページ|\b(\d+)ガイド|bilingual_guides-(\d+)", re.I),
    "regular": re.compile(r"\b(\d+)\s+(?:stable|regular)\b|(\d+)\s*项常规|通常\s*(\d+)|일반\s*(\d+)개|regular_packages-(\d+)", re.I),
    "experimental": re.compile(r"\b(\d+)\s+(?:opt-in\s+)?(?:experimental|experiments)\b|\b(\d+)\s+opt-in packages\b|([一二两三四五六七八九十\d]+)\s*项(?:隔离)?实验|実験\s*(\d+)|실험\s*(\d+)개|experimental_packages-(\d+)", re.I),
    "locale_guides": re.compile(r"\b(\d+)\s+(?:generated\s+)?(?:English|Simplified Chinese)\s+guides\b", re.I),
}
REQUIRED_LAUNCH_ASSETS = {
    "social-preview.svg", "social-preview.png",
    "storyboard-544-proof.svg", "storyboard-544-proof.png",
}
REQUIRED_COMPATIBILITY_TERMS = {
    ".codex/skills",
    ".claude/skills",
    ".agents/skills",
    ".codebuddy/skills",
    "WorkBuddy",
    "Agent Skills",
}
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
LOCAL_DEPENDENCY = re.compile(
    r"(?<![A-Za-z0-9_/-])((?:references|scripts)/[A-Za-z0-9_.\-/]+\.(?:md|json|jsonl|py|sh|ps1))"
)
EXCLUDED_REPOSITORY_PARTS = {
    ".git", ".venv", ".pytest_cache", "__pycache__", "build", "dist", "_scratch", "_temp"
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            hash(key)
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping", node.start_mark,
                "found unhashable key", key_node.start_mark,
            ) from exc
        if key in mapping:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def parse_frontmatter(path: Path) -> tuple[dict[str, object], set[str], str | None]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, set(), "missing opening frontmatter delimiter"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, set(), "missing closing frontmatter delimiter"

    try:
        payload = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        return {}, set(), f"invalid YAML frontmatter: {exc}"
    if not isinstance(payload, dict):
        return {}, set(), "frontmatter must be a YAML mapping"
    if not all(isinstance(key, str) for key in payload):
        return {}, set(), "frontmatter keys must be strings"
    values = {str(key): value for key, value in payload.items()}
    return values, set(values), None


def expected_skill_locations() -> dict[str, str]:
    data = json.loads((ROOT / "docs" / "skill-contracts.json").read_text(encoding="utf-8"))
    items = data.get("skills")
    if not isinstance(items, list):
        raise ValueError("docs/skill-contracts.json must contain a skills list")
    expected: dict[str, str] = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise ValueError("every skill contract must be an object with a string name")
        name = item["name"]
        if name in expected:
            raise ValueError(f"duplicate skill contract: {name}")
        expected[name] = "experimental" if item.get("status") == "experimental" else "skills"
    return expected


def validate_markdown_links(markdown_files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in markdown_files:
        text = path.read_text(encoding="utf-8-sig")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if target:
                resolved = (path.parent / target).resolve()
                if not is_within(resolved, ROOT.resolve()):
                    errors.append(
                        f"relative link escapes repository: {path.relative_to(ROOT)} -> {raw_target}"
                    )
                elif not resolved.exists():
                    errors.append(f"broken relative link: {path.relative_to(ROOT)} -> {raw_target}")
    return errors


def validate_local_dependencies(skill: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8-sig")
    for dependency in sorted(set(LOCAL_DEPENDENCY.findall(text))):
        if not (skill / dependency).is_file():
            errors.append(
                f"missing local dependency: {skill_file.relative_to(ROOT)} -> {dependency}"
            )
    return errors


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("invalid PNG header")
    return struct.unpack(">II", header[16:24])


def validate_launch_assets(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifest_path = root / "docs" / "assets" / "launch-assets.json"
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid launch asset manifest: {exc}"]
    assets = payload.get("assets")
    if not isinstance(assets, list) or not assets:
        return ["launch asset manifest must contain a non-empty assets list"]
    paths = [item.get("path") for item in assets if isinstance(item, dict) and isinstance(item.get("path"), str)]
    if len(paths) != len(set(paths)):
        errors.append("launch asset manifest contains duplicate paths")
    if set(paths) != REQUIRED_LAUNCH_ASSETS:
        errors.append(f"launch asset inventory mismatch: missing={sorted(REQUIRED_LAUNCH_ASSETS - set(paths))}, unexpected={sorted(set(paths) - REQUIRED_LAUNCH_ASSETS)}")
    for item in assets:
        if not isinstance(item, dict):
            errors.append("launch asset entry must be an object")
            continue
        relative = item.get("path")
        if not isinstance(relative, str) or not relative:
            errors.append("launch asset entry has no path")
            continue
        asset = manifest_path.parent / relative
        if not asset.is_file():
            errors.append(f"missing launch asset: docs/assets/{relative}")
            continue
        expected_hash = item.get("sha256")
        if not isinstance(expected_hash, str) or sha256(asset) != expected_hash.upper():
            errors.append(f"launch asset hash mismatch: docs/assets/{relative}")
        if asset.suffix.lower() == ".png":
            try:
                actual_size = png_dimensions(asset)
            except ValueError as exc:
                errors.append(f"invalid launch PNG docs/assets/{relative}: {exc}")
                continue
            expected_size = (item.get("width"), item.get("height"))
            if actual_size != expected_size:
                errors.append(
                    f"launch PNG size mismatch docs/assets/{relative}: "
                    f"expected {expected_size}, found {actual_size}"
                )
    return errors


def validate_public_reading_routes(skills: list[Path]) -> list[str]:
    """Keep the GitHub reading guide, runtime source, and ZIP visible for every module."""
    errors: list[str] = []
    catalog_path = ROOT / "SKILL_CATALOG.md"
    index_path = ROOT / "docs" / "skills" / "INDEX.md"
    readme_path = ROOT / "README.md"
    missing_routes = [path for path in (catalog_path, index_path, readme_path) if not path.is_file()]
    if missing_routes:
        for path in missing_routes:
            errors.append(f"missing public reading route: {path.relative_to(ROOT)}")
        return errors

    catalog = catalog_path.read_text(encoding="utf-8-sig")
    index = index_path.read_text(encoding="utf-8-sig")
    readme = readme_path.read_text(encoding="utf-8-sig")
    contracts = json.loads((ROOT / "docs" / "skill-contracts.json").read_text(encoding="utf-8"))
    by_name = {item["name"]: item for item in contracts["skills"]}
    for skill in skills:
        name = skill.name
        runtime = skill.relative_to(ROOT).as_posix() + "/SKILL.md"
        design_en = f"docs/skills/en/{name}.md"
        design_zh = f"zh-CN/{name}.md"
        if design_en not in catalog:
            errors.append(f"SKILL_CATALOG.md missing human design route for {name}")
        if runtime not in catalog:
            errors.append(f"SKILL_CATALOG.md missing runtime SKILL.md route for {name}")
        item = by_name.get(name, {})
        download = item.get("download", {})
        if download.get("state") in {"historical_snapshot", "published_snapshot"}:
            route = f"releases/download/{download.get('tag')}/{name}.zip"
            if route not in catalog:
                errors.append(f"SKILL_CATALOG.md missing tagged release ZIP route for {name}")
        elif download.get("state") == "source_only":
            if str(download.get("source_install", "")) not in catalog:
                errors.append(f"SKILL_CATALOG.md missing current source-install route for {name}")
        else:
            errors.append(f"{name} lacks an explicit current-source versus release-download contract")
        if f"en/{name}.md" not in index or design_zh not in index:
            errors.append(f"docs/skills/INDEX.md missing bilingual routes for {name}")
        if runtime not in index:
            errors.append(f"docs/skills/INDEX.md missing runtime route for {name}")

    guide_count = str(len(skills) * 2)
    for required in ("docs/skills/INDEX.md", "docs/SKILL_DESIGN_SYSTEM.md", guide_count):
        if required not in readme:
            errors.append(f"README.md missing GitHub reading term: {required}")
    cli_command = "npx --yes skills@latest add 62656456/ai-film-skills --list"
    if cli_command not in readme:
        errors.append("README.md missing the verified open Skills CLI discovery command")
    directory_badge = "https://skills.sh/b/62656456/ai-film-skills"
    if directory_badge not in readme:
        errors.append("README.md missing the verified skills.sh directory badge")
    return errors


def validate_public_counts(text: str, skill_count: int, regular_count: int | None = None,
                           experimental_count: int | None = None) -> list[str]:
    errors: list[str] = []
    expected_counts = {"modules": skill_count, "guides": skill_count * 2,
                       "regular": regular_count, "experimental": experimental_count,
                       "locale_guides": skill_count}
    history_level: int | None = None
    for line in text.splitlines():
        heading = re.match(r"^(#{1,6})\s+(.+)", line)
        if heading:
            level = len(heading.group(1))
            if history_level is not None and level <= history_level:
                history_level = None
            if re.search(r"historical|history|历史|過去", heading.group(2), re.I):
                history_level = level
        if history_level is not None:
            continue
        # Explicitly dated historical release counts remain valid historical evidence.
        if re.search(r"historical|previous release|历史|이전|v1\.3\.0", line, re.I):
            continue
        for kind, pattern in PUBLIC_COUNT_PATTERNS.items():
            expected = expected_counts[kind]
            if expected is None:
                continue
            for match in pattern.finditer(line):
                value = next(value for value in match.groups() if value is not None)
                if value.isdecimal():
                    found = int(value)
                else:
                    digits = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
                              "六": 6, "七": 7, "八": 8, "九": 9}
                    if "十" in value:
                        tens, ones = value.split("十", 1)
                        found = (digits.get(tens, 1) * 10) + digits.get(ones, 0)
                    else:
                        found = digits.get(value, -1)
                if found != expected:
                    errors.append(f"public {kind} count {found} differs from registered {expected}")
    return errors


def public_count_files(root: Path = ROOT) -> list[Path]:
    """Check current public entry points while keeping research history separate."""
    paths = set(root.glob("*.md")) | set((root / "docs").glob("*.md"))
    paths.update((root / "docs" / "i18n").glob("*/README.md"))
    paths.update({root / "docs" / "skills" / "INDEX.md", root / "docs" / "index.html"})
    return sorted(paths)


def validate_director_example(root: Path = ROOT) -> list[str]:
    path = root / "examples" / "director-agent-before-after.md"
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return [f"cannot read director-agent public example: {exc}"]
    required = ("### Earliest break", "## Upstream repair", "## Revised screenplay",
                "## Self-audit only", "SELF-AUDIT ONLY", "No independent cold reader was used")
    return [f"director-agent public example missing evidence term: {term}" for term in required if term not in text]


def validate_download_contracts() -> list[str]:
    errors: list[str] = []
    data = json.loads((ROOT / "docs" / "skill-contracts.json").read_text(encoding="utf-8"))
    for item in data["skills"]:
        for locale in ("en", "zh-CN"):
            page = ROOT / "docs" / "skills" / locale / f"{item['name']}.md"
            try:
                link, note = download_link(item, page, locale)
            except (ValueError, KeyError, TypeError) as exc:
                errors.append(f"invalid download contract: {exc}")
                continue
            if page.is_file():
                text = page.read_text(encoding="utf-8-sig")
                if link not in text or note not in text:
                    errors.append(f"guide does not expose its download state: {page.relative_to(ROOT)}")
                if "releases/latest/download/" in text:
                    errors.append(f"guide incorrectly maps current source to latest release: {page.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    skills: list[Path] = []

    for required in sorted(REQUIRED_REPOSITORY_FILES):
        if not (ROOT / required).is_file():
            errors.append(f"missing repository file: {required}")
    if (ROOT / "skills" / "references").exists():
        errors.append("shared skills/references directory is forbidden; every dependency must be local")

    compatibility = ROOT / "docs" / "COMPATIBILITY.md"
    if compatibility.is_file():
        compatibility_text = compatibility.read_text(encoding="utf-8-sig")
        for term in sorted(REQUIRED_COMPATIBILITY_TERMS):
            if term not in compatibility_text:
                errors.append(f"compatibility guide is missing: {term}")

    actual_locations: dict[str, str] = {}
    for skill_root in SKILL_ROOTS:
        if not skill_root.is_dir():
            errors.append(f"missing directory: {skill_root.relative_to(ROOT)}")
            continue
        for child in sorted(p for p in skill_root.iterdir() if p.is_dir()):
            if (child / "SKILL.md").exists():
                skills.append(child)
                actual_locations[child.name] = skill_root.name

    names = {path.name for path in skills}
    forbidden = sorted(names & FORBIDDEN_SKILL_DIRS)
    if forbidden:
        errors.append("forbidden Skill directories present: " + ", ".join(forbidden))
    try:
        expected_locations = expected_skill_locations()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        expected_locations = {}
        errors.append(f"invalid skill contract registry: {exc}")
    missing_skills = sorted(set(expected_locations) - set(actual_locations))
    extra_skills = sorted(set(actual_locations) - set(expected_locations))
    if missing_skills:
        errors.append("contracted Skills missing from repository: " + ", ".join(missing_skills))
    if extra_skills:
        errors.append("unregistered Skill directories present: " + ", ".join(extra_skills))
    for name in sorted(set(expected_locations) & set(actual_locations)):
        if expected_locations[name] != actual_locations[name]:
            errors.append(
                f"Skill status location mismatch for {name}: expected "
                f"{expected_locations[name]}, found {actual_locations[name]}"
            )

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
        missing = {"name", "description"} - keys
        if extras:
            errors.append(f"{skill_file.relative_to(ROOT)}: non-portable frontmatter keys {sorted(extras)}")
        if missing:
            errors.append(f"{skill_file.relative_to(ROOT)}: missing frontmatter keys {sorted(missing)}")
        if values.get("name") != skill.name:
            errors.append(
                f"{skill_file.relative_to(ROOT)}: name {values.get('name')!r} does not match directory"
            )
        description = values.get("description", "")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{skill_file.relative_to(ROOT)}: description must be 1-1024 characters")

        # Optional Codex metadata must never become a dependency for other hosts.
        agent_file = skill / "agents" / "openai.yaml"
        if agent_file.exists():
            agent_text = agent_file.read_text(encoding="utf-8-sig")
            for required in ("display_name:", "short_description:", "default_prompt:"):
                if required not in agent_text:
                    errors.append(f"{agent_file.relative_to(ROOT)}: missing {required[:-1]}")
            if f"${skill.name}" not in agent_text:
                errors.append(f"{agent_file.relative_to(ROOT)}: default_prompt must mention ${skill.name}")
        errors.extend(validate_local_dependencies(skill))
        try:
            safe_source_files(skill)
        except (OSError, SafetyError) as exc:
            errors.append(f"unsafe Skill source tree {rel}: {exc}")

    errors.extend(validate_public_reading_routes(skills))
    errors.extend(validate_download_contracts())
    errors.extend(validate_launch_assets())

    errors.extend(validate_director_example())
    stable_count = sum(1 for path in skills if path.parent.name == "skills")
    experimental_count = sum(1 for path in skills if path.parent.name == "experimental")
    for path in public_count_files():
        try:
            text = path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            errors.append(f"cannot read public count entry {path.relative_to(ROOT)}: {exc}")
            continue
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in
                      validate_public_counts(text, len(skills), stable_count, experimental_count))

    repository_paths = [
        path
        for path in ROOT.rglob("*")
        if not (set(path.relative_to(ROOT).parts) & EXCLUDED_REPOSITORY_PARTS)
    ]
    for path in repository_paths:
        if is_link_like(path):
            errors.append(f"repository links and junctions are forbidden: {path.relative_to(ROOT)}")
    markdown_files = sorted(
        path for path in repository_paths if path.is_file() and path.suffix.lower() == ".md" and not path.name.endswith(".next.md")
    )
    errors.extend(validate_markdown_links(markdown_files))

    scan_files = [
        path
        for path in repository_paths
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in {".md", ".yaml", ".yml", ".json", ".py", ".txt"}
    ]
    for path in scan_files:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {label}: {path.relative_to(ROOT)}")
        if path.resolve() != Path(__file__).resolve() and PRIVATE_WINDOWS_PATH.search(text):
            warnings.append(f"local absolute path reference: {path.relative_to(ROOT)}")

    stable_count = sum(1 for path in skills if path.parent.name == "skills")
    experimental_count = sum(1 for path in skills if path.parent.name == "experimental")
    print(f"Skills checked: {len(skills)} (stable={stable_count}, experimental={experimental_count})")
    print(f"Markdown files checked: {len(markdown_files)}")
    print(
        f"GitHub design guides required: {len(skills) * 2} "
        f"({len(skills)} English + {len(skills)} Simplified Chinese)"
    )
    print("Portable hosts documented: Codex, Claude Code, TRAE, CodeBuddy, WorkBuddy, generic")
    print(f"Warnings: {len(warnings)}")
    for warning in sorted(set(warnings)):
        print(f"WARN: {warning}")
    print(f"Errors: {len(errors)}")
    for error in sorted(set(errors)):
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
