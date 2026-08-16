# Installation

Every packaged Skill is self-contained and follows a portable `SKILL.md`-first layout. Install the complete studio or take one craft; no shared repository directory is required.

Read [Agent compatibility](COMPATIBILITY.md) first if your product name or install path differs from the examples below.

## Download one Skill

Open the [latest release](https://github.com/62656456/ai-film-skills/releases/latest) and download the ZIP named after the Skill, such as `ai-storyboard-director.zip`. The archive contains one complete Skill folder.

## Install from a clone

```bash
git clone https://github.com/62656456/ai-film-skills.git
cd ai-film-skills
python scripts/install_skill.py --list
```

Then choose the actual host explicitly:

```bash
python scripts/install_skill.py ai-storyboard-director --platform codex
python scripts/install_skill.py ai-storyboard-director --platform claude-code
python scripts/install_skill.py ai-storyboard-director --platform codebuddy
```

For a TRAE project, run the installer while your terminal is in that project, or provide the target directly:

```bash
python /path/to/ai-film-skills/scripts/install_skill.py ai-storyboard-director --platform trae
python scripts/install_skill.py ai-storyboard-director --target /path/to/project/.agents/skills
```

The installer refuses to overwrite an existing Skill unless you deliberately add `--force`.

## Native locations

| Host | Personal / global | Project |
|---|---|---|
| Codex | `$CODEX_HOME/skills/` or `~/.codex/skills/` | Use the Skill interface or project configuration supported by your Codex client |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| TRAE | Use the current client UI for global Skills | `.agents/skills/` |
| CodeBuddy Code | `~/.codebuddy/skills/` | `.codebuddy/skills/` |
| WorkBuddy | Upload the ZIP from **Add Skill → Upload Skill** | Managed by the WorkBuddy client |

## Install the complete studio

Download `open-film-skills-complete.zip` from the latest release. It contains `skills/<skill-name>/...`. Copy the individual Skill folders into the correct host directory, or import only the modules you need.

Example for Claude Code on macOS or Linux:

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

Example for CodeBuddy on Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codebuddy\skills" | Out-Null
Copy-Item -Recurse -Force .\skills\* "$env:USERPROFILE\.codebuddy\skills\"
```

## Other Agent software

If the host supports the [Agent Skills specification](https://agentskills.io/specification), place the complete Skill folder in its documented Skill library. If it has no native Skill loader:

1. attach or import `SKILL.md` as the Agent's instructions;
2. attach the Skill's `references/`, `assets/`, and `scripts/` when present;
3. tell the Agent that relative paths resolve from the Skill folder;
4. review every tool or script permission in that host before enabling execution.

This fallback preserves the method, but it cannot create native discovery or tool permissions that the host does not provide.

## WorkBuddy upload

WorkBuddy's official client supports local Skill-package import. Download one module ZIP, open **Add Skill**, choose **Upload Skill**, and select the file. Keep only the Skills needed for the current task enabled. Because the exact client UI and package checks may change, report an import failure with the WorkBuddy version and ZIP name.

## Experimental packages

Experimental Skills are not included in the complete-studio archive. Review their status first. The local installer requires `--experimental`.

## Verify an installation

Every installed folder must contain `SKILL.md` and every local file referenced by it. `agents/openai.yaml` is optional host metadata: Codex may use it for display and invocation, while other hosts may ignore it safely.

Structural installation does not prove real-project quality or identical behavior across models. Check [SKILL_CATALOG.md](../SKILL_CATALOG.md) for the release state.
