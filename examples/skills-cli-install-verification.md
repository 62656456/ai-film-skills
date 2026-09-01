# Open Skills CLI discovery and copy verification

This record verifies repository discovery and a bounded file-copy route. It does not claim that every Agent host loaded the Skill natively or produced identical model behavior.

## Environment

- Date: 2026-09-01
- Source: `62656456/ai-film-skills`
- Source type recorded by the CLI: `github`
- `skills` CLI: 1.5.23
- Node.js: 24.18.0
- npm: 11.16.0
- Test location: isolated temporary project directory
- Existing personal Codex installation: unchanged

## Discovery command

```bash
npx --yes skills@latest add 62656456/ai-film-skills --list
```

Recorded result:

- Repository cloned successfully.
- 18 stable Skills found and listed with their frontmatter descriptions.
- The isolated `hard-sci-fi-visual-director` experiment was not included in default discovery.

## Copy command

```bash
npx --yes skills@latest add 62656456/ai-film-skills --skill ai-storyboard-director --agent codex --copy --yes
```

Recorded result:

- One Skill selected.
- CLI reported Codex as the target Agent.
- Project copy route: `.agents/skills/ai-storyboard-director`.
- Six files copied.
- Recursive `SKILL.md` count: 1.
- `skills-lock.json` written with source `62656456/ai-film-skills`, source type `github`, and Skill path `skills/ai-storyboard-director/SKILL.md`.

## File parity

| Runtime file | Public source vs isolated copy |
|---|---|
| `SKILL.md` | SHA-256 match |
| `agents/openai.yaml` | SHA-256 match |
| `references/cinematography-design-engine.md` | SHA-256 match |
| `references/delivery-mode-guard.md` | SHA-256 match |
| `references/production-contract.md` | SHA-256 match |
| `references/shot-design-engine.md` | SHA-256 match |

## Evidence boundary

This test proves that the open Skills CLI can discover the stable repository modules and copy the selected Storyboard Director package without content drift. It does not prove:

- that the current conversation reloaded the new project path;
- that every Codex or Claude Code version uses the same native project directory;
- that a model followed the Skill correctly;
- that a generated storyboard or video passed user review;
- that the experimental package should appear in default discovery.

Use the repository's [explicit installer](../docs/INSTALLATION.md#install-from-a-clone) when a host-specific destination must be controlled directly.
