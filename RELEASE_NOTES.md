# Release notes

## v1.3.0 — 2026-09-01

Single-entry storyboard 5.4.4 and standalone-package completion.

- Updated the formal `ai-storyboard-director` runtime to 5.4.4 while keeping the user-facing invocation unchanged.
- Added the single-master-prompt gate, natural-language asset naming, continuous living-subject motion, locked-reference composition, multi-space separation, physically valid entrances, and visible camera-plan headings for every segmented shot.
- Retired the separate `ai-storyboard-director-motion-lab` package after its useful complex-camera rules were integrated into the formal single entry; it is no longer published or installable as a second storyboard Skill.
- Removed packaged cross-version rollback snapshots from the runtime tree so each Skill remains independently copyable without sibling versions or historical dependencies.
- Completed the standalone-package remediation and repository validation work prepared after v1.2.0, including package-local references, stricter independence checks, and function-conservation regression coverage.
- The repository now publishes 18 stable Skills and one isolated experimental Skill, with 19 English and 19 Simplified Chinese design guides.
- Rebuilt the repository entrance around three first-time outcomes—write the story, design executable shots, or organize AI-video production—and added a 60-second single-Skill trial.
- Added an auditable Storyboard Director 5.4.4 before/after example, deterministic campaign graphics, a social-preview export, a public launch kit, and a real-use showcase form.
- Added repository checks that reject stale public module counts and verify every launch asset's SHA-256 and PNG dimensions.
- Verified the open `skills` CLI 1.5.23 against the public repository: 18 stable Skills discovered, one six-file Storyboard Director package copied with full SHA-256 parity, and the isolated experiment excluded from default discovery.
- Verified the live skills.sh index: the repository page reports 18 Agent Skills, flagship pages resolve successfully, and the official install-count badge is available.
- Added an original `director-agent` diagnosis-and-revision case with explicit alternative tests, causal state changes, dialogue-response chains, and a self-audit-only evidence label.
- Added a dependency-free, responsive, accessible GitHub Pages landing page for non-technical creators, with proof-led outcomes, verified install routes, and explicit evidence boundaries.
- Added two original locally generated 3D previs clips with preserved poster frames, hashes, dimensions, status labels, exclusion rules, and explicit non-final/non-adoption boundaries.

This update proves repository structure, standalone closure, deterministic validation, and the recorded 5.4.4 text behavior. It does not claim successful video-model generation or explicit user acceptance of the resulting storyboard output.

## v1.2.0 — 2026-08-25

Safety hardening and 5.4.3 testing-candidate release.

- Promoted the existing `ai-storyboard-director` 5.4.2 source label from candidate wording to the current formal default while preserving the complete 5.4.1 rollback snapshot and the pre-formalization 5.4.2 candidate snapshot.
- Added `ai-storyboard-director-motion-lab` 5.4.3 under `experimental/`, visibly labeled **Testing**. It keeps `policy.allow_implicit_invocation: false`, requires deliberate experimental installation, stays outside the complete-studio ZIP, and does not replace formal 5.4.2.
- Expanded the public contract registry and generated design system to 20 modules and 40 English / Simplified Chinese guides.
- Release packaging now produces 20 individual Skill ZIPs, one stable-only complete-studio ZIP, and one manifest; both experimental ZIPs remain opt-in and outside the complete archive.
- Replaced unrestricted package-output deletion with an owned-output boundary, dangerous-root rejection, staging builds, atomic replacement, and rollback on swap failure.
- Packaging and installation now reject symbolic links, Windows junctions, and any resolved source path outside its standalone Skill root.
- Hardened the semantic-candidate validator against empty datasets, non-object JSON, blank required values, malformed URLs, non-strict dates, duplicate IDs, invalid version/section formats, and inconsistent date order. Optional `--as-of` validation checks review and expiry state without granting knowledge-write approval.
- Corrected the existing urban-romance saturation record from `有效` to `待复查` because its recorded `review_on` date had passed; the conclusion itself was not silently refreshed or re-approved.
- Hardened the market-dataset validator against all-blank records, missing usable source identity, malformed hostless URLs, non-strict dates, and evidence-free rows.
- Replaced regular-expression frontmatter parsing with safe YAML parsing and duplicate-key rejection.
- Made the reviewed contract registry the source of truth for expected Skill names and stable/experimental locations instead of hard-coded repository counts.
- Added negative regression tests for destructive output paths, unowned directories, source-tree links, folded/duplicate YAML, empty and malformed candidates, strict dates, hostless URLs, and unusable market records.
- CI and release workflows now install pinned validation dependencies, run the regression suite, verify regenerated guides, and derive package counts from the contract registry.
- Pinned GitHub Actions to full commit SHAs and removed release-asset `--clobber`; a published tag can no longer silently overwrite existing ZIP assets.
- Release manifests now record schema v3, the source commit, clean/dirty source-tree state, and the SHA-256 of `docs/skill-contracts.json`.

