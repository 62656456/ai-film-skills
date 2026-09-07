# Architecture

[Complete input-to-film workflow](WORKFLOW.md) · [Module catalog](../SKILL_CATALOG.md) · [Design and review system](SKILL_DESIGN_SYSTEM.md)

## Repository layers

```text
skills/<name>/                18 regular, self-contained packages
experimental/<name>/          2 opt-in packages; excluded from the complete-studio ZIP
docs/skill-contracts.json      reviewed bilingual documentation and inventory contract
docs/skills/en/               20 generated English guides
docs/skills/zh-CN/            20 generated Simplified Chinese guides
docs/WORKFLOW.md               complete workflow, handoffs and 20 film + 1 web responsibilities
docs/assets/production-workflow.mmd  editable full workflow source
docs/showcase/manifest.json    14 accepted original images and explicit evidence state
docs/i18n/                    translated entry pages
scripts/                      install, packaging, guide generation and validation
```

Each package contains its own `SKILL.md`, necessary `references/`, and optional `scripts/`, `assets/` or `agents/openai.yaml`. No sibling Skill, private path or shared runtime directory is needed to read its bounded contract. Media generation still depends on host tools and permissions.

## Runtime and human documentation

| Layer | Authority and role |
|---|---|
| `SKILL.md` and package-local files | Runtime instructions for the named outcome |
| `docs/skill-contracts.json` | Reviewed bilingual guide content and expected package inventory |
| Generated `docs/skills/` pages | Human explanations, exact source links and package boundaries |
| `docs/WORKFLOW.md` | Optional orchestration and explicit handoffs; not a new runtime super-Skill |
| Showcase manifest | File-level public examples and recorded acceptance, not generalized success rates |

Edit runtime instructions and the reviewed contract where needed, then regenerate 40 guides with `scripts/generate_skill_guides.py`. The generated pages are not an independently edited authority.

## Authority follows the deliverable

The current request selects one primary Skill. The Skill establishes its inputs, produces the requested artifact and applies its own review gates. A second Skill is useful only when it consumes a named handoff and delivers a different necessary result. Failure returns to the earliest responsible decision while preserving approved facts.

The director owns story and interpretation. Asset contracts own approved appearance and state. Genre modules supply observable visual choices. Storyboard 5.6 designs camera and timing and, inside an explicitly identified work directory, saves and restores the decisions in `.director_design`. Those records do not replace the project's overall state or new user instructions. The helper checks recorded versions, inheritance, timing and explicit geometry; it does not score aesthetics or make every chat invocation unavoidable.

Production consumes approved material and actual model/tool capability. Whitebox previs is optional and limited to implemented proxies and passed action gates. Market analysis supplies evidence; semantic writing requires its own explicit approval and target.

## Counting and distribution

The 20 repository modules are 19 filmmaking modules plus `web-design-director`. An external xianxia link adds one workflow responsibility, not a bundled module. Thus the complete workflow shows 20 filmmaking responsibilities plus one web helper, while the repository still builds 18 regular and 2 experimental packages.

Current source, old published archives and standalone Preview artifacts have different refs. Source Storyboard Director is 5.6; Release v1.3.0 preserves 5.4.4. See [Installation](INSTALLATION.md) before choosing a distribution.

## Evidence

File validity, loading, recorded behavior, viewed output and user acceptance are distinct. The 14 current showcase images were accepted; the historical gallery and previs clips retain their original evidence labels. None of these records proves an arbitrary complete film, identical output across hosts or a same-prompt old/new comparison.
