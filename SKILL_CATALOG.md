# Skill catalog

Every entry below is a bounded, self-contained module. Its name opens the human-readable GitHub design guide; the `SKILL.md` column opens the exact runtime instruction; the ZIP contains the standalone installable folder.

- [Browse all 38 English / Simplified Chinese guides](docs/skills/INDEX.md)
- [Read the shared directed-return, review, and pass logic](docs/SKILL_DESIGN_SYSTEM.md)
- [Installation](docs/INSTALLATION.md) · [Agent compatibility](docs/COMPATIBILITY.md)

After cloning, install one module with:

```bash
python scripts/install_skill.py <skill-name> --platform <codex|claude-code|trae|codebuddy>
```

“Standalone” means the module can deliver its named outcome without a shared repository directory. It does not mean that a visual-style module also writes a script, that an asset contract can generate images without a media tool, or that a production module can bypass host permissions, cost approval, rights, or user review. Each design guide states the exact boundary.

## Story and directing

| Skill design guide | Best for | Runtime | Standalone download | Release state |
|---|---|---|---|---|
| [`director-agent`](docs/skills/en/director-agent.md) | Script creation and revision, causality, character action, natural dialogue, and pre-storyboard directing decisions | [`SKILL.md`](skills/director-agent/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/director-agent.zip) | Deployed; long-term stability still accumulating |
| [`ai-storyboard-director`](docs/skills/en/ai-storyboard-director.md) | Script understanding, blocking, shot sentences, multi-camera projection, complex camera movement, and production prompts | [`SKILL.md`](skills/ai-storyboard-director/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-storyboard-director.zip) | Deployed; current baseline is the 5.4.2 candidate over the 5.4.1 continuity contract |

## Asset definition

| Skill design guide | Best for | Runtime | Standalone download | Release state |
|---|---|---|---|---|
| [`character-asset`](docs/skills/en/character-asset.md) | Character identity, views, expressions, actions, and continuity reference contracts | [`SKILL.md`](skills/character-asset/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/character-asset.zip) | Deployed |
| [`scene-asset`](docs/skills/en/scene-asset.md) | Reusable environment, spatial anchor, lighting, and continuity reference contracts | [`SKILL.md`](skills/scene-asset/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/scene-asset.zip) | Deployed |
| [`prop-asset`](docs/skills/en/prop-asset.md) | Prop identity, state, handling, material, scale, and continuity contracts | [`SKILL.md`](skills/prop-asset/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/prop-asset.zip) | Deployed |

## Genre visual language

| Skill design guide | Best for | Runtime | Standalone download | Release state |
|---|---|---|---|---|
| [`cyberpunk-design`](docs/skills/en/cyberpunk-design.md) | Observable cyberpunk image, color, space, action, material, and continuity parameters | [`SKILL.md`](skills/cyberpunk-design/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/cyberpunk-design.zip) | Deployed |
| [`epic-design`](docs/skills/en/epic-design.md) | Scale, spectacle, composition, light, movement, and material parameters | [`SKILL.md`](skills/epic-design/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/epic-design.zip) | Deployed |
| [`fantasy-design`](docs/skills/en/fantasy-design.md) | Fantasy world, magic, environment, light, material, and continuity parameters | [`SKILL.md`](skills/fantasy-design/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/fantasy-design.zip) | Deployed |
| [`horror-design`](docs/skills/en/horror-design.md) | Horror framing, space, light, threat, action, material, and continuity parameters | [`SKILL.md`](skills/horror-design/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/horror-design.zip) | Deployed |
| [`noir-design`](docs/skills/en/noir-design.md) | Noir and crime framing, contrast, space, action, and material parameters | [`SKILL.md`](skills/noir-design/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/noir-design.zip) | Deployed |
| [`romance-design`](docs/skills/en/romance-design.md) | Romantic distance, light, movement, material, emotion, and continuity parameters | [`SKILL.md`](skills/romance-design/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/romance-design.zip) | Deployed |
| [`war-design`](docs/skills/en/war-design.md) | War framing, terrain, explosions, action, material, and continuity parameters | [`SKILL.md`](skills/war-design/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/war-design.zip) | Deployed |
| [`wuxia-design`](docs/skills/en/wuxia-design.md) | Wuxia framing, blocking, weapons, action, Eastern materials, and continuity parameters | [`SKILL.md`](skills/wuxia-design/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/wuxia-design.zip) | Deployed |

## Production, product, and research

| Skill design guide | Best for | Runtime | Standalone download | Release state |
|---|---|---|---|---|
| [`produce-ai-video`](docs/skills/en/produce-ai-video.md) | Turning approved material into a qualified, watchable AI video through explicit cost and quality gates | [`SKILL.md`](skills/produce-ai-video/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/produce-ai-video.zip) | Deployed |
| [`ai-short-drama-production`](docs/skills/en/ai-short-drama-production.md) | Orchestrating script beats, assets, shots, generation, quality control, and editing | [`SKILL.md`](skills/ai-short-drama-production/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-short-drama-production.zip) | Packaged; not deployed |
| [`web-design-director`](docs/skills/en/web-design-director.md) | Directing, building, or auditing distinctive production-grade web interfaces | [`SKILL.md`](skills/web-design-director/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/web-design-director.zip) | Deployed |
| [`d-official-market-analysis`](docs/skills/en/d-official-market-analysis.md) | Source-backed official research for AI film and adjacent media markets | [`SKILL.md`](skills/d-official-market-analysis/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/d-official-market-analysis.zip) | Deployed |
| [`d-data-analysis-semantic-layer`](docs/skills/en/d-data-analysis-semantic-layer.md) | Reviewing and versioning approved analytical knowledge into a semantic layer | [`SKILL.md`](skills/d-data-analysis-semantic-layer/SKILL.md) | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/d-data-analysis-semantic-layer.zip) | Deployed |

## Experimental

| Skill design guide | Best for | Runtime | Standalone download | Release state |
|---|---|---|---|---|
| [`hard-sci-fi-visual-director`](docs/skills/en/hard-sci-fi-visual-director.md) | Evidence-grounded hard-science-fiction visual direction with physical, ecological, industrial, and story-legibility gates | [`SKILL.md`](experimental/hard-sci-fi-visual-director/SKILL.md) | [Experimental ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/hard-sci-fi-visual-director.zip) | Experimental; not deployed; user visual review pending |

Experimental packages are not included in the complete-studio ZIP and require deliberate installation.

## How review and return work

Every module has its own inputs and gates, but all use the same causal discipline:

```text
bounded input -> visible draft -> module review gates
    fail -> return to the earliest broken decision while preserving approved constraints
    pass -> record observable evidence and produce the named handoff
```

Read [How every Skill is designed](docs/SKILL_DESIGN_SYSTEM.md) for the common contract. A module pass, structural validation, host execution, real-task evidence, and explicit user acceptance are different states.

## Intentionally absent

- `sci-fi-design`: retired after failed real-image validation; it is not restored.
- `xianxia-visual-director`: third-party repository with no redistribution license verified at packaging time.
- `frontend-design`: third-party Apache-2.0 package; not presented as original work. The public `web-design-director` uses an original local creative-direction reference instead.
- System Skills and Lark connector Skills: outside the authored repository scope.

## Feedback

If a module works, fails, or almost works on a real task, share the evidence through [Discussions](https://github.com/62656456/ai-film-skills/discussions), [Issues](https://github.com/62656456/ai-film-skills/issues), or [haldissita@gmail.com](mailto:haldissita@gmail.com).
