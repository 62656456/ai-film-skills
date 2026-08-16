# GitHub Project Watchlist

This file records GitHub projects found through web verification that may help improve director-agent workflows. Treat this as a watchlist, not proof that the code is locally usable.

Before borrowing logic from any project:

1. Re-open the repository and verify current stars, forks, license, recent commits, issues, and README.
2. Check whether source code is available or only Docker/commercial docs remain.
3. Check whether the project solves director logic, production workflow, or only media orchestration.
4. Borrow only decision patterns, not unverified claims.

## Current High-Value Candidates

### VideoClaw — HITsz-TMG/VideoClaw

- URL: https://github.com/HITsz-TMG/VideoClaw
- Verified value: full production-line framing: idea/story outline -> script planning -> character/scene design -> storyboard planning -> reference image generation -> video generation -> post-production.
- Useful pattern: visible, editable intermediate assets; user intervention at every key node; not black-box one-shot generation.
- Caution: verify local install and model/API dependencies before calling it "usable" in a local workflow.

### ViMax — HKUDS/ViMax

- URL: https://github.com/hkuds/vimax
- Verified value: agentic video generation architecture with director/screenwriter/producer/video-generator roles; RAG long-script design; shot-level storyboard design; multi-camera filming simulation; reference-image selection for consistency.
- Useful pattern: long-script segmentation with retention of plot/dialogue; camera simulation; continuity through reference selection.
- Caution: verify install state and whether examples run locally before adopting.

### BigBanana AI Director — shuyu-labs/BigBanana-AI-Director

- URL: https://github.com/shuyu-labs/BigBanana-AI-Director
- Verified value: high public attention; industrial short-drama / motion-comic workflow; script-to-asset-to-keyframe pipeline; project/world/asset/shot/delivery stages.
- Useful pattern: project-level assets and world anchors before shot generation; keyframe-driven start/end frame control; shot workbench with scene/character/prop context.
- Caution: public repo states future updates are mainly through official Docker images and public repo may be docs/historical reference, not full continuously updated source.

### OpenDirector — seme-org/open-director

- URL: https://github.com/seme-org/open-director
- Verified value: 9-agent pipeline from idea to rendered video; research field with notes/cautions/sources; story/script/storyboard/voice/BGM/media agents.
- Useful pattern: shared graph state with research notes consumed by downstream agents; optional web research for factual references.
- Caution: lower star count than the leading projects; verify quality by running a sample before borrowing deeply.

### Storyboarder — wonderunit/storyboarder

- URL: https://github.com/wonderunit/storyboarder
- Verified value: mature storyboard/animatic tool with thousands of stars, long commit history, Fountain screenplay support, export and drawing workflow.
- Useful pattern: fast storyboard iteration, animatic playback, screenplay-to-board workflow.
- Caution: not an AI director logic engine; borrow UI/workflow ideas, not reasoning logic.

### GoogleCloudPlatform/genmedia-izumi-agent

- URL: https://github.com/GoogleCloudPlatform/genmedia-izumi-agent
- Verified value: Google Cloud reference architecture for generative media agents; AI Director mode for narrative pacing and brand-guideline control; specialized agents for ads and creative workflows.
- Useful pattern: specialized agents, strict template mode vs AI Director mode, brand/timing/pacing constraints.
- Caution: enterprise/cloud/Vertex-oriented; not necessarily suited for local creator workflow.

### aicontentskills/ai-video-storyboard-skill

- URL: https://github.com/aicontentskills/ai-video-storyboard-skill
- Verified value: skill-format storyboard generator with shared visual theme, shot list, copy-ready prompts, audio direction, and post-production checklist.
- Useful pattern: every shot respects a shared visual theme; output includes post-production checklist.
- Caution: more prompt/shot-list utility than deep director reasoning.

### Picrew/awesome-llm-story-generation

- URL: https://github.com/Picrew/awesome-llm-story-generation
- Verified value: curated list of story/novel/script generation papers and open-source projects with link verification notes.
- Useful pattern: research index for story-generation methods, consistency, controllability, refinement, evaluation.
- Caution: not a production tool; use it to discover papers/projects, not as a runtime engine.

## Borrowable Patterns For Director-Agent

- Use a visible staged workflow, not one-shot generation.
- Preserve a research field containing sources, cautions, and uncertainty.
- Keep world/character/scene/prop assets as anchors before shot generation.
- Split long scripts into retained segments and track coverage.
- Use shot workbench logic: per-shot context includes characters, scene, props, action, keyframes.
- Maintain visual consistency through shared theme and reference selection.
- Separate AI Director mode from strict template/contract mode.
- Add post-production handoff: transitions, BGM, LUT, export constraints when useful.

## Reliability Rule

Do not call a project "really usable" unless at least one of these is true:

- It was locally installed and a sample ran successfully.
- It has an official hosted/demo workflow the user can access.
- It has recent active maintenance, clear install docs, public code or Docker, and low blocking issue risk.

Otherwise say: "publicly promising, not locally verified."
