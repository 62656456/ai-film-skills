#!/usr/bin/env python3
"""Generate bilingual, GitHub-readable design guides for every packaged Skill."""

from __future__ import annotations

import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "docs" / "skill-contracts.json"
OUTPUT = ROOT / "docs" / "skills"
LOCALES = ("en", "zh-CN")


def local(value: object, locale: str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        result = value.get(locale)
        if isinstance(result, str):
            return result
    raise ValueError(f"missing {locale} text in {value!r}")


def merge_contract(data: dict[str, object], item: dict[str, object]) -> dict[str, object]:
    families = data["families"]
    assert isinstance(families, dict)
    family = families[item["family"]]
    assert isinstance(family, dict)
    merged: dict[str, object] = dict(family)
    merged.update(item)
    for key in ("principles", "inputs", "workflow", "returns", "review", "pass", "outputs", "boundaries"):
        base = family.get(key, [])
        extra = item.get(f"extra_{key}", [])
        assert isinstance(base, list) and isinstance(extra, list)
        merged[key] = [*base, *extra]
    return merged


def skill_root(item: dict[str, object]) -> Path:
    base = "experimental" if item["status"] == "experimental" else "skills"
    return ROOT / base / str(item["name"])


def rel_link(source_page: Path, destination: Path) -> str:
    return Path(os.path.relpath(destination, source_page.parent)).as_posix()


def resources(page: Path, skill: Path, locale: str) -> list[str]:
    groups: dict[str, list[Path]] = {"runtime": [], "references": [], "scripts": [], "versions": [], "other": []}
    # Sort by normalized relative paths so generated guides are identical across hosts.
    for path in sorted(
        (candidate for candidate in skill.rglob("*") if candidate.is_file()),
        key=lambda candidate: (
            candidate.relative_to(skill).as_posix().casefold(),
            candidate.relative_to(skill).as_posix(),
        ),
    ):
        rel = path.relative_to(skill)
        if rel.as_posix() in {"SKILL.md", "agents/openai.yaml"}:
            key = "runtime"
        elif rel.parts[0] == "references":
            key = "references"
        elif rel.parts[0] == "scripts":
            key = "scripts"
        elif rel.parts[0] == "versions":
            key = "versions"
        else:
            key = "other"
        groups[key].append(path)

    labels_by_locale = {
        "en": {
            "runtime": "Runtime and metadata",
            "references": "References",
            "scripts": "Deterministic helpers",
            "versions": "Version and rollback evidence",
            "other": "Other packaged files",
        },
        "zh-CN": {
            "runtime": "运行正文与元数据",
            "references": "引用资料",
            "scripts": "确定性辅助脚本",
            "versions": "版本与回退证据",
            "other": "其他随包文件",
        },
    }
    labels = labels_by_locale[locale]
    lines: list[str] = []
    for key in ("runtime", "references", "scripts", "versions", "other"):
        if not groups[key]:
            continue
        lines.extend([f"**{labels[key]}**", ""])
        for path in groups[key]:
            label = path.relative_to(skill).as_posix()
            lines.append(f"- [`{label}`]({rel_link(page, path)})")
        lines.append("")
    return lines


def numbered(values: list[object], locale: str) -> list[str]:
    return [f"{index}. {local(value, locale)}" for index, value in enumerate(values, start=1)]


def bullets(values: list[object], locale: str, checklist: bool = False) -> list[str]:
    prefix = "- [ ]" if checklist else "-"
    return [f"{prefix} {local(value, locale)}" for value in values]


HEADINGS = {
    "en": [
        "Purpose", "Design principles", "Standalone scope", "Inputs", "Workflow",
        "Return, rework, and rollback", "Review gates", "Pass standard and states",
        "Outputs", "Boundaries, dependencies, and permissions", "Cross-Agent use",
        "Source files and references",
    ],
    "zh-CN": [
        "设计目的", "设计理念", "适合单独使用的范围", "输入", "流程逻辑",
        "退回、重做与版本回滚", "审核门", "过关标准与状态",
        "输出", "边界、依赖与权限", "跨 Agent 使用", "原始文件与引用",
    ],
}


def guide(data: dict[str, object], item: dict[str, object], locale: str) -> str:
    contract = merge_contract(data, item)
    name = str(item["name"])
    page = OUTPUT / locale / f"{name}.md"
    skill = skill_root(item)
    headings = HEADINGS[locale]
    status = local(item["status_label"], locale)
    runtime = skill / "SKILL.md"
    zip_url = f"https://github.com/62656456/ai-film-skills/releases/latest/download/{name}.zip"
    common_system = rel_link(page, ROOT / "docs" / "SKILL_DESIGN_SYSTEM.md")
    install = rel_link(page, ROOT / "docs" / "INSTALLATION.md")
    compatibility = rel_link(page, ROOT / "docs" / "COMPATIBILITY.md")

    if locale == "en":
        summary_labels = ("Status", "Can deliver alone", "Cannot claim alone")
        links = f"[Runtime `SKILL.md`]({rel_link(page, runtime)}) · [Standalone ZIP]({zip_url}) · [Install]({install}) · [Compatibility]({compatibility}) · [Design system]({common_system})"
        status_note = "A pass below means this module's stated gates were met. Structural validity, real-task evidence, and user acceptance remain separate states."
        standalone_intro = "Use this module by itself when the requested result stays inside the following boundary:"
        cross_agent = [
            "The canonical package is the complete Skill folder, not a copied prompt fragment.",
            "`agents/openai.yaml` is optional Codex UI metadata and is not a runtime dependency for other hosts.",
            local(contract["requires"], locale),
            "An Agent may read the instructions without native Skill discovery, but prompt-only reading must not be described as native integration.",
        ]
    else:
        summary_labels = ("状态", "单独可交付", "单独不能声称")
        links = f"[运行正文 `SKILL.md`]({rel_link(page, runtime)}) · [独立 ZIP]({zip_url}) · [安装说明]({install}) · [兼容说明]({compatibility}) · [设计总则]({common_system})"
        status_note = "下方“通过”只表示本模块规定的审核门已通过；结构有效、真实任务证据和用户接受必须分开记录。"
        standalone_intro = "当点名结果落在以下边界内时，可以只拿这一个模块使用："
        cross_agent = [
            "标准包是完整 Skill 文件夹，不是只复制一段提示词。",
            "`agents/openai.yaml` 只是 Codex 的可选界面元数据，不是其他宿主的运行依赖。",
            local(contract["requires"], locale),
            "Agent 能阅读指令不等于原生发现或原生执行；提示词回退不能写成原生兼容。",
        ]

    lines = [
        f"# {local(item['title'], locale)}",
        "",
        f"| {summary_labels[0]} | {status} |",
        "|---|---|",
        f"| {summary_labels[1]} | {local(item['standalone'], locale)} |",
        f"| {summary_labels[2]} | {local(item['cannot'], locale)} |",
        "",
        links,
        "",
        "<!-- contract:purpose -->", f"## 1. {headings[0]}", "", local(item["purpose"], locale), "",
        "<!-- contract:principles -->", f"## 2. {headings[1]}", "", *bullets(contract["principles"], locale), "",
        "<!-- contract:standalone -->", f"## 3. {headings[2]}", "", standalone_intro, "", local(item["standalone"], locale), "", f"**{summary_labels[2]}:** {local(item['cannot'], locale)}", "",
        "<!-- contract:inputs -->", f"## 4. {headings[3]}", "", *bullets(contract["inputs"], locale), "",
        "<!-- contract:workflow -->", f"## 5. {headings[4]}", "", *numbered(contract["workflow"], locale), "",
        "<!-- contract:returns -->", f"## 6. {headings[5]}", "", *bullets(contract["returns"], locale), "",
        "<!-- contract:review -->", f"## 7. {headings[6]}", "", *bullets(contract["review"], locale, checklist=True), "",
        "<!-- contract:pass -->", f"## 8. {headings[7]}", "", *bullets(contract["pass"], locale), "", f"> {status_note}", "",
        "<!-- contract:outputs -->", f"## 9. {headings[8]}", "", *bullets(contract["outputs"], locale), "",
        "<!-- contract:boundaries -->", f"## 10. {headings[9]}", "", *bullets(contract["boundaries"], locale), "",
        "<!-- contract:agents -->", f"## 11. {headings[10]}", "", *bullets(cross_agent, locale), "",
        "<!-- contract:sources -->", f"## 12. {headings[11]}", "", *resources(page, skill, locale),
    ]
    return "\n".join(lines).rstrip() + "\n"


def index(data: dict[str, object]) -> str:
    items = data["skills"]
    assert isinstance(items, list)
    lines = [
        "# Standalone Skill design guides / 独立 Skill 设计说明",
        "",
        "Every module can be read directly on GitHub before installation. Each guide explains purpose, design logic, inputs, workflow, return paths, review gates, pass evidence, outputs, boundaries, host requirements, and every packaged source file.",
        "",
        "每个模块都可以在安装前直接通过 GitHub 阅读。每页都说明用途、设计理念、输入、流程、退回、审核、过关证据、输出、边界、宿主能力和全部随包文件。",
        "",
        "The English and Simplified Chinese pages are generated from the same reviewed contract data. Runtime truth remains the linked `SKILL.md`; these pages explain it rather than replace it.",
        "",
        "| Skill | State | English | 简体中文 | Runtime |",
        "|---|---|---|---|---|",
    ]
    for item in items:
        assert isinstance(item, dict)
        name = str(item["name"])
        skill = skill_root(item)
        runtime = rel_link(OUTPUT / "INDEX.md", skill / "SKILL.md")
        state = local(item["status_label"], "en")
        lines.append(f"| `{name}` | {state} | [Design guide](en/{name}.md) | [设计说明](zh-CN/{name}.md) | [`SKILL.md`]({runtime}) |")
    lines.extend([
        "",
        "## Common review logic / 共同审核逻辑",
        "",
        "Read [How every Skill is designed](../SKILL_DESIGN_SYSTEM.md) for the shared cause-directed return loop and evidence states.",
        "",
        "共同的定向退回和证据状态见 [每个 Skill 如何设计](../SKILL_DESIGN_SYSTEM.md)。",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    data = json.loads(CONTRACTS.read_text(encoding="utf-8"))
    items = data["skills"]
    assert isinstance(items, list)
    for locale in LOCALES:
        destination = OUTPUT / locale
        destination.mkdir(parents=True, exist_ok=True)
        expected = {f"{item['name']}.md" for item in items if isinstance(item, dict)}
        for stale in destination.glob("*.md"):
            if stale.name not in expected:
                stale.unlink()
        for item in items:
            assert isinstance(item, dict)
            (destination / f"{item['name']}.md").write_text(
                guide(data, item, locale), encoding="utf-8", newline="\n"
            )
    (OUTPUT / "INDEX.md").write_text(index(data), encoding="utf-8", newline="\n")
    print(f"Generated {len(items) * len(LOCALES)} guides and one index")


if __name__ == "__main__":
    main()
