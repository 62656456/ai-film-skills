<div align="center">

<img src="docs/assets/hero.svg" width="100%" alt="Open Film Skills — story, design, shot and production intelligence for AI filmmaking" />

# Open Film Skills

**Portable, modular directing intelligence for Codex, Claude Code, TRAE, CodeBuddy, WorkBuddy, and other Agent software.**

[简体中文](docs/i18n/zh-CN/README.md) · [日本語](docs/i18n/ja/README.md) · [한국어](docs/i18n/ko/README.md) · **English**

![Packaged skills](https://img.shields.io/badge/packaged_skills-18-FF6B35?style=flat-square)
![Experimental skills](https://img.shields.io/badge/experimental-1-D6A756?style=flat-square)
![Standalone packages](https://img.shields.io/badge/standalone_packages-19-7ED6A5?style=flat-square)
![Design guides](https://img.shields.io/badge/design_guides-38-46C2CB?style=flat-square)
![Agent hosts](https://img.shields.io/badge/agent_hosts-5%20documented%20%2B%20generic-46C2CB?style=flat-square)
![Languages](https://img.shields.io/badge/readme_languages-4-46C2CB?style=flat-square)
[![License](https://img.shields.io/badge/license-Apache--2.0-5B8CFF?style=flat-square)](LICENSE)
[![Validate Skills](https://github.com/62656456/ai-film-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/62656456/ai-film-skills/actions/workflows/validate.yml)

</div>

## Two ways in

| I need one craft | I want the complete studio |
|---|---|
| Read one module's design contract on GitHub, download one ZIP, and install one self-contained folder. No shared repository directory is required. | Install all 18 packaged Skills in the Agent host you already use, then move from script through assets, shots, production, and validation. |
| [Browse 38 English / Chinese design guides](docs/skills/INDEX.md) · [Choose one Skill](SKILL_CATALOG.md) · [Installation guide](docs/INSTALLATION.md) | [Download the complete package](https://github.com/62656456/ai-film-skills/releases/latest/download/open-film-skills-complete.zip) · [Architecture](docs/ARCHITECTURE.md) |

## Start here

The design guide is the human-readable entrance. The linked runtime file remains the exact Agent instruction, and the ZIP remains the standalone installable package.

| I want to… | Read the design | Runtime | ZIP |
|---|---|---|---|
| Write, revise, or diagnose a script | [`director-agent`](docs/skills/en/director-agent.md) | [`SKILL.md`](skills/director-agent/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/director-agent.zip) |
| Turn an approved script into readable shots and generation prompts | [`ai-storyboard-director`](docs/skills/en/ai-storyboard-director.md) | [`SKILL.md`](skills/ai-storyboard-director/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-storyboard-director.zip) |
| Define reusable character, scene, or prop references | [`character-asset`](docs/skills/en/character-asset.md) · [`scene-asset`](docs/skills/en/scene-asset.md) · [`prop-asset`](docs/skills/en/prop-asset.md) | [Character](skills/character-asset/SKILL.md) · [Scene](skills/scene-asset/SKILL.md) · [Prop](skills/prop-asset/SKILL.md) | [Character](https://github.com/62656456/ai-film-skills/releases/latest/download/character-asset.zip) · [Scene](https://github.com/62656456/ai-film-skills/releases/latest/download/scene-asset.zip) · [Prop](https://github.com/62656456/ai-film-skills/releases/latest/download/prop-asset.zip) |
| Add an observable genre-specific visual language | [Browse genre design guides](SKILL_CATALOG.md#genre-visual-language) | [Runtime index](docs/skills/INDEX.md) | [Latest release](https://github.com/62656456/ai-film-skills/releases/latest) |
| Produce an approved passage as AI video | [`produce-ai-video`](docs/skills/en/produce-ai-video.md) | [`SKILL.md`](skills/produce-ai-video/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/produce-ai-video.zip) |
| Plan an end-to-end short-drama workflow | [`ai-short-drama-production`](docs/skills/en/ai-short-drama-production.md) | [`SKILL.md`](skills/ai-short-drama-production/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-short-drama-production.zip) |
| Design or audit a distinctive web interface | [`web-design-director`](docs/skills/en/web-design-director.md) | [`SKILL.md`](skills/web-design-director/SKILL.md) | [Download](https://github.com/62656456/ai-film-skills/releases/latest/download/web-design-director.zip) |

## The promise

These Skills do not replace judgment with prompt decoration. They turn story causality, character purpose, blocking, spatial continuity, physical action, light, materials, and production gates into reusable operating contracts.

The visible result comes first: a readable script, shot plan, asset contract, visual direction, research report, or qualified media deliverable. Internal schemas and checks support that result; they do not replace it.

<img src="docs/assets/skill-map.svg" width="100%" alt="Open Film Skills map from story and assets through visual language, shots, production, and validation" />

## Read the design before installing

All 19 modules have a GitHub-readable design guide in both English and Simplified Chinese: **38 pages generated from one reviewed contract registry**. Every page explains the module's purpose, principles, inputs, workflow, directed return path, review gates, pass evidence, outputs, boundaries, host requirements, and every file shipped in that standalone package.

- [Browse all English and Chinese module guides](docs/skills/INDEX.md)
- [Understand the shared return, review, and pass logic](docs/SKILL_DESIGN_SYSTEM.md)
- [Compare modules by task, runtime source, ZIP, and evidence state](SKILL_CATALOG.md)

The guides explain the runtime contract; they do not replace it. `SKILL.md` remains the canonical Agent instruction. Structural validation, host execution, real-task evidence, and explicit user acceptance remain separate states.

## Quick install

Clone the repository:

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
```

See every available module:

```bash
python scripts/install_skill.py --list
```

Install one Skill:

```bash
python scripts/install_skill.py ai-storyboard-director --platform claude-code
```

Or download one ready-to-extract ZIP from the [latest release](https://github.com/62656456/ai-film-skills/releases/latest). Each archive contains one complete Skill folder.

Choose the host explicitly:

```bash
python scripts/install_skill.py ai-storyboard-director --platform codex
python scripts/install_skill.py ai-storyboard-director --platform claude-code
python scripts/install_skill.py ai-storyboard-director --platform codebuddy
```

TRAE uses a project-level `.agents/skills/` folder. WorkBuddy imports the release ZIP through **Add Skill → Upload Skill**. Every packaged folder carries its own required references; experimental Skills are excluded from the normal complete package. See [Installation](docs/INSTALLATION.md) and [Agent compatibility](docs/COMPATIBILITY.md).

## Designed to travel alone

- Every package contains a portable `SKILL.md` plus its own scripts and required references. `agents/openai.yaml` is optional Codex metadata and is never a runtime dependency.
- Every module is independently useful inside its stated outcome boundary. “Standalone” does not mean that a style module writes a script, an asset contract generates an image without a media tool, or a production workflow bypasses cost and permission gates.
- Each design guide states what the module can deliver alone, what it cannot claim alone, and which host capabilities are still required.
- The repository validator rejects missing local dependencies and a return of the old shared-reference folder.
- Releases publish one ZIP per Skill plus one complete-studio ZIP and a SHA-256 manifest.
- Structural portability is checked automatically; real-project quality remains a separate status claim.

Try a module immediately with the [quick-start prompts](examples/quick-start-prompts.md).

## Works with your Agent

| Host | Documented route |
|---|---|
| Codex | `~/.codex/skills/<name>/` |
| Claude Code | `~/.claude/skills/<name>/` or `.claude/skills/<name>/` |
| TRAE | `<project>/.agents/skills/<name>/` |
| CodeBuddy | `~/.codebuddy/skills/<name>/` or `.codebuddy/skills/<name>/` |
| WorkBuddy | Import the standalone ZIP in **Add Skill → Upload Skill** |
| Other Agents | Use the Agent Skills loader, or attach `SKILL.md` and its local resources as instructions |

The canonical content is shared across every host. Native discovery and tool permissions still belong to the host, so the repository distinguishes native support from a prompt-only fallback. The exact product-name checks—including “Cloud Code,” “Trint,” and “WorkerBilly”—are documented in [Agent compatibility](docs/COMPATIBILITY.md).

## Skill map

| Layer | Skills | Status |
|---|---|---|
| Story and directing | `director-agent`, `ai-storyboard-director` | Deployed |
| Asset definition | `character-asset`, `scene-asset`, `prop-asset` | Deployed |
| Visual language | `cyberpunk-design`, `epic-design`, `fantasy-design`, `horror-design`, `noir-design`, `romance-design`, `war-design`, `wuxia-design` | Deployed |
| Production | `produce-ai-video` | Deployed |
| Workflow orchestration | `ai-short-drama-production` | Packaged; validation pending |
| Product and research | `web-design-director`, `d-official-market-analysis`, `d-data-analysis-semantic-layer` | Deployed |
| Experimental | `hard-sci-fi-visual-director` | Not deployed; user visual review pending |

See the detailed [Skill catalog](SKILL_CATALOG.md), [38 design guides](docs/skills/INDEX.md), [shared design system](docs/SKILL_DESIGN_SYSTEM.md), and [architecture](docs/ARCHITECTURE.md).

## Status means something

- **Deployed**: the current personal runtime package is in use. It is not automatically described as stable in practice.
- **Packaged**: structurally complete enough to distribute, but not currently deployed.
- **Experimental**: isolated from normal installation and clearly marked as unapproved or incomplete.
- **Retired**: intentionally absent. A retired package is not restored from an old file.
- **Third-party**: not republished as original work.

## Repository design

The repository is organized as a production map rather than a wall of prompts. The visual system uses film-slate black, script-paper white, signal orange, cool cyan, and brass. One horizontal route—**story → assets → visual language → shots → production → validation**—acts as the signature element across the README and diagrams.

The information architecture was informed by [OmniRoute](https://github.com/diegosouzapw/OmniRoute): a strong visual thesis, immediate navigation, visible status, multilingual entry points, copyable quick starts, diagrams, contribution routes, security guidance, and explicit third-party notices. No OmniRoute brand asset, illustration, copy, or code is included here.

## Contributing and safety

- Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a Skill change.
- Report accidental secrets or private information through [SECURITY.md](SECURITY.md), not a public issue.
- See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for excluded and adapted material.
- Check the exact public boundary in [PUBLICATION_SCOPE.md](PUBLICATION_SCOPE.md).
- Regenerate the bilingual guides with `python scripts/generate_skill_guides.py` after changing the reviewed contract registry.
- Run `python scripts/validate_skill_docs.py` and `python scripts/validate_repository.py` before submitting changes.

## Feedback and contact

The project grows through concrete use, not promotional claims. Share the request you tried, the Skill used, what worked, and the one improvement that would matter most.

- Discuss workflows in [GitHub Discussions](https://github.com/62656456/ai-film-skills/discussions).
- Report reproducible problems or proposals in [GitHub Issues](https://github.com/62656456/ai-film-skills/issues).
- Contact the maintainer at [haldissita@gmail.com](mailto:haldissita@gmail.com).
- Use the structured [feedback guide](docs/FEEDBACK.md) when possible.

## License

Personally authored content in this repository is licensed under the [Apache License 2.0](LICENSE), unless a file says otherwise.
