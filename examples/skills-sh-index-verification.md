# skills.sh index verification

This record verifies that the stable Open Film Skills collection is present in the public Agent Skills directory. Directory install counts are telemetry events, not a count of distinct people or approved creative results.

## Verified public routes

| Route | Recorded result |
|---|---|
| `https://skills.sh/62656456/ai-film-skills` | HTTP 200; page contains `18 agent skills` |
| `https://skills.sh/62656456/ai-film-skills/ai-storyboard-director` | HTTP 200; source identity present |
| `https://skills.sh/62656456/ai-film-skills/director-agent` | HTTP 200; source identity present |
| `https://skills.sh/b/62656456/ai-film-skills` | HTTP 200; `image/svg+xml` badge |

The isolated `hard-sci-fi-visual-director` experiment remains outside the default stable index, matching the CLI discovery boundary.

## Verified search route

```bash
npx --yes skills@latest find ai-storyboard-director --owner 62656456
```

The search returned indexed entries from `62656456/ai-film-skills`, including:

- `ai-storyboard-director`
- `director-agent`
- `ai-short-drama-production`
- `produce-ai-video`
- `web-design-director`
- `character-asset`
- `scene-asset`
- `prop-asset`
- `d-official-market-analysis`

At the verification timestamp, the CLI displayed two installs for `ai-storyboard-director` and `director-agent`, and one for several other entries. These events include maintainer discovery and copy tests performed during release validation. They must not be translated into claims about distinct external users, active use, creative quality, or user acceptance.

## API and page boundary

The authenticated `/api/v1` endpoints require a Vercel OIDC token and returned HTTP 401 without one. The public web pages, badge, and user-facing `skills find` route were therefore used as the authoritative public evidence. No private or undocumented API was used.

## Evidence boundary

This test proves directory presence, public page availability, search visibility, and the default stable/experimental split. It does not prove:

- a specific number of external people;
- native activation in every Agent host;
- correct model behavior after installation;
- creative quality or final user approval;
- a security guarantee from the directory.

Review the source repository before installation and use the [installation verification](skills-cli-install-verification.md) for file-copy evidence.
