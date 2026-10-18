# Storyboard Director 5.8.6

Date: 2026-10-18. Scope: the default storyboard/video-prompt workflow and its production compilers.

## Result

- Keep six main modules in this order: generation task, visual style, principal subjects, scene state, emotional goal, segmented script. Append an unnumbered negative prompt.
- Describe medium, concrete style references and photography in the task without a one-sentence limit; reinforce the same camera, film/digital and lens direction in visual style.
- Select focal length, optical setup, viewing position, focus and movement together. Ordinary macro, wide probe, fixed-angle periscope, split diopters, tilt/shift, cinema zoom and lens character are options selected by the image's needs.
- Preserve actual optical/mechanical limits. A replaceable straight-view/90-degree module is not a continuously variable viewing prism. Do not invent hardware to make a proposed shot work.
- Consolidate repetitive explanations while preserving actions, dialogue, continuity and the intentional style emphasis in the first two modules. Do not impose a fixed shot quota.
- Align the video-production and short-drama prompt compilers so downstream work retains the same order and selected optics.

## Scope and preservation

The Storyboard package inherits its already effective project-style/image-reference guidance. This release does not revise scene design or include unrelated concurrent Skill changes. Existing media, prior releases and historical test records keep their contents and acceptance scope. Normal use still invokes `ai-storyboard-director`; no version argument is required.

The local complete 5.8.5 package is retained for rollback. Public Git history retains the previous source; current source and the new release use the same 5.8.6 Storyboard runtime.

## Validation and limits

Package/frontmatter/reference checks and independent text trials are separate from video execution. The two optical trials concern an ordinary macro task and a narrow-channel side-view task. A first side-view draft assumed unverified variable-prism hardware; the bounded mechanical guidance was tightened and that case was retested.

Individual recently tested clips received positive user feedback about realism. This is not evidence that every optical setup is executed correctly by every video model. No new image, audio or video was generated for this release. Refer to the commit's GitHub Actions results for repository, multi-platform and release-package checks.

## Distribution

[Current release](https://github.com/62656456/ai-film-skills/releases/tag/ai-storyboard-director-v5.8.6) · [Storyboard ZIP](https://github.com/62656456/ai-film-skills/releases/download/ai-storyboard-director-v5.8.6/ai-storyboard-director.zip)

The release manifest identifies the source commit and contract digest, and SHA-256 checksums identify the downloadable archives. The historical v1.4.0 archive remains the older 5.7.2 snapshot.
