# Release notes

## v1.1.0 — 2026-08-16

Cross-Agent, standalone packaging release.

- Every stable Skill is self-contained: required references now live inside the individual Skill folder, with no shared repository directory required at runtime.
- The same portable `SKILL.md` core is documented for Codex, Claude Code, TRAE, CodeBuddy, WorkBuddy local-package upload, and instructions-only fallback in other Agent software.
- `agents/openai.yaml` remains an optional Codex presentation enhancement and is not required by the canonical workflow.
- Added a platform-aware single-Skill installer with explicit targets for Codex, Claude Code, TRAE, and CodeBuddy.
- Added deterministic release packaging: 19 individual Skill ZIPs, one complete-studio ZIP, archive integrity checks, and a SHA-256 manifest.
- Added automatic packaging and asset attachment for GitHub Releases.
- Added installation, compatibility, feedback, quick-start, contribution, and security guidance across the multilingual repository entry points.
- Added the public maintainer contact `haldissita@gmail.com` for feedback and private security reports.
- The director Skill can optionally use the public AI Film Knowledge Base for deeper theory while remaining fully usable without it.
- Product-name boundaries are explicit: “Cloud Code” is handled as Claude Code unless another official product is supplied; Trint is not advertised as a native Agent-Skills host; “WorkerBilly” is not silently equated with WorkBuddy.

Validation for this release checked 19 Skills and 110 Markdown files with zero warnings and zero errors, built and verified 20 ZIP archives, and smoke-installed the same `director-agent` package into Codex, Claude Code, TRAE, and CodeBuddy directory layouts.

Structural portability does not claim identical output quality across models or hosts. Real-project validation status remains separate in [SKILL_CATALOG.md](SKILL_CATALOG.md).

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
