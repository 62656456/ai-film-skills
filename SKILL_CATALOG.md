# Skill catalog

**Current source: 18 regular + 2 experimental = 20 modules; 40 English / Simplified Chinese guides.**

[Full workflow and handoffs](docs/WORKFLOW.md) · [All guides](docs/skills/INDEX.md) · [Installation](docs/INSTALLATION.md) · [Design/review system](docs/SKILL_DESIGN_SYSTEM.md)

Current-source installation and published archives are different choices. The archive links below are explicitly pinned to historical **v1.3.0**, which preserves Storyboard Director **5.4.4** and predates this source refresh. Current storyboard source is **5.6**; its separate standalone Preview is a separately labeled artifact. No new Release is claimed here.

The normal complete-studio archive contains only regular packages. Both experiments require `--experimental`. A self-contained Skill owns its bounded output; it does not supply missing models, media tools, credits or host permissions.

```bash
python scripts/install_skill.py <skill-name> --platform codex
```

## Story and directing

| Module guide | Purpose | Current runtime | Source status | Historical archive |
|---|---|---|---|---|
| [director-agent](docs/skills/en/director-agent.md) | Create, revise, or diagnose scripts and make the directing decisions that must exist before full storyboard production. | [SKILL.md](skills/director-agent/SKILL.md) | Deployed; long-term practice evidence remains separate | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/director-agent.zip) |
| [ai-storyboard-director](docs/skills/en/ai-storyboard-director.md) | Turn an approved script into human-readable multi-shot design and production prompts while preserving causality, blocking, timing, and world-space continuity. | [SKILL.md](skills/ai-storyboard-director/SKILL.md) | Current source 5.6; selected for daily use; v1.3.0 ZIP preserves 5.4.4 | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/ai-storyboard-director.zip) |

## Asset definition

| Module guide | Purpose | Current runtime | Source status | Historical archive |
|---|---|---|---|---|
| [character-asset](docs/skills/en/character-asset.md) | Define a character's stable identity, views, expressions, actions, clothing, materials, and allowed state changes for downstream continuity. | [SKILL.md](skills/character-asset/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/character-asset.zip) |
| [scene-asset](docs/skills/en/scene-asset.md) | Define a reusable environment through layout, entrances, exits, landmarks, scale, lighting, materials, camera access, and continuity states. | [SKILL.md](skills/scene-asset/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/scene-asset.zip) |
| [prop-asset](docs/skills/en/prop-asset.md) | Define a prop's identity, scale, materials, usable faces, interfaces, holder, orientation, wear, operation, and state transitions. | [SKILL.md](skills/prop-asset/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/prop-asset.zip) |

## Genre visual language

| Module guide | Purpose | Current runtime | Source status | Historical archive |
|---|---|---|---|---|
| [cyberpunk-design](docs/skills/en/cyberpunk-design.md) | Translate body/technology relations and social space into functional light, color, materials, framing and continuity; daylight and dry interiors remain valid. | [SKILL.md](skills/cyberpunk-design/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/cyberpunk-design.zip) |
| [epic-design](docs/skills/en/epic-design.md) | Translate epic scale into human references, terrain, formation, layered spectacle, motivated camera distance, light, material, and movement. | [SKILL.md](skills/epic-design/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/epic-design.zip) |
| [fantasy-design](docs/skills/en/fantasy-design.md) | Translate fantasy into coherent world rules, magical cause and light, spatial behavior, materials, creatures, action, and continuity. | [SKILL.md](skills/fantasy-design/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/fantasy-design.zip) |
| [horror-design](docs/skills/en/horror-design.md) | Translate horror into threat placement, reveal timing, readable darkness, spatial uncertainty, physical traces, sound, and continuity. | [SKILL.md](skills/horror-design/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/horror-design.zip) |
| [noir-design](docs/skills/en/noir-design.md) | Translate noir and crime tension into readable contrast, motivated practical light, obstruction, power geometry, wet or worn materials, restrained action, and sound. | [SKILL.md](skills/noir-design/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/noir-design.zip) |
| [romance-design](docs/skills/en/romance-design.md) | Translate romance into distance, gaze, contact, reciprocal action, light and material choices driven by the actual relationship, without requiring warm lighting. | [SKILL.md](skills/romance-design/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/romance-design.zip) |
| [war-design](docs/skills/en/war-design.md) | Translate war into terrain, formation, weapon direction, cover, movement, impact, smoke and debris physics, logistics traces, sound, and continuity. | [SKILL.md](skills/war-design/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/war-design.zip) |
| [wuxia-design](docs/skills/en/wuxia-design.md) | Translate wuxia into grounded force, weapon paths, footwork, cloth and hair response, architecture, Eastern materials, rhythm, sound, and continuity. | [SKILL.md](skills/wuxia-design/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/wuxia-design.zip) |

