# Agent compatibility

Open Film Skills distributes complete, host-neutral Skill folders. Compatibility means preserving the instructions and local resources; it does not guarantee native discovery, identical model behavior or media tools in every host.

```text
skill-name/
  SKILL.md
  references/             when required by the Skill
  scripts/                deterministic helpers, when present
  assets/                 when present
  agents/openai.yaml      optional Codex presentation metadata
```

## Host routes and evidence

These are the repository's documented installation routes and prior compatibility references. They are not a fresh end-to-end certification of every current client version. Check the selected host's current documentation and the actual result of importing the package.

| Host | Documented route | Evidence boundary |
|---|---|---|
| Codex | `$CODEX_HOME/skills/<name>/`, falling back to `~/.codex/skills/<name>/`; installer `--platform codex` or explicit `--target` | The maintainer uses this package model; activation, tool access and a real task still need verification |
| Claude Code | `~/.claude/skills/<name>/` or project `.claude/skills/<name>/` | Portable package support documented by the host; no claim of current cross-model output parity |
| TRAE | Project `.agents/skills/<name>/` | Prior official changelog reference; verify the installed client |
| CodeBuddy Code / IDE | `~/.codebuddy/skills/<name>/` or project `.codebuddy/skills/<name>/` | Prior official package-layout references; verify import and execution |
| WorkBuddy | Local standalone ZIP import through its Skill UI | Prior import documentation; menu names and package validation may vary by version |
| Other hosts | Native Skill library if supported; otherwise attach complete instructions and resources | Reading instructions is not native discovery or permission to execute tools |

## Capability requirements

| Task | Required host capability |
|---|---|
| Script, visual parameters or prompt text | Read the complete Skill and relevant supplied material |
| Storyboard 5.6 persistence and recovery | Read/write the explicitly supplied project directory; run its standard-library Python helper |
| Actual reference images | Authorized image tool, usable result retrieval and visual inspection |
| Whitebox previs | Python, compatible Blender and actual MP4 decoding; implementation-specific proxies and action gates |
| Finished AI video | Model access, generation/edit/sound tools, full playback review and applicable permissions |
| Current market research | Current source access and evidence citation; offline text cannot invent live data |
| Semantic-layer writing | Explicit current approval, target access, version preservation and readback |

No Skill grants missing credits, account access, publication rights or host permissions. `agents/openai.yaml` is presentation metadata, not a universal execution engine. Experimental isolation is a distribution choice; it does not prove that a host has no local installation.

## Product names

The historical compatibility review distinguished Claude Code from an ambiguous “Cloud Code”, TRAE from Trint, and WorkBuddy from “WorkerBilly”. An unclear product name should be resolved from its actual official product and import format. This repository does not claim native Skill support for a transcription product merely because it can process text.

## Official references

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [TRAE changelog](https://www.trae.cn/changelog)
- [CodeBuddy Code Skills](https://www.codebuddy.cn/docs/cli/skills)
- [CodeBuddy IDE Skills](https://www.codebuddy.cn/docs/ide/Features/Skills)
- [WorkBuddy Skills](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [Trint product information](https://trint.com/how-to-trint)

See [Installation](INSTALLATION.md) for source versus historical-release choices. Report actual host versions and reproducible outcomes through [Issues](https://github.com/62656456/ai-film-skills/issues).
