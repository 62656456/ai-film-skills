# Agent compatibility

Open Film Skills uses one canonical, platform-neutral package:

```text
skill-name/
├── SKILL.md
├── references/   (optional)
├── scripts/      (optional)
├── assets/       (optional)
└── agents/openai.yaml   (optional Codex presentation metadata)
```

`SKILL.md` contains only the portable `name` and `description` frontmatter fields. A host may ignore files it does not recognize. In particular, `agents/openai.yaml` is an optional Codex enhancement; no Skill instruction depends on it.

## Compatibility levels

| Host | Level | Install or import path | What is verified |
|---|---|---|---|
| Codex | Native Skill package | `$CODEX_HOME/skills/<name>/` or `~/.codex/skills/<name>/` | This repository's current authoring and validation environment uses the same self-contained `SKILL.md` package model. |
| Claude Code | Native Agent Skill | `~/.claude/skills/<name>/` or `.claude/skills/<name>/` | Anthropic documents `SKILL.md`, supporting files, and the Agent Skills open standard. |
| TRAE | Native Skill package | `<project>/.agents/skills/<name>/` | TRAE's official changelog states that current versions auto-load Skill plugins from `.agents/skills`. |
| CodeBuddy Code / IDE | Native Skill package | `~/.codebuddy/skills/<name>/` or `.codebuddy/skills/<name>/` | Tencent's official docs define the same `SKILL.md` plus optional `scripts/`, `references/`, and `assets/` structure. |
| WorkBuddy | Official local-package import | **Add Skill → Upload Skill**, then select the downloaded ZIP | Tencent's official WorkBuddy docs support importing a local Skill package. The exact UI flow can change by client version. |
| Other Agent software | Portable fallback | Use the host's Skill library if it supports Agent Skills; otherwise attach/import `SKILL.md` and its local resources as instructions | Instruction portability is supported; native discovery, tools, permissions, and script execution depend on the host. |

## Name checks from the original request

- **“Cloud Code”** is treated here as **Claude Code**, because Claude Code is the officially documented Agent product with native Skills. If a different product was intended, please send its official product link.
- **“Trint”** currently resolves to Trint's transcription and content platform. Its official public material does not establish native `SKILL.md` loading, so this repository does **not** label Trint as a native Agent-Skills host. If **TRAE** was intended, TRAE is supported above.
- **“WorkerBilly”** was not matched to a verified official Agent product during the compatibility review. If **WorkBuddy** was intended, WorkBuddy is supported above. A different product can still use the portable fallback after its official import format is known.

These distinctions prevent a marketing claim from outrunning actual product support. “Can read the instructions” is not the same as “natively discovers and runs the Skill.”

## Host-neutral rules

1. The canonical source is always the Skill folder, not a host-specific copy.
2. Required knowledge and scripts stay inside that Skill folder.
3. No instruction may require a private path, another repository, or Codex-only metadata.
4. Host-specific permissions and tool names are resolved at runtime; a Skill never bypasses a host's approval model.
5. Structural compatibility does not prove identical output quality across models. Real-task validation is recorded separately.

## Official references

- [Agent Skills open specification](https://agentskills.io/specification)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [TRAE changelog](https://www.trae.cn/changelog)
- [CodeBuddy Code Skills](https://www.codebuddy.cn/docs/cli/skills)
- [CodeBuddy IDE Skills](https://www.codebuddy.cn/docs/ide/Features/Skills)
- [WorkBuddy Skills](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [Trint product guide](https://trint.com/how-to-trint)

To report a host whose official format is missing, open an issue or email [haldissita@gmail.com](mailto:haldissita@gmail.com).