## Production, product, and research

| Module guide | Purpose | Current runtime | Source status | Historical archive |
|---|---|---|---|---|
| [produce-ai-video](docs/skills/en/produce-ai-video.md) | Turn an approved script or passage into a qualified, watchable AI-generated final video through directing, shots, generation, edit, sound, full playback, and repair. | [SKILL.md](skills/produce-ai-video/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/produce-ai-video.zip) |
| [ai-short-drama-production](docs/skills/en/ai-short-drama-production.md) | Turn approved creative decisions into traceable beat, asset, blocking, lighting, action, sketch, prompt, and QC control contracts for AI short-drama production. | [SKILL.md](skills/ai-short-drama-production/SKILL.md) | Packaged; not deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/ai-short-drama-production.zip) |
| [web-design-director](docs/skills/en/web-design-director.md) | Direct, review, or build a distinctive production-grade web interface from product truth through rendered verification. | [SKILL.md](skills/web-design-director/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/web-design-director.zip) |
| [d-official-market-analysis](docs/skills/en/d-official-market-analysis.md) | Research film, short drama, animation, AI film, and adjacent media markets from current official and authoritative evidence for a defined decision. | [SKILL.md](skills/d-official-market-analysis/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/d-official-market-analysis.zip) |
| [d-data-analysis-semantic-layer](docs/skills/en/d-data-analysis-semantic-layer.md) | Validate, version, expire, preserve conflicts, and write approved analytical candidates into the D semantic target explicitly supplied by the current task, with a reconciled receipt. | [SKILL.md](skills/d-data-analysis-semantic-layer/SKILL.md) | Deployed | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/d-data-analysis-semantic-layer.zip) |

## Experimental

| Module guide | Purpose | Current runtime | Source status | Historical archive |
|---|---|---|---|---|
| [hard-sci-fi-visual-director](docs/skills/en/hard-sci-fi-visual-director.md) | Derive original hard-science-fiction worlds, systems, organisms, equipment, interfaces, camera, and prompts from script truth, evidence, physics, production, and continuity. | [SKILL.md](experimental/hard-sci-fi-visual-director/SKILL.md) | Experimental distribution; user-accepted image examples; broad reliability unproven | [v1.3.0 ZIP](https://github.com/62656456/ai-film-skills/releases/download/v1.3.0/hard-sci-fi-visual-director.zip) |
| [whitebox-previs-executor](docs/skills/en/whitebox-previs-executor.md) | Compile an existing prompt or storyboard into a playable 3D preview of camera, spatial parallax, basic blocking, timing and cuts, with explicit action-capability limits. | [SKILL.md](experimental/whitebox-previs-executor/SKILL.md) | Experimental; implemented basic previs and individually qualified action gates | [Source only](docs/INSTALLATION.md#experimental-packages) |

## External workflow route

[xianxia-visual-director](https://github.com/liyue-aigc/xianxia-visual-director) is listed only to complete the Eastern xianxia workflow. Its source and ZIP are not redistributed because no redistribution permission is verified. Ten visual routes therefore mean eight regular genres, one experimental hard-science-fiction module and this external route.

The repository has 19 filmmaking modules plus one web helper; including external xianxia gives 20 filmmaking responsibilities plus one web helper. The external entry is not counted in the 20 packaged modules or 40 guides.

## Evidence and return paths

The [14-image showcase](docs/showcase/manifest.json) contains actual user-accepted originals. The old [style gallery](docs/style-gallery/manifest.json), [5.4.4 text example](examples/storyboard-director-5.4.4-visible-camera-plan.md), and [previs clips](docs/media/media-manifest.json) retain their historical states. No old-version same-prompt A/B study was performed.

When a visible result fails, return to the earliest responsible story, asset, camera, light, material, execution or editing decision. Preserve approved constraints. File validity, host activation, real-task output and user acceptance are separate states. An experimental distribution can have accepted examples without being generally practice-validated.

## Intentionally absent

- `sci-fi-design`: retired; not restored.
- External or system/connector/plugin Skills outside the authored scope.
- Third-party `frontend-design` source, private projects, credentials and unlicensed media.

See [Publication scope](PUBLICATION_SCOPE.md) and [Third-party notices](THIRD_PARTY_NOTICES.md). Feedback: [Discussions](https://github.com/62656456/ai-film-skills/discussions) or [Issues](https://github.com/62656456/ai-film-skills/issues).
