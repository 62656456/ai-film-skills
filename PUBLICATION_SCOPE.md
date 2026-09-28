# Publication scope

## Current source inventory

The source tree contains **18 regular packages and 3 opt-in experimental packages: 21 modules, with 42 generated English / Simplified Chinese guides**. The regular complete-studio distribution includes the 18 packages under `skills/`; the three `experimental/` packages retain their explicit opt-in boundary.

The 21 repository modules comprise 20 filmmaking modules and one web-interface helper. The [complete workflow](docs/WORKFLOW.md) also links the external `xianxia-visual-director`, giving 21 filmmaking responsibilities plus one web helper without adding its source to this repository.

Included material consists of authored Skill instructions and package-local resources, public documentation and diagrams, build/install/validation tooling, and authorized original demonstration media. Human guides explain each module; runtime authority remains its `SKILL.md` and package-local references. Storyboard, prompt, creative-idea and actual-media requests retain separate delivery stages according to the current task.

The [September 21 source audit](docs/research/SOURCE_INVENTORY.md) remains a dated record. The [September 29 overhaul research](docs/research/skill-overhaul/index.md) records the later workflows, comparison designs, test images, review limits and known repairs. Later activation does not rewrite what a historical test proved.

Original personal and commercial permissions are explained in [Commercial use and copyright](COMMERCIAL_USE.md). The existing Apache 2.0 LICENSE and third-party file notices retain their respective scopes.

## Authorized public research and media

### Seven-genre, three-version storyboard study

The [seven-genre study](docs/research/skill-overhaul/seven-genres/index.md) contains seven original stories, 21 thirty-second storyboard plans with 149 shots, 21 first-round image boards, generation instructions and image-review findings. The [viewer](docs/research/skill-overhaul/seven-genres/viewer.html) lets readers compare versions by story. Original first-round results are preserved rather than replaced with later successful attempts.

These 21 boards are **not an aesthetically accepted batch**. The recorded review contains 29 definite or scope-limited repair observations affecting 15 boards; six boards had no confirmed hard conflict found in that review, which is not a pass. Still frames do not establish camera-motion execution, action continuity, speech delivery or a completed video. The comparison is not a strict blind test or a quantitative ranking of skill versions.

A and B share a creative core. B's optional Jev calls evaluate text requirements; their results do not establish pixel review or aesthetic approval. Model responses, usage and public test text may be published after removing private credential-source context and local-machine paths. Credentials themselves are excluded.

The [workflow diagrams](docs/research/skill-overhaul/workflows/index.md) and [same-story fusion research](docs/research/skill-overhaul/fusion/index.md) retain their selected, candidate and historical distinctions. The user's adoption of the direct live-character final shot is a specific design decision, not acceptance of every shot or the entire suite.

### Previously accepted showcase

The primary [showcase](docs/showcase/manifest.json) contains a separate set of **21 previously accepted outputs: 19 generated stills and two original interface screenshots**. Their full aspect ratios, original PNGs and original acceptance scope remain available. This accepted-art batch is distinct from the 21 new storyboard test boards and was not originally an old/new same-prompt A/B study.

The older [style gallery](docs/style-gallery/manifest.json) and [previs evidence](docs/media/media-manifest.json) remain historical records with their own original status. They are not silently reclassified as new accepted tests.

### Earlier visual and previs research

The [September 21 research pages](docs/RESEARCH.md) preserve 26 original image candidates, seven experimental/comparison showcases with eight MP4 files, source prompts, editable previs projects and a file-level media inventory. Their publication does not promote a candidate or rejected experiment into accepted production material. Third-party voice/music in the composed comparison retain the separate [media notice](docs/research/whitebox/MEDIA_LICENSE.md).

Rejected workflow layouts and superseded experiments may be retained as clearly labeled history, outside the default current-results view. Backups of the maintainer's machine are not research artifacts.

## Excluded private and third-party material

- `sci-fi-design`: retired and not restored.
- [xianxia-visual-director](https://github.com/liyue-aigc/xianxia-visual-director): external upstream without verified source redistribution permission; link only, no copied source or ZIP.
- Third-party reference images, course material, film stills or screenshots without verified redistribution rights.
- System, connector and plugin Skills outside this authored project; private projects, client work, credentials, private conversation history, local runtime state and caches.
- Raw local baseline, capture, activation and rollback snapshots; absolute user-machine paths and private credential-recovery provenance.
- Third-party `frontend-design` source: not republished as original work.

Public research copies use repository-relative references and retain the relevant source/output hashes. Local governance manifests remain local. Removing a local path does not permit editing a historical result or upgrading its acceptance status.

The former separate storyboard motion-lab entry remains retired. Its useful camera-design concepts belong to the single storyboard entry.

## Languages and evidence

Repository entry pages exist in English, Simplified Chinese, Japanese and Korean. All 21 per-module guides are available in English and Simplified Chinese, 42 pages total; Japanese and Korean are overview pages only.

Structural validity, successful loading, actual task results, media review and explicit user acceptance are separate evidence. Three different accepted real tasks are needed before the maintainer labels a Skill practice-validated. Packaging, CI, publication and internal review do not manufacture that state. Previously accepted images remain accepted examples without proving stable output across all models or hosts.

Hard-science-fiction, whitebox previs and guofeng retain their experimental distribution status. Existing accepted hard-science-fiction images and bounded previs examples keep their original success scopes; they do not establish arbitrary complete-fight support or final-video reliability.

## 2026-09-29 activation and version update

**A5.7.1 is selected as the default through the user's direct, explicit activation instruction. B5.7.1-jev remains optional text review.** This activation is a use decision, not an aesthetic pass for the first-round boards or an assertion that all 21 modules are practice-validated. Known image-repair observations remain published.

The update clarifies independent creative ideas, stage-specific storyboard/prompt delivery, inheritance of approved directing decisions, and story-driven shot timing. It publishes the workflow, comparison and fusion records together with their limits. See the [overhaul research](docs/research/skill-overhaul/index.md) and [release workflow](docs/RELEASE_WORKFLOW.md) for the current source and evidence boundaries.

- Current `skills/ai-storyboard-director/` source is **A5.7.1**.
- The “current 5.6.5” labels inside the study identify the default at test time; original boards are not relabeled as A outputs.
- Public Release **v1.3.0** remains a historical distribution snapshot containing Storyboard Director **5.4.4**. Source changes do not rewrite its ZIPs.
- The separately labeled **5.6 standalone Preview** remains its own artifact and does not imply a new complete-studio Release. See [installation/version selection](docs/INSTALLATION.md).
- Publishing updated source does not by itself create a new Release. Install from the intended branch/commit and verify the actual Skill version and archive manifest.