This release proves repository structure, negative safety properties, deterministic packaging within the declared toolchain, and explicit experimental isolation. It does not claim that 5.4.3 has passed video-model generation, real-project evaluation, or user acceptance.

## v1.1.0 — 2026-08-16

Cross-Agent, standalone packaging and GitHub-reading release.

- Every stable Skill is self-contained: required references now live inside the individual Skill folder, with no shared repository directory required at runtime.
- Added a GitHub-readable design system with one English and one Simplified Chinese guide for every module: 38 pages for 19 Skills.
- Every module guide explains purpose, design principles, standalone scope, inputs, workflow, directed return paths, review gates, pass evidence, outputs, boundaries, host requirements, and every file shipped in that package.
- The module name in the public catalog now opens the human design guide; the same row preserves the exact runtime `SKILL.md`, standalone ZIP, and evidence state.
- Added a shared cause-directed review loop: failed checks return to the earliest broken decision while preserving approved constraints; passed checks produce observable evidence and a named handoff.
- Kept structural validity, host execution, real-task evidence, and explicit user acceptance as separate states throughout the guides.
- English and Simplified Chinese contain all 19 module guides. Japanese and Korean remain honest repository entry pages and explicitly disclose that the detailed module pages are currently available only in English and Simplified Chinese.
- Added deterministic guide generation from a reviewed bilingual contract registry, full packaged-source linking, dedicated documentation validation, and a CI regeneration-drift check.
- The same portable `SKILL.md` core is documented for Codex, Claude Code, TRAE, CodeBuddy, WorkBuddy local-package upload, and instructions-only fallback in other Agent software.
- `agents/openai.yaml` remains an optional Codex presentation enhancement and is not required by the canonical workflow.
- Added a platform-aware single-Skill installer with explicit targets for Codex, Claude Code, TRAE, and CodeBuddy.
- Added deterministic release packaging: 19 individual Skill ZIPs, one complete-studio ZIP, archive integrity checks, and a SHA-256 manifest.
- Added automatic packaging and asset attachment for GitHub Releases.
- Added installation, compatibility, feedback, quick-start, contribution, security, design, and publication-boundary guidance across the multilingual repository entry points.
- Added the public maintainer contact `haldissita@gmail.com` for feedback and private security reports.
- The director Skill can optionally use the public AI Film Knowledge Base for deeper theory while remaining fully usable without it.
- Product-name boundaries are explicit: “Cloud Code” is handled as Claude Code unless another official product is supplied; Trint is not advertised as a native Agent-Skills host; “WorkerBilly” is not silently equated with WorkBuddy.

Pre-release validation now requires all 19 Skill folders, all 38 bilingual design pages, all packaged source links, the shared design system, the reviewed contract registry, the guide generator, the documentation validator, and the portable repository validator. It also builds and verifies 20 ZIP archives and smoke-installs the same `director-agent` package into Codex, Claude Code, TRAE, and CodeBuddy directory layouts.

Structural portability and a module-level pass do not claim identical output quality across models or hosts. Real-project validation and user-acceptance status remain separate in [SKILL_CATALOG.md](SKILL_CATALOG.md) and [PUBLICATION_SCOPE.md](PUBLICATION_SCOPE.md).

## v1.0.0 — 2026-08-16

Initial public packaging of the personal AI filmmaking Skill system.

- 18 packaged Skills across directing, storyboarding, assets, visual language, production, research, data, and interface design;
- 1 isolated experimental hard-science-fiction visual director;
- English, Simplified Chinese, Japanese, and Korean repository entry pages;
- original hero artwork and architecture diagrams;
- generated Codex UI metadata for every packaged Skill;
- repository validation for frontmatter, metadata, links, secrets, local paths, and publication exclusions;
- explicit third-party, security, contribution, status, and publication-scope documentation.

This release does not claim that every Skill is practice-validated. See [PUBLICATION_SCOPE.md](PUBLICATION_SCOPE.md) for the exact boundary.
