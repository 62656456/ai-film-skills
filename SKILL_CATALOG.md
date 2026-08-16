# Skill catalog

Every entry below is a self-contained module. After cloning, install one with:

```bash
python scripts/install_skill.py <skill-name> --platform <codex|claude-code|trae|codebuddy>
```

Without cloning, use the ZIP link in the table. The same self-contained folder can be installed in Codex, Claude Code, TRAE, or CodeBuddy, uploaded to WorkBuddy, or attached to another Agent as instructions. See [Installation](docs/INSTALLATION.md) and [Agent compatibility](docs/COMPATIBILITY.md).

## Story and directing

| Skill | Best for | Standalone download | Release state |
|---|---|---|---|
| [`director-agent`](skills/director-agent/) | Script creation and revision, causality, character action, natural dialogue, and pre-storyboard directing decisions | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/director-agent.zip) | Deployed; long-term stability still accumulating |
| [`ai-storyboard-director`](skills/ai-storyboard-director/) | Script understanding, blocking, shot sentences, multi-camera projection, complex camera movement, and production prompts | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-storyboard-director.zip) | Deployed; current baseline is the 5.4.2 candidate over the 5.4.1 continuity contract |

## Asset definition

| Skill | Best for | Standalone download | Release state |
|---|---|---|---|
| [`character-asset`](skills/character-asset/) | Character identity, views, expressions, actions, and continuity reference contracts | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/character-asset.zip) | Deployed |
| [`scene-asset`](skills/scene-asset/) | Reusable environment, spatial anchor, lighting, and continuity reference contracts | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/scene-asset.zip) | Deployed |
| [`prop-asset`](skills/prop-asset/) | Prop identity, state, handling, material, scale, and continuity contracts | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/prop-asset.zip) | Deployed |

## Genre visual language

| Skill | Best for | Standalone download | Release state |
|---|---|---|---|
| [`cyberpunk-design`](skills/cyberpunk-design/) | Observable cyberpunk image, color, space, action, material, and continuity parameters | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/cyberpunk-design.zip) | Deployed |
| [`epic-design`](skills/epic-design/) | Scale, spectacle, composition, light, movement, and material parameters | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/epic-design.zip) | Deployed |
| [`fantasy-design`](skills/fantasy-design/) | Fantasy world, magic, environment, light, material, and continuity parameters | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/fantasy-design.zip) | Deployed |
| [`horror-design`](skills/horror-design/) | Horror framing, space, light, threat, action, material, and continuity parameters | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/horror-design.zip) | Deployed |
| [`noir-design`](skills/noir-design/) | Noir and crime framing, contrast, space, action, and material parameters | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/noir-design.zip) | Deployed |
| [`romance-design`](skills/romance-design/) | Romantic distance, light, movement, material, emotion, and continuity parameters | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/romance-design.zip) | Deployed |
| [`war-design`](skills/war-design/) | War framing, terrain, explosions, action, material, and continuity parameters | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/war-design.zip) | Deployed |
| [`wuxia-design`](skills/wuxia-design/) | Wuxia framing, blocking, weapons, action, Eastern materials, and continuity parameters | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/wuxia-design.zip) | Deployed |

## Production, product, and research

| Skill | Best for | Standalone download | Release state |
|---|---|---|---|
| [`produce-ai-video`](skills/produce-ai-video/) | Turning approved material into a qualified, watchable AI video through explicit cost and quality gates | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/produce-ai-video.zip) | Deployed |
| [`ai-short-drama-production`](skills/ai-short-drama-production/) | Orchestrating script beats, assets, shots, generation, quality control, and editing | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/ai-short-drama-production.zip) | Packaged; not deployed |
| [`web-design-director`](skills/web-design-director/) | Directing, building, or auditing distinctive production-grade web interfaces | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/web-design-director.zip) | Deployed |
| [`d-official-market-analysis`](skills/d-official-market-analysis/) | Source-backed official research for AI film and adjacent media markets | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/d-official-market-analysis.zip) | Deployed |
| [`d-data-analysis-semantic-layer`](skills/d-data-analysis-semantic-layer/) | Reviewing and versioning approved analytical knowledge into a semantic layer | [ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/d-data-analysis-semantic-layer.zip) | Deployed |

## Experimental

| Skill | Best for | Standalone download | Release state |
|---|---|---|---|
| [`hard-sci-fi-visual-director`](experimental/hard-sci-fi-visual-director/) | Evidence-grounded hard-science-fiction visual direction with physical, ecological, industrial, and story-legibility gates | [Experimental ZIP](https://github.com/62656456/ai-film-skills/releases/latest/download/hard-sci-fi-visual-director.zip) | Experimental; not deployed; user visual review pending |

Experimental packages are not included in the complete-studio ZIP and require deliberate installation.

## Intentionally absent

- `sci-fi-design`: retired after failed real-image validation; it is not restored.
- `xianxia-visual-director`: third-party repository with no redistribution license verified at packaging time.
- `frontend-design`: third-party Apache-2.0 package; not presented as original work. The public `web-design-director` uses an original local creative-direction reference instead.
- System Skills and Lark connector Skills: outside the authored repository scope.

## Feedback

If a module works, fails, or almost works on a real task, share the evidence through [Discussions](https://github.com/62656456/ai-film-skills/discussions), [Issues](https://github.com/62656456/ai-film-skills/issues), or [haldissita@gmail.com](mailto:haldissita@gmail.com).
